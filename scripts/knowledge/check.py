from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import stat
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

from .fs import confined
from .graph import inspect_graph
from .schema import (
    REPO_ROOT,
    WIKILINK_RE,
    KnowledgeSchemaError,
    active_domain_for_path,
    canonical_document_paths,
    contract_format_checker,
    is_canonical_document_path,
    lifecycle_roots,
    load_taxonomy,
    markdown_fence_mask,
    parse_markdown,
    validate_instance,
    validator_for,
)

EXCLUDED_PARTS = {".git", ".venv", "venv", "__pycache__", "node_modules"}
RULE_REGISTRY = {
    "VR-KP-001": ("active", "contract-check"),
    "VR-KP-002": ("active", "artifact-evidence-check"),
    "VR-KP-003": ("active", "artifact-path-check"),
    "VR-KP-004": ("active", "schema-check"),
    "VR-KP-005": ("active", "schema-check"),
    "VR-KP-006": ("active", "schema-check"),
    "VR-KP-007": ("active", "graph-check"),
    "VR-KP-008": ("active", "graph-check"),
    "VR-KP-009": ("active", "artifact-evidence-check"),
    "VR-KP-010": ("active", "claim-check"),
    "VR-KP-011": ("active", "graph-check"),
    "VR-KP-012": ("active", "graph-check"),
    "VR-KP-013": ("active", "graph-check"),
    "VR-KP-014": ("active", "lifecycle-check"),
    "VR-KP-015": ("active", "page-command-contract"),
    "VR-KP-016": ("active", "page-command-contract"),
    "VR-KP-017": ("active", "cli-generated-parity"),
    "VR-KP-018": ("active", "cli-index-coverage"),
    "VR-KP-019": ("active", "architecture-check"),
    "VR-KP-020": ("active", "rule-coverage-check"),
    "VR-KP-021": ("active", "artifact-replay-check"),
    "VR-KP-022": ("active", "page-command-contract"),
    "VR-KP-023": ("active", "taxonomy-check"),
}
ARCHITECTURE_MODULE_PATHS = {
    "wiki_ingest": Path("scripts/wiki_ingest.py"),
    "knowledge.artifacts": Path("scripts/knowledge/artifacts.py"),
    "knowledge.check": Path("scripts/knowledge/check.py"),
    "knowledge.documents": Path("scripts/knowledge/documents.py"),
    "knowledge.fs": Path("scripts/knowledge/fs.py"),
    "knowledge.graph": Path("scripts/knowledge/graph.py"),
    "knowledge.materialize": Path("scripts/knowledge/materialize.py"),
    "knowledge.schema": Path("scripts/knowledge/schema.py"),
    "contracts.privacy": Path("scripts/contracts/privacy.py"),
    "contracts.timestamps": Path("scripts/contracts/timestamps.py"),
}
ARCHITECTURE_EXPECTED_EDGES = {
    ("wiki_ingest", "knowledge.artifacts"),
    ("wiki_ingest", "knowledge.check"),
    ("wiki_ingest", "knowledge.documents"),
    ("wiki_ingest", "knowledge.fs"),
    ("wiki_ingest", "knowledge.materialize"),
    ("knowledge.artifacts", "contracts.privacy"),
    ("knowledge.artifacts", "knowledge.fs"),
    ("knowledge.artifacts", "knowledge.schema"),
    ("knowledge.check", "knowledge.fs"),
    ("knowledge.check", "knowledge.graph"),
    ("knowledge.check", "knowledge.schema"),
    ("knowledge.documents", "knowledge.fs"),
    ("knowledge.documents", "knowledge.schema"),
    ("knowledge.materialize", "knowledge.fs"),
    ("knowledge.materialize", "knowledge.schema"),
    ("knowledge.schema", "contracts.timestamps"),
}
ARCHITECTURE_MAX_EDGE_DEPTH = 3
ARCHITECTURE_INITIALIZER_PATHS = (
    Path("scripts/knowledge/__init__.py"),
    Path("scripts/contracts/__init__.py"),
)


@dataclass(frozen=True)
class CheckResult:
    structural_verdict: str
    semantic_review: str
    mode: str
    exclusions: tuple[str, ...]
    findings: tuple[dict, ...]

    def to_dict(self) -> dict:
        return {
            "structural_verdict": self.structural_verdict,
            "semantic_review": self.semantic_review,
            "mode": self.mode,
            "exclusions": list(self.exclusions),
            "findings": list(self.findings),
        }


def _finding(
    rule_id: str,
    path: Path,
    subject: str,
    message: str,
    remediation: str,
    *,
    severity: str = "HIGH",
) -> dict:
    return {
        "rule_id": rule_id,
        "severity": severity,
        "path": str(path),
        "line": 1,
        "subject_id": subject,
        "message": message,
        "remediation": remediation,
    }


