#!/usr/bin/env python3
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from knowledge.schema import (  # noqa: E402
    CANONICAL_ROOT_EXCLUSIONS,
    SCHEMA_PATH,
    KnowledgeSchemaError,
    domain_registry,
    parse_markdown,
    schema_digest,
    table_contract,
    validator_for,
)

FIXTURES = ROOT / "tests" / "fixtures" / "knowledge"
REQUIREMENT_ID_PATTERN = r"(?:FR|NFR)-KP-\d{3}"
REQUIREMENT_MANIFEST_KEYS = {"schema_version", "requirements"}
REQUIREMENT_ENTRY_KEYS = {"id", "steps", "surfaces", "verification"}
PRD_REQUIREMENT_TABLES = (
    (
        "| ID | 요구사항 | 관찰 가능한 수용 기준 |\n|---|---|---|\n",
        r"FR-KP-\d{3}",
    ),
    ("| ID | 요구사항 | 기준 |\n|---|---|---|\n", r"NFR-KP-\d{3}"),
)
TRACEABILITY_HEADER = (
    "| PRD ID | Architecture surface | Logic surface |\n"
    "|---|---|---|\n"
)


def _requirement_traceability_errors(
    manifest: dict, prd: str, architecture: str
) -> list[str]:
    errors = []
    prd_id_list = []
    for header, id_pattern in PRD_REQUIREMENT_TABLES:
        if prd.count(header) != 1:
            errors.append("PRD requirement table header differs from the exact contract")
            continue
        table = prd.split(header, 1)[1].split("\n\n", 1)[0]
        for row in table.splitlines():
            cells = row.split("|")
            if len(cells) > 1 and re.fullmatch(REQUIREMENT_ID_PATTERN, cells[1].strip()):
                prd_id_list.append(cells[1].strip())
            if not re.fullmatch(rf"\| {id_pattern} \| [^|]+ \| [^|]+ \|", row):
                errors.append("PRD requirement row differs from the exact contract")
            semantic_cells = cells[1:-1]
            if len(semantic_cells) == 3 and any(
                not cell.strip() for cell in semantic_cells[1:]
            ):
                errors.append("PRD requirement semantic cells must be non-empty")
    prd_ids = set(prd_id_list)
    entries = manifest.get("requirements", [])
    manifest_ids = [entry.get("id") for entry in entries]

    if set(manifest) != REQUIREMENT_MANIFEST_KEYS:
        errors.append("manifest top-level keys differ from the exact contract")
    if len(prd_id_list) != len(prd_ids):
        errors.append("PRD requirement IDs are duplicated")
    if any(set(entry) != REQUIREMENT_ENTRY_KEYS for entry in entries):
        errors.append("manifest requirement entry keys differ from the exact contract")
    if len(manifest_ids) != len(set(manifest_ids)) or set(manifest_ids) != prd_ids:
        errors.append("manifest requirement IDs differ from PRD IDs")

    if architecture.count(TRACEABILITY_HEADER) != 1:
        errors.append("architecture traceability table header differs from the exact contract")
        return errors
    table = architecture.split(TRACEABILITY_HEADER, 1)[1].split("\n\n", 1)[0]
    architecture_rows = table.splitlines()
    architecture_id_list = []
    for row in architecture_rows:
        cells = row.split("|")
        if len(cells) > 1 and re.fullmatch(REQUIREMENT_ID_PATTERN, cells[1].strip()):
            architecture_id_list.append(cells[1].strip())
        mapping_cells = cells[1:-1]
        if len(mapping_cells) == 3 and any(
            not cell.strip() for cell in mapping_cells[1:]
        ):
            errors.append("architecture mapping cells must be non-empty")
    architecture_ids = set(architecture_id_list)
    if len(architecture_id_list) != len(architecture_ids):
        errors.append("architecture requirement IDs are duplicated")
    if any(
        not re.fullmatch(
            rf"\| {REQUIREMENT_ID_PATTERN} \| [^|]+ \| [^|]+ \|", row
        )
        for row in architecture_rows
    ):
        errors.append("architecture requirement row differs from the exact contract")
    if architecture_ids != prd_ids:
        errors.append("architecture requirement IDs differ from PRD IDs")
    return errors


def test_schema_metadata_contract_has_one_validated_owner():
    registry = domain_registry(ROOT)
    assert list(registry) == list(sorted(registry))
    assert registry["software-engineering"]["status"] == "active"
    assert schema_digest(ROOT) == hashlib.sha256(SCHEMA_PATH.read_bytes()).hexdigest()
    assert CANONICAL_ROOT_EXCLUSIONS == {"index.md", "overview.md", "log.md"}
    assert table_contract("Claims") == [
        "id",
        "primary",
        "claim",
        "status",
        "evidence",
        "notes",
    ]
    assert table_contract("Relations") == ["type", "target", "notes"]
    assert table_contract("Members") == ["member", "role", "rationale"]


