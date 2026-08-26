from __future__ import annotations

import ast
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError

from .fs import confined
from .graph import inspect_graph
from .schema import (
    REPO_ROOT,
    KnowledgeSchemaError,
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
    "VR-KP-015": ("inactive-until-7", "stale-plan-test"),
    "VR-KP-016": ("inactive-until-7", "write-set-test"),
    "VR-KP-017": ("inactive-until-8", "materialize-check"),
    "VR-KP-018": ("inactive-until-8", "index-coverage-check"),
    "VR-KP-019": ("active", "architecture-check"),
    "VR-KP-020": ("active", "rule-coverage-check"),
    "VR-KP-021": ("active", "artifact-replay-check"),
    "VR-KP-022": ("inactive-until-7", "promotion-semantic-gate"),
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
        Draft202012Validator(
            schema, format_checker=contract_format_checker()
        ).validate(fixture)
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


def _lifecycle_findings(target_root: Path, path: Path, instance: dict) -> list[dict]:
    relative = path.relative_to(target_root)
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
) -> CheckResult:
    if mode not in {"all", "changed"}:
        raise ValueError(f"unknown check mode: {mode}")
    if not target_root.is_dir():
        raise ValueError(f"target root must be an existing directory: {target_root}")
    all_paths = sorted(
        path
        for path in target_root.rglob("*.md")
        if not EXCLUDED_PARTS.intersection(path.parts)
        and is_canonical_document_path(target_root, path)
    )
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
    findings = contract_findings() + rule_coverage_findings() + architecture_findings()
    if not all_paths:
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
    for path in all_paths:
        try:
            instance = parse_markdown(path)
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
        impacted_paths = set(all_paths)
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
            path for path in all_paths if path.resolve() in changed_resolved
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
        findings.extend(_lifecycle_findings(target_root, path, instance))
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
