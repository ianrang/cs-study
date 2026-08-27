#!/usr/bin/env python3
import copy
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from knowledge.schema import (  # noqa: E402
    SCHEMA_PATH,
    KnowledgeSchemaError,
    parse_markdown,
    validator_for,
)

FIXTURES = ROOT / "tests" / "fixtures" / "knowledge"


def test_parser_produces_deterministic_document_instance():
    path = FIXTURES / "valid-concept.md"
    first = parse_markdown(path)
    second = parse_markdown(path)
    assert first == second
    assert first["id"] == "valid-concept"
    assert first["claims"][0]["primary"] is True
    assert first["relations"][0]["target"] == "fixture-parent"


def test_collection_member_row_order_is_preserved():
    instance = parse_markdown(FIXTURES / "valid-collection.md")
    assert instance["members"] == [
        {
            "target": "valid-concept",
            "role": "foundation",
            "rationale": "reviewed sequence",
        }
    ]


def test_section_order_mutation_is_rejected():
    path = FIXTURES / "valid-concept.md"
    text = path.read_text(encoding="utf-8")
    mutated = (
        text.replace("## Mechanism", "## TEMP", 1)
        .replace("## Variants", "## Mechanism", 1)
        .replace("## TEMP", "## Variants", 1)
    )
    try:
        parse_markdown(path, mutated)
    except KnowledgeSchemaError as exc:
        assert "ordered_sections" in str(exc)
    else:
        raise AssertionError("section order mutation accepted")


def test_unknown_frontmatter_property_is_rejected():
    path = FIXTURES / "valid-concept.md"
    text = path.read_text(encoding="utf-8").replace(
        "title: Contract Fixture Concept",
        "title: Contract Fixture Concept\nstatus: active",
    )
    try:
        parse_markdown(path, text)
    except KnowledgeSchemaError as exc:
        assert "Additional properties" in str(exc)
    else:
        raise AssertionError("unknown property accepted")


def test_duplicate_yaml_property_is_rejected():
    path = FIXTURES / "valid-concept.md"
    text = path.read_text(encoding="utf-8").replace(
        "title: Contract Fixture Concept",
        "title: Contract Fixture Concept\ntitle: duplicate",
    )
    try:
        parse_markdown(path, text)
    except KnowledgeSchemaError as exc:
        assert "duplicate YAML property" in str(exc)
    else:
        raise AssertionError("duplicate YAML property accepted")


def test_semantic_plan_rejects_write_authority_fields():
    plan = {
        "title": "Draft",
        "page_type": "concept",
        "domain": "software-engineering",
        "tags": ["architecture"],
        "source_paths": ["raw/sources/video/a/d/manifest.json"],
        "summary": "Draft summary",
        "sections": [],
        "claims": [],
        "relations": [],
        "members": [],
        "path": "wiki/domains/software-engineering/draft.md",
    }
    errors = list(validator_for("SemanticPlan").iter_errors(plan))
    assert any(error.validator == "additionalProperties" for error in errors)


def test_semantic_plan_reuses_manifest_path_contract():
    plan = {
        "title": "Draft",
        "page_type": "concept",
        "domain": "software-engineering",
        "tags": ["architecture"],
        "source_paths": ["raw/sources/video/a/d/manifest.json"],
        "summary": "Draft summary",
        "sections": [],
        "claims": [],
        "relations": [],
        "members": [],
    }
    errors = list(validator_for("SemanticPlan").iter_errors(plan))
    assert any(list(error.path) == ["source_paths", 0] for error in errors)