def test_domain_registry_rejects_duplicate_and_non_string_keys(tmp_path: Path):
    meta = tmp_path / "_meta"
    meta.mkdir()
    invalid_documents = (
        "version: 1\ndomains:\n  alpha:\n    status: active\n    label: A\n"
        "    source_roots: []\n  alpha:\n    status: inactive\n    label: B\n"
        "    source_roots: []\n",
        "version: 1\ndomains:\n  1:\n    status: active\n    label: A\n"
        "    source_roots: []\n  alpha:\n    status: active\n    label: B\n"
        "    source_roots: []\n",
    )
    for document in invalid_documents:
        (meta / "domains.yaml").write_text(document, encoding="utf-8")
        try:
            domain_registry(tmp_path)
        except KnowledgeSchemaError:
            pass
        else:
            raise AssertionError("invalid domain registry accepted")


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
        "source_paths": ["raw/sources/video/source-id/" + digest + "/manifest.json"],
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
    architecture = (ROOT / "docs" / "wiki-ingest-architecture.md").read_text(
        encoding="utf-8"
    )
    assert _requirement_traceability_errors(manifest, prd, architecture) == []
    assert len(ids) == len(set(ids)) == 37
    assert set(ids) == declared
    for entry in entries:
        assert entry["steps"] and entry["surfaces"] and entry["verification"]
        if min(entry["steps"]) <= 6:
            assert any(
                (ROOT / path).exists()
                for path in entry["surfaces"] + entry["verification"]
            )


def test_requirement_traceability_rejects_architecture_id_omission():
    manifest = json.loads(
        (ROOT / "_meta" / "knowledge-requirements.json").read_text(encoding="utf-8")
    )
    prd = (ROOT / "docs" / "wiki-ingest-prd.md").read_text(encoding="utf-8")
    architecture = (ROOT / "docs" / "wiki-ingest-architecture.md").read_text(
        encoding="utf-8"
    )
    mutated = architecture.replace(
        "| FR-KP-001 | §3, §4, §8 | BR-ART-007 |\n",
        "",
    )

    assert "architecture requirement IDs differ from PRD IDs" in (
        _requirement_traceability_errors(manifest, prd, mutated)
    )


def test_requirement_traceability_rejects_manifest_mapping_key():
    manifest = json.loads(
        (ROOT / "_meta" / "knowledge-requirements.json").read_text(encoding="utf-8")
    )
    mutated = copy.deepcopy(manifest)
    mutated["requirements"][0]["architecture"] = ["§4"]
    prd = (ROOT / "docs" / "wiki-ingest-prd.md").read_text(encoding="utf-8")
    architecture = (ROOT / "docs" / "wiki-ingest-architecture.md").read_text(
        encoding="utf-8"
    )

    assert "manifest requirement entry keys differ from the exact contract" in (
        _requirement_traceability_errors(mutated, prd, architecture)
    )


def test_requirement_traceability_rejects_prd_duplicate_id():
    manifest = json.loads(
        (ROOT / "_meta" / "knowledge-requirements.json").read_text(encoding="utf-8")
    )
    prd = (ROOT / "docs" / "wiki-ingest-prd.md").read_text(encoding="utf-8")
    architecture = (ROOT / "docs" / "wiki-ingest-architecture.md").read_text(
        encoding="utf-8"
    )
    duplicate = (
        "| FR-KP-001 | extractor는 provider-agnostic canonical payload를 출력한다 | "
        "payload가 versioned contract를 만족하고 cs-study 식별자·경로가 0건이며 "
        "exact payload path를 CLI 결과로 반환한다 |"
    )
    mutated = prd.replace(duplicate, f"{duplicate}\n{duplicate}", 1)

    assert "PRD requirement IDs are duplicated" in (
        _requirement_traceability_errors(manifest, mutated, architecture)
    )


def test_requirement_traceability_rejects_architecture_duplicate_id():
    manifest = json.loads(
        (ROOT / "_meta" / "knowledge-requirements.json").read_text(encoding="utf-8")
    )
    prd = (ROOT / "docs" / "wiki-ingest-prd.md").read_text(encoding="utf-8")
    architecture = (ROOT / "docs" / "wiki-ingest-architecture.md").read_text(
        encoding="utf-8"
    )
    duplicate = "| FR-KP-001 | §3, §4, §8 | BR-ART-007 |"
    mutated = architecture.replace(duplicate, f"{duplicate}\n{duplicate}", 1)

    assert "architecture requirement IDs are duplicated" in (
        _requirement_traceability_errors(manifest, prd, mutated)
    )