def contract_findings(repo_root: Path = REPO_ROOT) -> list[dict]:
    contracts = repo_root / "_meta" / "contracts"
    schema_path = contracts / "canonical-transcript-v1.schema.json"
    pin_path = contracts / "canonical-transcript-v1.pin.json"
    fixture_path = (
        repo_root / "tests" / "fixtures" / "contracts" / "canonical-transcript-v1.json"
    )
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        pin = json.loads(pin_path.read_text(encoding="utf-8"))
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema, format_checker=contract_format_checker()).validate(
            fixture
        )
        if schema["$id"] != pin["contract_id"]:
            raise ValueError("contract ID differs from pin")
        if fixture["schema_version"] != pin["schema_version"]:
            raise ValueError("fixture version differs from pin")
        if hashlib.sha256(schema_path.read_bytes()).hexdigest() != pin["schema_sha256"]:
            raise ValueError("schema digest differs from pin")
        if (
            hashlib.sha256(fixture_path.read_bytes()).hexdigest()
            != pin["fixture_sha256"]
        ):
            raise ValueError("fixture digest differs from pin")
    except (
        OSError,
        json.JSONDecodeError,
        KeyError,
        SchemaError,
        ValidationError,
        ValueError,
    ) as exc:
        return [
            _finding(
                "VR-KP-001",
                schema_path,
                "canonical-transcript-v1",
                f"invalid vendored transcript contract: {exc}",
                "update schema, fixture, and pin together from the upstream contract",
            )
        ]
    return []


def artifact_replay_findings(
    before: dict[str, bytes],
    after: dict[str, bytes],
    *,
    second_created: bool,
) -> list[dict]:
    if before == after and not second_created:
        return []
    return [
        _finding(
            "VR-KP-021",
            Path("raw"),
            "artifact-replay",
            "same-input artifact replay changed bytes or created a revision",
            "make same digest capture a byte-identical no-op",
        )
    ]


def _ast_contract_findings(
    required: dict[Path, set[str]],
    *,
    subject: str,
    unavailable_message: str,
    missing_message: str,
    unavailable_restore: str,
) -> list[dict]:
    findings: list[dict] = []
    for path, names in required.items():
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, SyntaxError) as exc:
            findings.append(
                _finding(
                    "VR-KP-020",
                    path,
                    subject,
                    f"{unavailable_message}: {exc}",
                    unavailable_restore,
                )
            )
            continue
        declared = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        for missing in sorted(names - declared):
            findings.append(
                _finding(
                    "VR-KP-020",
                    path,
                    missing,
                    f"UNSUPPORTED_RULE: missing {missing_message} {missing}",
                    "restore the named implementation or executable test",
                )
            )
    return findings


def page_command_contract_findings(repo_root: Path = REPO_ROOT) -> list[dict]:
    required = {
        repo_root / "scripts" / "knowledge" / "documents.py": {
            "apply_page_write_plan",
            "build_promote_plan",
        },
        repo_root / "tests" / "test_page_commands.py": {
            "test_apply_synthesize_requires_exact_confirmation_and_rejects_stale_tree",
            "test_apply_rejects_synthesize_operation_input_not_bound_to_target",
            "test_synthesize_renders_claims_and_relations_with_escaped_table_cells",
            "test_promote_requires_review_and_preserves_content_and_id",
            "test_promote_replay_revalidates_confirmed_review_semantics",
            "test_collection_add_and_reorder_change_only_collection_page",
            "test_collection_add_requires_one_explicit_policy_and_supports_id_order",
            "test_collection_delta_preserves_raw_bytes_outside_members",
            "test_apply_rechecks_tree_and_mode_after_candidate_validation",
            "test_apply_rolls_back_own_leaf_when_post_write_tree_differs",
            "test_move_is_same_lifecycle_only_and_rejects_collision",
            "test_cli_rejects_plan_applied_through_wrong_command",
            "test_document_tree_rejects_non_regular_markdown_entries",
        },
        repo_root / "tests" / "test_fs.py": {
            "test_post_commit_rollback_failure_is_reported_indeterminate",
            "test_repository_write_lock_is_nonblocking_and_process_scoped",
        },
    }
    return _ast_contract_findings(
        required,
        subject="page-command-contract",
        unavailable_message="page command contract surface is unavailable",
        missing_message="page command contract",
        unavailable_restore="restore the P2-T5 implementation and executable tests",
    )