def test_page_write_plan_is_strict_and_allows_at_most_one_page():
    digest = "a" * 64
    entry = {
        "action": "create",
        "source_path": None,
        "target_path": "staging/software-engineering/page-id.md",
        "base_sha256": None,
        "target_sha256": digest,
        "base_mode": None,
        "target_mode": 420,
        "base_content": None,
        "content": "# page\n",
    }
    plan = {
        "schema_version": "1.0",
        "operation": "synthesize",
        "knowledge_root": "wiki",
        "schema_sha256": digest,
        "base_tree_sha256": digest,
        "target_tree_sha256": digest,
        "input_sha256": digest,
        "generator": {"name": "cs-study", "version": "1.0"},
        "requires_review_approval": False,
        "review_verdicts": [],
        "operation_input": {
            "semantic_plan_sha256": digest,
            "source_paths": ["raw/sources/video/source/" + digest + "/manifest.json"],
            "page_id": "page-id",
            "now": "2026-08-26",
        },
        "write_set": [entry, entry],
    }
    errors = list(validator_for("PageWritePlan").iter_errors(plan))
    assert any(
        list(error.path) == ["write_set"] and error.validator == "maxItems"
        for error in errors
    )

    plan["write_set"] = [entry]
    plan["unexpected"] = True
    errors = list(validator_for("PageWritePlan").iter_errors(plan))
    assert any(error.validator == "additionalProperties" for error in errors)


def test_page_write_plan_rejects_invalid_mode_and_review_verdict_shape():
    digest = "a" * 64
    plan = {
        "schema_version": "1.0",
        "operation": "promote",
        "knowledge_root": "wiki",
        "schema_sha256": digest,
        "base_tree_sha256": digest,
        "target_tree_sha256": digest,
        "input_sha256": digest,
        "generator": {"name": "cs-study", "version": "1.0"},
        "requires_review_approval": True,
        "review_verdicts": [{"claim_id": "C1", "verdict": "support"}],
        "operation_input": {
            "source_path": "staging/software-engineering/page-id.md",
            "target_path": "domains/software-engineering/page-id.md",
            "review_verdicts_sha256": digest,
        },
        "write_set": [
            {
                "action": "move",
                "source_path": "staging/software-engineering/page-id.md",
                "target_path": "domains/software-engineering/page-id.md",
                "base_sha256": digest,
                "target_sha256": digest,
                "base_mode": 420,
                "target_mode": 8192,
                "base_content": None,
                "content": "# page\n",
            }
        ],
    }
    errors = list(validator_for("PageWritePlan").iter_errors(plan))
    assert any(list(error.path)[-1:] == ["target_mode"] for error in errors)

    plan["write_set"][0]["target_mode"] = 420
    plan["review_verdicts"][0]["unexpected"] = True
    errors = list(validator_for("PageWritePlan").iter_errors(plan))
    assert any(error.validator == "additionalProperties" for error in errors)

    plan["review_verdicts"][0].pop("unexpected")
    plan["operation"] = "move"
    plan["requires_review_approval"] = False
    plan["review_verdicts"] = []
    errors = list(validator_for("PageWritePlan").iter_errors(plan))
    assert errors, "move accepted promote-only operation_input and review verdicts"


def test_page_write_plan_rejects_ambiguous_collection_add_ordering_policy():
    digest = "a" * 64
    plan = {
        "schema_version": "1.0",
        "operation": "collection-add-member",
        "knowledge_root": "wiki",
        "schema_sha256": digest,
        "base_tree_sha256": digest,
        "target_tree_sha256": digest,
        "input_sha256": digest,
        "generator": {"name": "cs-study", "version": "1.0"},
        "requires_review_approval": False,
        "review_verdicts": [],
        "operation_input": {
            "collection_path": "collections/sequence.md",
            "member": "new-member",
            "before": "existing-member",
            "after": "existing-member",
            "order_by_id": True,
        },
        "write_set": [],
    }
    errors = list(validator_for("PageWritePlan").iter_errors(plan))
    assert errors, "ambiguous collection ordering policy was accepted"

    plan["operation"] = "collection-reorder"
    plan["operation_input"] = {
        "collection_path": "collections/sequence.md",
        "members": ["new-member"],
    }
    plan["write_set"] = [
        {
            "action": "replace",
            "source_path": "collections/sequence.md",
            "target_path": "collections/sequence.md",
            "base_sha256": digest,
            "target_sha256": digest,
            "base_mode": None,
            "target_mode": 420,
            "base_content": "# sequence\n",
            "content": "# sequence\n",
        }
    ]
    errors = list(validator_for("PageWritePlan").iter_errors(plan))
    assert errors, "replace accepted a null base_mode"

    plan["operation"] = "synthesize"
    plan["operation_input"] = {
        "semantic_plan_sha256": digest,
        "source_paths": [
            "raw/sources/video/source-id/" + digest + "/manifest.json"
        ],
        "page_id": "page-id",
        "now": "2026-08-26",
    }
    plan["write_set"] = []
    errors = list(validator_for("PageWritePlan").iter_errors(plan))
    assert errors, "synthesize accepted an empty write_set"


