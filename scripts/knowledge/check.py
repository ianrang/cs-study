from __future__ import annotations

import ast
import hashlib
import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

from .fs import confined
from .graph import inspect_graph
from .schema import (
    REPO_ROOT,
    KnowledgeSchemaError,
    active_domain_for_path,
    canonical_document_paths,
    contract_format_checker,
    is_canonical_document_path,
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
}


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
    rule_id: str, path: Path, subject: str, message: str, remediation: str
) -> dict:
    return {
        "rule_id": rule_id,
        "severity": "HIGH",
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
        except (OSError, SyntaxError) as exc:
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
        repo_root / "tests" / "test_migration_plan.py": {
            "test_migration_writers_share_repository_lock",
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
    logic_path = REPO_ROOT / "docs" / "wiki-ingest-business-logic.md"
    expected = set(
        re.findall(
            r"^\| (VR-KP-\d{3}) \|",
            logic_path.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
    )
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
        findings.extend(page_command_contract_findings())
    findings.extend(materialize_contract_findings())
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
    repo_root: Path, target_root: Path, path: Path, instance: dict
) -> list[dict]:
    relative = path.resolve().relative_to(target_root.resolve())
    parts = relative.parts
    lifecycle = [
        name
        for name in ("staging", "domains", "collections", "archive")
        if name in parts
    ]
    if len(lifecycle) != 1:
        return [
            _finding(
                "VR-KP-014",
                path,
                instance["id"],
                "page path must identify exactly one lifecycle root",
                "place the page under staging, domains, collections, or archive",
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
        and lifecycle[0] == "domains"
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
        and lifecycle[0] == "collections"
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


def _module_name(path: Path, scripts_root: Path) -> str:
    relative = path.relative_to(scripts_root).with_suffix("")
    parts = list(relative.parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def architecture_findings(repo_root: Path = REPO_ROOT) -> list[dict]:
    scripts_root = repo_root / "scripts"
    package_root = repo_root / "scripts" / "knowledge"
    python_paths = list(package_root.rglob("*.py"))
    entrypoint = scripts_root / "wiki_ingest.py"
    if entrypoint.is_file():
        python_paths.append(entrypoint)
    modules = {_module_name(path, scripts_root): path for path in python_paths}
    edges: dict[str, set[str]] = {module: set() for module in modules}
    findings: list[dict] = []
    for module, path in sorted(modules.items()):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            targets: list[str] = []
            if isinstance(node, ast.Import):
                targets = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    base = module.split(".")[:-1]
                    prefix = base[: len(base) - node.level + 1]
                    targets = [
                        ".".join(prefix + ([node.module] if node.module else []))
                    ]
                elif node.module:
                    targets = [node.module]
            for target in targets:
                if target.startswith(("ytscript", "ingest", "pipeline")):
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

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(module: str) -> None:
        if module in visiting:
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
        findings.extend(contract_findings())
        findings.extend(rule_coverage_findings())
        findings.extend(architecture_findings())
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
    records: list[tuple[Path, dict]] = []
    parse_findings: list[dict] = []
    for path in sorted_paths:
        try:
            instance = parse_markdown(path, override_by_path.get(path.resolve()))
        except (OSError, KnowledgeSchemaError) as exc:
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
        records.append((path, instance))

    if mode == "all":
        impacted_paths = set(sorted_paths)
        findings.extend(parse_findings)
    else:
        changed_resolved = {path.resolve() for path in changed_paths or []}
        changed_ids = {path.stem for path in changed_paths or []}
        impacted_ids = set(changed_ids)
        for _, instance in records:
            outgoing = set(instance["links"])
            outgoing.update(relation["target"] for relation in instance["relations"])
            outgoing.update(member["target"] for member in instance["members"])
            if instance["id"] in changed_ids:
                impacted_ids.update(outgoing)
            if outgoing.intersection(changed_ids):
                impacted_ids.add(instance["id"])
        impacted_paths = {
            path for path, instance in records if instance["id"] in impacted_ids
        }
        impacted_paths.update(
            path for path in sorted_paths if path.resolve() in changed_resolved
        )
        findings.extend(
            finding
            for finding in parse_findings
            if Path(finding["path"]).resolve() in changed_resolved
        )

    for path, instance in records:
        if path not in impacted_paths:
            continue
        findings.extend(_artifact_findings(repo_root, path, instance))
        findings.extend(_lifecycle_findings(repo_root, target_root, path, instance))
    findings.extend(
        finding
        for finding in inspect_graph(records)
        if Path(finding["path"]) in impacted_paths
    )
    findings.sort(key=lambda item: (item["path"], item["rule_id"], item["message"]))
    return CheckResult(
        structural_verdict="FAIL" if findings else "PASS",
        semantic_review="not-performed",
        mode=mode,
        exclusions=tuple(
            sorted(
                EXCLUDED_PARTS | {"templates/**", "index.md", "overview.md", "log.md"}
            )
        ),
        findings=tuple(findings),
    )
