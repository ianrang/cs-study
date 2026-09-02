#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import knowledge.fs as knowledge_fs  # noqa: E402
from knowledge.fs import (  # noqa: E402
    PathSafetyError,
    read_confined_regular_file,
    read_regular_leaf_at,
    verified_confined_directory,
)
from knowledge.schema import (  # noqa: E402
    KnowledgeSchemaError,
    canonical_document_paths,
    is_canonical_document_path,
    parse_markdown,
    validate_instance,
    validator_for,
)

LOCAL_USER_PATH_RE = re.compile(
    r"/Users/[^/\\<>{}\r\n]+/|[A-Za-z]:\\Users\\[^/\\<>{}\r\n]+\\"
)


def _source_manifest_paths(
    documents: list[tuple[Path, bytes]], *, target_root: Path, repo_root: Path
) -> set[Path]:
    schema_path = repo_root / "_meta" / "knowledge.schema.json"
    return {
        repo_root / source
        for path, content in documents
        if is_canonical_document_path(target_root, path)
        for source in parse_markdown(
            path, content.decode("utf-8"), schema_path=schema_path
        )["properties"]["source_paths"]
    }


def _regular_markdown_inventory(
    root: Path, *, trusted_root: Path | None = None
) -> list[tuple[Path, bytes]]:
    canonical_document_paths(root)
    anchor = root if trusted_root is None else trusted_root
    return [
        (path, read_confined_regular_file(anchor, path))
        for path in sorted(root.rglob("*.md"))
    ]


def _payload_contains_local_user_path(payload: bytes, media_type: str) -> bool:
    if not media_type.startswith("text/") and media_type != "application/json":
        return False
    text = payload.decode("utf-8")
    if media_type.startswith("text/"):
        return LOCAL_USER_PATH_RE.search(text) is not None
    pending = [json.loads(text)]
    while pending:
        value = pending.pop()
        if isinstance(value, str) and LOCAL_USER_PATH_RE.search(value):
            return True
        if isinstance(value, dict):
            pending.extend(value.keys())
            pending.extend(value.values())
        elif isinstance(value, list):
            pending.extend(value)
    return False


def test_markdown_inventory_rejects_non_regular_entries_before_read():
    for entry_type in ("leaf-symlink", "ancestor-symlink", "fifo"):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "root"
            root.mkdir()
            external = Path(directory) / "external"
            external.mkdir()
            (external / "content.md").write_text("SECRET-EXTERNAL", encoding="utf-8")
            if entry_type == "leaf-symlink":
                (root / "content.md").symlink_to(external / "content.md")
            elif entry_type == "ancestor-symlink":
                (root / "linked").symlink_to(external, target_is_directory=True)
            else:
                os.mkfifo(root / "content.md")

            real_read = knowledge_fs.os.read
            reads = 0

            def observe_read(descriptor: int, size: int) -> bytes:
                nonlocal reads
                reads += 1
                return real_read(descriptor, size)

            knowledge_fs.os.read = observe_read
            try:
                with pytest.raises(KnowledgeSchemaError):
                    _regular_markdown_inventory(root)
            finally:
                knowledge_fs.os.read = real_read
            assert reads == 0


def test_project_markdown_does_not_use_wiki_frontmatter():
    documents = _regular_markdown_inventory(ROOT / "projects")
    assert documents
    offenders = [
        str(path.relative_to(ROOT))
        for path, content in documents
        if content.startswith(b"---\n")
    ]
    assert offenders == []


def test_wiki_does_not_depend_on_project_paths():
    offenders = [
        str(path.relative_to(ROOT))
        for path, content in _regular_markdown_inventory(ROOT / "wiki")
        if b"projects/" in content
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
    wiki_documents = _regular_markdown_inventory(ROOT / "wiki")
    manifest_paths = _source_manifest_paths(
        wiki_documents, target_root=ROOT / "wiki", repo_root=ROOT
    )
    manifests = []
    for manifest in sorted(manifest_paths):
        with verified_confined_directory(ROOT / "raw", manifest.parent) as directory:
            manifest_bytes = read_regular_leaf_at(directory, "manifest.json")
            if manifest_bytes is None:
                raise PathSafetyError(
                    f"leaf must be regular non-symlink: {manifest}"
                )
            data = json.loads(manifest_bytes.decode("utf-8"))
            validate_instance(data, validator_for("ArtifactManifest"))
            payload = manifest.parent / data["payload"]
            payload_bytes = read_regular_leaf_at(directory, data["payload"])
            if payload_bytes is None:
                raise PathSafetyError(
                    f"leaf must be regular non-symlink: {payload}"
                )
            manifests.append((payload, payload_bytes, data["media_type"]))
    web_sources = _regular_markdown_inventory(
        ROOT / "raw" / "sources" / "web", trusted_root=ROOT / "raw"
    )
    offenders = [
        str(path.relative_to(ROOT))
        for path, content in wiki_documents + web_sources
        if LOCAL_USER_PATH_RE.search(content.decode("utf-8"))
    ]
    offenders.extend(
        str(path.relative_to(ROOT))
        for path, payload_bytes, media_type in manifests
        if _payload_contains_local_user_path(payload_bytes, media_type)
    )
    assert offenders == []


def test_source_manifest_inventory_accepts_schema_valid_space_in_source_id():
    source_path = (
        ROOT
        / "wiki"
        / "domains"
        / "information-security"
        / "queries"
        / "network-path-functions-and-placement.md"
    )
    source = read_confined_regular_file(ROOT / "wiki", source_path).decode("utf-8")
    source = re.sub(
        r"raw/sources/([^/]+)/[^/]+/",
        r"raw/sources/\1/source id/",
        source,
        count=1,
    )
    with tempfile.TemporaryDirectory() as directory:
        target_root = Path(directory)
        page = target_root / "domains" / "ai-engineering" / "concept.md"
        page.parent.mkdir(parents=True)
        page.write_text(source, encoding="utf-8")

        manifests = _source_manifest_paths(
            [(page, source.encode("utf-8"))], target_root=target_root, repo_root=ROOT
        )

        assert any("/source id/" in path.as_posix() for path in manifests)


def test_json_payload_local_user_path_is_checked_after_decoding():
    payload = json.dumps({"nested": {"path": r"C:\Users\ian\repo"}}).encode()

    assert _payload_contains_local_user_path(payload, "application/json")


def test_json_payload_decode_failures_are_fail_closed():
    cases = (
        (b"\xff", UnicodeDecodeError),
        (b'{"path":', json.JSONDecodeError),
    )
    for payload, expected in cases:
        try:
            _payload_contains_local_user_path(payload, "application/json")
        except expected:
            continue
        raise AssertionError(f"expected {expected.__name__}")


def test_terminal_migration_surfaces_are_git_ignored_and_untracked():
    relative = [
        ".knowledge-migration-fixture.json",
        ".wiki.migration.fixture/marker",
        ".wiki.restore.fixture/marker",
    ]
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
    forbidden_prefixes = (
        ".knowledge-migration-",
        ".wiki.migration.",
        ".wiki.restore.",
    )
    assert not any(item.startswith(forbidden_prefixes) for item in tracked)
    assert not any(item.startswith(forbidden_prefixes) for item in staged)


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
import pytest
