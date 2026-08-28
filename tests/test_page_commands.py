import hashlib
import json
import os
import stat
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import knowledge.documents as page_documents  # noqa: E402
import wiki_ingest  # noqa: E402
from knowledge.artifacts import capture  # noqa: E402
from knowledge.check import check_target  # noqa: E402
from knowledge.documents import (  # noqa: E402
    PagePlanError,
    build_collection_add_member_plan,
    build_collection_reorder_plan,
    build_move_plan,
    build_promote_plan,
    build_synthesize_plan,
    page_plan_bytes,
    write_set_overrides,
)
from knowledge.documents import (  # noqa: E402
    apply_page_write_plan as _apply_page_write_plan,
)
from knowledge.materialize import render_generated  # noqa: E402
from knowledge.schema import (  # noqa: E402
    KnowledgeSchemaError,
    document_tree_sha256,
    validator_for,
)

TRANSCRIPT = ROOT / "tests" / "fixtures" / "contracts" / "canonical-transcript-v1.json"
CONCEPT = ROOT / "tests" / "fixtures" / "knowledge" / "valid-concept.md"
COLLECTION = ROOT / "tests" / "fixtures" / "knowledge" / "valid-collection.md"
FIXTURE_MANIFEST = "raw/sources/video/fixture-video/" + "a" * 64 + "/manifest.json"
COLLECTION_MANIFEST = (
    "raw/sources/clipping/fixture-collection/" + "b" * 64 + "/manifest.json"
)
NOW = "2026-08-26"


def _setup_repo(tmp_path: Path) -> tuple[Path, Path, str]:
    repo = tmp_path / "repo"
    knowledge_root = repo / "wiki"
    (knowledge_root / "staging").mkdir(parents=True)
    (repo / "_meta").mkdir()
    (repo / "_meta" / "knowledge.schema.json").write_bytes(
        (ROOT / "_meta" / "knowledge.schema.json").read_bytes()
    )
    (repo / "_meta" / "domains.yaml").write_text(
        "version: 1\ndomains:\n  software-engineering:\n"
        "    status: active\n    label: Software Engineering\n"
        "    source_roots: []\n  architecture:\n"
        "    status: active\n    label: Architecture\n"
        "    source_roots: []\n  inactive-domain:\n"
        "    status: inactive\n    label: Inactive\n    source_roots: []\n",
        encoding="utf-8",
    )
    manifest = capture(
        TRANSCRIPT,
        source_type="video",
        source_id="fixture-video",
        primary_source="https://www.youtube.com/watch?v=fixture-video",
        media_type="application/json",
        created_at="2026-08-26T00:00:00Z",
        raw_root=repo / "raw",
    ).manifest_path
    for relative, content in render_generated(repo, knowledge_root).items():
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    return repo, knowledge_root, manifest.relative_to(repo).as_posix()


def _semantic_plan(manifest: str, **updates: object) -> dict:
    plan = {
        "title": "Page command contract",
        "page_type": "concept",
        "domain": "software-engineering",
        "tags": ["architecture"],
        "source_paths": [manifest],
        "summary": "Page command contract summary.",
        "sections": [
            {"heading": "Definition", "body": "Definition body."},
            {"heading": "Mechanism", "body": "Mechanism body."},
            {"heading": "Variants", "body": "Variants body."},
            {"heading": "Trade-offs", "body": "Trade-offs body."},
            {"heading": "Open Questions", "body": "Open question body."},
        ],
        "claims": [],
        "relations": [],
        "members": [],
    }
    plan.update(updates)
    return plan


def _candidate_check(repo: Path, knowledge_root: Path):
    def check(write_set: list[dict]) -> None:
        result = check_target(
            knowledge_root,
            repo_root=repo,
            mode="all",
            overrides=write_set_overrides(knowledge_root, write_set),
            include_repository_contracts=False,
        )
        if result.structural_verdict != "PASS":
            raise PagePlanError(f"candidate check failed: {result.findings}")

    return check


def apply_page_write_plan(
    plan_path: Path,
    confirmation: str,
    *,
    repo_root: Path,
    knowledge_root: Path,
    **kwargs,
) -> bool:
    return _apply_page_write_plan(
        plan_path,
        confirmation,
        repo_root=repo_root,
        knowledge_root=knowledge_root,
        candidate_check=_candidate_check(repo_root, knowledge_root),
        **kwargs,
    )


def _write_plan(path: Path, plan: dict) -> str:
    rendered = page_plan_bytes(plan)
    path.write_bytes(rendered)
    return hashlib.sha256(rendered).hexdigest()


def _write_existing_page(
    knowledge_root: Path,
    relative: str,
    manifest: str,
    *,
    collection: bool = False,
) -> Path:
    fixture = COLLECTION if collection else CONCEPT
    text = fixture.read_text(encoding="utf-8")
    text = text.replace(
        COLLECTION_MANIFEST if collection else FIXTURE_MANIFEST,
        manifest,
    )
    if not collection:
        text = text.replace(
            "| broader | [[fixture-parent]] | direct outgoing edge |",
            "",
        )
    path = knowledge_root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_synthesize_plan_is_deterministic_no_write_and_schema_valid(tmp_path: Path):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    semantic_path = repo / "semantic-plan.json"
    semantic_path.write_text(json.dumps(_semantic_plan(manifest)), encoding="utf-8")
    arguments = {
        "semantic_plan_path": semantic_path,
        "source_paths": [manifest],
        "page_id": "page-command-contract",
        "now": NOW,
        "repo_root": repo,
        "knowledge_root": knowledge_root,
    }

    first = build_synthesize_plan(**arguments)
    second = build_synthesize_plan(**arguments)

    assert first == second
    _candidate_check(repo, knowledge_root)(first["write_set"])
    assert list(validator_for("PageWritePlan").iter_errors(first)) == []
    assert first["operation"] == "synthesize"
    assert len(first["write_set"]) == 1
    assert first["write_set"][0]["target_path"] == (
        "staging/software-engineering/page-command-contract.md"
    )
    assert not (knowledge_root / first["write_set"][0]["target_path"]).exists()
    assert first["base_tree_sha256"] == document_tree_sha256(knowledge_root)


