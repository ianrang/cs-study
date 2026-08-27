import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from knowledge import migration  # noqa: E402
from knowledge.artifacts import capture, verify_manifest  # noqa: E402
from knowledge.check import check_target  # noqa: E402
from knowledge.fs import repository_write_lock  # noqa: E402
from knowledge.migration import (  # noqa: E402
    apply_resolved_plan,
    build_migration_plan,
    build_preservation_plan,
    build_reference_cascade_plan,
    build_tree_manifest,
    create_backup,
    load_preservation_resolution,
    load_resolved_plan,
    plan_bytes,
    preservation_capture_requests,
    preview_resolved_plan,
    recover_transaction,
    restore_backup,
    verify_backup,
)
from wiki_ingest import (  # noqa: E402
    _check_migration_candidate,
    _parser,
    _publish_cascade_bundle,
)


@pytest.mark.parametrize(
    ("operation", "arguments"),
    [
        (apply_resolved_plan, (Path("plan"), Path("backup"))),
        (restore_backup, (Path("plan"), Path("backup"))),
        (recover_transaction, (Path("journal"), Path("plan"), "0" * 64)),
    ],
)
def test_migration_writers_share_repository_lock(
    tmp_path: Path, operation, arguments: tuple
):
    (tmp_path / "wiki").mkdir()
    with repository_write_lock(tmp_path):
        with pytest.raises(BlockingIOError):
            if operation is recover_transaction:
                operation(*arguments, tmp_path, tmp_path / "wiki")
            else:
                operation(
                    *arguments,
                    tmp_path,
                    tmp_path / "wiki",
                    "0" * 64,
                    Path("journal"),
                    *(() if operation is restore_backup else (lambda *_: None,)),
                )


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _require_current_legacy_base() -> None:
    resolution = json.loads(
        (ROOT / "_meta" / "knowledge-migration-resolution.json").read_text(
            encoding="utf-8"
        )
    )
    current = build_tree_manifest(ROOT / "wiki")["tree_sha256"]
    if current == resolution["base_tree_sha256"]:
        return
    result = check_target(ROOT / "wiki", repo_root=ROOT, mode="all")
    assert result.structural_verdict == "PASS", (
        "live wiki is neither the exact migration base nor a valid canonical tree"
    )
    pytest.skip("legacy-base migration preflight is inactive after canonical cutover")


def _git_fixture() -> tuple[tempfile.TemporaryDirectory, Path, Path]:
    temporary = tempfile.TemporaryDirectory()
    repo = Path(temporary.name)
    wiki = repo / "wiki"
    (wiki / "pages").mkdir(parents=True)
    (wiki / ".empty").mkdir()
    (wiki / "index.md").write_text("# Generated Index\n", encoding="utf-8")
    (wiki / "pages" / "page.md").write_text("# Source Page\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(
        ["git", "config", "user.email", "fixture@example.invalid"],
        cwd=repo,
        check=True,
    )
    subprocess.run(["git", "config", "user.name", "Fixture"], cwd=repo, check=True)
    subprocess.run(["git", "add", "wiki"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "fixture"], cwd=repo, check=True)
    return temporary, repo, wiki


def _resolved_fixture(
    repo: Path,
    wiki: Path,
    *,
    target_path: str = "pages/page.md",
    target_bytes: bytes = b"# Target Page\n",
) -> tuple[Path, dict]:
    inventory = build_migration_plan(repo, wiki)
    source_path = inventory["canonical_universe"][0]
    source = wiki / source_path
    source_bytes = source.read_bytes()
    source_mode = source.stat().st_mode & 0o7777
    if target_path == source_path:
        source.write_bytes(target_bytes)
    else:
        source.unlink()
        target = wiki / target_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(target_bytes)
        os.chmod(target, source_mode)
    target_hash = build_tree_manifest(wiki)["tree_sha256"]
    target = wiki / target_path
    target.unlink()
    if target.parent != source.parent:
        target.parent.rmdir()
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_bytes(source_bytes)
    os.chmod(source, source_mode)
    plan = {
        "schema_version": "1.0",
        "mode": "resolved",
        "resolution_mode": "generic",
        "knowledge_root": "wiki",
        "repository_head": inventory["repository_head"],
        "inventory_plan_sha256": _sha256(plan_bytes(inventory)),
        "base_tree_sha256": inventory["wiki_tree_sha256"],
        "expected_target_tree_sha256": target_hash,
        "source_canonical_universe": inventory["canonical_universe"],
        "target_canonical_universe": [target_path],
        "unresolved_decisions": [],
        "operations": [
            {
                "source_path": source_path,
                "target_path": target_path,
                "source_sha256": _sha256(source_bytes),
                "target_sha256": _sha256(target_bytes),
                "target_mode": source_mode,
                "content_base64": base64.b64encode(target_bytes).decode("ascii"),
            }
        ],
    }
    plan_path = repo / "resolved-plan.json"
    plan_path.write_bytes(plan_bytes(plan))
    return plan_path, plan


def _cascade_fixture(repo: Path, plan_path: Path, plan: dict) -> tuple[Path, dict]:
    path = repo / "docs" / "wiki-ingest-architecture.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    base = f"wiki/{plan['operations'][0]['source_path']}\n".encode()
    target = f"wiki/{plan['operations'][0]['target_path']}\n".encode()
    path.write_bytes(base)
    mode = path.stat().st_mode & 0o7777
    operations = [
        {
            "path": path.relative_to(repo).as_posix(),
            "owner": "migration-architecture",
            "occurrences": 1,
            "action": "replace-paths",
            "base_sha256": _sha256(base),
            "target_sha256": _sha256(target),
            "base_mode": mode,
            "target_mode": mode,
            "base_content_base64": base64.b64encode(base).decode("ascii"),
            "target_content_base64": base64.b64encode(target).decode("ascii"),
        }
    ]
    cascade = {
        "schema_version": "1.0",
        "migration_plan_sha256": _sha256(plan_path.read_bytes()),
        "target_tree_sha256": plan["expected_target_tree_sha256"],
        "observed_reference_groups": 1,
        "observed_reference_occurrences": 1,
        "active_reference_groups": 1,
        "active_reference_occurrences": 1,
        "historical_exemptions": [],
        "source_ref_total": 0,
        "source_ref_path_changes": 0,
        "staged_stale_reference_occurrences": 0,
        "scan_policy": {
            "included": [],
            "excluded": [],
            "hidden_paths": "included unless explicitly excluded",
        },
        "operations": operations,
        "apply_requires_combined_transaction": True,
    }
    cascade["diff_sha256"] = _sha256(migration._cascade_diff(operations))
    path = repo / "cascade-plan.json"
    path.write_bytes(plan_bytes(cascade))
    return path, cascade


def test_recover_cli_keeps_journal_v1_reachable_without_cascade_arguments():
    args = _parser().parse_args(
        [
            "migrate-recover",
            "--journal",
            "journal.json",
            "--plan",
            "resolved.json",
            "--knowledge-root",
            "wiki",
            "--confirm-plan-sha256",
            "a" * 64,
        ]
    )
    assert args.cascade_plan is None
    assert args.confirm_cascade_plan_sha256 is None


def test_current_inventory_separates_canonical_and_reserved_conflicts():
    _require_current_legacy_base()
    plan = build_migration_plan(ROOT, ROOT / "wiki")
    assert plan["inventory"] == {
        "markdown": 84,
        "content": 75,
        "excluded": 9,
        "collision_groups": 0,
        "collision_files": 0,
        "reserved_conflict_groups": 1,
        "reserved_conflict_files": 1,
        "decision_pages": 75,
        "preserved_ids": 67,
    }
    assert plan["collisions"] == {}
    assert plan["reserved_conflicts"] == {
        "index": [
            (
                "wiki/domains/information-security/datasets/"
                "info-sec-engineer-practical-past-exams/index.md"
            )
        ]
    }


def test_plan_is_deterministic_and_does_not_write_wiki():
    _require_current_legacy_base()
    before = build_tree_manifest(ROOT / "wiki")
    first = plan_bytes(build_migration_plan(ROOT, ROOT / "wiki"))
    second = plan_bytes(build_migration_plan(ROOT, ROOT / "wiki"))
    assert first == second
    assert build_tree_manifest(ROOT / "wiki") == before


def test_cascade_approval_bundle_is_atomic_and_idempotent(tmp_path):
    destination = tmp_path / "cascade"
    assert _publish_cascade_bundle(destination, b"plan\n", b"diff\n") is True
    assert _publish_cascade_bundle(destination, b"plan\n", b"diff\n") is False
    before = {path.name: path.read_bytes() for path in destination.iterdir()}
    try:
        _publish_cascade_bundle(destination, b"different\n", b"diff\n")
    except FileExistsError as exc:
        assert "existing cascade bundle differs" in str(exc)
    else:
        raise AssertionError("divergent cascade bundle was accepted")
    assert {path.name: path.read_bytes() for path in destination.iterdir()} == before
    symlink_bundle = tmp_path / "symlink-bundle"
    symlink_bundle.mkdir()
    external_plan = tmp_path / "external-plan"
    external_diff = tmp_path / "external-diff"
    external_plan.write_bytes(b"plan\n")
    external_diff.write_bytes(b"diff\n")
    (symlink_bundle / "cascade-plan.json").symlink_to(external_plan)
    (symlink_bundle / "full.diff").symlink_to(external_diff)
    try:
        _publish_cascade_bundle(symlink_bundle, b"plan\n", b"diff\n")
    except FileExistsError as exc:
        assert "existing cascade bundle differs" in str(exc)
    else:
        raise AssertionError("cascade bundle accepted symlink entries")


def test_relative_knowledge_root_is_resolved_against_repository_root():
    _require_current_legacy_base()
    assert build_migration_plan(ROOT, Path("wiki")) == build_migration_plan(
        ROOT, ROOT / "wiki"
    )


def test_current_preservation_resolution_covers_exact_approved_universe():
    _require_current_legacy_base()
    inventory = build_migration_plan(ROOT, ROOT / "wiki")
    resolution = load_preservation_resolution(
        ROOT / "_meta" / "knowledge-migration-resolution.json",
        inventory,
        ROOT,
        ROOT / "wiki",
    )
    assert len(resolution["pages"]) == 75
    assert (
        sum(page["source_path"] != page["target_path"] for page in resolution["pages"])
        == 8
    )
    collection = [
        page for page in resolution["pages"] if page["page_type"] == "collection"
    ]
    assert len(collection) == 1
    assert collection[0]["target_path"] == (
        "collections/info-sec-engineer-practical-past-exams.md"
    )
    assert len(collection[0]["members"]) == len(set(collection[0]["members"])) == 52
    source_index = ROOT / "wiki" / collection[0]["source_path"]
    linked_members = [
        Path(link).stem
        for link in re.findall(
            r"\[[^]]+\]\(([^)]+\.md)\)",
            source_index.read_text(encoding="utf-8"),
        )
    ]
    assert collection[0]["members"] == linked_members


