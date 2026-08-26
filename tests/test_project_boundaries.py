#!/usr/bin/env python3
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCAL_USER_PATH_RE = re.compile(
    r"/Users/[^/\\<>{}\r\n]+/|[A-Za-z]:\\Users\\[^/\\<>{}\r\n]+\\"
)
MANIFEST_PATH_RE = re.compile(
    r"raw/sources/[^/\s]+/[^/\s]+/[a-f0-9]{64}/manifest\.json"
)


def test_project_markdown_does_not_use_wiki_frontmatter():
    documents = sorted((ROOT / "projects").rglob("*.md"))
    assert documents
    offenders = [
        str(path.relative_to(ROOT))
        for path in documents
        if path.read_text(encoding="utf-8").startswith("---\n")
    ]
    assert offenders == []


def test_wiki_does_not_depend_on_project_paths():
    offenders = [
        str(path.relative_to(ROOT))
        for path in sorted((ROOT / "wiki").rglob("*.md"))
        if "projects/" in path.read_text(encoding="utf-8")
    ]
    assert offenders == []


def test_executable_projects_are_outside_wiki():
    forbidden = (
        ROOT / "wiki" / "domains" / "information-security" / "practice",
        ROOT
        / "wiki"
        / "domains"
        / "information-security"
        / "labs"
        / "info-sec-engineer-practical",
    )
    assert all(not path.exists() for path in forbidden)


def test_persistent_markdown_does_not_expose_local_user_paths():
    wiki_documents = sorted((ROOT / "wiki").rglob("*.md"))
    manifest_paths = {
        ROOT / match
        for path in wiki_documents
        for match in MANIFEST_PATH_RE.findall(path.read_text(encoding="utf-8"))
    }
    active_payloads = [
        manifest.parent / "payload.md" for manifest in sorted(manifest_paths)
    ]
    web_sources = sorted((ROOT / "raw" / "sources" / "web").rglob("*.md"))
    documents = wiki_documents + active_payloads + web_sources
    assert all(path.is_file() for path in active_payloads)
    offenders = [
        str(path.relative_to(ROOT))
        for path in documents
        if LOCAL_USER_PATH_RE.search(path.read_text(encoding="utf-8"))
    ]
    assert offenders == []


def test_terminal_migration_evidence_is_preserved_and_git_ignored():
    journals = sorted(ROOT.glob(".knowledge-migration-*.json"))
    candidates = sorted(ROOT.glob(".wiki.migration.*")) + sorted(
        ROOT.glob(".wiki.restore.*")
    )
    runtime_roots = journals + candidates
    assert len(journals) == 3
    assert len(candidates) == 3
    assert all(path.exists() for path in runtime_roots)

    relative = [path.relative_to(ROOT).as_posix() for path in runtime_roots]
    ignored = subprocess.run(
        ["git", "check-ignore", "--no-index", "--stdin"],
        cwd=ROOT,
        input="\n".join(relative) + "\n",
        capture_output=True,
        text=True,
        check=False,
    )
    assert ignored.returncode == 0
    assert ignored.stdout.splitlines() == relative

    tracked = set(
        subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()
    )
    staged = set(
        subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()
    )
    assert all(
        not any(item == path or item.startswith(f"{path}/") for item in tracked)
        for path in relative
    )
    assert all(
        not any(item == path or item.startswith(f"{path}/") for item in staged)
        for path in relative
    )


def main() -> int:
    tests = [
        value
        for name, value in sorted(globals().items())
        if name.startswith("test_")
    ]
    failed = 0
    for test in tests:
        try:
            test()
            print(f"PASS {test.__name__}")
        except AssertionError as exc:
            failed += 1
            print(f"FAIL {test.__name__}: {exc}")
    print(f"\n--- {len(tests) - failed} passed, {failed} failed / {len(tests)} ---")
    return int(bool(failed))


if __name__ == "__main__":
    raise SystemExit(main())