def test_requirement_traceability_rejects_malformed_architecture_duplicate():
    manifest = json.loads(
        (ROOT / "_meta" / "knowledge-requirements.json").read_text(encoding="utf-8")
    )
    prd = (ROOT / "docs" / "wiki-ingest-prd.md").read_text(encoding="utf-8")
    architecture = (ROOT / "docs" / "wiki-ingest-architecture.md").read_text(
        encoding="utf-8"
    )
    canonical = "| FR-KP-001 | §3, §4, §8 | BR-ART-007 |"
    malformed = "| FR-KP-001 | §3 | BR-ART-007 | unexpected |"
    mutated = architecture.replace(canonical, f"{canonical}\n{malformed}", 1)

    errors = _requirement_traceability_errors(manifest, prd, mutated)
    assert "architecture requirement IDs are duplicated" in errors
    assert "architecture requirement row differs from the exact contract" in errors


def test_requirement_traceability_rejects_whitespace_malformed_architecture_row():
    manifest = json.loads(
        (ROOT / "_meta" / "knowledge-requirements.json").read_text(encoding="utf-8")
    )
    prd = (ROOT / "docs" / "wiki-ingest-prd.md").read_text(encoding="utf-8")
    architecture = (ROOT / "docs" / "wiki-ingest-architecture.md").read_text(
        encoding="utf-8"
    )
    canonical = "| FR-KP-001 | §3, §4, §8 | BR-ART-007 |"
    malformed = "|FR-KP-001| §3 | BR-ART-007 |"
    mutated = architecture.replace(canonical, f"{canonical}\n{malformed}", 1)

    assert "architecture requirement row differs from the exact contract" in (
        _requirement_traceability_errors(manifest, prd, mutated)
    )


def test_requirement_traceability_rejects_manifest_top_level_mapping():
    manifest = json.loads(
        (ROOT / "_meta" / "knowledge-requirements.json").read_text(encoding="utf-8")
    )
    mutated = copy.deepcopy(manifest)
    mutated["architecture"] = {"FR-KP-001": ["§3"]}
    prd = (ROOT / "docs" / "wiki-ingest-prd.md").read_text(encoding="utf-8")
    architecture = (ROOT / "docs" / "wiki-ingest-architecture.md").read_text(
        encoding="utf-8"
    )

    assert "manifest top-level keys differ from the exact contract" in (
        _requirement_traceability_errors(mutated, prd, architecture)
    )


def test_requirement_traceability_rejects_whitespace_malformed_prd_row():
    manifest = json.loads(
        (ROOT / "_meta" / "knowledge-requirements.json").read_text(encoding="utf-8")
    )
    prd = (ROOT / "docs" / "wiki-ingest-prd.md").read_text(encoding="utf-8")
    architecture = (ROOT / "docs" / "wiki-ingest-architecture.md").read_text(
        encoding="utf-8"
    )
    canonical = (
        "| FR-KP-001 | extractor는 provider-agnostic canonical payload를 출력한다 | "
        "payload가 versioned contract를 만족하고 cs-study 식별자·경로가 0건이며 "
        "exact payload path를 CLI 결과로 반환한다 |"
    )
    malformed = "|FR-KP-001| duplicate | duplicate |"
    mutated = prd.replace(canonical, f"{canonical}\n{malformed}", 1)

    assert "PRD requirement row differs from the exact contract" in (
        _requirement_traceability_errors(manifest, mutated, architecture)
    )


def test_requirement_traceability_rejects_blank_prd_semantic_cells():
    manifest = json.loads(
        (ROOT / "_meta" / "knowledge-requirements.json").read_text(encoding="utf-8")
    )
    prd = (ROOT / "docs" / "wiki-ingest-prd.md").read_text(encoding="utf-8")
    architecture = (ROOT / "docs" / "wiki-ingest-architecture.md").read_text(
        encoding="utf-8"
    )
    canonical = (
        "| FR-KP-001 | extractor는 provider-agnostic canonical payload를 출력한다 | "
        "payload가 versioned contract를 만족하고 cs-study 식별자·경로가 0건이며 "
        "exact payload path를 CLI 결과로 반환한다 |"
    )
    mutations = (
        "| FR-KP-001 |   | payload contract |",
        "| FR-KP-001 | extractor contract |   |",
    )

    for replacement in mutations:
        mutated = prd.replace(canonical, replacement, 1)
        assert "PRD requirement semantic cells must be non-empty" in (
            _requirement_traceability_errors(manifest, mutated, architecture)
        )


def test_requirement_traceability_rejects_blank_architecture_mapping_cells():
    manifest = json.loads(
        (ROOT / "_meta" / "knowledge-requirements.json").read_text(encoding="utf-8")
    )
    prd = (ROOT / "docs" / "wiki-ingest-prd.md").read_text(encoding="utf-8")
    architecture = (ROOT / "docs" / "wiki-ingest-architecture.md").read_text(
        encoding="utf-8"
    )
    canonical = "| FR-KP-001 | §3, §4, §8 | BR-ART-007 |"
    mutations = (
        "| FR-KP-001 |   | BR-ART-007 |",
        "| FR-KP-001 | §3 |   |",
    )

    for replacement in mutations:
        mutated = architecture.replace(canonical, replacement, 1)
        assert "architecture mapping cells must be non-empty" in (
            _requirement_traceability_errors(manifest, prd, mutated)
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