def test_preservation_resolution_rejects_invalid_capture_timestamp(tmp_path):
    _require_current_legacy_base()
    inventory = build_migration_plan(ROOT, ROOT / "wiki")
    resolution = json.loads(
        (ROOT / "_meta" / "knowledge-migration-resolution.json").read_text(
            encoding="utf-8"
        )
    )
    resolution["capture_created_at"] = "not-a-date"
    candidate = tmp_path / "resolution.json"
    candidate.write_text(json.dumps(resolution), encoding="utf-8")
    try:
        load_preservation_resolution(candidate, inventory, ROOT, ROOT / "wiki")
    except ValueError as exc:
        assert "date-time" in str(exc)
    else:
        raise AssertionError("invalid capture_created_at was accepted")


def test_preservation_collection_rejects_member_count_and_order_drift():
    _require_current_legacy_base()
    inventory = build_migration_plan(ROOT, ROOT / "wiki")
    original = json.loads(
        (ROOT / "_meta" / "knowledge-migration-resolution.json").read_text(
            encoding="utf-8"
        )
    )
    collection_index = next(
        index
        for index, page in enumerate(original["pages"])
        if page["page_type"] == "collection"
    )
    all_target_ids = [Path(page["target_path"]).stem for page in original["pages"]]
    with tempfile.TemporaryDirectory() as directory:
        for label, members in (
            ("short", original["pages"][collection_index]["members"][:-1]),
            (
                "long",
                original["pages"][collection_index]["members"]
                + [
                    next(
                        target
                        for target in all_target_ids
                        if target not in original["pages"][collection_index]["members"]
                    )
                ],
            ),
            (
                "reordered",
                list(reversed(original["pages"][collection_index]["members"])),
            ),
        ):
            changed = json.loads(json.dumps(original))
            changed["pages"][collection_index]["members"] = members
            candidate = Path(directory) / f"{label}.json"
            candidate.write_text(json.dumps(changed), encoding="utf-8")
            try:
                load_preservation_resolution(candidate, inventory, ROOT, ROOT / "wiki")
            except ValueError:
                pass
            else:
                raise AssertionError(f"collection {label} drift was accepted")


def test_current_preservation_capture_replay_is_byte_idempotent():
    _require_current_legacy_base()
    inventory = build_migration_plan(ROOT, ROOT / "wiki")
    resolution = load_preservation_resolution(
        ROOT / "_meta" / "knowledge-migration-resolution.json",
        inventory,
        ROOT,
        ROOT / "wiki",
    )
    clipping = ROOT / "raw" / "sources" / "clipping"
    before = build_tree_manifest(clipping)
    manifests = [
        capture(**request).manifest_path
        for request in preservation_capture_requests(resolution, ROOT, ROOT / "wiki")
    ]
    after = build_tree_manifest(clipping)
    assert len(manifests) == 75
    assert before == after


def test_current_preservation_plan_is_deterministic_and_no_write():
    _require_current_legacy_base()
    inventory = build_migration_plan(ROOT, ROOT / "wiki")
    resolution = load_preservation_resolution(
        ROOT / "_meta" / "knowledge-migration-resolution.json",
        inventory,
        ROOT,
        ROOT / "wiki",
    )
    wiki_before = build_tree_manifest(ROOT / "wiki")
    raw_before = build_tree_manifest(ROOT / "raw" / "sources" / "clipping")
    first = plan_bytes(
        build_preservation_plan(
            resolution, inventory, ROOT, ROOT / "wiki", verify_manifest
        )
    )
    second = plan_bytes(
        build_preservation_plan(
            resolution, inventory, ROOT, ROOT / "wiki", verify_manifest
        )
    )
    assert first == second
    plan = json.loads(first)
    assert len(plan["operations"]) == 75
    assert plan["unresolved_decisions"] == []
    assert build_tree_manifest(ROOT / "wiki") == wiki_before
    assert build_tree_manifest(ROOT / "raw" / "sources" / "clipping") == raw_before


def test_current_preservation_preview_audits_lineage_and_apply_blockers():
    _require_current_legacy_base()
    with tempfile.TemporaryDirectory() as directory:
        output = Path(directory)
        inventory = build_migration_plan(ROOT, ROOT / "wiki")
        resolution = load_preservation_resolution(
            ROOT / "_meta" / "knowledge-migration-resolution.json",
            inventory,
            ROOT,
            ROOT / "wiki",
        )
        plan_path = output / "resolved.json"
        plan_path.write_bytes(
            plan_bytes(
                build_preservation_plan(
                    resolution,
                    inventory,
                    ROOT,
                    ROOT / "wiki",
                    verify_manifest,
                )
            )
        )
        result = preview_resolved_plan(
            plan_path,
            output / "preview",
            ROOT,
            ROOT / "wiki",
            lambda candidate, candidate_repo, canonical_paths: None,
            manifest_verifier=verify_manifest,
        )
        audit = result["preservation_audit"]
        assert audit["page_count"] == audit["payload_exact_count"] == 75
        assert audit["claim_rows"] == audit["relation_rows"] == 0
        assert audit["member_rows"] == 52
        question_pack_occurrences = sum(
            int(finding["occurrences"])
            for finding in result["external_reference_findings"]
            if "/data/question-packs/" in str(finding["path"])
        )
        assert question_pack_occurrences == 329
        prefix = "domains/information-security/"
        target_by_source = {
            page["source_path"][len(prefix) :]: (
                page["target_path"][len(prefix) :]
                if page["target_path"].startswith(prefix)
                else "../../" + page["target_path"]
            )
            for page in resolution["pages"]
            if page["source_path"].startswith(prefix)
        }
        preview_domain = output / "preview" / "domains" / "information-security"
        statuses = {"source-derived": 0, "inferred": 0}
        source_ref_count = 0
        for pack in sorted(
            (
                ROOT
                / "projects"
                / "info-sec-engineer-practice"
                / "data"
                / "question-packs"
            ).glob("*.json")
        ):
            questions = json.loads(pack.read_text(encoding="utf-8"))["questions"]
            for question in questions:
                for reference in question["sourceRefs"]:
                    source_ref_count += 1
                    statuses[reference["status"]] += 1
                    target = (
                        preview_domain / target_by_source[reference["path"]]
                    ).resolve()
                    target_line = target.read_text(encoding="utf-8").splitlines()[
                        reference["line"] - 1
                    ]
                    assert reference["excerpt"] in target_line
        assert source_ref_count == 410
        assert statuses == {"source-derived": 397, "inferred": 13}
    assert result["apply_ready"] is False


def test_preservation_payload_cannot_downgrade_mode_before_preview_audit():
    _require_current_legacy_base()
    with tempfile.TemporaryDirectory() as directory:
        output = Path(directory)
        inventory = build_migration_plan(ROOT, ROOT / "wiki")
        resolution = load_preservation_resolution(
            ROOT / "_meta" / "knowledge-migration-resolution.json",
            inventory,
            ROOT,
            ROOT / "wiki",
        )
        plan = build_preservation_plan(
            resolution, inventory, ROOT, ROOT / "wiki", verify_manifest
        )
        plan["resolution_mode"] = "generic"
        plan_path = output / "downgraded.json"
        plan_path.write_bytes(plan_bytes(plan))

        try:
            preview_resolved_plan(
                plan_path,
                output / "preview",
                ROOT,
                ROOT / "wiki",
                lambda candidate, candidate_repo, canonical_paths: None,
                manifest_verifier=verify_manifest,
            )
        except ValueError as exc:
            assert "preservation manifests cannot declare generic mode" in str(exc)
        else:
            raise AssertionError("preservation mode downgrade bypassed lineage audit")


def test_preservation_payload_cannot_downgrade_mode_before_apply_audit():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, plan = _resolved_fixture(repo, wiki)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        operation = plan["operations"][0]
        expected_source_id = migration._source_id(operation["source_path"])
        rendered = (
            "---\n"
            "source_paths:\n"
            f"  - raw/sources/clipping/{expected_source_id}/"
            + operation["source_sha256"]
            + "/manifest.json\n"
            "---\n"
        ).encode()
        operation["content_base64"] = base64.b64encode(rendered).decode("ascii")
        operation["target_sha256"] = _sha256(rendered)
        plan_path.write_bytes(plan_bytes(plan))
        before = build_tree_manifest(wiki)
        try:
            apply_resolved_plan(
                plan_path,
                backup,
                repo,
                wiki,
                _sha256(plan_path.read_bytes()),
                repo / "journal.json",
                lambda candidate, candidate_repo, canonical_paths: None,
                manifest_verifier=verify_manifest,
            )
        except ValueError as exc:
            assert "preservation manifests cannot declare generic mode" in str(exc)
        else:
            raise AssertionError("preservation mode downgrade bypassed apply audit")
        assert build_tree_manifest(wiki) == before
        assert not (repo / "journal.json").exists()
    finally:
        temporary.cleanup()


def test_preservation_binding_classifier_requires_exact_clipping_identity():
    operation = {
        "source_path": "domains/example/source.md",
        "source_sha256": "a" * 64,
        "target_path": "domains/example/target.md",
    }
    expected_source_id = migration._source_id(operation["source_path"])

    def declares(source_path: str) -> bool:
        rendered = f"---\nsource_paths:\n  - {source_path}\n---\n".encode()
        candidate = {
            **operation,
            "content_base64": base64.b64encode(rendered).decode("ascii"),
        }
        return migration._operation_declares_preservation_manifest(candidate)

    assert declares(
        f"raw/sources/clipping/{expected_source_id}/{'a' * 64}/manifest.json"
    )
    assert not declares(
        f"raw/sources/clipping/unrelated/{'a' * 64}/manifest.json"
    )
    assert not declares(
        f"raw/sources/video/{expected_source_id}/{'a' * 64}/manifest.json"
    )


def test_resolved_preservation_plan_validates_privacy_normalized_source_digest():
    temporary, repo, wiki = _git_fixture()
    try:
        source = wiki / "pages" / "page.md"
        source.write_bytes(b"local source: /Users/alice/evidence.pdf\n")
        plan_path, plan = _resolved_fixture(repo, wiki)
        operation = plan["operations"][0]
        normalized = b"local source: <local-user-home>/evidence.pdf\n"
        operation["source_sha256"] = _sha256(normalized)
        source_id = migration._source_id(operation["source_path"])
        rendered = (
            "---\n"
            "source_paths:\n"
            f"  - raw/sources/clipping/{source_id}/"
            f"{operation['source_sha256']}/manifest.json\n"
            "---\n"
        ).encode()
        operation["content_base64"] = base64.b64encode(rendered).decode("ascii")
        operation["target_sha256"] = _sha256(rendered)
        plan["resolution_mode"] = "preservation"
        plan_path.write_bytes(plan_bytes(plan))

        loaded, _, _ = load_resolved_plan(plan_path, repo, wiki)
        assert loaded["operations"][0]["source_sha256"] == _sha256(normalized)
    finally:
        temporary.cleanup()


def test_non_wiki_knowledge_root_is_rejected():
    try:
        build_migration_plan(ROOT, ROOT / "projects")
    except ValueError as exc:
        assert "repository wiki directory" in str(exc)
    else:
        raise AssertionError("non-wiki root was accepted")