def test_synthesize_renders_claims_and_relations_with_escaped_table_cells(
    tmp_path: Path,
):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    semantic_path = repo / "semantic-plan.json"
    semantic_path.write_text(
        json.dumps(
            _semantic_plan(
                manifest,
                claims=[
                    {
                        "id": "C1",
                        "primary": False,
                        "text": "claim with | separator",
                        "status": "verified",
                        "evidence": "source:1",
                        "notes": "note with | separator",
                    }
                ],
                relations=[
                    {
                        "type": "related",
                        "target": "related-concept",
                        "notes": "relation with | separator",
                    }
                ],
            )
        ),
        encoding="utf-8",
    )

    plan = build_synthesize_plan(
        semantic_plan_path=semantic_path,
        source_paths=[manifest],
        page_id="page-command-contract",
        now=NOW,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )

    content = plan["write_set"][0]["content"]
    assert "claim with \\| separator" in content
    assert "note with \\| separator" in content
    assert "| related | [[related-concept]] | relation with \\| separator |" in content


def test_synthesize_validates_against_requested_repository_schema(tmp_path: Path):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    schema_path = repo / "_meta" / "knowledge.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    schema["$defs"]["PageWritePlan"]["required"].append("repo_only_field")
    schema_path.write_text(json.dumps(schema), encoding="utf-8")
    semantic_path = repo / "semantic-plan.json"
    semantic_path.write_text(json.dumps(_semantic_plan(manifest)), encoding="utf-8")

    with pytest.raises(PagePlanError, match="repo_only_field"):
        build_synthesize_plan(
            semantic_plan_path=semantic_path,
            source_paths=[manifest],
            page_id="page-command-contract",
            now=NOW,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )


@pytest.mark.parametrize(
    ("sources", "domain", "message"),
    [
        (
            ["raw/sources/video/other/" + "b" * 64 + "/manifest.json"],
            "software-engineering",
            "exact",
        ),
        (None, "inactive-domain", "active domain"),
    ],
)
def test_synthesize_rejects_source_mismatch_and_inactive_domain(
    tmp_path: Path,
    sources: list[str] | None,
    domain: str,
    message: str,
):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    semantic_path = repo / "semantic-plan.json"
    semantic_path.write_text(
        json.dumps(_semantic_plan(manifest, domain=domain)), encoding="utf-8"
    )
    with pytest.raises(PagePlanError, match=message):
        build_synthesize_plan(
            semantic_plan_path=semantic_path,
            source_paths=[manifest] if sources is None else sources,
            page_id="page-command-contract",
            now=NOW,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )


