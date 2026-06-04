#!/usr/bin/env python3
"""extract→ingest 오케스트레이터 — 한 명령으로 추출(ytscript) + 적재(ingest).

단방향 의존: ytscript 는 subprocess(CLI 계약)로, ingest 는 cs-study 내부 모듈로 호출.
추출기 python API 를 import 하지 않는다(canonical 포맷·CLI 에만 의존 → 순환·양방향 0).
wiki 합성(2차)은 raw→wiki 사람 review 게이트(AGENTS.md:85-91)라 자동화 경계 밖 —
enabled 여도 raw 적재 후 정지하고 안내만 한다.

사용:
    python3 scripts/pipeline.py <URL> [--config _meta/pipeline.yaml] [--force]

설정: _meta/pipeline.yaml (extractor / ingest / wiki 섹션). 설계: docs/architecture.md §7.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

try:
    import yaml  # PyYAML
except ImportError:
    print("ERROR: PyYAML 필요. `pip install pyyaml`", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import ingest  # cs-study 내부 모듈 (단방향)

DEFAULT_CONFIG = REPO_ROOT / "_meta" / "pipeline.yaml"

# ytscript 로 passthrough 하는 extractor 옵션 (YAML key → CLI flag).
_PASSTHROUGH = ("source", "whisper_model", "whisper_batch_size", "langs", "whisper_prompt", "proxy")


class PipelineError(Exception):
    """파이프라인 단계 실패 — exit 1."""


def load_config(path: Path) -> dict:
    if not path.exists():
        raise PipelineError(f"설정 파일 부재: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _flag_value(val) -> str:
    """YAML 값 → CLI 인자 문자열. list(langs) 는 쉼표 결합."""
    if isinstance(val, list):
        return ",".join(str(v) for v in val)
    return str(val)


def run_extractor(url: str, ex_cfg: dict) -> Path:
    """ytscript 를 subprocess 로 실행하고 canonical JSON 경로를 회수 (stage 1)."""
    project = Path(ex_cfg.get("project", "")).expanduser()
    if not project.exists():
        raise PipelineError(f"추출기 project 경로 부재: {project}")
    output_dir = Path(ex_cfg.get("output_dir") or (project / "out")).expanduser()

    cmd = ["uv", "run", "--project", str(project), "ytscript", url,
           "--output-dir", str(output_dir), "--print-json-path"]
    cfg_file = ex_cfg.get("config")
    if cfg_file:  # ytscript --config 전달 — 모든 추출기 옵션을 한 파일로(우선순위: per-flag > config)
        cmd += ["--config", str(Path(cfg_file).expanduser())]
    for key in _PASSTHROUGH:
        val = ex_cfg.get(key)
        if val not in (None, ""):
            cmd += [f"--{key.replace('_', '-')}", _flag_value(val)]

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.stderr:
        sys.stderr.write(proc.stderr)  # 추출기 상태(진행률·skip 등) passthrough
    if proc.returncode != 0:
        raise PipelineError(f"추출 실패 (ytscript exit {proc.returncode})")
    lines = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
    if not lines:
        raise PipelineError("추출기가 canonical JSON 경로를 출력하지 않음 (--print-json-path)")
    candidate = lines[-1]
    if not candidate.endswith(".json"):
        raise PipelineError(f"추출기 stdout 마지막 줄이 canonical JSON 경로가 아님: {candidate!r}")
    json_path = Path(candidate)
    if not json_path.is_absolute():
        json_path = (project / json_path).resolve()
    if not json_path.exists():
        raise PipelineError(f"추출 산출 canonical 부재: {json_path}")
    return json_path


def run(url: str, config: dict, *, force: bool | None = None) -> tuple[Path, Path, bool]:
    """stage 1 추출 → stage 2 적재. wiki(stage 3)는 게이트 정지."""
    json_path = run_extractor(url, config.get("extractor", {}))

    ing = config.get("ingest", {})
    out_dir = Path(ing.get("out", "raw/sources/video"))
    if not out_dir.is_absolute():
        out_dir = REPO_ROOT / out_dir
    force_flag = ing.get("force", False) if force is None else force
    md_path, json_out, skipped = ingest.ingest(json_path, out_dir=out_dir, force=force_flag)

    if config.get("wiki", {}).get("enabled"):
        print(
            "\n[wiki stage] raw→wiki 승격은 사람 review 게이트(AGENTS.md:85-91) — 자동 정지.\n"
            f"  raw 페이지 준비됨: {md_path}\n"
            "  검토 후 2차 합성(Claude Code/Codex CLI 세션)을 별도 실행하세요.",
            file=sys.stderr,
        )
    return md_path, json_out, skipped


def main() -> int:
    ap = argparse.ArgumentParser(description="extract→ingest 파이프라인 (ytscript + ingest)")
    ap.add_argument("url", help="YouTube 영상 URL")
    ap.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="파이프라인 설정 YAML")
    ap.add_argument("--force", action="store_true", help="기존 raw 산출물 덮어쓰기")
    args = ap.parse_args()

    try:
        config = load_config(args.config)
        md_path, json_out, skipped = run(args.url, config, force=args.force or None)
    except (PipelineError, ingest.IngestError, OSError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    if skipped:
        print(f"skip (이미 적재됨, --force 로 재생성): {md_path}")
    else:
        print(f"적재 완료: {md_path}\n           {json_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
