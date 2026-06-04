#!/usr/bin/env python3
"""video importer — YouTube 추출기 canonical JSON → cs-study raw/sources/video 페이지.

결정적(deterministic) importer. LLM 호출 없음. 추출기 모듈을 import 하지 않고
canonical JSON 을 dict 로만 소비한다(anti-corruption, 단방향 의존).

사용:
    python3 scripts/ingest.py <path> [--force] [--out raw/sources/video] [--now ISO]
        <path> = canonical JSON 파일 또는 추출기 out/<id>/ 디렉토리
        디렉토리면 best-variant 1개 선택 (manual > auto_sub > stt, 동률 extracted_at 최신)

산출: <out>/<video_id>.md (verbatim raw 페이지) + <out>/<video_id>.json (canonical 원본 복사)
멱등: 대상 .md 존재 시 skip (--force 에만 재생성). 트랜잭션: 둘째 실패 시 첫째 롤백.

설계: docs/{prd,architecture,business-logic}.md, docs/adr/0001-,0002-.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml  # PyYAML
except ImportError:
    print("ERROR: PyYAML 필요. `pip install pyyaml`", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO_ROOT / "raw" / "sources" / "video"

SUPPORTED_SCHEMA = "1.0"          # 추출기 domain.SCHEMA_VERSION 계약
MEDIA_TYPE = "video"              # cs-study source_type 상수

# best-variant 우선순위 (전사 충실도 순). 추출기 language.resolve 우선순위와 동형.
METHOD_PRIORITY = {"manual": 0, "auto_sub": 1, "stt": 2}


class IngestError(Exception):
    """검증/입력 실패 — exit 1."""


# --------------------------------------------------------------------------- #
# 입력 해석 + best-variant 선택 (BR-SEL-*)
# --------------------------------------------------------------------------- #
def load_canonical(path: Path) -> dict:
    """canonical JSON 1개 load + 구조 검증 (VR-2/3/4)."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != SUPPORTED_SCHEMA:
        raise IngestError(
            f"지원하지 않는 schema_version: {data.get('schema_version')!r} (기대 {SUPPORTED_SCHEMA!r}) — {path}"
        )
    video = data.get("video")
    if not isinstance(video, dict) or not video.get("id"):
        raise IngestError(f"video.id 부재 — 파일명 생성 불가: {path}")
    if not isinstance(data.get("extraction"), dict) or "full_text" not in data:
        raise IngestError(f"canonical 구조 손상 (extraction/full_text 누락): {path}")
    return data


def select_best(loaded: list[tuple[Path, dict]]) -> tuple[Path, dict]:
    """method 우선순위 manual>auto_sub>stt, 동률 시 extracted_at 최신 (BR-SEL-3/4)."""
    # 1차로 extracted_at 내림차순(최신 우선) → 2차로 priority 최소를 stable 하게 선택
    by_latest = sorted(
        loaded,
        key=lambda it: it[1]["extraction"].get("extracted_at", ""),
        reverse=True,
    )
    return min(
        by_latest,
        key=lambda it: METHOD_PRIORITY.get(it[1]["extraction"].get("method", ""), 99),
    )


def resolve_input(target: Path) -> tuple[Path, dict]:
    """입력 경로 → (선택된 canonical 경로, data). 파일=단건, 디렉토리=best-variant."""
    if not target.exists():
        raise IngestError(f"입력 경로 부재: {target}")
    if target.is_file():
        return target, load_canonical(target)
    loaded: list[tuple[Path, dict]] = []
    for p in sorted(target.glob("*.json")):
        try:
            loaded.append((p, load_canonical(p)))
        except (IngestError, json.JSONDecodeError):
            continue  # canonical 이 아닌 .json 은 후보에서 제외
    if not loaded:
        raise IngestError(f"canonical 후보 0건: {target}")
    return select_best(loaded)


# --------------------------------------------------------------------------- #
# 필드 매핑 + verbatim 본문 (P-MAP-*, BR-BODY-*)
# --------------------------------------------------------------------------- #
def _date_of(iso: str | None) -> str:
    """ISO datetime → YYYY-MM-DD (last_verified, P-MAP-5)."""
    if not iso:
        return ""
    try:
        return datetime.fromisoformat(str(iso)).date().isoformat()
    except ValueError:
        return str(iso)[:10]