def test_tree_manifest_covers_hidden_empty_directory_mode_and_bytes():
    temporary, _, wiki = _git_fixture()
    try:
        before = build_tree_manifest(wiki)
        assert any(
            entry["path"] == ".empty" and entry["kind"] == "directory"
            for entry in before["entries"]
        )
        page = wiki / "pages" / "page.md"
        os.chmod(page, 0o600)
        after_mode = build_tree_manifest(wiki)
        assert after_mode["tree_sha256"] != before["tree_sha256"]
        page.write_text("# Changed\n", encoding="utf-8")
        after_bytes = build_tree_manifest(wiki)
        assert after_bytes["tree_sha256"] != after_mode["tree_sha256"]
        os.chmod(wiki, 0o751)
        after_root_mode = build_tree_manifest(wiki)
        assert after_root_mode["root"] == {"kind": "directory", "mode": 0o751}
        assert after_root_mode["tree_sha256"] != after_bytes["tree_sha256"]
    finally:
        temporary.cleanup()


def test_tree_manifest_rejects_symlinks():
    temporary, _, wiki = _git_fixture()
    try:
        (wiki / "link").symlink_to(wiki / "pages" / "page.md")
        try:
            build_tree_manifest(wiki)
        except ValueError as exc:
            assert "symbolic links" in str(exc)
        else:
            raise AssertionError("symlink was accepted")
    finally:
        temporary.cleanup()


def test_resolved_plan_requires_exact_universe_and_zero_unresolved_decisions():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, plan = _resolved_fixture(repo, wiki)
        loaded, _, _ = load_resolved_plan(plan_path, repo, wiki)
        assert loaded == plan
        plan["unresolved_decisions"] = ["semantic-review"]
        plan_path.write_bytes(plan_bytes(plan))
        try:
            load_resolved_plan(plan_path, repo, wiki)
        except ValueError as exc:
            assert "invalid resolved migration plan" in str(exc)
        else:
            raise AssertionError("unresolved plan was accepted")
    finally:
        temporary.cleanup()


def test_resolved_plan_rejects_stale_head_inventory_digest_and_target_id():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, plan = _resolved_fixture(repo, wiki)
        cases = (
            ("repository_head", "0" * 40, "repository HEAD is stale"),
            ("inventory_plan_sha256", "0" * 64, "inventory digest mismatch"),
            (
                "target_path",
                "pages/Not-Kebab.md",
                "target ID must be kebab-case",
            ),
        )
        for field, value, expected in cases:
            changed = json.loads(json.dumps(plan))
            if field == "target_path":
                changed["operations"][0][field] = value
                changed["target_canonical_universe"] = [value]
            else:
                changed[field] = value
            plan_path.write_bytes(plan_bytes(changed))
            try:
                load_resolved_plan(plan_path, repo, wiki)
            except ValueError as exc:
                assert expected in str(exc)
            else:
                raise AssertionError(f"invalid {field} was accepted")
    finally:
        temporary.cleanup()


def test_resolved_plan_rejects_privileged_or_executable_source_mode():
    temporary, repo, wiki = _git_fixture()
    try:
        os.chmod(wiki / "pages" / "page.md", 0o755)
        plan_path, plan = _resolved_fixture(repo, wiki)
        try:
            load_resolved_plan(plan_path, repo, wiki)
        except ValueError as exc:
            assert "privileged or executable" in str(exc)
        else:
            raise AssertionError("executable canonical Markdown was accepted")
    finally:
        temporary.cleanup()


def test_stale_tree_rejects_before_backup_write():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, _ = _resolved_fixture(repo, wiki)
        (wiki / ".hidden-state").write_text("changed\n", encoding="utf-8")
        backup = repo / "backup.tar"
        try:
            create_backup(plan_path, backup, repo, wiki)
        except ValueError as exc:
            assert "stale" in str(exc)
        else:
            raise AssertionError("stale tree backup was accepted")
        assert not backup.exists()
    finally:
        temporary.cleanup()


def test_backup_verify_apply_and_restore_preserve_exact_trees():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, plan = _resolved_fixture(repo, wiki)
        backup = repo / "backup.tar"
        base_manifest = build_tree_manifest(wiki)
        create_backup(plan_path, backup, repo, wiki)
        descriptor = verify_backup(plan_path, backup, repo, wiki)
        assert descriptor["tree_manifest"] == base_manifest
        journal = repo / "journal.json"
        apply_resolved_plan(
            plan_path,
            backup,
            repo,
            wiki,
            _sha256(plan_path.read_bytes()),
            journal,
            lambda candidate, candidate_repo, canonical_paths: None,
        )
        assert (
            build_tree_manifest(wiki)["tree_sha256"]
            == plan["expected_target_tree_sha256"]
        )
        assert json.loads(journal.read_text(encoding="utf-8"))["state"] == "COMMITTED"
        restore_backup(
            plan_path,
            backup,
            repo,
            wiki,
            plan["expected_target_tree_sha256"],
            repo / "restore-journal.json",
        )
        assert build_tree_manifest(wiki) == base_manifest
    finally:
        temporary.cleanup()


def test_apply_and_restore_preserve_root_and_restrictive_directory_modes():
    temporary, repo, wiki = _git_fixture()
    try:
        os.chmod(wiki, 0o751)
        os.chmod(wiki / ".empty", 0o000)
        plan_path, plan = _resolved_fixture(repo, wiki)
        backup = repo / "backup.tar"
        base_manifest = build_tree_manifest(wiki)
        create_backup(plan_path, backup, repo, wiki)
        apply_resolved_plan(
            plan_path,
            backup,
            repo,
            wiki,
            _sha256(plan_path.read_bytes()),
            repo / "apply-journal.json",
            lambda candidate, candidate_repo, canonical_paths: None,
        )
        assert (wiki.stat().st_mode & 0o7777) == 0o751
        restore_backup(
            plan_path,
            backup,
            repo,
            wiki,
            plan["expected_target_tree_sha256"],
            repo / "restore-journal.json",
        )
        assert build_tree_manifest(wiki) == base_manifest
        assert ((wiki / ".empty").stat().st_mode & 0o7777) == 0o000
    finally:
        temporary.cleanup()


def test_corrupt_backup_is_rejected():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, _ = _resolved_fixture(repo, wiki)
        backup = repo / "backup.tar"
        corrupt = repo / "corrupt.tar"
        create_backup(plan_path, backup, repo, wiki)
        with tarfile.open(backup, "r") as source, tarfile.open(corrupt, "w") as target:
            for member in source.getmembers():
                handle = source.extractfile(member) if member.isfile() else None
                data = handle.read() if handle is not None else None
                if member.name == "tree/pages/page.md":
                    data = b"corrupt\n"
                    member.size = len(data)
                target.addfile(
                    member, None if data is None else __import__("io").BytesIO(data)
                )
        try:
            verify_backup(plan_path, corrupt, repo, wiki)
        except ValueError as exc:
            assert "content mismatch" in str(exc)
        else:
            raise AssertionError("corrupt backup was accepted")
    finally:
        temporary.cleanup()


def test_existing_backup_is_not_replaced():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, _ = _resolved_fixture(repo, wiki)
        backup = repo / "backup.tar"
        backup.write_bytes(b"existing")
        try:
            create_backup(plan_path, backup, repo, wiki)
        except FileExistsError:
            pass
        else:
            raise AssertionError("existing backup was replaced")
        assert backup.read_bytes() == b"existing"
    finally:
        temporary.cleanup()


def test_backup_is_not_published_if_tree_changes_during_creation():
    temporary, repo, wiki = _git_fixture()
    real_verify = migration._verify_backup_descriptor
    try:
        plan_path, _ = _resolved_fixture(repo, wiki)
        backup = repo / "backup.tar"

        def mutate_after_stage(path: Path, descriptor: dict, members: dict) -> None:
            real_verify(path, descriptor, members)
            (wiki / "concurrent.txt").write_text("changed\n", encoding="utf-8")

        migration._verify_backup_descriptor = mutate_after_stage
        try:
            create_backup(plan_path, backup, repo, wiki)
        except ValueError as exc:
            assert "changed while backup" in str(exc)
        else:
            raise AssertionError("backup from a changing tree was published")
        assert not backup.exists()
    finally:
        migration._verify_backup_descriptor = real_verify
        temporary.cleanup()


def test_confirmation_and_candidate_failure_leave_tree_unchanged():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, _ = _resolved_fixture(repo, wiki)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        before = build_tree_manifest(wiki)
        for confirmation, checker, expected in (
            (
                "0" * 64,
                lambda candidate, candidate_repo, canonical_paths: None,
                "confirmation",
            ),
            (
                _sha256(plan_path.read_bytes()),
                lambda candidate, candidate_repo, canonical_paths: (
                    _ for _ in ()
                ).throw(ValueError("check failed")),
                "check failed",
            ),
        ):
            journal = repo / f"journal-{expected}.json"
            try:
                apply_resolved_plan(
                    plan_path,
                    backup,
                    repo,
                    wiki,
                    confirmation,
                    journal,
                    checker,
                )
            except ValueError as exc:
                assert expected in str(exc)
            else:
                raise AssertionError("invalid apply was accepted")
            assert build_tree_manifest(wiki) == before
    finally:
        temporary.cleanup()


def test_transaction_state_files_inside_wiki_are_rejected():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, _ = _resolved_fixture(repo, wiki)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        before = build_tree_manifest(wiki)
        try:
            apply_resolved_plan(
                plan_path,
                backup,
                repo,
                wiki,
                _sha256(plan_path.read_bytes()),
                wiki / "journal.json",
                lambda candidate, candidate_repo, canonical_paths: None,
            )
        except ValueError as exc:
            assert "outside knowledge root" in str(exc)
        else:
            raise AssertionError("journal inside knowledge root was accepted")
        assert build_tree_manifest(wiki) == before
    finally:
        temporary.cleanup()


def test_atomic_exchange_failure_leaves_tree_unchanged():
    temporary, repo, wiki = _git_fixture()
    real_exchange = migration.exchange_directories
    try:
        plan_path, _ = _resolved_fixture(repo, wiki)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        before = build_tree_manifest(wiki)

        def unavailable(left: Path, right: Path) -> None:
            raise OSError("exchange unavailable")

        migration.exchange_directories = unavailable
        try:
            apply_resolved_plan(
                plan_path,
                backup,
                repo,
                wiki,
                _sha256(plan_path.read_bytes()),
                repo / "journal.json",
                lambda candidate, candidate_repo, canonical_paths: None,
            )
        except OSError as exc:
            assert "unavailable" in str(exc)
        else:
            raise AssertionError("unsupported exchange was accepted")
        assert build_tree_manifest(wiki) == before
    finally:
        migration.exchange_directories = real_exchange
        temporary.cleanup()


def test_crash_after_exchange_is_recovered_from_prepared_journal():
    temporary, repo, wiki = _git_fixture()
    real_write_journal = migration._write_journal
    try:
        plan_path, plan = _resolved_fixture(repo, wiki)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        before = build_tree_manifest(wiki)
        journal = repo / "journal.json"

        def crash_on_swapped(path: Path, value: dict) -> None:
            if value["state"] == "SWAPPED":
                raise SystemExit("simulated crash")
            real_write_journal(path, value)

        migration._write_journal = crash_on_swapped
        try:
            apply_resolved_plan(
                plan_path,
                backup,
                repo,
                wiki,
                _sha256(plan_path.read_bytes()),
                journal,
                lambda candidate, candidate_repo, canonical_paths: None,
            )
        except SystemExit as exc:
            assert "simulated crash" in str(exc)
        else:
            raise AssertionError("crash injection did not stop apply")
        migration._write_journal = real_write_journal
        prepared = json.loads(journal.read_text(encoding="utf-8"))
        assert prepared["state"] == "PREPARED"
        candidate = Path(prepared["candidate_root"])
        recovered = recover_transaction(
            journal,
            plan_path,
            _sha256(plan_path.read_bytes()),
            repo,
            wiki,
        )
        assert recovered["state"] == "ABORTED"
        assert build_tree_manifest(wiki) == before
        assert candidate.is_dir()
        assert (
            build_tree_manifest(candidate)["tree_sha256"]
            == plan["expected_target_tree_sha256"]
        )
    finally:
        migration._write_journal = real_write_journal
        temporary.cleanup()