def test_empty_source_paths_are_rejected_for_document_and_semantic_plan():
    collection = FIXTURES / "valid-collection.md"
    text = collection.read_text(encoding="utf-8").replace(
        "source_paths:\n"
        "  - raw/sources/clipping/fixture-collection/" + "b" * 64 + "/manifest.json",
        "source_paths: []",
    )
    try:
        parse_markdown(collection, text)
    except KnowledgeSchemaError as exc:
        assert "should be non-empty" in str(exc)
    else:
        raise AssertionError("empty DocumentInstance source_paths accepted")

    plan = {
        "title": "Draft",
        "page_type": "concept",
        "domain": "software-engineering",
        "tags": ["architecture"],
        "source_paths": [],
        "summary": "Draft summary",
        "sections": [],
        "claims": [],
        "relations": [],
        "members": [],
    }
    errors = list(validator_for("SemanticPlan").iter_errors(plan))
    assert any(
        list(error.path) == ["source_paths"] and error.validator == "minItems"
        for error in errors
    )


def test_incompatible_schema_mutation_rejects_unchanged_fixture():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    instance = parse_markdown(FIXTURES / "valid-concept.md")
    mutated = copy.deepcopy(schema)
    mutated["$defs"]["Properties"]["required"].append("new_required_field")
    selected = {
        "$schema": mutated["$schema"],
        "$ref": "#/$defs/DocumentInstance",
        "$defs": mutated["$defs"],
    }
    from jsonschema import Draft202012Validator

    assert list(Draft202012Validator(selected).iter_errors(instance))


def test_requirement_manifest_exactly_covers_prd_ids():
    manifest = json.loads(
        (ROOT / "_meta" / "knowledge-requirements.json").read_text(encoding="utf-8")
    )
    entries = manifest["requirements"]
    ids = [entry["id"] for entry in entries]
    prd = (ROOT / "docs" / "wiki-ingest-prd.md").read_text(encoding="utf-8")
    declared = set(re.findall(r"^\| ((?:FR|NFR)-KP-\d{3}) \|", prd, re.MULTILINE))
    assert len(ids) == len(set(ids)) == 37
    assert set(ids) == declared
    for entry in entries:
        assert entry["steps"] and entry["surfaces"] and entry["verification"]
        if min(entry["steps"]) <= 6:
            assert any(
                (ROOT / path).exists()
                for path in entry["surfaces"] + entry["verification"]
            )


def test_migration_preservation_requirement_has_exact_owners():
    manifest = json.loads(
        (ROOT / "_meta" / "knowledge-requirements.json").read_text(encoding="utf-8")
    )
    entry = next(
        item for item in manifest["requirements"] if item["id"] == "NFR-KP-015"
    )
    assert entry == {
        "id": "NFR-KP-015",
        "steps": [6, 9],
        "surfaces": [
            "_meta/knowledge-migration-plan.schema.json",
            "_meta/knowledge-migration-resolution.schema.json",
            "scripts/wiki_ingest.py",
            "scripts/knowledge/migration.py",
            "scripts/knowledge/fs.py",
        ],
        "verification": ["tests/test_migration_plan.py"],
    }


def main() -> int:
    tests = [
        value for name, value in sorted(globals().items()) if name.startswith("test_")
    ]
    failed = 0
    for test in tests:
        try:
            test()
            print(f"PASS {test.__name__}")
        except Exception as exc:
            failed += 1
            print(f"FAIL {test.__name__}: {exc}")
    print(f"\n--- {len(tests) - failed} passed, {failed} failed / {len(tests)} ---")
    return int(bool(failed))


if __name__ == "__main__":
    sys.exit(main())