def build_frontmatter(data: dict, ingested_date: str) -> dict:
    """canonical → raw frontmatter. 키 순서 고정(결정성). P-MAP-1~10."""
    video = data["video"]
    extraction = data["extraction"]
    duration = video.get("duration_seconds")
    fm: dict = {
        "title": video.get("title") or video["id"],          # P-MAP-1
        "source_url": video.get("url", ""),                   # P-MAP-2
        "source_date": video.get("upload_date") or "",        # P-MAP-3
        "source_type": MEDIA_TYPE,                            # P-MAP-4
        "last_verified": _date_of(extraction.get("extracted_at")),  # P-MAP-5
        "ingested_date": ingested_date,                       # P-MAP-6
        "tier": "raw",                                        # P-MAP-7
        "extraction_method": extraction.get("method", ""),   # P-MAP-8
    }
    if extraction.get("method") == "stt":                     # P-MAP-9
        fm["stt_model"] = extraction.get("model")
        fm["stt_engine"] = extraction.get("engine")
    fm["channel"] = video.get("channel") or ""               # P-MAP-10
    fm["duration_seconds"] = duration if duration is not None else ""
    fm["language"] = video.get("language") or extraction.get("language") or ""
    return fm


def _hms(seconds: float) -> str:
    total = int(seconds)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def build_body(data: dict) -> str:
    """full_text + 타임스탬프 segments 를 verbatim 으로 (BR-BODY-1, 무수정)."""
    video = data["video"]
    lines = [
        f"# {video.get('title') or video['id']}",
        "",
        "## 전체 스크립트",
        "",
        data.get("full_text", ""),
        "",
        "## 타임스탬프 세그먼트",
        "",
    ]
    for seg in data.get("segments", []):
        lines.append(f"- `{_hms(seg['start'])}` {seg['text']}")
    return "\n".join(lines) + "\n"


def render_page(frontmatter: dict, body: str) -> str:
    fm_yaml = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False, default_flow_style=False)
    return f"---\n{fm_yaml}---\n\n{body}"


# --------------------------------------------------------------------------- #
# atomic 산출 + 멱등 (BR-TXN-1, BR-IDEM-1, FR-6)
# --------------------------------------------------------------------------- #
def atomic_commit(
    out_dir: Path, video_id: str, page_text: str, canonical: dict, force: bool
) -> tuple[Path, Path, bool]:
    """raw .md + canonical .json 을 한 트랜잭션으로. 둘째 실패 시 첫째 롤백."""
    md_path = out_dir / f"{video_id}.md"
    json_path = out_dir / f"{video_id}.json"
    if md_path.exists() and not force:
        return md_path, json_path, True  # skip (멱등)

    out_dir.mkdir(parents=True, exist_ok=True)
    tmp_root = Path(tempfile.mkdtemp(dir=out_dir))
    try:
        tmp_md = tmp_root / "c.md"
        tmp_json = tmp_root / "c.json"
        tmp_md.write_text(page_text, encoding="utf-8")
        tmp_json.write_text(json.dumps(canonical, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp_md, md_path)
        try:
            os.replace(tmp_json, json_path)
        except BaseException:
            md_path.unlink(missing_ok=True)  # 롤백 — .md 만 남는 부분 산출물 방지
            raise
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)
    return md_path, json_path, False


# --------------------------------------------------------------------------- #
# orchestrator
# --------------------------------------------------------------------------- #
def ingest(
    target: Path, *, out_dir: Path = DEFAULT_OUT, force: bool = False, now: str | None = None
) -> tuple[Path, Path, bool]:
    """canonical 입력 → raw/sources/video 페이지. (md_path, json_path, skipped)."""
    ingested_date = now[:10] if now else datetime.now(timezone.utc).date().isoformat()
    _, data = resolve_input(target)
    video_id = data["video"]["id"]
    if "/" in video_id or "\\" in video_id:
        raise IngestError(f"video.id 에 경로 구분자 포함 — 거부: {video_id!r}")
    page = render_page(build_frontmatter(data, ingested_date), build_body(data))
    return atomic_commit(out_dir, video_id, page, data, force)


def main() -> int:
    ap = argparse.ArgumentParser(description="YouTube canonical JSON → cs-study raw/sources/video importer")
    ap.add_argument("path", help="canonical JSON 파일 또는 out/<id>/ 디렉토리")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="출력 디렉토리 (기본 raw/sources/video)")
    ap.add_argument("--force", action="store_true", help="기존 산출물 덮어쓰기")
    ap.add_argument("--now", default=None, help="ingested_date 주입 (테스트 결정성, ISO)")
    args = ap.parse_args()

    try:
        md_path, json_path, skipped = ingest(
            Path(args.path).expanduser(),
            out_dir=Path(args.out).expanduser(),
            force=args.force,
            now=args.now,
        )
    except (IngestError, json.JSONDecodeError, OSError, KeyError, TypeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    if skipped:
        print(f"skip (존재, --force 로 재생성): {md_path}")
    else:
        print(f"ingested: {md_path}\n          {json_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