def test_restore_crash_after_exchange_is_recovered_from_prepared_journal():
    temporary, repo, wiki = _git_fixture()
    real_write_journal = migration._write_journal
    try:
        plan_path, plan = _resolved_fixture(repo, wiki)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        apply_resolved_plan(
            plan_path,
            backup,
            repo,
            wiki,
            _sha256(plan_path.read_bytes()),
            repo / "apply-journal.json",
            lambda candidate, candidate_repo, canonical_paths: None,
        )
        target = build_tree_manifest(wiki)
        journal = repo / "restore-journal.json"

        def crash_on_swapped(path: Path, value: dict) -> None:
            if value["state"] == "SWAPPED":
                raise SystemExit("simulated restore crash")
            real_write_journal(path, value)

        migration._write_journal = crash_on_swapped
        try:
            restore_backup(
                plan_path,
                backup,
                repo,
                wiki,
                plan["expected_target_tree_sha256"],
                journal,
            )
        except SystemExit as exc:
            assert "simulated restore crash" in str(exc)
        else:
            raise AssertionError("crash injection did not stop restore")
        migration._write_journal = real_write_journal
        prepared = json.loads(journal.read_text(encoding="utf-8"))
        candidate = Path(prepared["candidate_root"])
        recovered = recover_transaction(
            journal,
            plan_path,
            _sha256(plan_path.read_bytes()),
            repo,
            wiki,
        )
        assert recovered["state"] == "ABORTED"
        assert build_tree_manifest(wiki) == target
        assert candidate.is_dir()
        assert build_tree_manifest(candidate)["tree_sha256"] == plan["base_tree_sha256"]
    finally:
        migration._write_journal = real_write_journal
        temporary.cleanup()


def test_recovery_rejects_unbound_root_and_unknown_candidate_without_deletion():
    temporary, repo, wiki = _git_fixture()
    real_write_journal = migration._write_journal
    try:
        plan_path, _ = _resolved_fixture(repo, wiki)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        journal = repo / "journal.json"

        def crash_on_swapped(path: Path, value: dict) -> None:
            if value["state"] == "SWAPPED":
                raise SystemExit("simulated crash")
            real_write_journal(path, value)

        migration._write_journal = crash_on_swapped
        try:
            apply_resolved_plan(
                plan_path,
                backup,
                repo,
                wiki,
                _sha256(plan_path.read_bytes()),
                journal,
                lambda candidate, candidate_repo, canonical_paths: None,
            )
        except SystemExit:
            pass
        migration._write_journal = real_write_journal
        saved = json.loads(journal.read_text(encoding="utf-8"))
        candidate = Path(saved["candidate_root"])
        (candidate / "unknown.txt").write_text("preserve\n", encoding="utf-8")
        try:
            recover_transaction(
                journal,
                plan_path,
                _sha256(plan_path.read_bytes()),
                repo,
                wiki,
            )
        except ValueError as exc:
            assert "recoverable state" in str(exc)
        else:
            raise AssertionError("unknown recovery candidate was deleted")
        assert candidate.exists()

        victim = repo / "victim"
        victim.mkdir()
        (victim / "keep.txt").write_text("keep\n", encoding="utf-8")
        saved["knowledge_root"] = str(victim)
        journal.write_bytes(plan_bytes(saved))
        try:
            recover_transaction(
                journal,
                plan_path,
                _sha256(plan_path.read_bytes()),
                repo,
                wiki,
            )
        except ValueError as exc:
            assert "not requested root" in str(exc)
        else:
            raise AssertionError("unbound recovery root was accepted")
        assert (victim / "keep.txt").read_text(encoding="utf-8") == "keep\n"
    finally:
        migration._write_journal = real_write_journal
        temporary.cleanup()


def test_moved_page_with_external_old_path_reference_is_rejected():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, _ = _resolved_fixture(repo, wiki, target_path="collections/page.md")
        (repo / "outside.md").write_text("wiki/pages/page.md\n", encoding="utf-8")
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        before = build_tree_manifest(wiki)
        try:
            apply_resolved_plan(
                plan_path,
                backup,
                repo,
                wiki,
                _sha256(plan_path.read_bytes()),
                repo / "journal.json",
                lambda candidate, candidate_repo, canonical_paths: None,
            )
        except ValueError as exc:
            assert "stale external" in str(exc)
        else:
            raise AssertionError("stale external reference was accepted")
        assert build_tree_manifest(wiki) == before
    finally:
        temporary.cleanup()


def test_moved_page_with_bare_relative_old_path_reference_is_rejected():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, _ = _resolved_fixture(repo, wiki, target_path="collections/page.md")
        (repo / "outside.yaml").write_text("source: pages/page.md\n", encoding="utf-8")
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        try:
            apply_resolved_plan(
                plan_path,
                backup,
                repo,
                wiki,
                _sha256(plan_path.read_bytes()),
                repo / "journal.json",
                lambda candidate, candidate_repo, canonical_paths: None,
            )
        except ValueError as exc:
            assert "stale external" in str(exc)
        else:
            raise AssertionError("bare stale external reference was accepted")
    finally:
        temporary.cleanup()


def test_immutable_raw_payload_is_excluded_from_live_reference_scan():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, plan = _resolved_fixture(
            repo, wiki, target_path="collections/page.md"
        )
        payload = repo / "raw" / "sources" / "clipping" / "fixture" / "revision"
        payload.mkdir(parents=True)
        (payload / "payload.md").write_text(
            "wiki/pages/page.md [[page]]\n", encoding="utf-8"
        )
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        result = apply_resolved_plan(
            plan_path,
            backup,
            repo,
            wiki,
            _sha256(plan_path.read_bytes()),
            repo / "journal.json",
            lambda candidate, candidate_repo, canonical_paths: None,
        )
        assert result["state"] == "COMMITTED"
        assert (
            build_tree_manifest(wiki)["tree_sha256"]
            == plan["expected_target_tree_sha256"]
        )
    finally:
        temporary.cleanup()


def test_append_only_log_reference_is_historical_not_active():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, plan = _resolved_fixture(
            repo, wiki, target_path="collections/page.md"
        )
        candidate = repo / "candidate"
        migration._build_candidate(plan, wiki, candidate)
        (candidate / "log.md").write_text(
            "## [2026-01-01] ingest | fixture\n\n"
            "- 생성: `wiki/pages/page.md`\n",
            encoding="utf-8",
        )
        active = migration._stale_path_references(
            plan, repo, wiki, candidate, {plan_path.resolve()}
        )
        historical = migration._historical_log_references(plan, candidate)
        assert active == []
        assert historical == [
            {
                "path": "wiki/log.md",
                "source_path": "pages/page.md",
                "occurrences": 1,
                "classification": "append-only-history",
            }
        ]
    finally:
        temporary.cleanup()


def test_question_pack_cascade_preserves_non_path_source_ref_fields(tmp_path):
    candidate = tmp_path / "candidate"
    target = candidate / "collections" / "page.md"
    target.parent.mkdir(parents=True)
    target.write_text("supported excerpt\n", encoding="utf-8")
    before = {
        "questions": [
            {
                "sourceRefs": [
                    {
                        "path": "pages/page.md",
                        "line": 1,
                        "excerpt": "supported excerpt",
                        "status": "official",
                    }
                ]
            }
        ]
    }
    after = json.loads(json.dumps(before))
    after["questions"][0]["sourceRefs"][0]["path"] = "collections/page.md"
    total, changed = migration._validate_question_pack_rewrite(
        json.dumps(before).encode(),
        json.dumps(after).encode(),
        {"pages/page.md": "collections/page.md"},
        candidate,
    )
    assert (total, changed) == (1, 1)
    after["questions"][0]["sourceRefs"][0]["status"] = "inferred"
    try:
        migration._validate_question_pack_rewrite(
            json.dumps(before).encode(),
            json.dumps(after).encode(),
            {"pages/page.md": "collections/page.md"},
            candidate,
        )
    except ValueError as exc:
        assert "sourceRefs.status changed" in str(exc)
    else:
        raise AssertionError("sourceRefs status drift was accepted")


def test_question_pack_cascade_rejects_traversal_symlink_and_ambiguous_targets(
    tmp_path,
):
    before = {
        "sourceRefs": [
            {
                "path": "pages/page.md",
                "line": 1,
                "excerpt": "supported",
                "status": "official",
            }
        ]
    }
    for unsafe in ("../../outside.md", "/absolute.md"):
        after = json.loads(json.dumps(before))
        after["sourceRefs"][0]["path"] = unsafe
        try:
            migration._validate_question_pack_rewrite(
                json.dumps(before).encode(),
                json.dumps(after).encode(),
                {"pages/page.md": unsafe},
                tmp_path,
            )
        except ValueError as exc:
            assert "unsafe relative path" in str(exc)
        else:
            raise AssertionError(f"unsafe sourceRef path was accepted: {unsafe}")

    outside = tmp_path / "outside.md"
    outside.write_text("supported\n", encoding="utf-8")
    symlink = tmp_path / "collections" / "page.md"
    symlink.parent.mkdir()
    symlink.symlink_to(outside)
    after = json.loads(json.dumps(before))
    after["sourceRefs"][0]["path"] = "collections/page.md"
    try:
        migration._validate_question_pack_rewrite(
            json.dumps(before).encode(),
            json.dumps(after).encode(),
            {"pages/page.md": "collections/page.md"},
            tmp_path,
        )
    except ValueError as exc:
        assert "unsafe staged sourceRef target" in str(exc)
    else:
        raise AssertionError("symlink sourceRef target was accepted")
    symlink.unlink()
    symlink.write_text("supported\n", encoding="utf-8")
    duplicate = (
        tmp_path
        / "domains"
        / "information-security"
        / "collections"
        / "page.md"
    )
    duplicate.parent.mkdir(parents=True)
    duplicate.write_text("supported\n", encoding="utf-8")
    try:
        migration._validate_question_pack_rewrite(
            json.dumps(before).encode(),
            json.dumps(after).encode(),
            {"pages/page.md": "collections/page.md"},
            tmp_path,
        )
    except ValueError as exc:
        assert "invalid staged sourceRef target" in str(exc)
    else:
        raise AssertionError("ambiguous sourceRef target was accepted")