def materialize_contract_findings(repo_root: Path = REPO_ROOT) -> list[dict]:
    required = {
        repo_root / "scripts" / "knowledge" / "materialize.py": {
            "render_generated",
            "validate_generated",
            "generated_drift",
            "apply_generated",
        },
        repo_root / "tests" / "test_materialize.py": {
            "test_render_is_deterministic_and_manifest_is_schema_derived",
            "test_index_overview_templates_and_base_follow_canonical_contract",
            "test_schema_page_type_change_automatically_changes_template_manifest",
            "test_check_is_no_write_and_reports_missing_or_changed_leaf",
            "test_canonical_page_marker_text_is_not_an_unexpected_generated_leaf",
            "test_apply_preflight_rejects_markerless_symlink_and_unknown_generated_leaf",
            "test_apply_rejects_generated_parent_symlink_before_external_write",
            "test_apply_rejects_parent_swap_after_preflight_without_external_write",
            "test_apply_rejects_leaf_swap_after_preflight_and_preserves_human_bytes",
            "test_independent_validator_rejects_index_and_template_renderer_mutations",
            "test_independent_validator_rejects_active_record_common_mode_mutation",
            "test_validator_rejects_relocated_base_marker",
            "test_apply_rejects_leaf_swap_at_atomic_exchange_and_preserves_human_bytes",
            "test_temp_file_failure_leaves_no_leaf_and_exact_replay_converges",
            "test_temp_content_mutation_before_commit_never_publishes_corrupt_bytes",
            "test_managed_temp_leftover_does_not_block_exact_replay",
            "test_check_reports_managed_marker_temp_until_apply_recovers",
            "test_cleanup_unlink_failure_converges_on_next_replay",
            "test_post_commit_failure_preserves_same_bytes_competing_inode",
            "test_partial_leaf_failure_is_detected_and_exact_replay_converges",
            "test_apply_rechecks_rendered_input_inside_repository_lock",
            "test_cli_repository_check_executes_generated_parity_rules",
            "test_inactive_domain_page_fails_checker_and_materializer",
            "test_invalid_utf8_domain_registry_fails_both_public_boundaries",
            "test_display_text_contract_rejects_multiline_and_table_separator",
            "test_display_text_contract_rejects_trailing_line_break",
            "test_schema_loader_fails_closed_at_materializer_boundary",
            "test_generator_identity_has_one_runtime_owner",
            "test_materialize_command_call_graph_max_depth_is_exactly_ratcheted",
            "test_page_candidate_checks_base_parity_then_canonical_then_candidate_coverage",
        },
    }
    return _ast_contract_findings(
        required,
        subject="materialize-contract",
        unavailable_message="materialize contract surface is unavailable",
        missing_message="materialize contract",
        unavailable_restore="restore the P2-T6 implementation and executable tests",
    )


def generated_surface_findings(drift: tuple[str, ...]) -> list[dict]:
    findings = []
    for message in drift:
        navigation_path = next(
            (
                Path(path)
                for path in ("wiki/index.md", "wiki/overview.md")
                if path in message
            ),
            None,
        )
        findings.append(
            _finding(
                "VR-KP-018" if navigation_path else "VR-KP-017",
                navigation_path or Path("wiki"),
                "generated-index" if navigation_path else "generated-surface",
                message,
                "run materialize after canonical pages, schema, or domain registry "
                "changes",
            )
        )
    return findings


def rule_coverage_findings(
    registry: dict[str, tuple[str, str]] | None = None,
    *,
    repo_root: Path = REPO_ROOT,
) -> list[dict]:
    selected = RULE_REGISTRY if registry is None else registry
    executable_surfaces = {
        "contract-check": contract_findings,
        "artifact-evidence-check": _artifact_findings,
        "artifact-path-check": _artifact_findings,
        "schema-check": validate_instance,
        "graph-check": inspect_graph,
        "claim-check": _artifact_findings,
        "lifecycle-check": _lifecycle_findings,
        "architecture-check": architecture_findings,
        "rule-coverage-check": rule_coverage_findings,
        "artifact-replay-check": artifact_replay_findings,
        "page-command-contract": page_command_contract_findings,
        "cli-generated-parity": generated_surface_findings,
        "cli-index-coverage": generated_surface_findings,
        "taxonomy-check": _taxonomy_findings,
    }
    findings = []
    for rule_id, (status, implementation) in sorted(selected.items()):
        surface = executable_surfaces.get(implementation)
        unavailable = not callable(surface)
        if status == "active" and unavailable:
            findings.append(
                _finding(
                    "VR-KP-020",
                    Path("_meta/knowledge.schema.json"),
                    rule_id,
                    f"UNSUPPORTED_RULE: {rule_id}",
                    "register an existing executable checker or contract test",
                )
            )
    logic_path = repo_root / "docs" / "wiki-ingest-business-logic.md"
    try:
        logic = logic_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        findings.append(
            _finding(
                "VR-KP-020",
                logic_path,
                "business-logic-rules",
                f"unavailable business logic rule source: {exc}",
                "restore a readable UTF-8 business logic specification",
            )
        )
        logic = ""
    expected = set(re.findall(r"^\| (VR-KP-\d{3}) \|", logic, re.MULTILINE))
    for missing in sorted(expected - set(selected)):
        findings.append(
            _finding(
                "VR-KP-020",
                Path("docs/wiki-ingest-business-logic.md"),
                missing,
                f"UNSUPPORTED_RULE: {missing}",
                "add the validation rule to the executable registry",
            )
        )
    if any(
        status == "active" and implementation == "page-command-contract"
        for status, implementation in selected.values()
    ):
        findings.extend(page_command_contract_findings(repo_root))
    findings.extend(materialize_contract_findings(repo_root))
    return findings