def test_apply_synthesize_requires_exact_confirmation_and_rejects_stale_tree(
    tmp_path: Path,
):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    semantic_path = repo / "semantic-plan.json"
    semantic_path.write_text(json.dumps(_semantic_plan(manifest)), encoding="utf-8")
    plan = build_synthesize_plan(
        semantic_plan_path=semantic_path,
        source_paths=[manifest],
        page_id="page-command-contract",
        now=NOW,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    plan_path = repo / "page-plan.json"
    digest = _write_plan(plan_path, plan)

    with pytest.raises(PagePlanError, match="confirmation"):
        apply_page_write_plan(
            plan_path,
            "0" * 64,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )
    assert not (knowledge_root / plan["write_set"][0]["target_path"]).exists()

    _write_existing_page(
        knowledge_root,
        "staging/unrelated.md",
        manifest,
    )
    with pytest.raises(PagePlanError, match="stale"):
        apply_page_write_plan(
            plan_path,
            digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )
    assert not (knowledge_root / plan["write_set"][0]["target_path"]).exists()


def test_apply_synthesize_creates_exact_candidate_after_validation(tmp_path: Path):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    semantic_path = repo / "semantic-plan.json"
    semantic_path.write_text(json.dumps(_semantic_plan(manifest)), encoding="utf-8")
    plan = build_synthesize_plan(
        semantic_plan_path=semantic_path,
        source_paths=[manifest],
        page_id="page-command-contract",
        now=NOW,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    plan_path = repo / "page-plan.json"
    digest = _write_plan(plan_path, plan)

    changed = apply_page_write_plan(
        plan_path,
        digest,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )

    target = knowledge_root / plan["write_set"][0]["target_path"]
    assert changed is True
    assert target.read_text(encoding="utf-8") == plan["write_set"][0]["content"]
    assert document_tree_sha256(knowledge_root) == plan["target_tree_sha256"]
    assert (
        apply_page_write_plan(
            plan_path,
            digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )
        is False
    )
    assert target.read_text(encoding="utf-8") == plan["write_set"][0]["content"]


def test_apply_rejects_synthesize_operation_input_not_bound_to_target(tmp_path: Path):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    semantic_path = repo / "semantic-plan.json"
    semantic_path.write_text(json.dumps(_semantic_plan(manifest)), encoding="utf-8")
    plan = build_synthesize_plan(
        semantic_plan_path=semantic_path,
        source_paths=[manifest],
        page_id="page-command-contract",
        now=NOW,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    plan["operation_input"]["page_id"] = "different-id"
    plan["input_sha256"] = page_documents._canonical_digest(plan["operation_input"])
    plan_path = repo / "forged-synthesize-plan.json"
    digest = _write_plan(plan_path, plan)
    with pytest.raises(PagePlanError, match="synthesize.*input|page ID"):
        apply_page_write_plan(
            plan_path,
            digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )


def test_apply_runs_full_candidate_check_inside_transaction(tmp_path: Path):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    semantic_path = repo / "semantic-plan.json"
    semantic_path.write_text(json.dumps(_semantic_plan(manifest)), encoding="utf-8")
    plan = build_synthesize_plan(
        semantic_plan_path=semantic_path,
        source_paths=[manifest],
        page_id="page-command-contract",
        now=NOW,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    entry = plan["write_set"][0]
    entry["content"] = entry["content"].replace(
        "|---|---|---|\n\n## Sources",
        "|---|---|---|\n| broader | [[missing-page]] | invalid |\n\n## Sources",
    )
    entry["target_sha256"] = hashlib.sha256(entry["content"].encode()).hexdigest()
    plan["target_tree_sha256"] = document_tree_sha256(
        knowledge_root,
        {knowledge_root / entry["target_path"]: entry["content"]},
    )
    plan_path = repo / "invalid-candidate-plan.json"
    digest = _write_plan(plan_path, plan)
    with pytest.raises(PagePlanError, match="candidate"):
        apply_page_write_plan(
            plan_path,
            digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )
    assert not (knowledge_root / entry["target_path"]).exists()


def test_promote_requires_review_and_preserves_content_and_id(tmp_path: Path):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    (knowledge_root / "domains" / "software-engineering").mkdir(parents=True)
    draft = _write_existing_page(
        knowledge_root,
        "staging/software-engineering/valid-concept.md",
        manifest,
    )
    draft.write_text(
        draft.read_text(encoding="utf-8").replace("| claimed |", "| verified |"),
        encoding="utf-8",
    )
    verdicts = repo / "review-verdicts.json"
    verdicts.write_text(
        json.dumps([{"claim_id": "C1", "verdict": "support"}]),
        encoding="utf-8",
    )
    plan = build_promote_plan(
        draft,
        knowledge_root / "domains" / "software-engineering",
        review_verdicts_path=verdicts,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    plan_path = repo / "promote-plan.json"
    digest = _write_plan(plan_path, plan)
    original = draft.read_bytes()

    with pytest.raises(PagePlanError, match="review approval"):
        apply_page_write_plan(
            plan_path,
            digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )
    assert draft.read_bytes() == original

    assert apply_page_write_plan(
        plan_path,
        digest,
        repo_root=repo,
        knowledge_root=knowledge_root,
        review_approved=True,
    )
    target = knowledge_root / "domains/software-engineering/valid-concept.md"
    assert target.read_bytes() == original
    assert not draft.exists()
    assert (
        apply_page_write_plan(
            plan_path,
            digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
            review_approved=True,
        )
        is False
    )


def test_promote_rejects_claimed_or_insufficient_primary_claim(tmp_path: Path):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    (knowledge_root / "domains" / "software-engineering").mkdir(parents=True)
    draft = _write_existing_page(
        knowledge_root,
        "staging/software-engineering/valid-concept.md",
        manifest,
    )
    verdicts = repo / "review-verdicts.json"
    verdicts.write_text(
        json.dumps([{"claim_id": "C1", "verdict": "insufficient"}]),
        encoding="utf-8",
    )
    with pytest.raises(PagePlanError, match="claimed|insufficient"):
        build_promote_plan(
            draft,
            knowledge_root / "domains" / "software-engineering",
            review_verdicts_path=verdicts,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )


def test_promote_rejects_unsorted_review_verdict_input(tmp_path: Path):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    (knowledge_root / "domains" / "software-engineering").mkdir(parents=True)
    draft = _write_existing_page(
        knowledge_root,
        "staging/software-engineering/valid-concept.md",
        manifest,
    )
    draft.write_text(
        draft.read_text(encoding="utf-8")
        .replace("| claimed |", "| verified |")
        .replace(
            "| C1 | true |",
            "| C2 | true | Second supported claim. | verified | "
            "`raw/sources/video/fixture-video/"
            + "a" * 64
            + "/manifest.json#L1` | reviewed |\n| C1 | true |",
        ),
        encoding="utf-8",
    )
    verdicts = repo / "review-verdicts.json"
    verdicts.write_text(
        json.dumps(
            [
                {"claim_id": "C2", "verdict": "support"},
                {"claim_id": "C1", "verdict": "support"},
            ]
        ),
        encoding="utf-8",
    )
    with pytest.raises(PagePlanError, match="sorted"):
        build_promote_plan(
            draft,
            knowledge_root / "domains" / "software-engineering",
            review_verdicts_path=verdicts,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )


def test_promote_replay_revalidates_confirmed_review_semantics(tmp_path: Path):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    (knowledge_root / "domains" / "software-engineering").mkdir(parents=True)
    draft = _write_existing_page(
        knowledge_root,
        "staging/software-engineering/valid-concept.md",
        manifest,
    )
    draft.write_text(
        draft.read_text(encoding="utf-8").replace("| claimed |", "| verified |"),
        encoding="utf-8",
    )
    verdicts = repo / "review-verdicts.json"
    verdicts.write_text(
        json.dumps([{"claim_id": "C1", "verdict": "support"}]),
        encoding="utf-8",
    )
    plan = build_promote_plan(
        draft,
        knowledge_root / "domains" / "software-engineering",
        review_verdicts_path=verdicts,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    plan_path = repo / "valid-promote-plan.json"
    digest = _write_plan(plan_path, plan)
    assert apply_page_write_plan(
        plan_path,
        digest,
        repo_root=repo,
        knowledge_root=knowledge_root,
        review_approved=True,
    )

    plan["review_verdicts"] = [{"claim_id": "C1", "verdict": "contradiction"}]
    plan["operation_input"]["review_verdicts_sha256"] = (
        page_documents._canonical_digest(plan["review_verdicts"])
    )
    plan["input_sha256"] = page_documents._canonical_digest(plan["operation_input"])
    malicious_path = repo / "malicious-promote-replay.json"
    malicious_digest = _write_plan(malicious_path, plan)
    with pytest.raises(PagePlanError, match="review verdict"):
        apply_page_write_plan(
            malicious_path,
            malicious_digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
            review_approved=True,
        )


def test_collection_add_and_reorder_change_only_collection_page(tmp_path: Path):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    collection = _write_existing_page(
        knowledge_root,
        "collections/valid-collection.md",
        manifest,
        collection=True,
    )
    _write_existing_page(
        knowledge_root, "domains/software-engineering/valid-concept.md", manifest
    )
    _write_existing_page(
        knowledge_root, "domains/software-engineering/second-concept.md", manifest
    )
    before_other = {
        path: path.read_bytes()
        for path in knowledge_root.rglob("*.md")
        if path != collection
    }
    add = build_collection_add_member_plan(
        collection,
        "second-concept",
        before=None,
        after="valid-concept",
        order_by_id=False,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    assert len(add["write_set"]) == 1
    assert "[[valid-concept]]" in add["write_set"][0]["content"]
    assert add["write_set"][0]["content"].index("[[valid-concept]]") < add["write_set"][
        0
    ]["content"].index("[[second-concept]]")
    add_path = repo / "add-plan.json"
    add_digest = _write_plan(add_path, add)
    assert apply_page_write_plan(
        add_path,
        add_digest,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    assert (
        apply_page_write_plan(
            add_path,
            add_digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )
        is False
    )
    assert all(path.read_bytes() == data for path, data in before_other.items())

    reorder = build_collection_reorder_plan(
        collection,
        ["second-concept", "valid-concept"],
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    content = reorder["write_set"][0]["content"]
    assert content.index("[[second-concept]]") < content.index("[[valid-concept]]")
    reorder_path = repo / "reorder-plan.json"
    reorder_digest = _write_plan(reorder_path, reorder)
    assert apply_page_write_plan(
        reorder_path,
        reorder_digest,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    assert (
        apply_page_write_plan(
            reorder_path,
            reorder_digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )
        is False
    )
    with pytest.raises(PagePlanError, match="exact member set"):
        build_collection_reorder_plan(
            collection,
            ["valid-concept"],
            repo_root=repo,
            knowledge_root=knowledge_root,
        )


def test_collection_add_requires_one_explicit_policy_and_supports_id_order(
    tmp_path: Path,
):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    collection = _write_existing_page(
        knowledge_root,
        "collections/valid-collection.md",
        manifest,
        collection=True,
    )
    _write_existing_page(
        knowledge_root,
        "domains/software-engineering/aardvark-concept.md",
        manifest,
    )

    with pytest.raises(PagePlanError, match="exactly one"):
        build_collection_add_member_plan(
            collection,
            "aardvark-concept",
            before=None,
            after=None,
            order_by_id=False,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )

    plan = build_collection_add_member_plan(
        collection,
        "aardvark-concept",
        before=None,
        after=None,
        order_by_id=True,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    content = plan["write_set"][0]["content"]
    assert content.index("[[aardvark-concept]]") < content.index("[[valid-concept]]")


def test_collection_rejects_invalid_duplicate_base_and_non_member_mutation(
    tmp_path: Path,
):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    collection = _write_existing_page(
        knowledge_root,
        "collections/valid-collection.md",
        manifest,
        collection=True,
    )
    _write_existing_page(
        knowledge_root, "domains/software-engineering/valid-concept.md", manifest
    )
    _write_existing_page(
        knowledge_root, "domains/software-engineering/second-concept.md", manifest
    )
    original = collection.read_text(encoding="utf-8")
    collection.write_text(
        original.replace(
            "| [[valid-concept]] | foundation | reviewed sequence |",
            "| [[valid-concept]] | foundation | reviewed sequence |\n"
            "| [[valid-concept]] | duplicate | conflicting row |",
        ),
        encoding="utf-8",
    )
    with pytest.raises(PagePlanError, match="duplicate"):
        build_collection_reorder_plan(
            collection,
            ["valid-concept"],
            repo_root=repo,
            knowledge_root=knowledge_root,
        )

    collection.write_text(original, encoding="utf-8")
    plan = build_collection_add_member_plan(
        collection,
        "second-concept",
        before=None,
        after="valid-concept",
        order_by_id=False,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    entry = plan["write_set"][0]
    entry["content"] = entry["content"].replace(
        "Collection overview.", "Tampered collection overview."
    )
    entry["target_sha256"] = hashlib.sha256(entry["content"].encode()).hexdigest()
    plan["target_tree_sha256"] = document_tree_sha256(
        knowledge_root, {collection: entry["content"]}
    )
    plan_path = repo / "tampered-collection-plan.json"
    digest = _write_plan(plan_path, plan)
    with pytest.raises(PagePlanError, match="Members|delta"):
        apply_page_write_plan(
            plan_path,
            digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )
    assert collection.read_text(encoding="utf-8") == original

    plan = build_collection_add_member_plan(
        collection,
        "second-concept",
        before=None,
        after="valid-concept",
        order_by_id=False,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    entry = plan["write_set"][0]
    valid_row = "| [[valid-concept]] | foundation | reviewed sequence |"
    added_row = "| [[second-concept]] |  |  |"
    entry["content"] = entry["content"].replace(
        f"{valid_row}\n{added_row}", f"{added_row}\n{valid_row}"
    )
    entry["target_sha256"] = hashlib.sha256(entry["content"].encode()).hexdigest()
    plan["target_tree_sha256"] = document_tree_sha256(
        knowledge_root, {collection: entry["content"]}
    )
    plan_path = repo / "wrong-position-collection-plan.json"
    digest = _write_plan(plan_path, plan)
    with pytest.raises(PagePlanError, match="ordering|delta"):
        apply_page_write_plan(
            plan_path,
            digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )


def test_collection_reorder_noop_revalidates_operation_input(tmp_path: Path):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    collection = _write_existing_page(
        knowledge_root,
        "collections/valid-collection.md",
        manifest,
        collection=True,
    )
    _write_existing_page(
        knowledge_root, "domains/software-engineering/valid-concept.md", manifest
    )
    plan = build_collection_reorder_plan(
        collection,
        ["valid-concept"],
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    assert plan["write_set"] == []
    plan["operation_input"]["collection_path"] = "collections/other.md"
    plan["input_sha256"] = page_documents._canonical_digest(plan["operation_input"])
    plan_path = repo / "invalid-noop-plan.json"
    digest = _write_plan(plan_path, plan)
    with pytest.raises(PagePlanError, match="no-op|collection"):
        apply_page_write_plan(
            plan_path,
            digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )


def test_collection_reorder_apply_rejects_member_set_loss(tmp_path: Path):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    collection = _write_existing_page(
        knowledge_root,
        "collections/valid-collection.md",
        manifest,
        collection=True,
    )
    _write_existing_page(
        knowledge_root, "domains/software-engineering/valid-concept.md", manifest
    )
    _write_existing_page(
        knowledge_root, "domains/software-engineering/second-concept.md", manifest
    )
    collection.write_text(
        collection.read_text(encoding="utf-8").replace(
            "| [[valid-concept]] | foundation | reviewed sequence |",
            "| [[valid-concept]] | foundation | reviewed sequence |\n"
            "| [[second-concept]] | follow-up | reviewed sequence |",
        ),
        encoding="utf-8",
    )
    plan = build_collection_reorder_plan(
        collection,
        ["second-concept", "valid-concept"],
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    plan["operation_input"]["members"] = ["valid-concept"]
    plan["input_sha256"] = page_documents._canonical_digest(plan["operation_input"])
    entry = plan["write_set"][0]
    entry["content"] = entry["content"].replace(
        "| [[second-concept]] | follow-up | reviewed sequence |\n", ""
    )
    entry["target_sha256"] = hashlib.sha256(entry["content"].encode()).hexdigest()
    plan["target_tree_sha256"] = document_tree_sha256(
        knowledge_root, {collection: entry["content"]}
    )
    plan_path = repo / "member-loss-reorder-plan.json"
    digest = _write_plan(plan_path, plan)
    with pytest.raises(PagePlanError, match="exact member set|delta"):
        apply_page_write_plan(
            plan_path,
            digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )


def test_collection_delta_preserves_raw_bytes_outside_members(tmp_path: Path):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    collection = _write_existing_page(
        knowledge_root,
        "collections/valid-collection.md",
        manifest,
        collection=True,
    )
    _write_existing_page(
        knowledge_root, "domains/software-engineering/valid-concept.md", manifest
    )
    _write_existing_page(
        knowledge_root, "domains/software-engineering/second-concept.md", manifest
    )
    original = collection.read_text(encoding="utf-8")
    plan = build_collection_add_member_plan(
        collection,
        "second-concept",
        before=None,
        after="valid-concept",
        order_by_id=False,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    entry = plan["write_set"][0]
    entry["content"] = entry["content"].rstrip("\n")
    entry["target_sha256"] = hashlib.sha256(entry["content"].encode()).hexdigest()
    plan["target_tree_sha256"] = document_tree_sha256(
        knowledge_root, {collection: entry["content"]}
    )
    plan_path = repo / "raw-byte-mutation-plan.json"
    digest = _write_plan(plan_path, plan)
    with pytest.raises(PagePlanError, match="Members|raw bytes|delta"):
        apply_page_write_plan(
            plan_path,
            digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )

    collection.write_text(entry["content"], encoding="utf-8")
    with pytest.raises(PagePlanError, match="member.*metadata|ordering|delta"):
        apply_page_write_plan(
            plan_path,
            digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )
    collection.write_text(original, encoding="utf-8")

    plan = build_collection_add_member_plan(
        collection,
        "second-concept",
        before=None,
        after="valid-concept",
        order_by_id=False,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    entry = plan["write_set"][0]
    entry["content"] = entry["content"].replace(
        "| [[second-concept]] |  |  |",
        "| [[second-concept]] | unauthorized | unauthorized |",
    )
    entry["target_sha256"] = hashlib.sha256(entry["content"].encode()).hexdigest()
    plan["target_tree_sha256"] = document_tree_sha256(
        knowledge_root, {collection: entry["content"]}
    )
    plan_path = repo / "unauthorized-member-metadata-plan.json"
    digest = _write_plan(plan_path, plan)
    with pytest.raises(PagePlanError, match="member.*metadata|delta"):
        apply_page_write_plan(
            plan_path,
            digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )


def test_collection_plan_preserves_crlf_base_bytes_outside_members(tmp_path: Path):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    collection = _write_existing_page(
        knowledge_root,
        "collections/valid-collection.md",
        manifest,
        collection=True,
    )
    _write_existing_page(
        knowledge_root, "domains/software-engineering/valid-concept.md", manifest
    )
    _write_existing_page(
        knowledge_root, "domains/software-engineering/second-concept.md", manifest
    )
    raw_base = collection.read_bytes().replace(b"\n", b"\r\n")
    collection.write_bytes(raw_base)
    plan = build_collection_add_member_plan(
        collection,
        "second-concept",
        before=None,
        after="valid-concept",
        order_by_id=False,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    entry = plan["write_set"][0]
    assert entry["base_content"].encode("utf-8") == raw_base
    plan_path = repo / "crlf-collection-plan.json"
    digest = _write_plan(plan_path, plan)
    assert apply_page_write_plan(
        plan_path,
        digest,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )


def test_apply_rechecks_tree_and_mode_after_candidate_validation(tmp_path: Path):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    semantic_path = repo / "semantic-plan.json"
    semantic_path.write_text(json.dumps(_semantic_plan(manifest)), encoding="utf-8")
    base_check = _candidate_check(repo, knowledge_root)
    plan = build_synthesize_plan(
        semantic_plan_path=semantic_path,
        source_paths=[manifest],
        page_id="page-command-contract",
        now=NOW,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    plan_path = repo / "race-plan.json"
    digest = _write_plan(plan_path, plan)
    mutated = False

    def racing_check(write_set: list[dict]) -> None:
        nonlocal mutated
        base_check(write_set)
        if not mutated:
            mutated = True
            _write_existing_page(knowledge_root, "staging/unrelated.md", manifest)

    with pytest.raises(PagePlanError, match="stale"):
        _apply_page_write_plan(
            plan_path,
            digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
            candidate_check=racing_check,
        )
    assert not (knowledge_root / plan["write_set"][0]["target_path"]).exists()

    source = knowledge_root / "staging/unrelated.md"
    target_dir = knowledge_root / "staging/nested"
    target_dir.mkdir()
    move = build_move_plan(
        source,
        target_dir,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    move_path = repo / "mode-plan.json"
    move_digest = _write_plan(move_path, move)
    source.chmod(0o600)
    with pytest.raises(PagePlanError, match="mode"):
        apply_page_write_plan(
            move_path,
            move_digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )
    assert source.exists()


def test_move_is_same_lifecycle_only_and_rejects_collision(tmp_path: Path):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    page = _write_existing_page(
        knowledge_root,
        "domains/software-engineering/valid-concept.md",
        manifest,
    )
    target_dir = knowledge_root / "domains" / "architecture"
    target_dir.mkdir(parents=True)
    plan = build_move_plan(
        page,
        target_dir,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    assert plan["write_set"][0]["source_path"].endswith("valid-concept.md")
    assert plan["write_set"][0]["target_path"].endswith("valid-concept.md")
    assert plan["write_set"][0]["content"] == page.read_text(encoding="utf-8")
    page.chmod(0o600)
    plan = build_move_plan(
        page,
        target_dir,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    plan_path = repo / "move-plan.json"
    digest = _write_plan(plan_path, plan)
    assert apply_page_write_plan(
        plan_path,
        digest,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    moved = target_dir / page.name
    assert stat.S_IMODE(moved.stat().st_mode) == 0o600
    assert (
        apply_page_write_plan(
            plan_path,
            digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )
        is False
    )

    with pytest.raises(PagePlanError, match="same lifecycle"):
        build_move_plan(
            page,
            knowledge_root / "archive",
            repo_root=repo,
            knowledge_root=knowledge_root,
        )

    collision = target_dir / page.name
    page.write_bytes(collision.read_bytes())
    with pytest.raises(PagePlanError, match="target"):
        build_move_plan(
            page,
            target_dir,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )


def test_apply_rolls_back_own_leaf_when_post_write_tree_differs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    semantic_path = repo / "semantic-plan.json"
    semantic_path.write_text(json.dumps(_semantic_plan(manifest)), encoding="utf-8")
    plan = build_synthesize_plan(
        semantic_plan_path=semantic_path,
        source_paths=[manifest],
        page_id="page-command-contract",
        now=NOW,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    plan_path = repo / "rollback-plan.json"
    digest = _write_plan(plan_path, plan)
    publish = page_documents.publish_bytes_no_replace

    def publish_then_mutate(path: Path, data: bytes) -> bool:
        changed = publish(path, data)
        _write_existing_page(knowledge_root, "staging/unrelated.md", manifest)
        return changed

    monkeypatch.setattr(page_documents, "publish_bytes_no_replace", publish_then_mutate)
    with pytest.raises(PagePlanError, match="rolled back"):
        apply_page_write_plan(
            plan_path,
            digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )
    assert not (knowledge_root / plan["write_set"][0]["target_path"]).exists()
    assert (knowledge_root / "staging/unrelated.md").is_file()


def test_apply_rolls_back_when_post_write_tree_digest_raises(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    semantic_path = repo / "semantic-plan.json"
    semantic_path.write_text(json.dumps(_semantic_plan(manifest)), encoding="utf-8")
    plan = build_synthesize_plan(
        semantic_plan_path=semantic_path,
        source_paths=[manifest],
        page_id="page-command-contract",
        now=NOW,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    plan_path = repo / "post-tree-error-plan.json"
    digest = _write_plan(plan_path, plan)
    target = knowledge_root / plan["write_set"][0]["target_path"]
    tree_digest = page_documents.document_tree_sha256

    def fail_after_commit(root: Path, overrides=None) -> str:
        if overrides is None and target.exists():
            raise OSError("injected post-tree digest failure")
        return tree_digest(root, overrides)

    monkeypatch.setattr(page_documents, "document_tree_sha256", fail_after_commit)
    with pytest.raises(PagePlanError, match="rolled back"):
        apply_page_write_plan(
            plan_path,
            digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )
    assert not target.exists()


def test_apply_reports_indeterminate_when_post_commit_leaf_cannot_be_observed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    semantic_path = repo / "semantic-plan.json"
    semantic_path.write_text(json.dumps(_semantic_plan(manifest)), encoding="utf-8")
    plan = build_synthesize_plan(
        semantic_plan_path=semantic_path,
        source_paths=[manifest],
        page_id="page-command-contract",
        now=NOW,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    plan_path = repo / "unobservable-leaf-plan.json"
    digest = _write_plan(plan_path, plan)
    target = knowledge_root / plan["write_set"][0]["target_path"]
    read_bytes = Path.read_bytes

    def fail_target_observation(path: Path) -> bytes:
        if path == target and target.exists():
            raise PermissionError("injected target observation failure")
        return read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", fail_target_observation)
    with pytest.raises(PagePlanError, match="indeterminate"):
        apply_page_write_plan(
            plan_path,
            digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )
    assert target.exists()


def test_move_post_tree_conflict_preserves_reappeared_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    source = _write_existing_page(
        knowledge_root,
        "domains/software-engineering/valid-concept.md",
        manifest,
    )
    target_dir = knowledge_root / "domains" / "architecture"
    target_dir.mkdir(parents=True)
    plan = build_move_plan(
        source,
        target_dir,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    plan_path = repo / "move-source-conflict-plan.json"
    digest = _write_plan(plan_path, plan)
    rename = page_documents.rename_path_no_replace

    def move_then_recreate(source_path: Path, target_path: Path) -> None:
        rename(source_path, target_path)
        source_path.write_bytes(b"external\n")

    monkeypatch.setattr(page_documents, "rename_path_no_replace", move_then_recreate)
    with pytest.raises(PagePlanError, match="indeterminate"):
        apply_page_write_plan(
            plan_path,
            digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )
    assert source.read_bytes() == b"external\n"
    assert (target_dir / source.name).is_file()


def test_apply_rejects_cross_lifecycle_move_from_confirmed_external_plan(
    tmp_path: Path,
):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    source = _write_existing_page(
        knowledge_root,
        "domains/software-engineering/valid-concept.md",
        manifest,
    )
    target_dir = knowledge_root / "domains" / "architecture"
    target_dir.mkdir(parents=True)
    plan = build_move_plan(
        source,
        target_dir,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    (knowledge_root / "archive").mkdir()
    entry = plan["write_set"][0]
    entry["target_path"] = "archive/valid-concept.md"
    plan["target_tree_sha256"] = document_tree_sha256(
        knowledge_root,
        {
            source: None,
            knowledge_root / entry["target_path"]: entry["content"],
        },
    )
    plan_path = repo / "cross-lifecycle-plan.json"
    digest = _write_plan(plan_path, plan)

    with pytest.raises(PagePlanError, match="same lifecycle|operation input"):
        apply_page_write_plan(
            plan_path,
            digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )
    assert source.is_file()
    assert not (knowledge_root / entry["target_path"]).exists()


def test_apply_rejects_move_content_mutation_before_filesystem_write(tmp_path: Path):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    source = _write_existing_page(
        knowledge_root,
        "domains/software-engineering/valid-concept.md",
        manifest,
    )
    target_dir = knowledge_root / "domains" / "architecture"
    target_dir.mkdir(parents=True)
    plan = build_move_plan(
        source,
        target_dir,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    entry = plan["write_set"][0]
    entry["content"] = entry["content"].replace(
        "Deterministic parser contract fixture.",
        "Mutated move content.",
    )
    entry["target_sha256"] = hashlib.sha256(
        entry["content"].encode("utf-8")
    ).hexdigest()
    plan["target_tree_sha256"] = document_tree_sha256(
        knowledge_root,
        {source: None, target_dir / source.name: entry["content"]},
    )
    plan_path = repo / "mutated-move-plan.json"
    digest = _write_plan(plan_path, plan)

    with pytest.raises(PagePlanError, match="preserve source bytes"):
        apply_page_write_plan(
            plan_path,
            digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )
    assert source.is_file()
    assert not (target_dir / source.name).exists()


def test_move_replay_rejects_mode_not_preserved_from_base(tmp_path: Path):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    source = _write_existing_page(
        knowledge_root,
        "domains/software-engineering/valid-concept.md",
        manifest,
    )
    source.chmod(0o600)
    target_dir = knowledge_root / "domains" / "architecture"
    target_dir.mkdir(parents=True)
    plan = build_move_plan(
        source,
        target_dir,
        repo_root=repo,
        knowledge_root=knowledge_root,
    )
    plan["write_set"][0]["target_mode"] = 0o644
    plan_path = repo / "forged-mode-replay.json"
    digest = _write_plan(plan_path, plan)
    target = target_dir / source.name
    os.rename(source, target)
    target.chmod(0o644)
    with pytest.raises(PagePlanError, match="preserve.*mode|mode.*preserve"):
        apply_page_write_plan(
            plan_path,
            digest,
            repo_root=repo,
            knowledge_root=knowledge_root,
        )


def test_document_tree_digest_ignores_generated_files_and_changes_for_page_overlay(
    tmp_path: Path,
):
    _, knowledge_root, _ = _setup_repo(tmp_path)
    empty = document_tree_sha256(knowledge_root)
    (knowledge_root / "index.md").write_text("generated\n", encoding="utf-8")
    assert document_tree_sha256(knowledge_root) == empty
    target = knowledge_root / "staging/page.md"
    candidate = document_tree_sha256(knowledge_root, {target: "page\n"})
    assert candidate != empty
    assert document_tree_sha256(knowledge_root, {target: "page\n"}) == candidate


@pytest.mark.parametrize("kind", ["symlink", "broken-symlink", "fifo"])
def test_document_tree_rejects_non_regular_markdown_entries(tmp_path: Path, kind: str):
    _, knowledge_root, _ = _setup_repo(tmp_path)
    target = knowledge_root / "staging" / "unsafe.md"
    if kind == "symlink":
        source = knowledge_root / "staging" / "source.md"
        source.write_text("source\n", encoding="utf-8")
        target.symlink_to(source)
    elif kind == "broken-symlink":
        target.symlink_to(knowledge_root / "missing.md")
    else:
        os.mkfifo(target)

    with pytest.raises(KnowledgeSchemaError, match="regular|symlink"):
        document_tree_sha256(knowledge_root)
    result = check_target(knowledge_root, repo_root=knowledge_root.parent, mode="all")
    assert result.structural_verdict == "FAIL"
    assert any("regular" in finding["message"] for finding in result.findings)


def test_document_tree_rejects_symlinked_knowledge_root(tmp_path: Path):
    _, knowledge_root, _ = _setup_repo(tmp_path)
    alias = tmp_path / "wiki-alias"
    alias.symlink_to(knowledge_root, target_is_directory=True)
    with pytest.raises(KnowledgeSchemaError, match="root.*directory|symlink"):
        document_tree_sha256(alias)


def test_cli_synthesize_plan_then_apply_uses_confirmed_plan_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repo, knowledge_root, manifest = _setup_repo(tmp_path)
    semantic_path = repo / "semantic-plan.json"
    semantic_path.write_text(json.dumps(_semantic_plan(manifest)), encoding="utf-8")
    output = repo / "page-plan.json"
    monkeypatch.setattr(wiki_ingest, "REPO_ROOT", repo)

    assert (
        wiki_ingest.main(
            [
                "synthesize",
                "--semantic-plan",
                str(semantic_path),
                "--source",
                manifest,
                "--page-id",
                "page-command-contract",
                "--now",
                NOW,
                "--output",
                str(output),
            ]
        )
        == 0
    )
    assert output.is_file()
    target = knowledge_root / "staging/software-engineering/page-command-contract.md"
    assert not target.exists()

    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    assert (
        wiki_ingest.main(
            [
                "synthesize",
                "--apply-plan",
                str(output),
                "--confirm-plan-sha256",
                digest,
            ]
        )
        == 0
    )
    assert target.is_file()


def test_cli_exposes_every_p2_t5_command_surface():
    parser = wiki_ingest._parser()
    command_action = next(
        action
        for action in parser._actions
        if getattr(action, "choices", None) is not None
    )
    assert {
        "synthesize",
        "promote",
        "collection",
        "move",
    }.issubset(command_action.choices)


def test_cli_rejects_plan_applied_through_wrong_command(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repo, _, manifest = _setup_repo(tmp_path)
    semantic_path = repo / "semantic-plan.json"
    semantic_path.write_text(json.dumps(_semantic_plan(manifest)), encoding="utf-8")
    monkeypatch.setattr(wiki_ingest, "REPO_ROOT", repo)
    output = repo / "page-plan.json"
    assert (
        wiki_ingest.main(
            [
                "synthesize",
                "--semantic-plan",
                str(semantic_path),
                "--source",
                manifest,
                "--page-id",
                "page-command-contract",
                "--now",
                NOW,
                "--output",
                str(output),
            ]
        )
        == 0
    )
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    assert (
        wiki_ingest.main(
            [
                "move",
                "--apply-plan",
                str(output),
                "--confirm-plan-sha256",
                digest,
            ]
        )
        == 1
    )