def test_cascade_stage_rejects_symlink_and_write_set_drift(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    external = tmp_path / "external"
    external.mkdir()
    (repo / "linked").symlink_to(external, target_is_directory=True)
    stage = tmp_path / "stage"
    stage.mkdir()
    try:
        migration._copy_cascade_stage(repo, stage)
    except ValueError as exc:
        assert "cascade input contains symlink" in str(exc)
    else:
        raise AssertionError("cascade stage accepted a symlink")
    root_link = tmp_path / "root-link"
    root_link.symlink_to(external, target_is_directory=True)
    try:
        migration._regular_tree_snapshot(root_link)
    except ValueError as exc:
        assert "snapshot root is not a regular directory" in str(exc)
    else:
        raise AssertionError("regular tree snapshot accepted a root symlink")
    (repo / "linked").unlink()
    clipping_parent = repo / "raw" / "sources"
    clipping_parent.mkdir(parents=True)
    (clipping_parent / "clipping").symlink_to(external, target_is_directory=True)
    second_stage = tmp_path / "second-stage"
    second_stage.mkdir()
    try:
        migration._copy_cascade_stage(repo, second_stage)
    except ValueError as exc:
        assert "snapshot root is not a regular directory" in str(exc)
    else:
        raise AssertionError("cascade stage accepted a clipping-root symlink")
    before = {"approved": ("file", 0o644, "a")}
    after = {
        "approved": ("file", 0o644, "b"),
        "unexpected": ("file", 0o644, "c"),
    }
    assert migration._changed_snapshot_paths(before, after) == {
        "approved",
        "unexpected",
    }


def test_current_reference_cascade_plan_is_complete_and_no_write(tmp_path):
    _require_current_legacy_base()
    before_wiki = build_tree_manifest(ROOT / "wiki")
    protected = [
        ROOT / "projects" / "info-sec-engineer-practice" / "practice-data.js",
        ROOT / ".claude" / "resume_prompt.md",
        ROOT / "docs" / "wiki-ingest-architecture.md",
    ]
    before_protected = {path: _sha256(path.read_bytes()) for path in protected}
    project_root = ROOT / "projects" / "info-sec-engineer-practice"
    before_project = migration._regular_tree_snapshot(project_root)
    inventory = build_migration_plan(ROOT, ROOT / "wiki")
    resolution = load_preservation_resolution(
        ROOT / "_meta" / "knowledge-migration-resolution.json",
        inventory,
        ROOT,
        ROOT / "wiki",
    )
    plan = build_preservation_plan(
        resolution, inventory, ROOT, ROOT / "wiki", verify_manifest
    )
    plan_path = tmp_path / "resolved.json"
    plan_path.write_bytes(plan_bytes(plan))
    candidate = tmp_path / "candidate"
    migration._build_candidate(plan, ROOT / "wiki", candidate)

    cascade, diff = build_reference_cascade_plan(
        plan_path, candidate, ROOT, ROOT / "wiki"
    )

    assert cascade["observed_reference_groups"] == 22
    assert cascade["observed_reference_occurrences"] == 676
    assert cascade["active_reference_groups"] == 21
    assert cascade["active_reference_occurrences"] == 675
    assert sum(
        item["occurrences"] for item in cascade["historical_exemptions"]
    ) == 1
    assert cascade["source_ref_total"] == 410
    assert cascade["source_ref_path_changes"] == 329
    assert cascade["staged_stale_reference_occurrences"] == 0
    assert cascade["scan_policy"]["hidden_paths"] == (
        "included unless explicitly excluded"
    )
    assert "non-UTF-8 files" in cascade["scan_policy"]["excluded"]
    assert "journal-bound terminal migration/restore candidate trees" in cascade[
        "scan_policy"
    ]["excluded"]
    assert cascade["diff_sha256"] == _sha256(diff)
    assert cascade["apply_requires_combined_transaction"] is True
    assert len(cascade["operations"]) == 15
    assert all(
        operation["base_mode"] == operation["target_mode"]
        for operation in cascade["operations"]
    )
    generated = next(
        operation
        for operation in cascade["operations"]
        if operation["owner"] == "generated-practice-data"
    )
    assert generated["action"] == "regenerate"
    assert generated["command"] == migration.CASCADE_PRACTICE_COMMAND
    generated_past_exams = next(
        operation
        for operation in cascade["operations"]
        if operation["owner"] == "generated-past-exams"
    )
    assert generated_past_exams["action"] == "regenerate"
    assert generated_past_exams["command"] == migration.CASCADE_PRACTICE_COMMAND
    assert generated_past_exams["occurrences"] == 0
    assert b"practice-data.js" in diff
    assert build_tree_manifest(ROOT / "wiki") == before_wiki
    assert {path: _sha256(path.read_bytes()) for path in protected} == before_protected
    assert migration._regular_tree_snapshot(project_root) == before_project


def _write_candidate_journal(
    repo: Path,
    wiki: Path,
    candidate: Path,
    *,
    operation: str,
    state: str,
) -> None:
    candidate_hash = build_tree_manifest(candidate)["tree_sha256"]
    base_hash, target_hash = (
        (candidate_hash, "1" * 64)
        if state == "COMMITTED"
        else ("1" * 64, candidate_hash)
    )
    journal = {
        "schema_version": "2.0",
        "operation": operation,
        "state": state,
        "knowledge_root": str(wiki.resolve()),
        "candidate_root": str(candidate.resolve()),
        "plan_sha256": "2" * 64,
        "base_tree_sha256": base_hash,
        "target_tree_sha256": target_hash,
        "cascade_plan_sha256": "3" * 64,
    }
    (repo / f"journal-{operation}-{state.lower()}.json").write_bytes(
        plan_bytes(journal)
    )


def test_only_journal_bound_terminal_candidates_are_excluded(tmp_path):
    repo = tmp_path / "repo"
    wiki = repo / "wiki"
    wiki.mkdir(parents=True)
    (wiki / "page.md").write_text("# Page\n", encoding="utf-8")
    for name, operation, state in (
        (".wiki.migration.base", "apply", "COMMITTED"),
        (".wiki.restore.target", "restore", "ABORTED"),
    ):
        root = repo / name
        root.mkdir()
        (root / "page.md").write_text("legacy reference\n", encoding="utf-8")
        _write_candidate_journal(
            repo, wiki, root, operation=operation, state=state
        )
    unbound = repo / ".wiki.migration.unbound"
    unbound.mkdir()
    (unbound / "reference.md").write_text("active reference\n", encoding="utf-8")
    hidden = repo / ".active-hidden"
    hidden.mkdir()
    (hidden / "reference.md").write_text("active reference\n", encoding="utf-8")
    stage = tmp_path / "stage"
    stage.mkdir()

    migration._copy_cascade_stage(repo, stage, knowledge_root=wiki)

    assert not (stage / ".wiki.migration.base").exists()
    assert not (stage / ".wiki.restore.target").exists()
    assert (stage / ".wiki.migration.unbound" / "reference.md").is_file()
    assert (stage / ".active-hidden" / "reference.md").is_file()


def test_nonterminal_journal_does_not_exclude_reserved_candidate(tmp_path):
    repo = tmp_path / "repo"
    wiki = repo / "wiki"
    wiki.mkdir(parents=True)
    (wiki / "page.md").write_text("# Page\n", encoding="utf-8")
    candidate = repo / ".wiki.migration.prepared"
    candidate.mkdir()
    (candidate / "reference.md").write_text("active reference\n", encoding="utf-8")
    _write_candidate_journal(
        repo, wiki, candidate, operation="apply", state="PREPARED"
    )
    stage = tmp_path / "stage"
    stage.mkdir()

    migration._copy_cascade_stage(repo, stage, knowledge_root=wiki)

    assert (stage / ".wiki.migration.prepared" / "reference.md").is_file()


def test_terminal_journal_digest_mismatch_does_not_exclude_candidate(tmp_path):
    repo = tmp_path / "repo"
    wiki = repo / "wiki"
    wiki.mkdir(parents=True)
    (wiki / "page.md").write_text("# Page\n", encoding="utf-8")
    candidate = repo / ".wiki.migration.changed"
    candidate.mkdir()
    reference = candidate / "reference.md"
    reference.write_text("before journal\n", encoding="utf-8")
    _write_candidate_journal(
        repo, wiki, candidate, operation="apply", state="COMMITTED"
    )
    reference.write_text("changed after journal\n", encoding="utf-8")
    stage = tmp_path / "stage"
    stage.mkdir()

    migration._copy_cascade_stage(repo, stage, knowledge_root=wiki)

    assert (stage / ".wiki.migration.changed" / "reference.md").read_text(
        encoding="utf-8"
    ) == "changed after journal\n"


def test_terminal_candidate_symlink_is_rejected_instead_of_excluded(tmp_path):
    repo = tmp_path / "repo"
    wiki = repo / "wiki"
    wiki.mkdir(parents=True)
    external = tmp_path / "external"
    external.mkdir()
    (repo / ".wiki.migration.link").symlink_to(external, target_is_directory=True)
    stage = tmp_path / "stage"
    stage.mkdir()

    with pytest.raises(ValueError, match="reserved migration candidate"):
        migration._copy_cascade_stage(repo, stage, knowledge_root=wiki)


def test_preview_reports_live_reference_impacts_without_applying():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, plan = _resolved_fixture(
            repo, wiki, target_path="collections/page.md"
        )
        (repo / "outside.md").write_text("wiki/pages/page.md\n", encoding="utf-8")
        before = build_tree_manifest(wiki)
        preview = repo / "preview"
        result = preview_resolved_plan(
            plan_path,
            preview,
            repo,
            Path("wiki"),
            lambda candidate, candidate_repo, canonical_paths: None,
        )
        assert result["structural_verdict"] == "PASS"
        assert result["apply_ready"] is False
        assert result["external_reference_occurrences"] == 1
        assert result["external_reference_findings"] == [
            {
                "path": str(repo / "outside.md"),
                "source_path": "pages/page.md",
                "occurrences": 1,
            }
        ]
        assert build_tree_manifest(wiki) == before
        assert (
            build_tree_manifest(preview)["tree_sha256"]
            == plan["expected_target_tree_sha256"]
        )
    finally:
        temporary.cleanup()


def test_preview_publish_failure_leaves_no_final_or_partial_destination():
    temporary, repo, wiki = _git_fixture()
    real_publish = migration.rename_path_no_replace
    try:
        plan_path, _ = _resolved_fixture(repo, wiki)
        preview = repo / "preview"

        def fail_publish(source: Path, target: Path) -> None:
            raise OSError("injected preview publish failure")

        migration.rename_path_no_replace = fail_publish
        try:
            preview_resolved_plan(
                plan_path,
                preview,
                repo,
                wiki,
                lambda candidate, candidate_repo, canonical_paths: None,
            )
        except OSError as exc:
            assert "injected preview publish failure" in str(exc)
        else:
            raise AssertionError("preview publish failure was accepted")
        assert not preview.exists()
        assert list(repo.glob(".preview.preview.*")) == []
    finally:
        migration.rename_path_no_replace = real_publish
        temporary.cleanup()


def test_preservation_apply_repeats_lineage_audit_before_exchange():
    temporary, repo, wiki = _git_fixture()
    real_audit = migration._audit_preservation_candidate
    called = False
    try:
        plan_path, plan = _resolved_fixture(repo, wiki)
        plan["resolution_mode"] = "preservation"
        plan_path.write_bytes(plan_bytes(plan))
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        before = build_tree_manifest(wiki)

        def reject_audit(*args, **kwargs):
            nonlocal called
            called = True
            raise ValueError("injected preservation audit failure")

        migration._audit_preservation_candidate = reject_audit
        try:
            apply_resolved_plan(
                plan_path,
                backup,
                repo,
                wiki,
                _sha256(plan_path.read_bytes()),
                repo / "journal.json",
                lambda candidate, candidate_repo, canonical_paths: None,
                lambda manifest: {},
            )
        except ValueError as exc:
            assert "injected preservation audit failure" in str(exc)
        else:
            raise AssertionError("preservation audit failure was accepted")
        assert called
        assert build_tree_manifest(wiki) == before
    finally:
        migration._audit_preservation_candidate = real_audit
        temporary.cleanup()


def test_moved_page_with_renamed_old_wikilink_id_is_rejected():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, _ = _resolved_fixture(
            repo, wiki, target_path="collections/new-page.md"
        )
        (repo / "outside.md").write_text("[[page|old]]\n", encoding="utf-8")
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        try:
            apply_resolved_plan(
                plan_path,
                backup,
                repo,
                wiki,
                _sha256(plan_path.read_bytes()),
                repo / "journal.json",
                lambda candidate, candidate_repo, canonical_paths: None,
            )
        except ValueError as exc:
            assert "stale external" in str(exc)
        else:
            raise AssertionError("renamed stale wikilink ID was accepted")
    finally:
        temporary.cleanup()


def test_checker_created_stale_reference_is_rejected_by_second_scan():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, _ = _resolved_fixture(
            repo, wiki, target_path="collections/new-page.md"
        )
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)

        def create_stale_reference(
            candidate: Path, candidate_repo: Path, canonical_paths: list[Path]
        ) -> None:
            (repo / "late.md").write_text("[[page]]\n", encoding="utf-8")

        try:
            apply_resolved_plan(
                plan_path,
                backup,
                repo,
                wiki,
                _sha256(plan_path.read_bytes()),
                repo / "journal.json",
                create_stale_reference,
            )
        except ValueError as exc:
            assert "stale external" in str(exc)
        else:
            raise AssertionError("late stale reference was accepted")
    finally:
        temporary.cleanup()