def _taxonomy_entity_slugs(path: Path, text: str) -> list[tuple[str, int]]:
    values: list[tuple[str, int]] = []
    if path.parent.name == "entities":
        values.append((path.stem, 1))
    lines = text.splitlines()
    for line_number, (line, fenced) in enumerate(
        zip(lines, markdown_fence_mask(lines)), start=1
    ):
        if fenced:
            continue
        for target in WIKILINK_RE.findall(line):
            clean = target.strip().rstrip("/")
            parts = clean.split("/")
            if len(parts) >= 2 and parts[-2] == "entities":
                leaf = parts[-1]
                if leaf.endswith(".md"):
                    leaf = leaf[: -len(".md")]
                values.append((leaf, line_number))
    return values


def _taxonomy_findings(
    path: Path,
    text: str,
    instance: dict,
    taxonomy: tuple[
        frozenset[str], dict[str, str], frozenset[str], dict[str, str]
    ],
) -> list[dict]:
    canonical_tags, tag_aliases, canonical_entities, entity_aliases = taxonomy
    findings: list[dict] = []
    for tag in instance["properties"]["tags"]:
        if tag in canonical_tags:
            continue
        if tag in tag_aliases:
            findings.append(
                _finding(
                    "VR-KP-023",
                    path,
                    tag,
                    f"taxonomy alias tag: {tag}; use {tag_aliases[tag]}",
                    "replace the alias with its canonical taxonomy tag",
                    severity="MEDIUM",
                )
            )
        else:
            findings.append(
                _finding(
                    "VR-KP-023",
                    path,
                    tag,
                    f"taxonomy unknown tag: {tag}",
                    "register the tag through taxonomy review or use a canonical tag",
                )
            )
    for entity, line_number in _taxonomy_entity_slugs(path, text):
        if entity in canonical_entities:
            continue
        if entity in entity_aliases:
            finding = _finding(
                "VR-KP-023",
                path,
                entity,
                f"taxonomy alias entity: {entity}; use {entity_aliases[entity]}",
                "replace the alias with its canonical taxonomy entity",
                severity="MEDIUM",
            )
        else:
            finding = _finding(
                "VR-KP-023",
                path,
                entity,
                f"taxonomy unknown entity: {entity}",
                "register the entity through taxonomy review or use a canonical entity",
            )
        finding["line"] = line_number
        findings.append(finding)
    return findings


def _artifact_findings(repo_root: Path, path: Path, instance: dict) -> list[dict]:
    findings: list[dict] = []
    source_paths = instance["properties"]["source_paths"]
    for relative in source_paths:
        manifest_path = repo_root / relative
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            validate_instance(manifest, validator_for("ArtifactManifest"))
            descriptors = [
                {
                    "path": manifest["payload"],
                    "digest": manifest["artifact_digest"],
                    "size": manifest["size"],
                }
            ]
            if "content" in manifest:
                descriptors.append(manifest["content"])
            descriptors.extend(manifest.get("assets", []))
            expected_names = {"manifest.json"}
            for descriptor in descriptors:
                item = confined(
                    manifest_path.parent, manifest_path.parent / descriptor["path"]
                )
                item_bytes = item.read_bytes()
                item_digest = hashlib.sha256(item_bytes).hexdigest()
                if descriptor["digest"] != f"sha256:{item_digest}" or descriptor[
                    "size"
                ] != len(item_bytes):
                    raise ValueError(
                        f"descriptor digest or size mismatch: {descriptor['path']}"
                    )
                expected_names.add(descriptor["path"])
            actual_names = {item.name for item in manifest_path.parent.iterdir()}
            if actual_names != expected_names:
                raise ValueError("artifact bundle file set mismatch")
            digest = manifest["artifact_digest"].removeprefix("sha256:")
            expected = (
                repo_root
                / "raw"
                / "sources"
                / manifest["source_type"]
                / manifest["source_id"]
                / digest
                / "manifest.json"
            )
            if manifest_path.resolve() != expected.resolve():
                raise ValueError(
                    "manifest path does not match source identity and digest"
                )
        except (OSError, json.JSONDecodeError, KnowledgeSchemaError, ValueError) as exc:
            findings.append(
                _finding(
                    "VR-KP-009",
                    path,
                    instance["id"],
                    f"invalid source manifest {relative}: {exc}",
                    "reference one existing verified ArtifactBundle manifest",
                )
            )

    claim_ids: set[str] = set()
    for claim in instance["claims"]:
        if claim["id"] in claim_ids:
            findings.append(
                _finding(
                    "VR-KP-010",
                    path,
                    instance["id"],
                    f"duplicate claim ID: {claim['id']}",
                    "make claim IDs unique within the page",
                )
            )
        claim_ids.add(claim["id"])
        if claim["evidence"] not in source_paths:
            findings.append(
                _finding(
                    "VR-KP-010",
                    path,
                    instance["id"],
                    "claim evidence is not declared in source_paths: "
                    f"{claim['evidence']}",
                    "add the evidence manifest to source_paths or correct the claim",
                )
            )
    return findings


