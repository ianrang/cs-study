#!/usr/bin/env python3
"""
Repository lint dispatcher — canonical wiki + legacy raw/authored 검증.

사용:
    python3 scripts/lint.py                    # 전수 검증
    python3 scripts/lint.py --changed          # git diff base..HEAD 변경 파일만
    python3 scripts/lint.py --paths wiki/      # 특정 path 만
    python3 scripts/lint.py --report markdown  # markdown report 출력

wiki 요청은 `knowledge.check.check_target`에 단독 위임한다. 이 파일은 wiki 규칙을
복제하지 않고 legacy curated raw/authored의 broken link·recency·필수 필드와
AGENTS.md directive만 직접 검사한다.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    import yaml  # PyYAML
    from knowledge.artifacts import ArtifactError, verify_manifest
    from knowledge.check import check_target, generated_surface_findings
    from knowledge.materialize import generated_drift
except ImportError:
    print(
        "ERROR: lint dependencies 필요. `pip install -r requirements-lint.txt`",
        file=sys.stderr,
    )
    sys.exit(1)


REPO_ROOT = Path(__file__).resolve().parent.parent
META_DIR = REPO_ROOT / "_meta"
WIKI_DIR = REPO_ROOT / "wiki"
RAW_SOURCES_DIR = REPO_ROOT / "raw" / "sources"

# ADR-0001 (2026-06-04): 페이지 본문 model_id/자기추론 grep 규칙 폐기.
# 모델명은 taxonomy.md 가 wiki entity vocab 으로 요구(예: gpt-5, claude-opus-4-7)하므로
# 본문 grep 은 taxonomy 와 모순 + raw verbatim 원본 보존(AGENTS.md raw 등급) 위반.
# model_id alias 규율은 LLM 호출 site(scripts) 코드 규약으로만 유지(마크다운 검사 아님).

# raw/ frontmatter 최소 필드
RAW_REQUIRED_FIELDS = {"title", "source_url", "source_date", "source_type", "last_verified", "tier"}

# LLM write 금지 영역 (Panel A 결정)
LLM_READONLY_DIRS = {"cs", "development", "coding-test", "lang", "tools"}

# 재현성·시의성 임계
WARN_AGE_DAYS = 180        # ≥6m
HARDFAIL_AGE_DAYS = 730    # ≥2y

SHA256_DIR_RE = re.compile(r"^[0-9a-f]{64}$")


def is_raw_source_path(path: Path) -> bool:
    try:
        path.relative_to(RAW_SOURCES_DIR)
    except ValueError:
        return False
    return True


class Finding:
    __slots__ = ("severity", "axis", "path", "line", "message")

    def __init__(self, severity: str, axis: str, path: Path, line: int | None, message: str):
        self.severity = severity  # HIGH | MEDIUM | LOW
        self.axis = axis          # 1..6 or "directive"
        self.path = path
        self.line = line
        self.message = message

    def to_dict(self) -> dict:
        try:
            display_path = self.path.relative_to(REPO_ROOT)
        except ValueError:
            display_path = self.path
        return {
            "severity": self.severity,
            "axis": self.axis,
            "path": str(display_path),
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


def _markdown_inventory(paths: list[Path]) -> tuple[list[Path], list[Finding]]:
    markdown_paths: list[Path] = []
    findings: list[Finding] = []

    def inventory_error(path: Path, message: str) -> None:
        findings.append(Finding("HIGH", "io", path, None, message))

    def add_file(path: Path) -> None:
        try:
            mode = path.lstat().st_mode
        except OSError as exc:
            inventory_error(path, f"Markdown inventory stat failure: {exc}")
            return
        if stat.S_ISLNK(mode):
            inventory_error(path, "Markdown inventory rejects symbolic links")
        elif not stat.S_ISREG(mode):
            inventory_error(path, "Markdown inventory requires a regular file")
        elif path.suffix == ".md" and not is_artifact_bundle_markdown(path):
            markdown_paths.append(path)

    for path in paths:
        try:
            mode = path.lstat().st_mode
        except OSError as exc:
            inventory_error(path, f"Markdown inventory stat failure: {exc}")
            continue
        if stat.S_ISLNK(mode):
            inventory_error(path, "Markdown inventory rejects symbolic links")
            continue
        if stat.S_ISREG(mode):
            add_file(path)
            continue
        if not stat.S_ISDIR(mode):
            inventory_error(path, "Markdown inventory requires a regular file or directory")
            continue

        def walk_error(exc: OSError, requested: Path = path) -> None:
            failed = Path(exc.filename) if exc.filename else requested
            inventory_error(failed, f"Markdown inventory walk failure: {exc}")

        for directory, names, filenames in os.walk(
            path, topdown=True, followlinks=False, onerror=walk_error
        ):
            names.sort()
            filenames.sort()
            parent = Path(directory)
            accepted_names: list[str] = []
            for name in names:
                child = parent / name
                try:
                    child_mode = child.lstat().st_mode
                except OSError as exc:
                    inventory_error(child, f"Markdown inventory stat failure: {exc}")
                    continue
                if stat.S_ISLNK(child_mode):
                    inventory_error(child, "Markdown inventory rejects symbolic links")
                elif stat.S_ISDIR(child_mode):
                    accepted_names.append(name)
                else:
                    inventory_error(child, "Markdown inventory requires a directory")
            names[:] = accepted_names
            for name in filenames:
                child = parent / name
                if child.suffix == ".md":
                    add_file(child)
    return markdown_paths, findings


def is_artifact_bundle_markdown(path: Path) -> bool:
    """Identify immutable content-addressed artifact Markdown payloads."""
    try:
        relative = path.resolve().relative_to(REPO_ROOT.resolve())
    except ValueError:
        return False
    parts = relative.parts
    shaped_as_bundle = (
        len(parts) == 6
        and parts[:2] == ("raw", "sources")
        and bool(parts[2])
        and bool(parts[3])
        and SHA256_DIR_RE.fullmatch(parts[4]) is not None
        and path.suffix == ".md"
    )
    if not shaped_as_bundle:
        return False
    try:
        manifest = verify_manifest(path.parent / "manifest.json")
    except (ArtifactError, OSError):
        return False
    declared_paths = {manifest.get("payload")}
    content = manifest.get("content")
    if isinstance(content, dict):
        declared_paths.add(content.get("path"))
    for asset in manifest.get("assets", []):
        if isinstance(asset, dict):
            declared_paths.add(asset.get("path"))
    return (
        manifest.get("source_type") == parts[2]
        and manifest.get("source_id") == parts[3]
        and manifest.get("artifact_digest") == f"sha256:{parts[4]}"
        and path.name in declared_paths
    )


def check_axis_5_integrity_broken_links(path: Path, text: str) -> list[Finding]:
    """축 5 정합성 — broken link 검출."""
    findings = []
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


def check_axis_6_recency(path: Path, fm: dict | None) -> list[Finding]:
    """축 6 재현성·시의성 — last_verified 임계."""
    findings = []
    if not fm:
        return findings
    relative = path.relative_to(REPO_ROOT)
    is_raw = is_raw_source_path(path)
    is_authored = bool(relative.parts) and relative.parts[0] in LLM_READONLY_DIRS
    last_verified = fm.get("last_verified")
    if not last_verified:
        if is_raw:
            findings.append(Finding("HIGH", "6", path, 1, "raw 페이지에 last_verified 누락"))
        return findings
    from datetime import date, datetime
    try:
        if isinstance(last_verified, date):
            verified_date = last_verified
        else:
            verified_date = datetime.fromisoformat(str(last_verified)).date()
        age_days = (date.today() - verified_date).days
        evergreen_exempt = (
            is_authored
            and fm.get("page_type") == "concept"
            and fm.get("evergreen") is True
        )
        if age_days >= HARDFAIL_AGE_DAYS and not evergreen_exempt:
            message = f"last_verified ≥{HARDFAIL_AGE_DAYS}d (실제 {age_days}d)"
            if is_authored:
                message += ". concept evergreen=true이면 HIGH 면제 가능"
            findings.append(Finding("HIGH", "6", path, 1, message))
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
    if not is_raw_source_path(path):
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
                                "LLM write scope 위반: read-only 영역에 llm-synthesis 페이지"))
    return findings


def collect_legacy_findings(paths: list[Path]) -> list[Finding]:
    findings = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            findings.append(
                Finding("HIGH", "io", path, None, f"Markdown read failure: {exc}")
            )
            continue
        fm, _ = parse_frontmatter(text)
        findings.extend(check_axis_5_integrity_broken_links(path, text))
        findings.extend(check_axis_6_recency(path, fm))
        findings.extend(check_raw_required_fields(path, fm))
        findings.extend(check_directive_write_scope(path, fm))
        # 축 5 (orphan) 은 별도 wrapper 필요 — TODO
        # 축 4 (logic-proposition-checker 호출) 은 외부 subagent — TODO
    return findings


def _target_finding(value: dict) -> Finding:
    path = Path(str(value["path"]))
    if not path.is_absolute():
        path = REPO_ROOT / path
    return Finding(
        str(value.get("severity", "HIGH")),
        str(value.get("rule_id", "canonical")),
        path,
        value.get("line") if isinstance(value.get("line"), int) else None,
        str(value.get("message", "canonical wiki validation failed")),
    )


def collect_findings(paths: list[Path]) -> list[Finding]:
    repository_paths: list[Path] = []
    findings: list[Finding] = []
    for path in paths:
        try:
            boundary_path = path.parent.resolve(strict=False) / path.name
            boundary_path.relative_to(REPO_ROOT)
        except (OSError, ValueError) as exc:
            detail = f": {exc}" if isinstance(exc, OSError) else ""
            findings.append(
                Finding(
                    "HIGH",
                    "io",
                    path,
                    None,
                    f"Markdown inventory path is outside repository{detail}",
                )
            )
        else:
            repository_paths.append(path)
    markdown_paths, inventory_findings = _markdown_inventory(repository_paths)
    findings.extend(inventory_findings)
    wiki_paths = [path for path in markdown_paths if is_relative_to(path, WIKI_DIR)]
    wiki_requested = bool(wiki_paths) or any(
        is_relative_to(path, WIKI_DIR) or is_relative_to(WIKI_DIR, path)
        for path in paths
    )
    if not wiki_requested:
        findings.extend(collect_legacy_findings(markdown_paths))
        return findings
    non_wiki_paths = [
        path for path in markdown_paths if not is_relative_to(path, WIKI_DIR)
    ]
    if non_wiki_paths:
        findings.extend(collect_legacy_findings(non_wiki_paths))
    wiki_inventory_failed = False
    for finding in inventory_findings:
        try:
            finding.path.relative_to(WIKI_DIR)
        except ValueError:
            continue
        wiki_inventory_failed = True
        break
    if wiki_inventory_failed:
        return findings
    result = check_target(WIKI_DIR, repo_root=REPO_ROOT, mode="all")
    findings.extend(_target_finding(value) for value in result.findings)
    findings.extend(
        _target_finding(value)
        for value in generated_surface_findings(generated_drift(REPO_ROOT, WIKI_DIR))
    )
    return findings


def _utf8_path(value: str | bytes) -> Path:
    raw = os.fsencode(value) if isinstance(value, str) else value
    return Path(raw.decode("utf-8", errors="strict"))


def git_changed_paths(base: str = "main") -> list[Path]:
    out = subprocess.run(
        ["git", "diff", "--no-renames", "--name-status", "-z", f"{base}..HEAD"],
        check=True,
        capture_output=True,
        cwd=REPO_ROOT,
        text=False,
    ).stdout
    records = out.split(b"\0")
    if not records or records[-1] != b"" or (len(records) - 1) % 2:
        raise UnicodeError("malformed Git changed-path inventory")
    changed: list[Path] = []
    for index in range(0, len(records) - 1, 2):
        status = records[index].decode("ascii", errors="strict")
        value = records[index + 1].decode("utf-8", errors="strict")
        pure = PurePosixPath(value)
        if len(status) != 1 or status not in "ABCDMTUX":
            raise UnicodeError("unsupported Git changed-path status")
        if (
            not pure.parts
            or pure.is_absolute()
            or ".." in pure.parts
            or value != pure.as_posix()
        ):
            raise UnicodeError("non-canonical Git changed path")
        relative = Path(*pure.parts)
        if relative.suffix != ".md":
            continue
        if relative.parts and relative.parts[0] == "wiki":
            candidate = WIKI_DIR
        elif status == "D":
            candidate = REPO_ROOT / relative
            try:
                candidate.lstat()
            except FileNotFoundError:
                continue
        else:
            candidate = REPO_ROOT / relative
        if candidate not in changed:
            changed.append(candidate)
    return changed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paths", nargs="*", default=None, help="특정 path. 기본 = wiki/ + raw/ + _meta/ + AGENTS.md")
    ap.add_argument("--changed", action="store_true", help="git diff base..HEAD 변경 .md 만")
    ap.add_argument("--base", default="main")
    ap.add_argument("--report", choices=["text", "jsonl", "markdown"], default="text")
    args = ap.parse_args()

    initial_findings: list[Finding] = []
    if args.changed:
        try:
            paths = git_changed_paths(args.base)
        except (subprocess.CalledProcessError, OSError, UnicodeError):
            paths = []
            initial_findings.append(
                Finding(
                    "HIGH",
                    "io",
                    REPO_ROOT,
                    None,
                    "Git changed-path inventory failure",
                )
            )
    elif args.paths:
        try:
            paths = [_utf8_path(p).absolute() for p in args.paths]
        except UnicodeError:
            paths = []
            initial_findings.append(
                Finding(
                    "HIGH",
                    "io",
                    REPO_ROOT,
                    None,
                    "Markdown input path encoding failure",
                )
            )
    else:
        paths = [WIKI_DIR, REPO_ROOT / "raw", META_DIR, REPO_ROOT / "AGENTS.md"]

    findings = [*initial_findings, *collect_findings(paths)]
    high = sum(1 for f in findings if f.severity == "HIGH")
    medium = sum(1 for f in findings if f.severity == "MEDIUM")

    if args.report == "jsonl":
        for f in findings:
            print(json.dumps(f.to_dict(), ensure_ascii=False))
    elif args.report == "markdown":
        print(f"# Lint Report\n\n- HIGH: {high}\n- MEDIUM: {medium}\n")
        for f in findings:
            path = json.dumps(f.to_dict()["path"], ensure_ascii=False).replace("`", "\\`")
            message = json.dumps(f.message, ensure_ascii=False).replace("`", "\\`")
            print(f"- [{f.severity}] axis {f.axis} {path}:{f.line or '?'} — {message}")
    else:
        for f in findings:
            path = json.dumps(f.to_dict()["path"], ensure_ascii=False)
            message = json.dumps(f.message, ensure_ascii=False)
            print(f"[{f.severity}] axis {f.axis} {path}:{f.line or '?'} — {message}")
        print(f"\n--- Summary: HIGH={high}, MEDIUM={medium} ---")

    # hard-fail = HIGH ≥1
    return 1 if high >= 1 else 0


if __name__ == "__main__":
    sys.exit(main())