def test_apply_and_restore_retain_committed_rollback_candidates():
    temporary, repo, wiki = _git_fixture()
    real_write_journal = migration._write_journal
    try:
        plan_path, plan = _resolved_fixture(repo, wiki)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        late_candidates: list[Path] = []

        def write_late_file(path: Path, value: dict) -> None:
            real_write_journal(path, value)
            if value["state"] == "COMMITTED":
                candidate = Path(value["candidate_root"])
                (candidate / "late.txt").write_text("preserve\n", encoding="utf-8")
                late_candidates.append(candidate)

        migration._write_journal = write_late_file
        apply_resolved_plan(
            plan_path,
            backup,
            repo,
            wiki,
            _sha256(plan_path.read_bytes()),
            repo / "apply-journal.json",
            lambda candidate, candidate_repo, canonical_paths: None,
        )
        restore_backup(
            plan_path,
            backup,
            repo,
            wiki,
            plan["expected_target_tree_sha256"],
            repo / "restore-journal.json",
        )
        assert len(late_candidates) == 2
        for candidate in late_candidates:
            assert (candidate / "late.txt").read_text(encoding="utf-8") == "preserve\n"
    finally:
        migration._write_journal = real_write_journal
        temporary.cleanup()


def test_concurrent_apply_mutation_rolls_back_and_preserves_both_trees():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, _ = _resolved_fixture(repo, wiki)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        journal = repo / "journal.json"

        def mutate_live_tree(
            candidate: Path, candidate_repo: Path, canonical_paths: list[Path]
        ) -> None:
            (wiki / "concurrent.txt").write_text("keep\n", encoding="utf-8")

        try:
            apply_resolved_plan(
                plan_path,
                backup,
                repo,
                wiki,
                _sha256(plan_path.read_bytes()),
                journal,
                mutate_live_tree,
            )
        except ValueError as exc:
            assert "concurrent tree mutation" in str(exc)
        else:
            raise AssertionError("concurrent apply mutation was accepted")
        state = json.loads(journal.read_text(encoding="utf-8"))
        assert state["state"] == "CONFLICT"
        assert (wiki / "concurrent.txt").read_text(encoding="utf-8") == "keep\n"
        assert Path(state["candidate_root"]).is_dir()
        try:
            recover_transaction(
                journal,
                plan_path,
                _sha256(plan_path.read_bytes()),
                repo,
                wiki,
            )
        except ValueError as exc:
            assert "manual resolution" in str(exc)
        else:
            raise AssertionError("conflicted transaction was auto-recovered")
        assert Path(state["candidate_root"]).is_dir()
    finally:
        temporary.cleanup()


def test_concurrent_restore_mutation_rolls_back_and_preserves_both_trees():
    temporary, repo, wiki = _git_fixture()
    real_exchange = migration.exchange_directories
    try:
        plan_path, plan = _resolved_fixture(repo, wiki)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        apply_resolved_plan(
            plan_path,
            backup,
            repo,
            wiki,
            _sha256(plan_path.read_bytes()),
            repo / "apply-journal.json",
            lambda candidate, candidate_repo, canonical_paths: None,
        )
        calls = 0

        def mutate_before_exchange(left: Path, right: Path) -> None:
            nonlocal calls
            calls += 1
            if calls == 1:
                (left / "concurrent.txt").write_text("keep\n", encoding="utf-8")
            real_exchange(left, right)

        migration.exchange_directories = mutate_before_exchange
        journal = repo / "restore-journal.json"
        try:
            restore_backup(
                plan_path,
                backup,
                repo,
                wiki,
                plan["expected_target_tree_sha256"],
                journal,
            )
        except ValueError as exc:
            assert "concurrent tree mutation" in str(exc)
        else:
            raise AssertionError("concurrent restore mutation was accepted")
        state = json.loads(journal.read_text(encoding="utf-8"))
        assert state["state"] == "CONFLICT"
        assert (wiki / "concurrent.txt").read_text(encoding="utf-8") == "keep\n"
        assert Path(state["candidate_root"]).is_dir()
    finally:
        migration.exchange_directories = real_exchange
        temporary.cleanup()


def test_real_candidate_checker_scopes_validation_to_canonical_pages():
    temporary, repo, wiki = _git_fixture()
    try:
        artifact = (
            ROOT / "tests" / "fixtures" / "contracts" / "canonical-transcript-v1.json"
        )
        manifest = capture(
            artifact,
            source_type="video",
            source_id="fixture-video",
            primary_source="https://www.youtube.com/watch?v=fixture-video",
            media_type="application/json",
            created_at="2026-08-21T00:00:00+00:00",
            raw_root=repo / "raw",
        ).manifest_path
        manifest_ref = str(manifest.resolve().relative_to(repo.resolve()))
        fixture_ref = "raw/sources/video/fixture-video/" + "a" * 64 + "/manifest.json"
        concept = (
            ROOT / "tests" / "fixtures" / "knowledge" / "valid-concept.md"
        ).read_text(encoding="utf-8")
        concept = concept.replace(fixture_ref, manifest_ref).replace(
            "| broader | [[fixture-parent]] | direct outgoing edge |", ""
        )
        canonical = wiki / "staging" / "valid-concept.md"
        canonical.parent.mkdir()
        canonical.write_text(concept, encoding="utf-8")
        (wiki / "index.md").write_text("invalid generated page\n", encoding="utf-8")
        (wiki / "templates").mkdir()
        (wiki / "templates" / "invalid.md").write_text(
            "invalid template\n", encoding="utf-8"
        )
        _check_migration_candidate(wiki, repo, [canonical])
    finally:
        temporary.cleanup()


def test_restore_rejects_stale_current_tree():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, plan = _resolved_fixture(repo, wiki)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        apply_resolved_plan(
            plan_path,
            backup,
            repo,
            wiki,
            _sha256(plan_path.read_bytes()),
            repo / "apply-journal.json",
            lambda candidate, candidate_repo, canonical_paths: None,
        )
        (wiki / "post-apply-extra").write_text("stale\n", encoding="utf-8")
        before = build_tree_manifest(wiki)
        try:
            restore_backup(
                plan_path,
                backup,
                repo,
                wiki,
                plan["expected_target_tree_sha256"],
                repo / "restore-journal.json",
            )
        except ValueError as exc:
            assert "stale or unconfirmed" in str(exc)
        else:
            raise AssertionError("stale restore was accepted")
        assert build_tree_manifest(wiki) == before
    finally:
        temporary.cleanup()


def test_path_traversal_backup_member_is_rejected():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, _ = _resolved_fixture(repo, wiki)
        backup = repo / "malicious.tar"
        with tarfile.open(backup, "w") as archive:
            member = tarfile.TarInfo("../escape")
            member.size = 1
            archive.addfile(member, __import__("io").BytesIO(b"x"))
        try:
            verify_backup(plan_path, backup, repo, wiki)
        except ValueError as exc:
            assert "unsafe relative path" in str(exc)
        else:
            raise AssertionError("path traversal member was accepted")
    finally:
        temporary.cleanup()


def test_combined_apply_commits_wiki_and_external_reference_together():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, plan = _resolved_fixture(
            repo, wiki, target_path="collections/page.md"
        )
        cascade_path, cascade = _cascade_fixture(repo, plan_path, plan)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        journal = repo / "combined-apply-journal.json"

        result = apply_resolved_plan(
            plan_path,
            backup,
            repo,
            wiki,
            _sha256(plan_path.read_bytes()),
            journal,
            lambda candidate, candidate_repo, canonical_paths: None,
            cascade_plan_path=cascade_path,
            confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
        )

        external = repo / cascade["operations"][0]["path"]
        assert result["schema_version"] == "2.0"
        assert result["state"] == "COMMITTED"
        assert build_tree_manifest(wiki)["tree_sha256"] == plan[
            "expected_target_tree_sha256"
        ]
        assert _sha256(external.read_bytes()) == cascade["operations"][0][
            "target_sha256"
        ]
    finally:
        temporary.cleanup()


def test_combined_apply_rejects_unbound_or_unsafe_cascade_fields_before_write():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, plan = _resolved_fixture(
            repo, wiki, target_path="collections/page.md"
        )
        cascade_path, cascade = _cascade_fixture(repo, plan_path, plan)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        external = repo / cascade["operations"][0]["path"]
        base_tree = build_tree_manifest(wiki)
        base_external = external.read_bytes()
        mutations = {
            "plan-binding": lambda value: value.__setitem__(
                "migration_plan_sha256", "0" * 64
            ),
            "tree-binding": lambda value: value.__setitem__(
                "target_tree_sha256", "0" * 64
            ),
            "owner": lambda value: value["operations"][0].__setitem__(
                "owner", "system-handoff"
            ),
            "path": lambda value: value["operations"][0].__setitem__(
                "path", "../escape"
            ),
            "mode": lambda value: value["operations"][0].__setitem__(
                "base_mode", 0o600
            ),
            "bytes": lambda value: value["operations"][0].__setitem__(
                "base_content_base64",
                base64.b64encode(b"tampered\n").decode("ascii"),
            ),
        }
        for label, mutate in mutations.items():
            value = json.loads(json.dumps(cascade))
            mutate(value)
            mutated_path = repo / f"cascade-{label}.json"
            mutated_path.write_bytes(plan_bytes(value))
            journal = repo / f"journal-{label}.json"
            try:
                apply_resolved_plan(
                    plan_path,
                    backup,
                    repo,
                    wiki,
                    _sha256(plan_path.read_bytes()),
                    journal,
                    lambda candidate, candidate_repo, canonical_paths: None,
                    cascade_plan_path=mutated_path,
                    confirm_cascade_plan_sha256=_sha256(mutated_path.read_bytes()),
                )
            except ValueError:
                pass
            else:
                raise AssertionError(f"unsafe cascade mutation was accepted: {label}")
            assert not journal.exists()
            assert build_tree_manifest(wiki) == base_tree
            assert external.read_bytes() == base_external
    finally:
        temporary.cleanup()