def _lifecycle_findings(
    repo_root: Path,
    target_root: Path,
    path: Path,
    instance: dict,
    roots: tuple[str, ...],
) -> list[dict]:
    relative = path.resolve().relative_to(target_root.resolve())
    parts = relative.parts
    lifecycle_occurrences = [part for part in parts if part in roots]
    if (
        not parts
        or parts[0] not in roots
        or lifecycle_occurrences != [parts[0]]
    ):
        return [
            _finding(
                "VR-KP-014",
                path,
                instance["id"],
                "page path must identify exactly one lifecycle root",
                "place the page under one of: " + ", ".join(roots),
            )
        ]
    try:
        active_domain_for_path(repo_root, target_root, path)
    except KnowledgeSchemaError as exc:
        return [
            _finding(
                "VR-KP-014",
                path,
                instance["id"],
                str(exc),
                "move the page to an active registered domain or activate its domain",
            )
        ]
    if (
        instance["properties"]["page_type"] == "collection"
        and parts[0] == "domains"
    ):
        return [
            _finding(
                "VR-KP-014",
                path,
                instance["id"],
                "active collection must be under collections",
                "move the page to the collections lifecycle root",
            )
        ]
    if (
        instance["properties"]["page_type"] != "collection"
        and parts[0] == "collections"
    ):
        return [
            _finding(
                "VR-KP-014",
                path,
                instance["id"],
                "non-collection page cannot be under collections",
                "move the page to domains or staging, or use page_type collection",
            )
        ]
    return []


def _architecture_module_name(relative: Path) -> str:
    if relative == Path("scripts/wiki_ingest.py"):
        return "wiki_ingest"
    if relative.parts[:2] == ("scripts", "knowledge"):
        parts = relative.with_suffix("").parts[2:]
        if parts[-1:] == ("__init__",):
            parts = parts[:-1]
        return ".".join(("knowledge", *parts))
    if relative.parts[:2] == ("scripts", "contracts"):
        parts = relative.with_suffix("").parts[2:]
        if parts[-1:] == ("__init__",):
            parts = parts[:-1]
        return ".".join(("contracts", *parts))
    raise ValueError(f"architecture path is outside the module roots: {relative}")


def _architecture_import_targets(module: str, node: ast.AST) -> list[str]:
    if isinstance(node, ast.Import):
        targets = [alias.name for alias in node.names]
    elif not isinstance(node, ast.ImportFrom):
        return []
    else:
        if node.level:
            package = module.split(".")[:-1]
            prefix = package[: len(package) - node.level + 1]
            base = ".".join(prefix + ([node.module] if node.module else []))
        else:
            base = node.module or ""
        targets = [base] if base else []
        targets.extend(
            ".".join(part for part in (base, alias.name) if part)
            for alias in node.names
            if alias.name != "*"
        )

    return targets


def _architecture_source_tree(path: Path, subject: str) -> tuple[ast.AST | None, list[dict]]:
    try:
        mode = path.lstat().st_mode
    except OSError as exc:
        return None, [
            _finding(
                "VR-KP-019",
                path,
                subject,
                f"unavailable architecture source (stat): {exc}",
                "restore a regular non-symlink UTF-8 Python architecture source",
            )
        ]
    if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
        return None, [
            _finding(
                "VR-KP-019",
                path,
                subject,
                "non-regular architecture source",
                "restore a regular non-symlink UTF-8 Python architecture source",
            )
        ]
    try:
        return ast.parse(path.read_text(encoding="utf-8")), []
    except (OSError, UnicodeDecodeError, SyntaxError) as exc:
        category = (
            "read"
            if isinstance(exc, OSError)
            else "encoding"
            if isinstance(exc, UnicodeDecodeError)
            else "syntax"
        )
        return None, [
            _finding(
                "VR-KP-019",
                path,
                subject,
                f"unavailable architecture source ({category}): {exc}",
                "restore a regular non-symlink UTF-8 Python architecture source",
            )
        ]


def _architecture_python_paths(root: Path) -> tuple[list[Path], list[dict]]:
    paths: list[Path] = []
    findings: list[dict] = []

    def report_walk_error(error: OSError) -> None:
        location = Path(error.filename) if error.filename else root
        findings.append(
            _finding(
                "VR-KP-019",
                location,
                "architecture",
                f"unavailable architecture inventory: {error}",
                "restore a readable architecture module directory",
            )
        )

    try:
        for current, directory_names, file_names in os.walk(
            root, followlinks=False, onerror=report_walk_error
        ):
            current_path = Path(current)
            traversable: list[str] = []
            for name in directory_names:
                directory = current_path / name
                try:
                    mode = directory.lstat().st_mode
                except OSError as exc:
                    report_walk_error(exc)
                    continue
                if name.endswith(".py"):
                    findings.append(
                        _finding(
                            "VR-KP-019",
                            directory,
                            "architecture",
                            "non-regular architecture source",
                            "restore a regular non-symlink UTF-8 Python "
                            "architecture source",
                        )
                    )
                    continue
                if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
                    findings.append(
                        _finding(
                            "VR-KP-019",
                            directory,
                            "architecture",
                            "non-regular architecture inventory",
                            "restore a regular non-symlink architecture directory",
                        )
                    )
                    continue
                traversable.append(name)
            directory_names[:] = traversable
            paths.extend(
                current_path / name
                for name in file_names
                if name.endswith(".py")
            )
    except OSError as exc:
        report_walk_error(exc)
    return paths, findings


