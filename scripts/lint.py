#!/usr/bin/env python3
"""
LLM Wiki Lint — 6축 + AGENTS.md directive 자동 검증.

사용:
    python3 scripts/lint.py                    # 전수 검증
    python3 scripts/lint.py --changed          # git diff base..HEAD 변경 파일만
    python3 scripts/lint.py --paths wiki/      # 특정 path 만
    python3 scripts/lint.py --report markdown  # markdown report 출력

검증 축:
    1. 정확도 (Accuracy)     : source_paths ≥1 + provenance
    2. 전문성 (Expertise)    : page_type 표준 섹션 (soft)
    3. 일관성 (Consistency)  : taxonomy controlled vocab
    4. 논리성 (Logical)      : page 간 모순 — logic-proposition-checker 호출 (별도 wrapper)
    5. 정합성 (Integrity)    : orphan / broken link / index 등재 / log 추적
    6. 재현성·시의성         : source_date + last_verified + superseded
    + raw 필수 필드          : raw/sources/ 페이지 RAW_REQUIRED_FIELDS 강제
    + AGENTS.md directive    : write scope 위반 (model_id 본문 grep 은 ADR-0001 로 폐기)

본 파일은 skeleton. dogfood 1주 후 calibration (P50/P90) 으로 임계 조정.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Iterator

try:
    import yaml  # PyYAML
except ImportError:
    print("ERROR: PyYAML 필요. `pip install pyyaml`", file=sys.stderr)
    sys.exit(1)


REPO_ROOT = Path(__file__).resolve().parent.parent
META_DIR = REPO_ROOT / "_meta"
WIKI_DIR = REPO_ROOT / "wiki"
WIKI_TEMPLATE_DIR = WIKI_DIR / "templates"
WIKI_SYSTEM_PAGES = {
    WIKI_DIR / "overview.md",
    WIKI_DIR / "index.md",
    WIKI_DIR / "log.md",
}
VERIFIED_EVIDENCE_ROOTS = (
    REPO_ROOT / "raw" / "sources" / "papers",
    REPO_ROOT / "raw" / "sources" / "web",
    REPO_ROOT / "raw" / "sources" / "urls",
)

# ADR-0001 (2026-06-04): 페이지 본문 model_id/자기추론 grep 규칙 폐기.
# 모델명은 taxonomy.md 가 wiki entity vocab 으로 요구(예: gpt-5, claude-opus-4-7)하므로
# 본문 grep 은 taxonomy 와 모순 + raw verbatim 원본 보존(AGENTS.md raw 등급) 위반.
# model_id alias 규율은 LLM 호출 site(scripts) 코드 규약으로만 유지(마크다운 검사 아님).

# wiki/ content page frontmatter 필수 필드 (frontmatter-spec.md §wiki §15 필드)
WIKI_REQUIRED_FIELDS = {
    "title", "tier", "page_type", "domain", "domain_confidence",
    "shared_scope", "tags", "status", "date_created", "date_updated",
    "source_paths", "source_count", "provenance", "summary", "evergreen",
}

# raw/ frontmatter 최소 필드
RAW_REQUIRED_FIELDS = {"title", "source_url", "source_date", "source_type", "last_verified", "tier"}

# LLM write 금지 영역 (Panel A 결정)
LLM_READONLY_DIRS = {"cs", "development", "coding-test", "lang", "tools"}

# 재현성·시의성 임계
WARN_AGE_DAYS = 180        # ≥6m
HARDFAIL_AGE_DAYS = 730    # ≥2y

CLAIM_TABLE_COLUMNS = ["id", "primary", "claim", "status", "evidence", "notes"]
CLAIM_STATUSES = ("claimed", "corroborated", "verified", "rejected")
CLAIM_STATUS_SET = set(CLAIM_STATUSES)
ROLLUP_RANK = {"claimed": 0, "corroborated": 1, "verified": 2}
PAGE_TYPES = {"concept", "entity", "comparison", "benchmark", "dataset", "method"}


class Finding:
    __slots__ = ("severity", "axis", "path", "line", "message")

    def __init__(self, severity: str, axis: str, path: Path, line: int | None, message: str):
        self.severity = severity  # HIGH | MEDIUM | LOW
        self.axis = axis          # 1..6 or "directive"
        self.path = path
        self.line = line
        self.message = message

    def to_dict(self) -> dict:
        return {
            "severity": self.severity,
            "axis": self.axis,
            "path": str(self.path.relative_to(REPO_ROOT)),
            "line": self.line,
            "message": self.message,
        }


def parse_frontmatter(text: str) -> tuple[dict | None, int]:
    """YAML frontmatter 추출. (data, frontmatter 끝 라인) 반환. 없으면 (None, 0)."""
    if not text.startswith("---\n"):
        return None, 0
    end_index = text.find("\n---\n", 4)
    if end_index == -1:
        return None, 0
    fm_text = text[4:end_index]
    try:
        return yaml.safe_load(fm_text), text[:end_index].count("\n") + 1
    except yaml.YAMLError:
        return None, 0


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def is_wiki_page(path: Path) -> bool:
    return is_relative_to(path, WIKI_DIR) and path.suffix == ".md"


def is_wiki_template(path: Path) -> bool:
    return is_relative_to(path, WIKI_TEMPLATE_DIR)


def is_wiki_system_page(path: Path) -> bool:
    try:
        resolved = path.resolve()
    except OSError:
        return False
    return resolved in {p.resolve() for p in WIKI_SYSTEM_PAGES}


def is_wiki_content_page(path: Path) -> bool:
    return is_wiki_page(path) and not is_wiki_template(path) and not is_wiki_system_page(path)


def strip_fenced_code_blocks(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def resolve_obsidian_link(path: Path, link: str) -> Path:
    clean = link.strip().split("#", 1)[0]
    if not clean:
        return path.resolve()
    if clean.startswith("/"):
        return (REPO_ROOT / clean.lstrip("/")).resolve()
    root_candidate = (REPO_ROOT / clean).resolve()
    if link_exists(root_candidate):
        return root_candidate
    return (path.parent / clean).resolve()


def link_exists(target: Path) -> bool:
    if target.is_file():
        return True
    if target.is_dir():
        return (target / "index.md").is_file() or (target / "overview.md").is_file()
    if target.suffix:
        return False
    md_target = target.with_suffix(".md")
    if md_target.exists():
        return True
    return (target / "index.md").exists() or (target / "overview.md").exists()


def is_curated_verified_evidence(evidence: str) -> bool:
    if not isinstance(evidence, str) or not evidence:
        return False
    target = (REPO_ROOT / evidence).resolve()
    return (target.is_file()
            and target.suffix == ".md"
            and any(is_relative_to(target, root) for root in VERIFIED_EVIDENCE_ROOTS))


def split_pipe_row(line: str) -> list[str]:
    row = line.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [cell.replace(r"\|", "|").strip() for cell in re.split(r"(?<!\\)\|", row)]


def is_delimiter_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def parse_claim_table(text: str) -> tuple[list[dict[str, str]] | None, str | None]:
    lines = text.splitlines()
    heading_index = next((i for i, line in enumerate(lines) if line.strip() == "## Claims"), None)
    if heading_index is None:
        return None, "missing ## Claims section"

    index = heading_index + 1
    while index < len(lines) and not lines[index].strip():
        index += 1
    if index + 1 >= len(lines):
        return None, "missing claim table header or delimiter"

    header = split_pipe_row(lines[index])
    delimiter = split_pipe_row(lines[index + 1])
    if header != CLAIM_TABLE_COLUMNS:
        return None, f"invalid claim table columns: {header}"
    if len(delimiter) != len(CLAIM_TABLE_COLUMNS) or not is_delimiter_row(delimiter):
        return None, "invalid claim table delimiter row"

    rows: list[dict[str, str]] = []
    index += 2
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            break
        if not line.lstrip().startswith("|"):
            break
        cells = split_pipe_row(line)
        if len(cells) != len(CLAIM_TABLE_COLUMNS):
            return None, f"invalid claim table row cell count at line {index + 1}: {len(cells)}"
        rows.append(dict(zip(CLAIM_TABLE_COLUMNS, cells)))
        index += 1
    if not rows:
        return None, "claim table has no rows"
    return rows, None


def calculate_claim_rollup(rows: list[dict[str, str]]) -> tuple[str, dict[str, int]]:
    counts = {status: 0 for status in CLAIM_STATUSES}
    for row in rows:
        counts[row["status"]] += 1

    primary_statuses = [row["status"] for row in rows if row["primary"] == "true"]
    if not primary_statuses:
        return "claimed", counts
    if all(status == "rejected" for status in primary_statuses):
        return "rejected", counts
    if counts["rejected"] == 0 and all(status == "verified" for status in primary_statuses):
        return "verified", counts
    if counts["rejected"] == 0 and all(ROLLUP_RANK.get(status, -1) >= ROLLUP_RANK["corroborated"] for status in primary_statuses):
        return "corroborated", counts
    return "claimed", counts


def iter_markdown_files(paths: list[Path]) -> Iterator[Path]:
    for p in paths:
        if p.is_file() and p.suffix == ".md":
            yield p
        elif p.is_dir():
            for child in p.rglob("*.md"):
                yield child


def check_axis_1_accuracy(path: Path, text: str, fm: dict | None) -> list[Finding]:
    """축 1 정확도 — source_paths ≥1 + provenance (wiki 한정)."""
    findings = []
    if not is_wiki_content_page(path):
        return findings
    if not fm:
        findings.append(Finding("HIGH", "1", path, 1, "frontmatter 부재"))
        return findings
    if not fm.get("source_paths"):
        findings.append(Finding("HIGH", "1", path, 1, "source_paths 누락 또는 빈 배열"))
    if fm.get("provenance") not in {"extracted", "inferred", "ambiguous"}:
        findings.append(Finding("HIGH", "1", path, 1, f"provenance 누락 또는 invalid: {fm.get('provenance')}"))
    return findings


def check_axis_5_integrity_broken_links(path: Path, text: str) -> list[Finding]:
    """축 5 정합성 — broken link 검출."""
    findings = []
    if is_wiki_template(path):
        return findings
    text = strip_fenced_code_blocks(text)
    # markdown link [text](path) 와 wikilink [[path]] 모두 검사
    md_links = re.findall(r"\[[^\]]*\]\(([^)]+)\)", text)
    wikilinks = re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", text)
    for link in md_links + wikilinks:
        if link.startswith(("http://", "https://", "mailto:", "#")):
            continue
        link_path = resolve_obsidian_link(path, link)
        if not link_exists(link_path):
            findings.append(Finding("HIGH", "5", path, None, f"broken link: {link}"))
    return findings


def check_wiki_required_fields(path: Path, fm: dict | None) -> list[Finding]:
    """frontmatter-spec.md §wiki — wiki content page 필수 필드 강제."""
    findings = []
    if not is_wiki_content_page(path):
        return findings
    if not fm:
        findings.append(Finding("HIGH", "frontmatter", path, 1, "wiki content page frontmatter 부재"))
        return findings
    missing = sorted(WIKI_REQUIRED_FIELDS - set(fm.keys()))
    if missing:
        findings.append(Finding("HIGH", "frontmatter", path, 1,
                                f"wiki 필수 필드 누락: {', '.join(missing)}"))
    enum_fields = {
        "tier": {"llm-synthesis"},
        "page_type": PAGE_TYPES,
        "domain_confidence": {"high", "medium", "low"},
        "shared_scope": {"domain", "global"},
        "status": {"draft", "active", "staged", "archived"},
        "provenance": {"extracted", "inferred", "ambiguous"},
    }
    for field, allowed in enum_fields.items():
        if field in fm and fm.get(field) not in allowed:
            findings.append(Finding("HIGH", "frontmatter", path, 1,
                                    f"{field} invalid: {fm.get(field)}"))
    for field in ("title", "summary"):
        if field in fm and (not isinstance(fm.get(field), str) or not fm.get(field).strip()):
            findings.append(Finding("HIGH", "frontmatter", path, 1,
                                    f"{field} 형식 오류: 비어 있지 않은 문자열 필요"))
    for field in ("date_created", "date_updated"):
        value = fm.get(field)
        valid_date = isinstance(value, date)
        if isinstance(value, str):
            try:
                date.fromisoformat(value)
                valid_date = True
            except ValueError:
                valid_date = False
        if field in fm and not valid_date:
            findings.append(Finding("HIGH", "frontmatter", path, 1,
                                    f"{field} 형식 오류: ISO 8601 date 필요"))
    if "domain" in fm and (not isinstance(fm.get("domain"), str)
                           or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", fm.get("domain", ""))):
        findings.append(Finding("HIGH", "frontmatter", path, 1, "domain 형식 오류"))
    if "tags" in fm and (not isinstance(fm.get("tags"), list)
                         or not all(isinstance(tag, str) for tag in fm.get("tags", []))):
        findings.append(Finding("HIGH", "frontmatter", path, 1, "tags 형식 오류: 문자열 배열 필요"))
    source_paths = fm.get("source_paths")
    source_count = fm.get("source_count")
    if "source_paths" in fm and (not isinstance(source_paths, list)
                                 or not source_paths
                                 or not all(isinstance(source, str) and source.strip() for source in source_paths)):
        findings.append(Finding("HIGH", "frontmatter", path, 1,
                                "source_paths 형식 오류: 비어 있지 않은 문자열 배열 필요"))
    if "source_count" in fm and (type(source_count) is not int or source_count < 0):
        findings.append(Finding("HIGH", "frontmatter", path, 1,
                                "source_count 형식 오류: 비음수 정수 필요"))
    elif isinstance(source_paths, list) and source_count is not None and source_count != len(source_paths):
        findings.append(Finding("HIGH", "frontmatter", path, 1,
                                f"source_count 불일치: {source_count} != {len(source_paths)}"))
    if "evergreen" in fm and type(fm.get("evergreen")) is not bool:
        findings.append(Finding("HIGH", "frontmatter", path, 1, "evergreen 형식 오류: boolean 필요"))
    return findings


def check_claim_table(path: Path, text: str, fm: dict | None) -> list[Finding]:
    """source summary claim table schema 와 derived roll-up 정합성 검증."""
    findings = []
    if not is_wiki_content_page(path):
        return findings
    if "## Claims" not in text and not (fm and ("verification_status" in fm or "claim_status_counts" in fm)):
        return findings
    rows, error = parse_claim_table(text)
    if error or rows is None:
        findings.append(Finding("HIGH", "frontmatter", path, None, f"claim table invalid: {error}"))
        return findings

    seen_ids: set[str] = set()
    for row in rows:
        claim_id = row["id"]
        if not re.fullmatch(r"C[1-9][0-9]*", claim_id):
            findings.append(Finding("HIGH", "frontmatter", path, None, f"invalid claim id: {claim_id}"))
        if claim_id in seen_ids:
            findings.append(Finding("HIGH", "frontmatter", path, None, f"duplicate claim id: {claim_id}"))
        seen_ids.add(claim_id)
        if row["primary"] not in {"true", "false"}:
            findings.append(Finding("HIGH", "frontmatter", path, None, f"invalid claim primary: {row['primary']}"))
        if row["status"] not in CLAIM_STATUS_SET:
            findings.append(Finding("HIGH", "frontmatter", path, None, f"invalid claim status: {row['status']}"))
        if not row["claim"]:
            findings.append(Finding("HIGH", "frontmatter", path, None, f"empty claim text: {claim_id}"))
        if not row["evidence"]:
            findings.append(Finding("HIGH", "frontmatter", path, None, f"empty claim evidence: {claim_id}"))
        if row["status"] == "verified":
            if re.fullmatch(r"raw/sources/video/[A-Za-z0-9_-]+\.md", row["evidence"]):
                findings.append(Finding("HIGH", "frontmatter", path, None,
                                        f"영상 단독 evidence로 verified 금지: {claim_id}"))
            elif not is_curated_verified_evidence(row["evidence"]):
                findings.append(Finding("HIGH", "frontmatter", path, None,
                                        f"verified evidence 부재 또는 허용 경로 이탈: {claim_id}"))

    if findings:
        return findings

    rollup, counts = calculate_claim_rollup(rows)
    if not fm or fm.get("verification_status") is None:
        findings.append(Finding("HIGH", "frontmatter", path, 1, "verification_status 누락"))
    elif fm.get("verification_status") != rollup:
        findings.append(Finding("HIGH", "frontmatter", path, 1,
                                f"verification_status 불일치: {fm.get('verification_status')} != {rollup}"))
    if not fm or fm.get("claim_status_counts") is None:
        findings.append(Finding("HIGH", "frontmatter", path, 1, "claim_status_counts 누락"))
    else:
        raw_counts = fm.get("claim_status_counts")
        if not isinstance(raw_counts, dict):
            findings.append(Finding("HIGH", "frontmatter", path, 1,
                                    "claim_status_counts 형식 오류: status별 정수 mapping 필요"))
        elif set(raw_counts) != CLAIM_STATUS_SET:
            findings.append(Finding("HIGH", "frontmatter", path, 1,
                                    f"claim_status_counts key 오류: {sorted(raw_counts)}"))
        elif any(type(value) is not int or value < 0 for value in raw_counts.values()):
            findings.append(Finding("HIGH", "frontmatter", path, 1,
                                    "claim_status_counts 값 오류: 비음수 정수 필요"))
        elif raw_counts != counts:
            findings.append(Finding("HIGH", "frontmatter", path, 1,
                                    f"claim_status_counts 불일치: {raw_counts} != {counts}"))
    return findings


def check_axis_6_recency(path: Path, fm: dict | None) -> list[Finding]:
    """축 6 재현성·시의성 — last_verified 임계."""
    findings = []
    if not fm:
        return findings
    if fm.get("evergreen"):
        return findings
    last_verified = fm.get("last_verified")
    if not last_verified:
        # raw/ 페이지면 last_verified 필수
        if "raw/sources/" in str(path.relative_to(REPO_ROOT)):
            findings.append(Finding("HIGH", "6", path, 1, "raw 페이지에 last_verified 누락"))
        return findings
    from datetime import date, datetime
    try:
        if isinstance(last_verified, date):
            verified_date = last_verified
        else:
            verified_date = datetime.fromisoformat(str(last_verified)).date()
        age_days = (date.today() - verified_date).days
        if age_days >= HARDFAIL_AGE_DAYS:
            findings.append(Finding("HIGH", "6", path, 1, f"last_verified ≥{HARDFAIL_AGE_DAYS}d (실제 {age_days}d). evergreen=true 면제 가능"))
        elif age_days >= WARN_AGE_DAYS:
            findings.append(Finding("MEDIUM", "6", path, 1, f"last_verified ≥{WARN_AGE_DAYS}d (실제 {age_days}d)"))
    except (ValueError, TypeError):
        findings.append(Finding("MEDIUM", "6", path, 1, f"last_verified 형식 오류: {last_verified}"))
    return findings


def check_raw_required_fields(path: Path, fm: dict | None) -> list[Finding]:
    """frontmatter-spec.md §raw — raw/sources/ 페이지 필수 필드 강제.

    ADR-0001 / frontmatter-spec.md 의 'raw 최소 필드 hard-fail' 을 실제 구현
    (RAW_REQUIRED_FIELDS 가 선언만 되고 미호출이던 skeleton 갭 완성).
    """
    findings = []
    if "raw/sources/" not in str(path.relative_to(REPO_ROOT)):
        return findings
    if not fm:
        findings.append(Finding("HIGH", "frontmatter", path, 1, "raw 페이지 frontmatter 부재"))
        return findings
    missing = sorted(RAW_REQUIRED_FIELDS - set(fm.keys()))
    if missing:
        findings.append(Finding("HIGH", "frontmatter", path, 1,
                                f"raw 필수 필드 누락: {', '.join(missing)}"))
    return findings


def check_directive_write_scope(path: Path, fm: dict | None) -> list[Finding]:
    """AGENTS.md directive — LLM write scope 위반 (LLM commit author=swan-bot 가 read-only 영역 수정)."""
    # 본 check 는 git hook 또는 PreToolUse hook 단계에서 더 정확. lint.py 는 frontmatter author 기반 추정만.
    findings = []
    rel = str(path.relative_to(REPO_ROOT))
    first_segment = rel.split("/", 1)[0]
    if first_segment not in LLM_READONLY_DIRS:
        return findings
    # tier=llm-synthesis 면 위반 의심
    if fm and fm.get("tier") == "llm-synthesis":
        findings.append(Finding("HIGH", "directive", path, 1,
                                f"LLM write scope 위반: read-only 영역에 llm-synthesis 페이지"))
    return findings


def collect_findings(paths: list[Path]) -> list[Finding]:
    findings = []
    for path in iter_markdown_files(paths):
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue
        fm, _ = parse_frontmatter(text)
        findings.extend(check_axis_1_accuracy(path, text, fm))
        findings.extend(check_axis_5_integrity_broken_links(path, text))
        findings.extend(check_axis_6_recency(path, fm))
        findings.extend(check_wiki_required_fields(path, fm))
        findings.extend(check_claim_table(path, text, fm))
        findings.extend(check_raw_required_fields(path, fm))
        findings.extend(check_directive_write_scope(path, fm))
        # 축 3 (taxonomy controlled vocab) · 축 5 (orphan) 은 별도 wrapper 필요 — TODO
        # 축 4 (logic-proposition-checker 호출) 은 외부 subagent — TODO
    return findings


def git_changed_paths(base: str = "main") -> list[Path]:
    try:
        out = subprocess.run(
            ["git", "diff", "--name-only", f"{base}..HEAD"],
            check=True, capture_output=True, text=True,
        ).stdout
    except subprocess.CalledProcessError:
        return []
    return [REPO_ROOT / line.strip() for line in out.splitlines() if line.strip().endswith(".md")]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paths", nargs="*", default=None, help="특정 path. 기본 = wiki/ + raw/ + _meta/ + AGENTS.md")
    ap.add_argument("--changed", action="store_true", help="git diff base..HEAD 변경 .md 만")
    ap.add_argument("--base", default="main")
    ap.add_argument("--report", choices=["text", "jsonl", "markdown"], default="text")
    args = ap.parse_args()

    if args.changed:
        paths = git_changed_paths(args.base)
    elif args.paths:
        paths = [Path(p).resolve() for p in args.paths]
    else:
        paths = [WIKI_DIR, REPO_ROOT / "raw", META_DIR, REPO_ROOT / "AGENTS.md"]
        paths = [p for p in paths if p.exists()]

    findings = collect_findings(paths)
    high = sum(1 for f in findings if f.severity == "HIGH")
    medium = sum(1 for f in findings if f.severity == "MEDIUM")

    if args.report == "jsonl":
        for f in findings:
            print(json.dumps(f.to_dict(), ensure_ascii=False))
    elif args.report == "markdown":
        print(f"# Lint Report\n\n- HIGH: {high}\n- MEDIUM: {medium}\n")
        for f in findings:
            print(f"- [{f.severity}] axis {f.axis} `{f.to_dict()['path']}`:{f.line or '?'} — {f.message}")
    else:
        for f in findings:
            loc = f"{f.to_dict()['path']}:{f.line or '?'}"
            print(f"[{f.severity}] axis {f.axis} {loc} — {f.message}")
        print(f"\n--- Summary: HIGH={high}, MEDIUM={medium} ---")

    # hard-fail = HIGH ≥1
    return 1 if high >= 1 else 0


if __name__ == "__main__":
    sys.exit(main())