def test_combined_preflight_failure_writes_neither_side_nor_journal():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, plan = _resolved_fixture(
            repo, wiki, target_path="collections/page.md"
        )
        cascade_path, cascade = _cascade_fixture(repo, plan_path, plan)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        journal = repo / "combined-apply-journal.json"
        external = repo / cascade["operations"][0]["path"]
        base_tree = build_tree_manifest(wiki)
        base_external = external.read_bytes()

        def reject_candidate(
            candidate: Path, candidate_repo: Path, canonical_paths: list[Path]
        ) -> None:
            raise ValueError("injected combined preflight failure")

        try:
            apply_resolved_plan(
                plan_path,
                backup,
                repo,
                wiki,
                _sha256(plan_path.read_bytes()),
                journal,
                reject_candidate,
                cascade_plan_path=cascade_path,
                confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
            )
        except ValueError as exc:
            assert "injected combined preflight failure" in str(exc)
        else:
            raise AssertionError("combined preflight failure was accepted")

        assert not journal.exists()
        assert build_tree_manifest(wiki) == base_tree
        assert external.read_bytes() == base_external
    finally:
        temporary.cleanup()


def test_combined_preflight_rejects_stale_references_before_and_after_checker():
    temporary, repo, wiki = _git_fixture()
    real_reject_stale = migration._reject_stale_path_references
    events: list[str] = []
    try:
        plan_path, plan = _resolved_fixture(
            repo, wiki, target_path="collections/page.md"
        )
        cascade_path, _ = _cascade_fixture(repo, plan_path, plan)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)

        def record_stale_check(*args: object, **kwargs: object) -> None:
            events.append("stale")

        def record_candidate_check(
            candidate: Path, candidate_repo: Path, canonical_paths: list[Path]
        ) -> None:
            events.append("checker")

        migration._reject_stale_path_references = record_stale_check
        apply_resolved_plan(
            plan_path,
            backup,
            repo,
            wiki,
            _sha256(plan_path.read_bytes()),
            repo / "combined-apply-journal.json",
            record_candidate_check,
            cascade_plan_path=cascade_path,
            confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
        )

        assert events == ["stale", "checker", "stale"]
    finally:
        migration._reject_stale_path_references = real_reject_stale
        temporary.cleanup()


def test_combined_staging_does_not_duplicate_candidate_history_as_external_input():
    temporary, repo, wiki = _git_fixture()
    try:
        (wiki / "log.md").write_text(
            "## [2026-01-01] migration\n\n- 이전: `wiki/pages/page.md`\n",
            encoding="utf-8",
        )
        plan_path, plan = _resolved_fixture(
            repo, wiki, target_path="collections/page.md"
        )
        cascade_path, _ = _cascade_fixture(repo, plan_path, plan)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)

        result = apply_resolved_plan(
            plan_path,
            backup,
            repo,
            wiki,
            _sha256(plan_path.read_bytes()),
            repo / "combined-apply-journal.json",
            lambda candidate, candidate_repo, canonical_paths: None,
            cascade_plan_path=cascade_path,
            confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
        )

        assert result["state"] == "COMMITTED"
    finally:
        temporary.cleanup()


def test_combined_apply_recovery_restores_base_after_external_write_crash():
    temporary, repo, wiki = _git_fixture()
    real_write_journal = migration._write_journal
    try:
        plan_path, plan = _resolved_fixture(
            repo, wiki, target_path="collections/page.md"
        )
        cascade_path, cascade = _cascade_fixture(repo, plan_path, plan)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        journal = repo / "combined-apply-journal.json"

        def crash_after_external(path: Path, value: dict) -> None:
            real_write_journal(path, value)
            if value["state"] == "EXTERNAL_WRITTEN":
                raise SystemExit("injected crash")

        migration._write_journal = crash_after_external
        try:
            apply_resolved_plan(
                plan_path,
                backup,
                repo,
                wiki,
                _sha256(plan_path.read_bytes()),
                journal,
                lambda candidate, candidate_repo, canonical_paths: None,
                cascade_plan_path=cascade_path,
                confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
            )
        except SystemExit as exc:
            assert "injected crash" in str(exc)
        else:
            raise AssertionError("combined apply crash was not injected")
        migration._write_journal = real_write_journal

        result = recover_transaction(
            journal,
            plan_path,
            _sha256(plan_path.read_bytes()),
            repo,
            wiki,
            cascade_plan_path=cascade_path,
            confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
        )

        external = repo / cascade["operations"][0]["path"]
        assert result["state"] == "ABORTED"
        assert build_tree_manifest(wiki)["tree_sha256"] == plan["base_tree_sha256"]
        assert _sha256(external.read_bytes()) == cascade["operations"][0][
            "base_sha256"
        ]
    finally:
        migration._write_journal = real_write_journal
        temporary.cleanup()


def test_combined_restore_recovery_restores_target_after_external_write_crash():
    temporary, repo, wiki = _git_fixture()
    real_write_journal = migration._write_journal
    try:
        plan_path, plan = _resolved_fixture(
            repo, wiki, target_path="collections/page.md"
        )
        cascade_path, cascade = _cascade_fixture(repo, plan_path, plan)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        apply_resolved_plan(
            plan_path,
            backup,
            repo,
            wiki,
            _sha256(plan_path.read_bytes()),
            repo / "combined-apply-journal.json",
            lambda candidate, candidate_repo, canonical_paths: None,
            cascade_plan_path=cascade_path,
            confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
        )
        journal = repo / "combined-restore-journal.json"

        def crash_after_external(path: Path, value: dict) -> None:
            real_write_journal(path, value)
            if value["state"] == "EXTERNAL_WRITTEN":
                raise SystemExit("injected crash")

        migration._write_journal = crash_after_external
        try:
            restore_backup(
                plan_path,
                backup,
                repo,
                wiki,
                plan["expected_target_tree_sha256"],
                journal,
                cascade_plan_path=cascade_path,
                confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
            )
        except SystemExit as exc:
            assert "injected crash" in str(exc)
        else:
            raise AssertionError("combined restore crash was not injected")
        migration._write_journal = real_write_journal

        result = recover_transaction(
            journal,
            plan_path,
            _sha256(plan_path.read_bytes()),
            repo,
            wiki,
            cascade_plan_path=cascade_path,
            confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
        )

        external = repo / cascade["operations"][0]["path"]
        assert result["state"] == "ABORTED"
        assert build_tree_manifest(wiki)["tree_sha256"] == plan[
            "expected_target_tree_sha256"
        ]
        assert _sha256(external.read_bytes()) == cascade["operations"][0][
            "target_sha256"
        ]
    finally:
        migration._write_journal = real_write_journal
        temporary.cleanup()


def test_combined_apply_recovery_restores_both_sides_after_swap_crash():
    temporary, repo, wiki = _git_fixture()
    real_write_journal = migration._write_journal
    try:
        plan_path, plan = _resolved_fixture(
            repo, wiki, target_path="collections/page.md"
        )
        cascade_path, cascade = _cascade_fixture(repo, plan_path, plan)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        journal = repo / "combined-apply-journal.json"

        def crash_after_swap(path: Path, value: dict) -> None:
            real_write_journal(path, value)
            if value["state"] == "SWAPPED":
                raise SystemExit("injected crash")

        migration._write_journal = crash_after_swap
        try:
            apply_resolved_plan(
                plan_path,
                backup,
                repo,
                wiki,
                _sha256(plan_path.read_bytes()),
                journal,
                lambda candidate, candidate_repo, canonical_paths: None,
                cascade_plan_path=cascade_path,
                confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
            )
        except SystemExit as exc:
            assert "injected crash" in str(exc)
        else:
            raise AssertionError("combined swap crash was not injected")
        migration._write_journal = real_write_journal

        result = recover_transaction(
            journal,
            plan_path,
            _sha256(plan_path.read_bytes()),
            repo,
            wiki,
            cascade_plan_path=cascade_path,
            confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
        )

        external = repo / cascade["operations"][0]["path"]
        assert result["state"] == "ABORTED"
        assert build_tree_manifest(wiki)["tree_sha256"] == plan["base_tree_sha256"]
        assert _sha256(external.read_bytes()) == cascade["operations"][0][
            "base_sha256"
        ]
    finally:
        migration._write_journal = real_write_journal
        temporary.cleanup()


def test_combined_recovery_preserves_unknown_external_content_as_conflict():
    temporary, repo, wiki = _git_fixture()
    real_write_journal = migration._write_journal
    try:
        plan_path, plan = _resolved_fixture(
            repo, wiki, target_path="collections/page.md"
        )
        cascade_path, cascade = _cascade_fixture(repo, plan_path, plan)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        journal = repo / "combined-apply-journal.json"

        def crash_after_external(path: Path, value: dict) -> None:
            real_write_journal(path, value)
            if value["state"] == "EXTERNAL_WRITTEN":
                raise SystemExit("injected crash")

        migration._write_journal = crash_after_external
        try:
            apply_resolved_plan(
                plan_path,
                backup,
                repo,
                wiki,
                _sha256(plan_path.read_bytes()),
                journal,
                lambda candidate, candidate_repo, canonical_paths: None,
                cascade_plan_path=cascade_path,
                confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
            )
        except SystemExit:
            pass
        else:
            raise AssertionError("combined external crash was not injected")
        migration._write_journal = real_write_journal
        external = repo / cascade["operations"][0]["path"]
        external.write_bytes(b"concurrent content\n")

        try:
            recover_transaction(
                journal,
                plan_path,
                _sha256(plan_path.read_bytes()),
                repo,
                wiki,
                cascade_plan_path=cascade_path,
                confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
            )
        except ValueError as exc:
            assert "unknown external content" in str(exc)
        else:
            raise AssertionError("unknown external content was overwritten")

        assert external.read_bytes() == b"concurrent content\n"
        assert json.loads(journal.read_text(encoding="utf-8"))["state"] == "CONFLICT"
        assert build_tree_manifest(wiki)["tree_sha256"] == plan["base_tree_sha256"]
    finally:
        migration._write_journal = real_write_journal
        temporary.cleanup()