def architecture_findings(repo_root: Path = REPO_ROOT) -> list[dict]:
    actual_paths: set[Path] = set()
    findings: list[dict] = []
    scripts_root = repo_root / "scripts"
    module_roots = tuple(
        repo_root / relative.parent for relative in ARCHITECTURE_INITIALIZER_PATHS
    )
    invalid_inventory_roots: set[Path] = set()
    for root in (repo_root, scripts_root, *module_roots):
        try:
            mode = root.lstat().st_mode
        except OSError as exc:
            findings.append(
                _finding(
                    "VR-KP-019",
                    root,
                    "architecture",
                    f"unavailable architecture inventory: {exc}",
                    "restore a regular non-symlink architecture directory",
                )
            )
            invalid_inventory_roots.add(root)
            continue
        if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
            findings.append(
                _finding(
                    "VR-KP-019",
                    root,
                    "architecture",
                    "non-regular architecture inventory",
                    "restore a regular non-symlink architecture directory",
                )
            )
            invalid_inventory_roots.add(root)
    if repo_root in invalid_inventory_roots or scripts_root in invalid_inventory_roots:
        return findings
    try:
        script_entries = list(scripts_root.iterdir())
    except OSError as exc:
        findings.append(
            _finding(
                "VR-KP-019",
                scripts_root,
                "architecture",
                f"unavailable architecture inventory: {exc}",
                "restore a readable architecture scripts directory",
            )
        )
        return findings
    local_sibling_modules = {
        path.stem
        for path in script_entries
        if path.suffix == ".py"
        and path.stem.isidentifier()
        and path.name != "wiki_ingest.py"
    }
    local_sibling_modules.update(
        path.name
        for path in script_entries
        if path.name not in {"knowledge", "contracts"} and path.name.isidentifier()
    )
    for root in module_roots:
        if any(
            invalid == root or invalid in root.parents
            for invalid in invalid_inventory_roots
        ):
            continue
        candidates, inventory_findings = _architecture_python_paths(root)
        findings.extend(inventory_findings)
        actual_paths.update(
            relative
            for path in candidates
            if (relative := path.relative_to(repo_root))
            not in ARCHITECTURE_INITIALIZER_PATHS
        )
    entrypoint = Path("scripts/wiki_ingest.py")
    try:
        (repo_root / entrypoint).lstat()
    except FileNotFoundError:
        pass
    except OSError as exc:
        findings.append(
            _finding(
                "VR-KP-019",
                repo_root / entrypoint,
                "wiki_ingest",
                f"unavailable architecture inventory: {exc}",
                "restore a readable architecture entrypoint",
            )
        )
    else:
        actual_paths.add(entrypoint)
    expected_paths = set(ARCHITECTURE_MODULE_PATHS.values())
    modules: dict[str, Path] = {}
    for relative in sorted(actual_paths):
        module = _architecture_module_name(relative)
        path = repo_root / relative
        if module in modules:
            findings.append(
                _finding(
                    "VR-KP-019",
                    path,
                    module,
                    f"duplicate architecture module identity: {module}",
                    "remove the colliding module path or revise the architecture contract",
                )
            )
            continue
        modules[module] = path
    edges: dict[str, set[str]] = {module: set() for module in modules}
    for module, relative in ARCHITECTURE_MODULE_PATHS.items():
        if module not in modules:
            findings.append(
                _finding(
                    "VR-KP-019",
                    repo_root / relative,
                    module,
                    f"missing architecture module: {module}",
                    "restore the exact documented architecture module set",
                )
            )
    for relative in sorted(actual_paths - expected_paths):
        module = _architecture_module_name(relative)
        findings.append(
            _finding(
                "VR-KP-019",
                repo_root / relative,
                module,
                f"unexpected architecture module: {module}",
                "remove the module or revise the architecture contract before use",
            )
        )
    for relative in ARCHITECTURE_INITIALIZER_PATHS:
        initializer = repo_root / relative
        if initializer.parent in invalid_inventory_roots:
            continue
        tree, source_findings = _architecture_source_tree(
            initializer, relative.parent.name
        )
        findings.extend(source_findings)
        if tree is not None and any(
            isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(tree)
        ):
            findings.append(
                _finding(
                    "VR-KP-019",
                    initializer,
                    relative.parent.name,
                    "package initializer import is forbidden",
                    "keep architecture package initializers import-free",
                )
            )
    for module, path in sorted(modules.items()):
        tree, source_findings = _architecture_source_tree(path, module)
        findings.extend(source_findings)
        if tree is None:
            continue
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.ImportFrom)
                and node.level > len(module.split(".")[:-1])
            ):
                findings.append(
                    _finding(
                        "VR-KP-019",
                        path,
                        module,
                        f"invalid relative architecture import level: {node.level}",
                        "keep relative imports within the declaring package",
                    )
                )
                continue
            import_targets = _architecture_import_targets(module, node)
            if isinstance(node, ast.Import):
                module_references = import_targets
            elif isinstance(node, ast.ImportFrom) and import_targets:
                base = import_targets[0]
                module_references = (
                    import_targets[1:] or [base]
                    if base in {"knowledge", "contracts", "scripts"}
                    else [base]
                )
            else:
                module_references = []
            for target in sorted(set(module_references)):
                if (
                    (
                        target in {"knowledge", "contracts", "scripts"}
                        or target.startswith(
                            ("knowledge.", "contracts.", "scripts.")
                        )
                    )
                    and target not in ARCHITECTURE_MODULE_PATHS
                ):
                    findings.append(
                        _finding(
                            "VR-KP-019",
                            path,
                            module,
                            f"unregistered architecture import: {module} -> {target}",
                            "register the module in the architecture contract or remove the import",
                        )
                    )
            for target in sorted(set(import_targets)):
                target_parts = target.split(".")
                local_sibling = target_parts[0] in local_sibling_modules or (
                    len(target_parts) > 1
                    and target_parts[0] == "scripts"
                    and target_parts[1] in local_sibling_modules
                )
                if target_parts[0] == "projects" or local_sibling:
                    findings.append(
                        _finding(
                            "VR-KP-019",
                            path,
                            module,
                            f"forbidden repository import: {module} -> {target}",
                            "remove dependencies outside the declared architecture modules",
                        )
                    )
                if target_parts[0] in {"ytscript", "ingest", "pipeline"}:
                    findings.append(
                        _finding(
                            "VR-KP-019",
                            path,
                            module,
                            f"forbidden import edge: {module} -> {target}",
                            "consume versioned files rather than upstream "
                            "runtime modules",
                        )
                    )
                if target in modules:
                    edges[module].add(target)

    actual_edges = {
        (source, target) for source, targets in edges.items() for target in targets
    }
    for source, target in sorted(actual_edges - ARCHITECTURE_EXPECTED_EDGES):
        findings.append(
            _finding(
                "VR-KP-019",
                modules[source],
                source,
                f"unexpected architecture edge: {source} -> {target}",
                "remove the edge or revise the architecture contract before use",
            )
        )
    for source, target in sorted(ARCHITECTURE_EXPECTED_EDGES - actual_edges):
        findings.append(
            _finding(
                "VR-KP-019",
                modules.get(source, repo_root / ARCHITECTURE_MODULE_PATHS[source]),
                source,
                f"missing architecture edge: {source} -> {target}",
                "restore the exact documented architecture edge set",
            )
        )

    visiting: set[str] = set()
    visited: set[str] = set()
    cycle_detected = False

    def visit(module: str) -> None:
        nonlocal cycle_detected
        if module in visiting:
            cycle_detected = True
            findings.append(
                _finding(
                    "VR-KP-019",
                    modules[module],
                    module,
                    "knowledge module import cycle detected",
                    "restore the documented one-way module DAG",
                )
            )
            return
        if module in visited:
            return
        visiting.add(module)
        for target in sorted(edges[module]):
            visit(target)
        visiting.remove(module)
        visited.add(module)

    for module in sorted(modules):
        visit(module)
    if not cycle_detected and set(modules) == set(ARCHITECTURE_MODULE_PATHS):
        depth_cache: dict[str, int] = {}

        def longest_path(module: str) -> int:
            if module not in depth_cache:
                depth_cache[module] = (
                    0
                    if not edges[module]
                    else 1 + max(longest_path(target) for target in edges[module])
                )
            return depth_cache[module]

        maximum_depth = max(longest_path(module) for module in modules)
        if maximum_depth != ARCHITECTURE_MAX_EDGE_DEPTH:
            findings.append(
                _finding(
                    "VR-KP-019",
                    repo_root / "scripts/knowledge/check.py",
                    "architecture",
                    f"architecture dependency edge depth is {maximum_depth}, "
                    f"expected {ARCHITECTURE_MAX_EDGE_DEPTH}",
                    "restore the exact documented architecture depth",
                )
            )
    return findings


