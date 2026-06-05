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

# ADR-0001 (2026-06-04): 페이지 본문 model_id/자기추론 grep 규칙 폐기.
# 모델명은 taxonomy.md 가 wiki entity vocab 으로 요구(예: gpt-5, claude-opus-4-7)하므로
# 본문 grep 은 taxonomy 와 모순 + raw verbatim 원본 보존(AGENTS.md raw 등급) 위반.
# model_id alias 규율은 LLM 호출 site(scripts) 코드 규약으로만 유지(마크다운 검사 아님).

# wiki/ frontmatter 필수 필드 (frontmatter-spec.md §wiki §14 필드)
WIKI_REQUIRED_FIELDS = {
    "title", "tier", "page_type", "domain", "domain_confidence",
    "tags", "status", "date_created", "date_updated",
    "source_paths", "provenance", "summary",
}

# raw/ frontmatter 최소 필드
RAW_REQUIRED_FIELDS = {"title", "source_url", "source_date", "source_type", "last_verified", "tier"}

# LLM write 금지 영역 (Panel A 결정)
LLM_READONLY_DIRS = {"cs", "development", "coding-test", "lang", "tools"}

# 재현성·시의성 임계
WARN_AGE_DAYS = 180        # ≥6m
HARDFAIL_AGE_DAYS = 730    # ≥2y


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
    if "wiki/" not in str(path.relative_to(REPO_ROOT)):
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
    # markdown link [text](path) 와 wikilink [[path]] 모두 검사
    md_links = re.findall(r"\[[^\]]*\]\(([^)]+)\)", text)
    wikilinks = re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", text)
    for link in md_links + wikilinks:
        if link.startswith(("http://", "https://", "mailto:", "#")):
            continue
        link_path = (path.parent / link).resolve()
        # .md 확장자 보강 시도
        if not link_path.exists() and not link.endswith(".md"):
            link_path = link_path.with_suffix(".md")
        if not link_path.exists():
            findings.append(Finding("HIGH", "5", path, None, f"broken link: {link}"))
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