def test_combined_recovery_classifies_a_missing_external_file_as_conflict():
    temporary, repo, wiki = _git_fixture()
    real_write_journal = migration._write_journal
    try:
        plan_path, plan = _resolved_fixture(
            repo, wiki, target_path="collections/page.md"
        )
        cascade_path, cascade = _cascade_fixture(repo, plan_path, plan)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        journal = repo / "combined-apply-journal.json"

        def crash_after_external(path: Path, value: dict) -> None:
            real_write_journal(path, value)
            if value["state"] == "EXTERNAL_WRITTEN":
                raise SystemExit("injected crash")

        migration._write_journal = crash_after_external
        try:
            apply_resolved_plan(
                plan_path,
                backup,
                repo,
                wiki,
                _sha256(plan_path.read_bytes()),
                journal,
                lambda candidate, candidate_repo, canonical_paths: None,
                cascade_plan_path=cascade_path,
                confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
            )
        except SystemExit:
            pass
        else:
            raise AssertionError("combined external crash was not injected")
        migration._write_journal = real_write_journal
        external = repo / cascade["operations"][0]["path"]
        external.unlink()

        try:
            recover_transaction(
                journal,
                plan_path,
                _sha256(plan_path.read_bytes()),
                repo,
                wiki,
                cascade_plan_path=cascade_path,
                confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
            )
        except ValueError as exc:
            assert "unknown external content" in str(exc)
        else:
            raise AssertionError("missing external file was not classified as conflict")

        assert not external.exists()
        assert json.loads(journal.read_text(encoding="utf-8"))["state"] == "CONFLICT"
        assert build_tree_manifest(wiki)["tree_sha256"] == plan["base_tree_sha256"]
    finally:
        migration._write_journal = real_write_journal
        temporary.cleanup()


def test_external_state_classifies_a_missing_parent_directory_as_unknown():
    temporary, repo, wiki = _git_fixture()
    try:
        plan_path, plan = _resolved_fixture(
            repo, wiki, target_path="collections/page.md"
        )
        _, cascade = _cascade_fixture(repo, plan_path, plan)
        external = repo / cascade["operations"][0]["path"]
        shutil.rmtree(external.parent)
        assert migration._external_state(cascade, repo.resolve()) == "unknown"
    finally:
        temporary.cleanup()


def test_combined_apply_partial_external_failure_rolls_back_to_base():
    temporary, repo, wiki = _git_fixture()
    real_write_external = migration._write_external_state
    try:
        plan_path, plan = _resolved_fixture(
            repo, wiki, target_path="collections/page.md"
        )
        cascade_path, cascade = _cascade_fixture(repo, plan_path, plan)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        journal = repo / "combined-apply-journal.json"

        def fail_after_first_write(value: dict, root: Path, state: str) -> None:
            if state == "target":
                operation = value["operations"][0]
                migration._replace_external_file(
                    root / operation["path"],
                    migration._decode_cascade_content(operation, "target"),
                    operation["target_mode"],
                )
                raise OSError("injected partial external failure")
            real_write_external(value, root, state)

        migration._write_external_state = fail_after_first_write
        try:
            apply_resolved_plan(
                plan_path,
                backup,
                repo,
                wiki,
                _sha256(plan_path.read_bytes()),
                journal,
                lambda candidate, candidate_repo, canonical_paths: None,
                cascade_plan_path=cascade_path,
                confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
            )
        except OSError as exc:
            assert "injected partial external failure" in str(exc)
        else:
            raise AssertionError("partial external apply failure was accepted")

        external = repo / cascade["operations"][0]["path"]
        assert json.loads(journal.read_text(encoding="utf-8"))["state"] == "ABORTED"
        assert build_tree_manifest(wiki)["tree_sha256"] == plan["base_tree_sha256"]
        assert _sha256(external.read_bytes()) == cascade["operations"][0][
            "base_sha256"
        ]
    finally:
        migration._write_external_state = real_write_external
        temporary.cleanup()


def test_combined_restore_partial_external_failure_rolls_back_to_target():
    temporary, repo, wiki = _git_fixture()
    real_write_external = migration._write_external_state
    try:
        plan_path, plan = _resolved_fixture(
            repo, wiki, target_path="collections/page.md"
        )
        cascade_path, cascade = _cascade_fixture(repo, plan_path, plan)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        apply_resolved_plan(
            plan_path,
            backup,
            repo,
            wiki,
            _sha256(plan_path.read_bytes()),
            repo / "combined-apply-journal.json",
            lambda candidate, candidate_repo, canonical_paths: None,
            cascade_plan_path=cascade_path,
            confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
        )
        journal = repo / "combined-restore-journal.json"

        def fail_after_first_write(value: dict, root: Path, state: str) -> None:
            if state == "base":
                operation = value["operations"][0]
                migration._replace_external_file(
                    root / operation["path"],
                    migration._decode_cascade_content(operation, "base"),
                    operation["base_mode"],
                )
                raise OSError("injected partial external failure")
            real_write_external(value, root, state)

        migration._write_external_state = fail_after_first_write
        try:
            restore_backup(
                plan_path,
                backup,
                repo,
                wiki,
                plan["expected_target_tree_sha256"],
                journal,
                cascade_plan_path=cascade_path,
                confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
            )
        except OSError as exc:
            assert "injected partial external failure" in str(exc)
        else:
            raise AssertionError("partial external restore failure was accepted")

        external = repo / cascade["operations"][0]["path"]
        assert json.loads(journal.read_text(encoding="utf-8"))["state"] == "ABORTED"
        assert build_tree_manifest(wiki)["tree_sha256"] == plan[
            "expected_target_tree_sha256"
        ]
        assert _sha256(external.read_bytes()) == cascade["operations"][0][
            "target_sha256"
        ]
    finally:
        migration._write_external_state = real_write_external
        temporary.cleanup()


def test_combined_apply_prepared_journal_always_binds_complete_candidate():
    temporary, repo, wiki = _git_fixture()
    real_write_journal = migration._write_journal
    try:
        plan_path, plan = _resolved_fixture(
            repo, wiki, target_path="collections/page.md"
        )
        cascade_path, _ = _cascade_fixture(repo, plan_path, plan)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        journal = repo / "combined-apply-journal.json"

        def crash_on_prepared(path: Path, value: dict) -> None:
            real_write_journal(path, value)
            if value["state"] == "PREPARED":
                raise SystemExit("injected prepared crash")

        migration._write_journal = crash_on_prepared
        try:
            apply_resolved_plan(
                plan_path,
                backup,
                repo,
                wiki,
                _sha256(plan_path.read_bytes()),
                journal,
                lambda candidate, candidate_repo, canonical_paths: None,
                cascade_plan_path=cascade_path,
                confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
            )
        except SystemExit:
            pass
        else:
            raise AssertionError("combined prepared crash was not injected")

        saved = json.loads(journal.read_text(encoding="utf-8"))
        assert build_tree_manifest(Path(saved["candidate_root"]))[
            "tree_sha256"
        ] == plan["expected_target_tree_sha256"]
        migration._write_journal = real_write_journal
        recovered = recover_transaction(
            journal,
            plan_path,
            _sha256(plan_path.read_bytes()),
            repo,
            wiki,
            cascade_plan_path=cascade_path,
            confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
        )
        assert recovered["state"] == "ABORTED"
        assert build_tree_manifest(wiki)["tree_sha256"] == plan["base_tree_sha256"]
    finally:
        migration._write_journal = real_write_journal
        temporary.cleanup()


def test_combined_restore_prepared_journal_always_binds_complete_candidate():
    temporary, repo, wiki = _git_fixture()
    real_write_journal = migration._write_journal
    try:
        plan_path, plan = _resolved_fixture(
            repo, wiki, target_path="collections/page.md"
        )
        cascade_path, _ = _cascade_fixture(repo, plan_path, plan)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        apply_resolved_plan(
            plan_path,
            backup,
            repo,
            wiki,
            _sha256(plan_path.read_bytes()),
            repo / "combined-apply-journal.json",
            lambda candidate, candidate_repo, canonical_paths: None,
            cascade_plan_path=cascade_path,
            confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
        )
        journal = repo / "combined-restore-journal.json"

        def crash_on_prepared(path: Path, value: dict) -> None:
            real_write_journal(path, value)
            if value["state"] == "PREPARED":
                raise SystemExit("injected prepared crash")

        migration._write_journal = crash_on_prepared
        try:
            restore_backup(
                plan_path,
                backup,
                repo,
                wiki,
                plan["expected_target_tree_sha256"],
                journal,
                cascade_plan_path=cascade_path,
                confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
            )
        except SystemExit:
            pass
        else:
            raise AssertionError("combined restore prepared crash was not injected")

        saved = json.loads(journal.read_text(encoding="utf-8"))
        assert build_tree_manifest(Path(saved["candidate_root"]))[
            "tree_sha256"
        ] == plan["base_tree_sha256"]
        migration._write_journal = real_write_journal
        recovered = recover_transaction(
            journal,
            plan_path,
            _sha256(plan_path.read_bytes()),
            repo,
            wiki,
            cascade_plan_path=cascade_path,
            confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
        )
        assert recovered["state"] == "ABORTED"
        assert build_tree_manifest(wiki)["tree_sha256"] == plan[
            "expected_target_tree_sha256"
        ]
    finally:
        migration._write_journal = real_write_journal
        temporary.cleanup()


def test_combined_recovery_rejects_a_missing_prepared_candidate():
    temporary, repo, wiki = _git_fixture()
    real_write_journal = migration._write_journal
    try:
        plan_path, plan = _resolved_fixture(
            repo, wiki, target_path="collections/page.md"
        )
        cascade_path, cascade = _cascade_fixture(repo, plan_path, plan)
        backup = repo / "backup.tar"
        create_backup(plan_path, backup, repo, wiki)
        journal = repo / "combined-apply-journal.json"

        def crash_after_external(path: Path, value: dict) -> None:
            real_write_journal(path, value)
            if value["state"] == "EXTERNAL_WRITTEN":
                raise SystemExit("injected crash")

        migration._write_journal = crash_after_external
        try:
            apply_resolved_plan(
                plan_path,
                backup,
                repo,
                wiki,
                _sha256(plan_path.read_bytes()),
                journal,
                lambda candidate, candidate_repo, canonical_paths: None,
                cascade_plan_path=cascade_path,
                confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
            )
        except SystemExit:
            pass
        else:
            raise AssertionError("combined external crash was not injected")
        migration._write_journal = real_write_journal
        saved = json.loads(journal.read_text(encoding="utf-8"))
        shutil.rmtree(Path(saved["candidate_root"]))

        try:
            recover_transaction(
                journal,
                plan_path,
                _sha256(plan_path.read_bytes()),
                repo,
                wiki,
                cascade_plan_path=cascade_path,
                confirm_cascade_plan_sha256=_sha256(cascade_path.read_bytes()),
            )
        except ValueError as exc:
            assert "do not match a recoverable state" in str(exc)
        else:
            raise AssertionError("missing combined candidate was auto-recovered")

        external = repo / cascade["operations"][0]["path"]
        assert json.loads(journal.read_text(encoding="utf-8"))["state"] == "CONFLICT"
        assert _sha256(external.read_bytes()) == cascade["operations"][0][
            "target_sha256"
        ]
        assert build_tree_manifest(wiki)["tree_sha256"] == plan["base_tree_sha256"]
    finally:
        migration._write_journal = real_write_journal
        temporary.cleanup()


def main() -> int:
    tests = [
        value for name, value in sorted(globals().items()) if name.startswith("test_")
    ]
    failed = 0
    for test in tests:
        try:
            test()
            print(f"PASS {test.__name__}")
        except (AssertionError, OSError, TypeError, ValueError) as exc:
            failed += 1
            print(f"FAIL {test.__name__}: {exc}")
    print(f"\n--- {len(tests) - failed} passed, {failed} failed / {len(tests)} ---")
    return int(bool(failed))


if __name__ == "__main__":
    sys.exit(main())