def check_target(
    target_root: Path,
    *,
    repo_root: Path = REPO_ROOT,
    mode: str = "all",
    changed_paths: list[Path] | None = None,
    overrides: Mapping[Path, str | None] | None = None,
    include_repository_contracts: bool = True,
) -> CheckResult:
    if mode not in {"all", "changed"}:
        raise ValueError(f"unknown check mode: {mode}")
    if not target_root.is_dir():
        raise ValueError(f"target root must be an existing directory: {target_root}")
    root = target_root.resolve()
    override_by_path: dict[Path, str | None] = {}
    for path, content in (overrides or {}).items():
        resolved = path.resolve()
        if not resolved.is_relative_to(root) or not is_canonical_document_path(
            root, resolved
        ):
            raise ValueError(f"invalid candidate override path: {path}")
        override_by_path[resolved] = content
    try:
        all_paths = {
            path
            for path in canonical_document_paths(target_root)
            if not EXCLUDED_PARTS.intersection(path.parts)
        }
    except KnowledgeSchemaError as exc:
        return CheckResult(
            structural_verdict="FAIL",
            semantic_review="not-performed",
            mode=mode,
            exclusions=tuple(sorted(EXCLUDED_PARTS)),
            findings=(
                _finding(
                    "VR-KP-004",
                    target_root,
                    "<target-root>",
                    str(exc),
                    "replace symlink or special entries with regular directories/files",
                ),
            ),
        )
    for path, content in override_by_path.items():
        all_paths = {
            candidate for candidate in all_paths if candidate.resolve() != path
        }
        if content is None:
            continue
        else:
            all_paths.add(path)
    sorted_paths = sorted(all_paths)
    if mode == "changed" and not changed_paths:
        raise ValueError("changed mode requires at least one explicit path")
    if mode == "changed":
        target = target_root.resolve()
        for changed_path in changed_paths or []:
            resolved = changed_path.resolve()
            if (
                not resolved.is_relative_to(target)
                or changed_path.suffix != ".md"
                or (resolved.exists() and not resolved.is_file())
            ):
                raise ValueError(
                    "changed path must be a Markdown file location under target root: "
                    f"{changed_path}"
                )
    findings = []
    if include_repository_contracts:
        findings.extend(contract_findings(repo_root))
        findings.extend(rule_coverage_findings(repo_root=repo_root))
        findings.extend(architecture_findings(repo_root))
    if not sorted_paths:
        findings.append(
            _finding(
                "VR-KP-004",
                target_root,
                "<target-root>",
                "target root contains no Markdown pages",
                "select the intended non-empty canonical scope",
            )
        )
    records: list[tuple[Path, dict, str]] = []
    parse_findings: list[dict] = []
    for path in sorted_paths:
        try:
            source = override_by_path.get(path.resolve())
            if source is None:
                source = path.read_text(encoding="utf-8")
            instance = parse_markdown(
                path,
                source,
                schema_path=repo_root / "_meta" / "knowledge.schema.json",
            )
        except (OSError, UnicodeDecodeError, KnowledgeSchemaError) as exc:
            parse_findings.append(
                _finding(
                    "VR-KP-004",
                    path,
                    path.stem,
                    str(exc),
                    "make the Markdown parse to a schema-valid DocumentInstance",
                )
            )
            continue
        records.append((path, instance, source))

    taxonomy = None
    try:
        taxonomy = load_taxonomy(repo_root)
    except KnowledgeSchemaError as exc:
        findings.append(
            _finding(
                "VR-KP-023",
                repo_root / "_meta" / "taxonomy.md",
                "taxonomy",
                str(exc),
                "make taxonomy canonical and alias entries unique and parseable",
            )
        )

    try:
        roots = lifecycle_roots(repo_root)
    except KnowledgeSchemaError as exc:
        findings.append(
            _finding(
                "VR-KP-004",
                repo_root / "_meta" / "knowledge.schema.json",
                "schema",
                str(exc),
                (
                    "define one non-empty LifecyclePath and reference it from "
                    "PageWrite source_path and target_path"
                ),
            )
        )
        roots = ()

    if mode == "all":
        impacted_paths = set(sorted_paths)
        findings.extend(parse_findings)
    else:
        changed_resolved = {path.resolve() for path in changed_paths or []}
        changed_ids = {path.stem for path in changed_paths or []}
        impacted_ids = set(changed_ids)
        for _, instance, _ in records:
            outgoing = set(instance["links"])
            outgoing.update(relation["target"] for relation in instance["relations"])
            outgoing.update(member["target"] for member in instance["members"])
            if instance["id"] in changed_ids:
                impacted_ids.update(outgoing)
            if outgoing.intersection(changed_ids):
                impacted_ids.add(instance["id"])
        impacted_paths = {
            path
            for path, instance, _ in records
            if instance["id"] in impacted_ids
        }
        impacted_paths.update(
            path for path in sorted_paths if path.resolve() in changed_resolved
        )
        findings.extend(
            finding
            for finding in parse_findings
            if Path(finding["path"]).resolve() in changed_resolved
        )

    for path, instance, source in records:
        if path not in impacted_paths:
            continue
        if taxonomy is not None:
            findings.extend(_taxonomy_findings(path, source, instance, taxonomy))
        findings.extend(_artifact_findings(repo_root, path, instance))
        if roots:
            findings.extend(
                _lifecycle_findings(repo_root, target_root, path, instance, roots)
            )
    findings.extend(
        finding
        for finding in inspect_graph(
            [(path, instance) for path, instance, _ in records]
        )
        if Path(finding["path"]) in impacted_paths
    )
    findings.sort(key=lambda item: (item["path"], item["rule_id"], item["message"]))
    return CheckResult(
        structural_verdict=(
            "FAIL" if any(item["severity"] == "HIGH" for item in findings) else "PASS"
        ),
        semantic_review="not-performed",
        mode=mode,
        exclusions=tuple(
            sorted(
                EXCLUDED_PARTS | {"templates/**", "index.md", "overview.md"}
            )
        ),
        findings=tuple(findings),
    )
