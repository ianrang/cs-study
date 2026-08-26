from __future__ import annotations

import base64
import binascii
import difflib
import hashlib
import io
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import unicodedata
from collections import defaultdict
from collections.abc import Callable
from pathlib import Path, PurePosixPath

from contracts.privacy import normalize_local_user_paths
from jsonschema import Draft202012Validator

from .documents import render_preserved_document, replace_paths
from .fs import (
    chmod_fsync,
    exchange_directories,
    fsync_directory,
    rename_directory_no_replace,
    write_bytes_fsync,
)
from .schema import (
    KnowledgeSchemaError,
    inspect_headings,
    inspect_markdown,
    is_canonical_document_path,
    knowledge_format_checker,
    load_schema,
    parse_markdown,
    section_contract,
)

KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MANIFEST_PATH_RE = re.compile(
    r"^raw/sources/[^/]+/[^/]+/[a-f0-9]{64}/manifest\.json$"
)
CASCADE_PRACTICE_GENERATOR = PurePosixPath(
    "projects/info-sec-engineer-practice/scripts/build-practice-data.py"
)
CASCADE_PRACTICE_COMMAND = f"python3 {CASCADE_PRACTICE_GENERATOR.as_posix()}"
MARKDOWN_DOCUMENT_LINK_RE = re.compile(r"\[[^]]+\]\(([^)]+\.md)\)")
MIGRATION_SCHEMA = (
    Path(__file__).resolve().parents[2]
    / "_meta"
    / "knowledge-migration-plan.schema.json"
)
RESOLUTION_SCHEMA = (
    Path(__file__).resolve().parents[2]
    / "_meta"
    / "knowledge-migration-resolution.schema.json"
)
CANONICAL_JSON_ENCODER = json.JSONEncoder(
    ensure_ascii=False, sort_keys=True, separators=(",", ":")
)
TRANSACTION_JOURNAL_V1_FIELDS = frozenset(
    {
        "schema_version",
        "operation",
        "state",
        "knowledge_root",
        "candidate_root",
        "plan_sha256",
        "base_tree_sha256",
        "target_tree_sha256",
    }
)
TRANSACTION_JOURNAL_V2_FIELDS = TRANSACTION_JOURNAL_V1_FIELDS | {
    "cascade_plan_sha256"
}


def _canonical_json(value: object) -> bytes:
    return (CANONICAL_JSON_ENCODER.encode(value) + "\n").encode("utf-8")


def _safe_relative(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if (
        not value
        or value != path.as_posix()
        or path.is_absolute()
        or ".." in path.parts
        or "." in path.parts
        or "\\" in value
    ):
        raise ValueError(f"unsafe relative path: {value!r}")
    return path


def build_tree_manifest(root: Path) -> dict:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"tree root must be an existing directory: {root}")
    entries: list[dict[str, object]] = []
    casefold_paths: dict[str, str] = {}
    for path in sorted(
        root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()
    ):
        relative = path.relative_to(root).as_posix()
        if "\\" in relative:
            raise ValueError(f"unsafe tree path: {relative!r}")
        folded = relative.casefold()
        if folded in casefold_paths:
            raise ValueError(
                f"casefold path collision: {casefold_paths[folded]} and {relative}"
            )
        casefold_paths[folded] = relative
        metadata = path.lstat()
        mode = stat.S_IMODE(metadata.st_mode)
        if stat.S_ISLNK(metadata.st_mode):
            raise ValueError(
                f"symbolic links are forbidden in migration trees: {relative}"
            )
        if stat.S_ISDIR(metadata.st_mode):
            entries.append(
                {
                    "path": relative,
                    "kind": "directory",
                    "mode": mode,
                    "size": 0,
                    "sha256": None,
                }
            )
        elif stat.S_ISREG(metadata.st_mode):
            data = path.read_bytes()
            entries.append(
                {
                    "path": relative,
                    "kind": "file",
                    "mode": mode,
                    "size": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                }
            )
        else:
            raise ValueError(
                f"special files are forbidden in migration trees: {relative}"
            )
    payload = {
        "schema_version": "3.0",
        "root": {
            "kind": "directory",
            "mode": stat.S_IMODE(root.lstat().st_mode),
        },
        "entries": entries,
    }
    encoded = (CANONICAL_JSON_ENCODER.encode(payload) + "\n").encode("utf-8")
    payload["tree_sha256"] = hashlib.sha256(encoded).hexdigest()
    return payload


def _head(repo_root: Path) -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _knowledge_root(repo_root: Path, candidate: Path) -> Path:
    repo_root = repo_root.resolve()
    candidate = (
        candidate.resolve()
        if candidate.is_absolute()
        else (repo_root / candidate).resolve()
    )
    expected = repo_root / "wiki"
    if candidate != expected or not candidate.is_dir():
        raise ValueError(
            f"knowledge root must be the repository wiki directory: {expected}"
        )
    return candidate


def _outside_knowledge_root(knowledge_root: Path, candidate: Path, label: str) -> Path:
    resolved = candidate.resolve()
    if resolved == knowledge_root or resolved.is_relative_to(knowledge_root):
        raise ValueError(f"{label} must be outside knowledge root")
    return resolved


def _journal_path(knowledge_root: Path, candidate: Path) -> Path:
    resolved = _outside_knowledge_root(knowledge_root, candidate, "transaction journal")
    if resolved.parent != knowledge_root.parent:
        raise ValueError("transaction journal must be a sibling of knowledge root")
    return resolved


def build_migration_plan(repo_root: Path, target_root: Path) -> dict:
    repo_root = repo_root.resolve()
    target_root = _knowledge_root(repo_root, target_root)
    tree_manifest = build_tree_manifest(target_root)
    all_markdown = sorted(target_root.rglob("*.md"))
    excluded = [
        path
        for path in all_markdown
        if not is_canonical_document_path(target_root, path)
    ]
    content = [path for path in all_markdown if path not in excluded]
    grouped: dict[str, list[Path]] = defaultdict(list)
    for path in content:
        grouped[path.stem].append(path)
    collisions = {
        stem: [str(path.relative_to(repo_root)) for path in paths]
        for stem, paths in sorted(grouped.items())
        if len(paths) > 1
    }
    reserved_stems = {path.stem for path in excluded}
    reserved_conflicts = {
        stem: [str(path.relative_to(repo_root)) for path in paths]
        for stem, paths in sorted(grouped.items())
        if stem in reserved_stems
    }

    schema = load_schema()
    property_schema = schema["$defs"]["Properties"]
    required = set(property_schema["required"])
    allowed = set(property_schema["properties"])
    page_types = set(schema["$defs"]["PageType"]["enum"])
    items = []
    for path in content:
        reasons: list[str] = []
        try:
            properties, headings = inspect_markdown(path)
        except KnowledgeSchemaError as exc:
            properties, headings = {}, inspect_headings(path)
            reasons.append(f"frontmatter-or-heading-parse: {exc}")
        page_type = properties.get("page_type")
        if page_type not in page_types:
            reasons.append("page-type-decision")
            required_sections = []
        else:
            required_sections = section_contract(page_type)
            if headings != required_sections:
                reasons.append("section-migration-review")

        stem = path.stem
        if stem in collisions:
            id_action = "decision-collision"
            reasons.append("basename-collision")
        elif stem in reserved_conflicts:
            id_action = "decision-reserved"
            reasons.append("reserved-name-conflict")
        elif not KEBAB_RE.fullmatch(stem):
            id_action = "decision-non-kebab"
        else:
            id_action = "preserve"
        if not KEBAB_RE.fullmatch(stem):
            reasons.append("stable-id-decision")

        missing = sorted(required - set(properties))
        remove = sorted(set(properties) - allowed)
        if missing:
            reasons.append("frontmatter-required-fields")
        if remove:
            reasons.append("frontmatter-legacy-fields")
        source_paths = properties.get("source_paths")
        invalid_sources = []
        if isinstance(source_paths, list):
            invalid_sources = [
                value
                for value in source_paths
                if not isinstance(value, str)
                or MANIFEST_PATH_RE.fullmatch(value) is None
            ]
        else:
            invalid_sources = ["<missing-or-non-list>"]
        if invalid_sources:
            reasons.append("artifact-provenance-migration")

        items.append(
            {
                "path": str(path.relative_to(repo_root)),
                "current_stem": stem,
                "id_action": id_action,
                "page_type": page_type if page_type in page_types else None,
                "missing_properties": missing,
                "remove_properties": remove,
                "current_sections": headings,
                "required_sections": required_sections,
                "invalid_source_paths": invalid_sources,
                "requires_decision": sorted(set(reasons)),
            }
        )

    return {
        "schema_version": "2.0",
        "mode": "inventory",
        "repository_head": _head(repo_root),
        "knowledge_root": str(target_root.relative_to(repo_root)),
        "canonical_universe": [str(path.relative_to(target_root)) for path in content],
        "inventory": {
            "markdown": len(all_markdown),
            "content": len(content),
            "excluded": len(excluded),
            "collision_groups": len(collisions),
            "collision_files": sum(len(paths) for paths in collisions.values()),
            "reserved_conflict_groups": len(reserved_conflicts),
            "reserved_conflict_files": sum(
                len(paths) for paths in reserved_conflicts.values()
            ),
            "decision_pages": sum(bool(item["requires_decision"]) for item in items),
            "preserved_ids": sum(item["id_action"] == "preserve" for item in items),
        },
        "exclusions": [str(path.relative_to(repo_root)) for path in excluded],
        "collisions": collisions,
        "reserved_conflicts": reserved_conflicts,
        "tree_manifest": tree_manifest,
        "wiki_tree_sha256": tree_manifest["tree_sha256"],
        "backup_plan": {
            "required_before_apply": True,
            "format": (
                "deterministic tar of exact tree path/type/mode/bytes "
                "plus resolved plan"
            ),
            "filename": f"wiki-{tree_manifest['tree_sha256']}.tar",
            "refusal": (
                "apply rejects stale tree, unresolved plan, invalid backup, "
                "unsupported atomic exchange, or digest mismatch"
            ),
        },
        "items": items,
    }


def plan_bytes(plan: dict) -> bytes:
    return (
        json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def _source_locator(source_path: str) -> str:
    return unicodedata.normalize("NFC", f"wiki/{source_path}")


def _source_id(source_path: str) -> str:
    locator = _source_locator(source_path)
    return hashlib.sha256(locator.encode("utf-8")).hexdigest()


def _preservation_payload_bytes(source: Path) -> bytes:
    return normalize_local_user_paths(source.read_bytes())


def load_preservation_resolution(
    resolution_path: Path,
    inventory: dict,
    repo_root: Path,
    knowledge_root: Path,
) -> dict:
    knowledge_root = _knowledge_root(repo_root, knowledge_root)
    try:
        resolution = json.loads(resolution_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid preservation resolution JSON: {exc}") from exc
    schema = json.loads(RESOLUTION_SCHEMA.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(
            schema, format_checker=knowledge_format_checker()
        ).iter_errors(resolution),
        key=lambda error: list(error.path),
    )
    if errors:
        raise ValueError(f"invalid preservation resolution: {errors[0].message}")
    if resolution["base_tree_sha256"] != inventory["wiki_tree_sha256"]:
        raise ValueError("preservation resolution base tree is stale")
    pages = resolution["pages"]
    if [page["source_path"] for page in pages] != inventory["canonical_universe"]:
        raise ValueError(
            "preservation resolution must cover the exact canonical universe in order"
        )
    page_types = set(load_schema()["$defs"]["PageType"]["enum"])
    target_paths = [page["target_path"] for page in pages]
    target_ids = [PurePosixPath(path).stem for path in target_paths]
    if (
        len(target_paths) != len(set(target_paths))
        or len(target_paths) != len({path.casefold() for path in target_paths})
        or len(target_ids) != len(set(target_ids))
        or len(target_ids) != len({value.casefold() for value in target_ids})
    ):
        raise ValueError("preservation target paths and IDs must be globally unique")
    target_id_set = set(target_ids)
    collection_count = 0
    source_ids: set[str] = set()
    for page in pages:
        source_relative = _safe_relative(page["source_path"])
        target_relative = _safe_relative(page["target_path"])
        if not KEBAB_RE.fullmatch(target_relative.stem):
            raise ValueError(
                f"preservation target ID must be kebab-case: {target_relative.stem}"
            )
        if page["page_type"] not in page_types:
            raise ValueError(f"unknown preservation page type: {page['page_type']}")
        source = knowledge_root.joinpath(*source_relative.parts)
        if hashlib.sha256(_preservation_payload_bytes(source)).hexdigest() != page[
            "source_sha256"
        ]:
            raise ValueError(f"preservation source digest is stale: {source_relative}")
        logical_id = _source_id(page["source_path"])
        if logical_id in source_ids:
            raise ValueError(
                f"duplicate preservation source identity: {source_relative}"
            )
        source_ids.add(logical_id)
        if page["page_type"] == "collection":
            collection_count += 1
            linked_members = [
                PurePosixPath(link).stem
                for link in MARKDOWN_DOCUMENT_LINK_RE.findall(
                    source.read_text(encoding="utf-8")
                )
            ]
            if page["members"] != linked_members:
                raise ValueError(
                    "preservation collection members must exactly match "
                    "source link order"
                )
            missing = sorted(set(page["members"]) - target_id_set)
            if missing:
                raise ValueError(
                    f"preservation collection has missing members: {missing}"
                )
        elif page["members"]:
            raise ValueError("only preservation collections may declare members")
    if collection_count != 1:
        raise ValueError("preservation resolution requires exactly one collection")
    return resolution


def preservation_capture_requests(
    resolution: dict,
    repo_root: Path,
    knowledge_root: Path,
) -> list[dict]:
    knowledge_root = _knowledge_root(repo_root, knowledge_root)
    requests = []
    for page in resolution["pages"]:
        source = knowledge_root.joinpath(*PurePosixPath(page["source_path"]).parts)
        requests.append(
            {
                "artifact": source,
                "source_type": "clipping",
                "source_id": _source_id(page["source_path"]),
                "primary_source": _source_locator(page["source_path"]),
                "media_type": "text/markdown",
                "created_at": resolution["capture_created_at"],
                "raw_root": repo_root / "raw",
                "expected_sha256": page["source_sha256"],
            }
        )
    return requests


def build_preservation_plan(
    resolution: dict,
    inventory: dict,
    repo_root: Path,
    knowledge_root: Path,
    manifest_verifier: Callable[[Path], dict],
) -> dict:
    knowledge_root = _knowledge_root(repo_root, knowledge_root)
    moved = {
        page["source_path"]: page["target_path"]
        for page in resolution["pages"]
        if page["source_path"] != page["target_path"]
    }
    operations = []
    for page in resolution["pages"]:
        source = knowledge_root.joinpath(*PurePosixPath(page["source_path"]).parts)
        legacy_text = _preservation_payload_bytes(source).decode("utf-8")
        legacy_properties, _ = inspect_markdown(source, legacy_text)
        legacy_lines = legacy_text.splitlines()
        try:
            frontmatter_end = legacy_lines.index("---", 1) + 1
        except ValueError as exc:
            raise ValueError(
                f"legacy frontmatter closing delimiter missing: {source}"
            ) from exc
        body_lines = legacy_lines[frontmatter_end:]
        digest = page["source_sha256"]
        manifest_relative = (
            f"raw/sources/clipping/{_source_id(page['source_path'])}/"
            f"{digest}/manifest.json"
        )
        manifest = manifest_verifier(repo_root / manifest_relative)
        if (
            manifest["artifact_digest"] != f"sha256:{digest}"
            or manifest["primary_source"] != _source_locator(page["source_path"])
            or manifest["created_at"] != resolution["capture_created_at"]
        ):
            raise ValueError(
                f"preservation manifest binding mismatch: {page['source_path']}"
            )
        target_properties = {
            "title": legacy_properties["title"],
            "page_type": page["page_type"],
            "tags": legacy_properties["tags"],
        }
        if "aliases" in legacy_properties:
            target_properties["aliases"] = legacy_properties["aliases"]
        target_properties.update(
            {
                "date_created": legacy_properties["date_created"],
                "date_updated": legacy_properties["date_updated"],
                "source_paths": [manifest_relative],
                "summary": legacy_properties["summary"],
            }
        )
        try:
            rendered = render_preserved_document(
                properties=target_properties,
                legacy_body_lines=body_lines,
                legacy_frontmatter_end_line=frontmatter_end,
                required_sections=section_contract(page["page_type"]),
                source_manifest=manifest_relative,
                members=page["members"],
                path_replacements=moved,
            )
        except ValueError as exc:
            raise ValueError(
                f"preservation render failed for {page['source_path']}: {exc}"
            ) from exc
        parsed = parse_markdown(Path(page["target_path"]), rendered.decode("utf-8"))
        if parsed["claims"] or parsed["relations"]:
            raise ValueError("preservation renderer must not infer claims or relations")
        operations.append(
            {
                "source_path": page["source_path"],
                "target_path": page["target_path"],
                "source_sha256": digest,
                "target_sha256": hashlib.sha256(rendered).hexdigest(),
                "target_mode": stat.S_IMODE(source.lstat().st_mode),
                "content_base64": base64.b64encode(rendered).decode("ascii"),
            }
        )
    plan = {
        "schema_version": "1.0",
        "mode": "resolved",
        "resolution_mode": "preservation",
        "knowledge_root": "wiki",
        "repository_head": inventory["repository_head"],
        "inventory_plan_sha256": hashlib.sha256(plan_bytes(inventory)).hexdigest(),
        "base_tree_sha256": inventory["wiki_tree_sha256"],
        "expected_target_tree_sha256": "0" * 64,
        "source_canonical_universe": inventory["canonical_universe"],
        "target_canonical_universe": [
            page["target_path"] for page in resolution["pages"]
        ],
        "unresolved_decisions": [],
        "operations": operations,
    }
    temporary = Path(
        tempfile.mkdtemp(prefix=".wiki-preservation-plan-", dir=knowledge_root.parent)
    )
    temporary.rmdir()
    try:
        _build_candidate(plan, knowledge_root, temporary)
        plan["expected_target_tree_sha256"] = build_tree_manifest(temporary)[
            "tree_sha256"
        ]
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    _validate_resolved_document(plan_bytes(plan))
    return plan


def _validate_resolved_document(raw: bytes) -> dict:
    try:
        plan = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid migration plan JSON: {exc}") from exc
    schema = json.loads(MIGRATION_SCHEMA.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(plan),
        key=lambda error: list(error.path),
    )
    if errors:
        raise ValueError(f"invalid resolved migration plan: {errors[0].message}")
    if plan["resolution_mode"] == "generic" and any(
        _operation_declares_preservation_manifest(operation)
        for operation in plan["operations"]
    ):
        raise ValueError(
            "resolved plan with preservation manifests cannot declare generic mode"
        )
    return plan


def _operation_declares_preservation_manifest(operation: dict) -> bool:
    try:
        rendered = base64.b64decode(operation["content_base64"], validate=True).decode(
            "utf-8"
        )
        properties, _ = inspect_markdown(
            Path(operation["target_path"]), rendered
        )
    except (binascii.Error, KeyError, UnicodeDecodeError, KnowledgeSchemaError):
        return False
    source_paths = properties.get("source_paths")
    expected = (
        f"raw/sources/clipping/{_source_id(operation['source_path'])}/"
        f"{operation['source_sha256']}/manifest.json"
    )
    return isinstance(source_paths, list) and expected in source_paths


def load_resolved_plan(
    plan_path: Path, repo_root: Path, knowledge_root: Path
) -> tuple[dict, bytes, str]:
    raw = plan_path.read_bytes()
    plan = _validate_resolved_document(raw)
    knowledge_root = _knowledge_root(repo_root, knowledge_root)
    if plan["knowledge_root"] != str(knowledge_root.relative_to(repo_root.resolve())):
        raise ValueError("resolved plan knowledge_root does not match requested root")
    inventory = build_migration_plan(repo_root, knowledge_root)
    if plan["source_canonical_universe"] != inventory["canonical_universe"]:
        raise ValueError(
            "resolved plan does not cover the exact current canonical universe"
        )
    if plan["base_tree_sha256"] != inventory["wiki_tree_sha256"]:
        raise ValueError("resolved plan base tree is stale")
    if plan["repository_head"] != inventory["repository_head"]:
        raise ValueError("resolved plan repository HEAD is stale")
    if (
        plan["inventory_plan_sha256"]
        != hashlib.sha256(plan_bytes(inventory)).hexdigest()
    ):
        raise ValueError("resolved plan inventory digest mismatch")
    operations = plan["operations"]
    if [item["source_path"] for item in operations] != plan[
        "source_canonical_universe"
    ]:
        raise ValueError(
            "resolved plan operations must cover source universe in exact order"
        )
    targets = [item["target_path"] for item in operations]
    target_stems = [PurePosixPath(target).stem for target in targets]
    if (
        targets != plan["target_canonical_universe"]
        or len(targets) != len(set(targets))
        or len(targets) != len({target.casefold() for target in targets})
        or len(target_stems) != len(set(target_stems))
        or len(target_stems)
        != len({target_stem.casefold() for target_stem in target_stems})
    ):
        raise ValueError("resolved plan target universe must be ordered and unique")
    source_paths = set(plan["source_canonical_universe"])
    reserved_stems = {Path(path).stem for path in inventory["exclusions"]}
    for operation in operations:
        source_relative = _safe_relative(operation["source_path"])
        target_relative = _safe_relative(operation["target_path"])
        source = knowledge_root.joinpath(*source_relative.parts)
        if source.suffix != ".md" or target_relative.suffix != ".md":
            raise ValueError("migration operations must map Markdown pages")
        if not KEBAB_RE.fullmatch(target_relative.stem):
            raise ValueError(
                f"resolved plan target ID must be kebab-case: {target_relative.stem}"
            )
        if target_relative.stem.casefold() in {
            stem.casefold() for stem in reserved_stems
        }:
            raise ValueError(
                f"resolved plan target uses a reserved page ID: {target_relative.stem}"
            )
        target = knowledge_root.joinpath(*target_relative.parts)
        if target.exists() and operation["target_path"] not in source_paths:
            raise ValueError(
                "resolved plan target would replace a non-canonical path: "
                f"{target_relative}"
            )
        source_bytes = source.read_bytes()
        if _operation_declares_preservation_manifest(operation):
            source_bytes = normalize_local_user_paths(source_bytes)
        if hashlib.sha256(source_bytes).hexdigest() != operation["source_sha256"]:
            raise ValueError(f"resolved plan source digest is stale: {source_relative}")
        source_mode = stat.S_IMODE(source.lstat().st_mode)
        if source_mode & 0o7111:
            raise ValueError(
                "canonical Markdown mode cannot be privileged or executable: "
                f"{source_relative}"
            )
        if operation["target_mode"] != source_mode:
            raise ValueError(
                f"resolved plan cannot change file mode: {source_relative}"
            )
        try:
            rendered = base64.b64decode(operation["content_base64"], validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ValueError(
                f"invalid target content encoding: {target_relative}"
            ) from exc
        if hashlib.sha256(rendered).hexdigest() != operation["target_sha256"]:
            raise ValueError(f"resolved plan target digest mismatch: {target_relative}")
    return plan, raw, hashlib.sha256(raw).hexdigest()


def _tar_info(
    name: str, mode: int, size: int = 0, directory: bool = False
) -> tarfile.TarInfo:
    if directory and not name.endswith("/"):
        name += "/"
    info = tarfile.TarInfo(name)
    info.type = tarfile.DIRTYPE if directory else tarfile.REGTYPE
    info.mode = mode
    info.size = 0 if directory else size
    info.mtime = 0
    info.uid = info.gid = 0
    info.uname = info.gname = ""
    return info


def create_backup(
    plan_path: Path,
    backup_path: Path,
    repo_root: Path,
    knowledge_root: Path,
) -> dict:
    knowledge_root = _knowledge_root(repo_root, knowledge_root)
    backup_path = _outside_knowledge_root(
        knowledge_root.resolve(), backup_path, "backup"
    )
    _, raw_plan, plan_sha = load_resolved_plan(plan_path, repo_root, knowledge_root)
    tree = build_tree_manifest(knowledge_root)
    descriptor = {
        "schema_version": "1.0",
        "plan_sha256": plan_sha,
        "tree_manifest": tree,
    }
    temporary = backup_path.with_name(f".{backup_path.name}.{os.getpid()}.tmp")
    if temporary.exists():
        raise ValueError(f"stale backup temporary file exists: {temporary}")
    try:
        with temporary.open("xb") as output:
            with tarfile.open(
                fileobj=output, mode="w", format=tarfile.PAX_FORMAT
            ) as archive:
                descriptor_bytes = _canonical_json(descriptor)
                archive.addfile(
                    _tar_info("manifest.json", 0o644, len(descriptor_bytes)),
                    io.BytesIO(descriptor_bytes),
                )
                archive.addfile(
                    _tar_info("plan.json", 0o644, len(raw_plan)),
                    io.BytesIO(raw_plan),
                )
                for entry in tree["entries"]:
                    name = f"tree/{entry['path']}"
                    if entry["kind"] == "directory":
                        archive.addfile(
                            _tar_info(name, int(entry["mode"]), directory=True)
                        )
                    else:
                        relative = PurePosixPath(str(entry["path"]))
                        data = knowledge_root.joinpath(*relative.parts).read_bytes()
                        archive.addfile(
                            _tar_info(name, int(entry["mode"]), len(data)),
                            io.BytesIO(data),
                        )
            output.flush()
            os.fsync(output.fileno())
        staged_descriptor, staged_plan, staged_members = _backup_members(temporary)
        if staged_descriptor != descriptor or staged_plan != raw_plan:
            raise ValueError("staged backup descriptor or plan mismatch")
        _verify_backup_descriptor(temporary, staged_descriptor, staged_members)
        if build_tree_manifest(knowledge_root) != tree:
            raise ValueError("knowledge tree changed while backup was created")
        os.link(temporary, backup_path)
        fsync_directory(backup_path.parent)
    finally:
        if temporary.exists():
            temporary.unlink()
    return descriptor


def _backup_members(
    backup_path: Path,
) -> tuple[dict, bytes, dict[str, tarfile.TarInfo]]:
    with tarfile.open(backup_path, "r") as archive:
        by_name: dict[str, tarfile.TarInfo] = {}
        casefold_names: set[str] = set()
        for member in archive.getmembers():
            name = member.name.rstrip("/")
            if (
                name in by_name
                or name.casefold() in casefold_names
                or not (member.isfile() or member.isdir())
            ):
                raise ValueError(f"invalid or duplicate backup member: {member.name}")
            _safe_relative(name)
            by_name[name] = member
            casefold_names.add(name.casefold())
        if {"manifest.json", "plan.json"} - set(by_name):
            raise ValueError("backup is missing manifest.json or plan.json")
        manifest_handle = archive.extractfile(by_name["manifest.json"])
        plan_handle = archive.extractfile(by_name["plan.json"])
        if manifest_handle is None or plan_handle is None:
            raise ValueError("backup descriptors must be regular files")
        descriptor = json.loads(manifest_handle.read())
        embedded_plan = plan_handle.read()
    return descriptor, embedded_plan, by_name


def _verify_backup_descriptor(
    backup_path: Path, descriptor: dict, by_name: dict[str, tarfile.TarInfo]
) -> None:
    tree = descriptor.get("tree_manifest")
    if not isinstance(tree, dict) or not isinstance(tree.get("entries"), list):
        raise TypeError("backup tree manifest is invalid")
    manifest_payload = {
        "schema_version": tree.get("schema_version"),
        "root": tree.get("root"),
        "entries": tree["entries"],
    }
    if (
        tree.get("schema_version") != "3.0"
        or tree.get("root", {}).get("kind") != "directory"
        or not isinstance(tree.get("root", {}).get("mode"), int)
    ):
        raise ValueError("backup tree root metadata is invalid")
    if (
        tree.get("tree_sha256")
        != hashlib.sha256(_canonical_json(manifest_payload)).hexdigest()
    ):
        raise ValueError("backup tree manifest digest is invalid")
    expected_names = {"manifest.json", "plan.json"}
    expected_names.update(f"tree/{entry['path']}" for entry in tree["entries"])
    if set(by_name) != expected_names:
        raise ValueError("backup member set does not match tree manifest")
    with tarfile.open(backup_path, "r") as archive:
        for entry in tree["entries"]:
            member = by_name[f"tree/{entry['path']}"]
            if (entry["kind"] == "directory") != member.isdir() or stat.S_IMODE(
                member.mode
            ) != entry["mode"]:
                raise ValueError(f"backup metadata mismatch: {entry['path']}")
            if entry["kind"] == "file":
                handle = archive.extractfile(member)
                if handle is None:
                    raise ValueError(f"backup file is unreadable: {entry['path']}")
                data = handle.read()
                if (
                    len(data) != entry["size"]
                    or hashlib.sha256(data).hexdigest() != entry["sha256"]
                ):
                    raise ValueError(f"backup content mismatch: {entry['path']}")


def verify_backup(
    plan_path: Path,
    backup_path: Path,
    repo_root: Path,
    knowledge_root: Path,
) -> dict:
    knowledge_root = _knowledge_root(repo_root, knowledge_root)
    backup_path = _outside_knowledge_root(
        knowledge_root.resolve(), backup_path, "backup"
    )
    plan, raw_plan, plan_sha = load_resolved_plan(plan_path, repo_root, knowledge_root)
    return _verify_backup_binding(backup_path, plan, raw_plan, plan_sha)


def _verify_backup_binding(
    backup_path: Path,
    plan: dict,
    raw_plan: bytes,
    plan_sha: str,
) -> dict:
    descriptor, embedded_plan, by_name = _backup_members(backup_path)
    if embedded_plan != raw_plan or descriptor.get("plan_sha256") != plan_sha:
        raise ValueError("backup plan binding mismatch")
    tree = descriptor.get("tree_manifest")
    if (
        not isinstance(tree, dict)
        or tree.get("tree_sha256") != plan["base_tree_sha256"]
    ):
        raise ValueError("backup tree binding mismatch")
    _verify_backup_descriptor(backup_path, descriptor, by_name)
    return descriptor


def _write_tree_from_backup(
    backup_path: Path, descriptor: dict, destination: Path
) -> None:
    destination.mkdir(mode=0o700)
    entries = descriptor["tree_manifest"]["entries"]
    with tarfile.open(backup_path, "r") as archive:
        by_name = {member.name.rstrip("/"): member for member in archive.getmembers()}
        for entry in entries:
            if entry["kind"] == "directory":
                path = destination.joinpath(*PurePosixPath(entry["path"]).parts)
                path.mkdir(parents=True, exist_ok=True)
        for entry in entries:
            if entry["kind"] == "file":
                path = destination.joinpath(*PurePosixPath(entry["path"]).parts)
                path.parent.mkdir(parents=True, exist_ok=True)
                handle = archive.extractfile(by_name[f"tree/{entry['path']}"])
                if handle is None:
                    raise ValueError(f"backup file is unreadable: {entry['path']}")
                write_bytes_fsync(path, handle.read())
                chmod_fsync(path, entry["mode"])
    directories = [
        destination.joinpath(*PurePosixPath(entry["path"]).parts)
        for entry in entries
        if entry["kind"] == "directory"
    ]
    for directory in sorted(
        directories, key=lambda path: len(path.parts), reverse=True
    ):
        entry = next(
            item
            for item in entries
            if destination.joinpath(*PurePosixPath(item["path"]).parts) == directory
        )
        chmod_fsync(directory, entry["mode"])
    chmod_fsync(destination, descriptor["tree_manifest"]["root"]["mode"])


def _write_journal(path: Path, value: dict) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    if temporary.exists():
        raise ValueError(f"stale journal temporary file exists: {temporary}")
    write_bytes_fsync(temporary, plan_bytes(value))
    os.replace(temporary, path)
    fsync_directory(path.parent)


def _build_candidate(plan: dict, knowledge_root: Path, destination: Path) -> None:
    source_manifest = build_tree_manifest(knowledge_root)
    destination.mkdir(mode=0o700)
    source_directories: dict[Path, int] = {}
    for entry in source_manifest["entries"]:
        path = destination.joinpath(*PurePosixPath(entry["path"]).parts)
        if entry["kind"] == "directory":
            path.mkdir(parents=True, exist_ok=True, mode=0o700)
            source_directories[path] = entry["mode"]
    for entry in source_manifest["entries"]:
        if entry["kind"] != "file":
            continue
        relative = PurePosixPath(entry["path"])
        source = knowledge_root.joinpath(*relative.parts)
        target = destination.joinpath(*relative.parts)
        target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        write_bytes_fsync(target, source.read_bytes())
        chmod_fsync(target, entry["mode"])
    for operation in plan["operations"]:
        source = destination.joinpath(*PurePosixPath(operation["source_path"]).parts)
        source.unlink()
    for operation in plan["operations"]:
        target = destination.joinpath(*PurePosixPath(operation["target_path"]).parts)
        missing_directories: list[Path] = []
        parent = target.parent
        while parent != destination and not parent.exists():
            missing_directories.append(parent)
            parent = parent.parent
        target.parent.mkdir(parents=True, exist_ok=True)
        for directory in reversed(missing_directories):
            os.chmod(directory, 0o755)
        data = base64.b64decode(operation["content_base64"], validate=True)
        write_bytes_fsync(target, data)
        chmod_fsync(target, operation["target_mode"])
    for directory in sorted(
        (path for path in destination.rglob("*") if path.is_dir()),
        key=lambda path: len(path.parts),
        reverse=True,
    ):
        chmod_fsync(directory, source_directories.get(directory, 0o755))
    chmod_fsync(destination, source_manifest["root"]["mode"])


def _stale_path_references(
    plan: dict,
    repo_root: Path,
    knowledge_root: Path,
    candidate: Path,
    ignored: set[Path],
) -> list[dict[str, object]]:
    moved = [
        (
            operation["source_path"],
            f"wiki/{operation['source_path']}",
            PurePosixPath(operation["source_path"]).stem,
            PurePosixPath(operation["target_path"]).stem,
        )
        for operation in plan["operations"]
        if operation["source_path"] != operation["target_path"]
    ]
    if not moved:
        return []
    findings: list[dict[str, object]] = []
    ignored = {
        *ignored,
        (repo_root / "_meta" / "knowledge-migration-resolution.json").resolve(),
    }
    roots = [candidate]
    roots.extend(
        _cascade_repository_roots(
            repo_root, knowledge_root, excluded_roots={candidate}
        )
    )
    for root in roots:
        paths = [root] if root.is_file() else root.rglob("*")
        for path in paths:
            if not path.is_file() or path.resolve() in ignored or path.is_symlink():
                continue
            if path.resolve() == (candidate / "log.md").resolve():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for source_path, repo_path, source_id, target_id in moved:
                shortened = source_path.removeprefix("domains/information-security/")
                tokens = {source_path, repo_path, shortened}
                if source_id != target_id:
                    tokens.update(
                        {
                            f"[[{source_id}]]",
                            f"[[{source_id}|",
                            f"[[{source_id}#",
                        }
                    )
                pattern = re.compile(
                    "|".join(
                        re.escape(token)
                        for token in sorted(tokens, key=len, reverse=True)
                    )
                )
                occurrences = len(pattern.findall(text))
                if occurrences:
                    findings.append(
                        {
                            "path": str(path),
                            "source_path": source_path,
                            "occurrences": occurrences,
                        }
                    )
    return sorted(
        findings,
        key=lambda item: (str(item["path"]), str(item["source_path"])),
    )


def _historical_log_references(
    plan: dict, candidate: Path
) -> list[dict[str, object]]:
    log_path = candidate / "log.md"
    if not log_path.is_file():
        return []
    text = log_path.read_text(encoding="utf-8")
    findings = []
    for operation in plan["operations"]:
        if operation["source_path"] == operation["target_path"]:
            continue
        source_path = operation["source_path"]
        source_id = PurePosixPath(source_path).stem
        target_id = PurePosixPath(operation["target_path"]).stem
        tokens = {
            source_path,
            f"wiki/{source_path}",
            source_path.removeprefix("domains/information-security/"),
        }
        if source_id != target_id:
            tokens.update(
                {f"[[{source_id}]]", f"[[{source_id}|", f"[[{source_id}#"}
            )
        pattern = re.compile(
            "|".join(
                re.escape(token) for token in sorted(tokens, key=len, reverse=True)
            )
        )
        occurrences = len(pattern.findall(text))
        if occurrences:
            findings.append(
                {
                    "path": "wiki/log.md",
                    "source_path": source_path,
                    "occurrences": occurrences,
                    "classification": "append-only-history",
                }
            )
    return findings


def _cascade_owner(relative: PurePosixPath) -> str:
    value = relative.as_posix()
    question_prefix = "projects/info-sec-engineer-practice/data/question-packs/"
    if value.startswith(question_prefix) and value.endswith(".json"):
        return "canonical-question-pack"
    if value == "projects/info-sec-engineer-practice/practice-data.js":
        return "generated-practice-data"
    if value.startswith("projects/info-sec-engineer-practice/docs/") and value.endswith(
        ".md"
    ):
        return "project-documentation"
    if value == ".claude/resume_prompt.md":
        return "system-handoff"
    if value == "docs/wiki-ingest-architecture.md":
        return "migration-architecture"
    raise ValueError(f"unclassified external migration reference owner: {value}")


def _question_source_refs(value: object) -> list[dict[str, object]]:
    refs: list[dict[str, object]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "sourceRefs" and isinstance(child, list):
                refs.extend(item for item in child if isinstance(item, dict))
            else:
                refs.extend(_question_source_refs(child))
    elif isinstance(value, list):
        for child in value:
            refs.extend(_question_source_refs(child))
    return refs


def _validate_question_pack_rewrite(
    source: bytes,
    target: bytes,
    replacements: dict[str, str],
    candidate: Path,
) -> tuple[int, int]:
    before = json.loads(source)
    after = json.loads(target)
    before_refs = _question_source_refs(before)
    after_refs = _question_source_refs(after)
    if len(before_refs) != len(after_refs):
        raise ValueError("sourceRefs cardinality changed during cascade planning")
    changed = 0
    for old, new in zip(before_refs, after_refs, strict=True):
        old_path = old.get("path")
        expected_path = replacements.get(old_path, old_path)
        if new.get("path") != expected_path:
            raise ValueError("sourceRefs.path rewrite is incomplete")
        for field in ("line", "excerpt", "status"):
            if old.get(field) != new.get(field):
                raise ValueError(f"sourceRefs.{field} changed during path cascade")
        if old_path != expected_path:
            changed += 1
        line = new.get("line")
        excerpt = new.get("excerpt")
        relative = _safe_relative(str(expected_path))
        roots = (
            candidate / "domains" / "information-security",
            candidate,
        )
        existing_targets: list[Path] = []
        for root in roots:
            target = root.joinpath(*relative.parts)
            if not target.exists() and not target.is_symlink():
                continue
            resolved_root = root.resolve()
            resolved_target = target.resolve()
            if (
                target.is_symlink()
                or not resolved_target.is_relative_to(resolved_root)
                or not target.is_file()
            ):
                raise ValueError(f"unsafe staged sourceRef target: {expected_path}")
            relative_target = target.relative_to(root)
            current = root
            for part in relative_target.parts[:-1]:
                current /= part
                if current.is_symlink():
                    raise ValueError(
                        f"unsafe staged sourceRef target: {expected_path}"
                    )
            existing_targets.append(target)
        if (
            len(existing_targets) != 1
            or not isinstance(line, int)
            or line < 1
        ):
            raise ValueError(f"invalid staged sourceRef target: {expected_path}:{line}")
        target_path = existing_targets[0]
        lines = target_path.read_text(encoding="utf-8").splitlines()
        if (
            line > len(lines)
            or not isinstance(excerpt, str)
            or excerpt not in lines[line - 1].strip()
        ):
            raise ValueError(
                f"staged sourceRef excerpt mismatch: {expected_path}:{line}"
            )
    normalized_before = json.loads(source)
    for ref in _question_source_refs(normalized_before):
        path = ref.get("path")
        if isinstance(path, str) and path in replacements:
            ref["path"] = replacements[path]
    if normalized_before != after:
        raise ValueError("question pack changed outside sourceRefs.path")
    return len(after_refs), changed


def _is_reserved_migration_candidate(path: Path, knowledge_root: Path) -> bool:
    prefixes = (
        f".{knowledge_root.name}.migration.",
        f".{knowledge_root.name}.restore.",
    )
    return any(
        path.name.startswith(prefix) and path.name != prefix for prefix in prefixes
    )


def _terminal_journal_candidate_roots(
    repo_root: Path, knowledge_root: Path
) -> set[Path]:
    roots: set[Path] = set()
    for journal_path in repo_root.iterdir():
        try:
            mode = journal_path.lstat().st_mode
        except OSError:
            continue
        if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
            continue
        try:
            raw = journal_path.read_bytes()
            journal = json.loads(raw)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        if not isinstance(journal, dict) or raw != plan_bytes(journal):
            continue
        keys = set(journal)
        if not (
            (
                journal.get("schema_version") == "1.0"
                and keys == TRANSACTION_JOURNAL_V1_FIELDS
            )
            or (
                journal.get("schema_version") == "2.0"
                and keys == TRANSACTION_JOURNAL_V2_FIELDS
            )
        ):
            continue
        if journal.get("state") not in {"COMMITTED", "ABORTED"}:
            continue
        operation = journal.get("operation")
        if operation not in {"apply", "restore"}:
            continue
        if journal.get("knowledge_root") != str(knowledge_root):
            continue
        digests = [
            journal.get("plan_sha256"),
            journal.get("base_tree_sha256"),
            journal.get("target_tree_sha256"),
        ]
        if journal.get("schema_version") == "2.0":
            digests.append(journal.get("cascade_plan_sha256"))
        if any(
            not isinstance(digest, str)
            or re.fullmatch(r"[a-f0-9]{64}", digest) is None
            for digest in digests
        ):
            continue
        candidate_value = journal.get("candidate_root")
        if not isinstance(candidate_value, str):
            continue
        candidate = Path(candidate_value)
        candidate_kind = "migration" if operation == "apply" else "restore"
        prefix = f".{knowledge_root.name}.{candidate_kind}."
        if (
            not candidate.is_absolute()
            or candidate.parent != knowledge_root.parent
            or not candidate.name.startswith(prefix)
            or candidate.name == prefix
        ):
            continue
        try:
            candidate_hash = build_tree_manifest(candidate)["tree_sha256"]
        except (OSError, ValueError):
            continue
        expected_hash = (
            journal["base_tree_sha256"]
            if journal["state"] == "COMMITTED"
            else journal["target_tree_sha256"]
        )
        if candidate_hash == expected_hash:
            roots.add(candidate.resolve())
    return roots


def _cascade_repository_roots(
    repo_root: Path,
    knowledge_root: Path,
    excluded_roots: set[Path] | None = None,
) -> list[Path]:
    excluded = {path.resolve() for path in (excluded_roots or set())}
    terminal_candidates = _terminal_journal_candidate_roots(
        repo_root, knowledge_root
    )
    roots: list[Path] = []
    for path in repo_root.iterdir():
        if path == knowledge_root or path.name in {".git", "raw"}:
            continue
        if path.resolve() in excluded:
            continue
        if _is_reserved_migration_candidate(path, knowledge_root):
            try:
                mode = path.lstat().st_mode
            except OSError as exc:
                raise ValueError(
                    f"reserved migration candidate is unavailable: {path}"
                ) from exc
            if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
                raise ValueError(
                    f"reserved migration candidate is not a regular directory: {path}"
                )
            try:
                _regular_tree_snapshot(path)
            except ValueError as exc:
                raise ValueError(
                    f"reserved migration candidate is not a regular tree: {path}"
                ) from exc
            if path.resolve() in terminal_candidates:
                continue
        roots.append(path)
    return roots


def _copy_cascade_stage(
    repo_root: Path,
    stage: Path,
    excluded_roots: set[Path] | None = None,
    *,
    knowledge_root: Path | None = None,
) -> None:
    excluded = {path.resolve() for path in (excluded_roots or set())}
    knowledge_root = (knowledge_root or repo_root / "wiki").resolve()
    for source in _cascade_repository_roots(
        repo_root, knowledge_root, excluded
    ):
        target = stage / source.name
        if source.is_symlink():
            raise ValueError(f"cascade input contains symlink: {source}")
        elif source.is_dir():
            _regular_tree_snapshot(source)
            shutil.copytree(source, target, symlinks=True)
        elif source.is_file():
            shutil.copy2(source, target)
        else:
            raise ValueError(f"cascade input contains special file: {source}")
    clipping = repo_root / "raw" / "sources" / "clipping"
    if clipping.is_dir():
        _regular_tree_snapshot(clipping)
        shutil.copytree(
            clipping, stage / "raw" / "sources" / "clipping", symlinks=True
        )
    _regular_tree_snapshot(stage)


def _regular_tree_snapshot(root: Path) -> dict[str, tuple[str, int, str | None]]:
    try:
        root_mode = root.lstat().st_mode
    except OSError as exc:
        raise ValueError(f"snapshot root is unavailable: {root}") from exc
    if stat.S_ISLNK(root_mode) or not stat.S_ISDIR(root_mode):
        raise ValueError(f"snapshot root is not a regular directory: {root}")
    root = root.resolve()
    snapshot: dict[str, tuple[str, int, str | None]] = {}
    for directory, names, files in os.walk(root, followlinks=False):
        parent = Path(directory)
        for name in names:
            path = parent / name
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
                raise ValueError(f"cascade tree contains non-directory: {path}")
            snapshot[path.relative_to(root).as_posix()] = (
                "directory",
                stat.S_IMODE(mode),
                None,
            )
        for name in files:
            path = parent / name
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
                raise ValueError(f"cascade tree contains non-regular file: {path}")
            snapshot[path.relative_to(root).as_posix()] = (
                "file",
                stat.S_IMODE(mode),
                hashlib.sha256(path.read_bytes()).hexdigest(),
            )
    return snapshot


def _changed_snapshot_paths(
    before: dict[str, tuple[str, int, str | None]],
    after: dict[str, tuple[str, int, str | None]],
) -> set[str]:
    return {
        path
        for path in before.keys() | after.keys()
        if before.get(path) != after.get(path)
    }


def _cascade_diff(operations: list[dict[str, object]]) -> bytes:
    chunks: list[str] = []
    for operation in operations:
        before = base64.b64decode(str(operation["base_content_base64"])).decode(
            "utf-8"
        )
        after = base64.b64decode(str(operation["target_content_base64"])).decode(
            "utf-8"
        )
        path = str(operation["path"])
        chunks.extend(
            difflib.unified_diff(
                before.splitlines(keepends=True),
                after.splitlines(keepends=True),
                fromfile=f"a/{path}",
                tofile=f"b/{path}",
            )
        )
    return "".join(chunks).encode("utf-8")


def build_reference_cascade_plan(
    plan_path: Path,
    candidate: Path,
    repo_root: Path,
    knowledge_root: Path,
) -> tuple[dict, bytes]:
    knowledge_root = _knowledge_root(repo_root, knowledge_root)
    plan, _, migration_plan_sha = load_resolved_plan(
        plan_path, repo_root, knowledge_root
    )
    _regular_tree_snapshot(candidate)
    candidate = candidate.resolve()
    if build_tree_manifest(candidate)["tree_sha256"] != plan[
        "expected_target_tree_sha256"
    ]:
        raise ValueError("cascade candidate tree digest does not match resolved plan")
    findings = _stale_path_references(
        plan, repo_root, knowledge_root, candidate, {plan_path.resolve()}
    )
    historical = _historical_log_references(plan, candidate)
    grouped: dict[Path, dict[str, object]] = {}
    for finding in findings:
        path = Path(str(finding["path"])).resolve()
        if path.is_relative_to(candidate):
            raise ValueError(f"active stale reference remains inside candidate: {path}")
        relative = path.relative_to(repo_root.resolve())
        owner = _cascade_owner(PurePosixPath(relative.as_posix()))
        entry = grouped.setdefault(
            path,
            {"path": relative.as_posix(), "owner": owner, "occurrences": 0},
        )
        if entry["owner"] != owner:
            raise ValueError(f"multiple owners for cascade path: {relative}")
        entry["occurrences"] = int(entry["occurrences"]) + int(
            finding["occurrences"]
        )

    replacements = {
        operation["source_path"]: operation["target_path"]
        for operation in plan["operations"]
        if operation["source_path"] != operation["target_path"]
    }
    short_replacements = {
        source.removeprefix("domains/information-security/"): target.removeprefix(
            "domains/information-security/"
        )
        for source, target in replacements.items()
    }
    staged = Path(tempfile.mkdtemp(prefix="knowledge-reference-cascade."))
    try:
        _copy_cascade_stage(
            repo_root, staged, {candidate}, knowledge_root=knowledge_root
        )
        shutil.copytree(candidate, staged / "wiki", symlinks=True)
        _regular_tree_snapshot(staged)
        operations: list[dict[str, object]] = []
        source_ref_total = 0
        source_ref_changed = 0
        generated_path: Path | None = None
        for path, entry in sorted(
            grouped.items(), key=lambda item: str(item[1]["path"])
        ):
            if entry["owner"] == "generated-practice-data":
                generated_path = path
                continue
            source = path.read_bytes()
            text = source.decode("utf-8")
            target = replace_paths(text, replacements).encode("utf-8")
            if target == source:
                raise ValueError(f"cascade operation made no change: {entry['path']}")
            if entry["owner"] == "canonical-question-pack":
                total, changed = _validate_question_pack_rewrite(
                    source, target, short_replacements, candidate
                )
                source_ref_total += total
                source_ref_changed += changed
            staged_path = staged / str(entry["path"])
            staged_path.write_bytes(target)
            operations.append(
                {
                    **entry,
                    "action": "replace-paths",
                    "base_sha256": hashlib.sha256(source).hexdigest(),
                    "target_sha256": hashlib.sha256(target).hexdigest(),
                    "base_mode": stat.S_IMODE(path.lstat().st_mode),
                    "target_mode": stat.S_IMODE(staged_path.lstat().st_mode),
                    "base_content_base64": base64.b64encode(source).decode("ascii"),
                    "target_content_base64": base64.b64encode(target).decode("ascii"),
                }
            )
        if generated_path is None:
            raise ValueError("generated practice-data owner was not found")
        generator = staged.joinpath(*CASCADE_PRACTICE_GENERATOR.parts)
        baseline_generator = repo_root.joinpath(*CASCADE_PRACTICE_GENERATOR.parts)
        baseline_root = baseline_generator.parent.parent
        baseline_before = _regular_tree_snapshot(baseline_root)
        no_bytecode_env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        baseline = subprocess.run(
            [sys.executable, "-B", os.fspath(baseline_generator), "--check"],
            cwd=baseline_root,
            check=False,
            capture_output=True,
            text=True,
            env=no_bytecode_env,
        )
        if baseline.returncode:
            raise ValueError(
                "current generated practice data is stale before cascade: "
                + baseline.stderr.strip()
            )
        if _regular_tree_snapshot(baseline_root) != baseline_before:
            raise ValueError("baseline generator check modified the repository")
        stage_before_generation = _regular_tree_snapshot(staged)
        completed = subprocess.run(
            [sys.executable, "-B", os.fspath(generator)],
            cwd=generator.parent.parent,
            check=False,
            capture_output=True,
            text=True,
            env=no_bytecode_env,
        )
        if completed.returncode:
            raise ValueError(
                "isolated practice-data regeneration failed: "
                + completed.stderr.strip()
            )
        stage_after_generation = _regular_tree_snapshot(staged)
        expected_generator_changes = {
            "projects/info-sec-engineer-practice/practice-data.js",
            "projects/info-sec-engineer-practice/data/generated/past-exams.json",
        }
        actual_generator_changes = _changed_snapshot_paths(
            stage_before_generation, stage_after_generation
        )
        if actual_generator_changes != expected_generator_changes:
            raise ValueError(
                "generator write-set differs from approved outputs: "
                f"{sorted(actual_generator_changes)}"
            )
        generated_relative = grouped[generated_path]["path"]
        generated_source = generated_path.read_bytes()
        generated_target = (staged / str(generated_relative)).read_bytes()
        operations.append(
            {
                **grouped[generated_path],
                "action": "regenerate",
                "command": CASCADE_PRACTICE_COMMAND,
                "base_sha256": hashlib.sha256(generated_source).hexdigest(),
                "target_sha256": hashlib.sha256(generated_target).hexdigest(),
                "base_mode": stat.S_IMODE(generated_path.lstat().st_mode),
                "target_mode": stat.S_IMODE(
                    (staged / str(generated_relative)).lstat().st_mode
                ),
                "base_content_base64": base64.b64encode(generated_source).decode(
                    "ascii"
                ),
                "target_content_base64": base64.b64encode(generated_target).decode(
                    "ascii"
                ),
            }
        )
        past_exams_relative = PurePosixPath(
            "projects/info-sec-engineer-practice/data/generated/past-exams.json"
        )
        past_exams_source_path = repo_root.joinpath(*past_exams_relative.parts)
        past_exams_target_path = staged.joinpath(*past_exams_relative.parts)
        past_exams_source = past_exams_source_path.read_bytes()
        past_exams_target = past_exams_target_path.read_bytes()
        if past_exams_source != past_exams_target:
            operations.append(
                {
                    "path": past_exams_relative.as_posix(),
                    "owner": "generated-past-exams",
                    "occurrences": 0,
                    "action": "regenerate",
                    "command": CASCADE_PRACTICE_COMMAND,
                    "base_sha256": hashlib.sha256(past_exams_source).hexdigest(),
                    "target_sha256": hashlib.sha256(past_exams_target).hexdigest(),
                    "base_mode": stat.S_IMODE(
                        past_exams_source_path.lstat().st_mode
                    ),
                    "target_mode": stat.S_IMODE(
                        past_exams_target_path.lstat().st_mode
                    ),
                    "base_content_base64": base64.b64encode(past_exams_source).decode(
                        "ascii"
                    ),
                    "target_content_base64": base64.b64encode(
                        past_exams_target
                    ).decode("ascii"),
                }
            )
        operations.sort(key=lambda operation: str(operation["path"]))
        staged_findings = _stale_path_references(
            plan, staged, staged / "wiki", staged / "wiki", set()
        )
        if staged_findings:
            raise ValueError(
                "staged cascade leaves stale references: "
                + "; ".join(str(item["path"]) for item in staged_findings)
            )
        cascade = {
            "schema_version": "1.0",
            "migration_plan_sha256": migration_plan_sha,
            "target_tree_sha256": plan["expected_target_tree_sha256"],
            "observed_reference_groups": len(findings) + len(historical),
            "observed_reference_occurrences": sum(
                int(item["occurrences"]) for item in findings + historical
            ),
            "active_reference_groups": len(findings),
            "active_reference_occurrences": sum(
                int(item["occurrences"]) for item in findings
            ),
            "historical_exemptions": historical,
            "source_ref_total": source_ref_total,
            "source_ref_path_changes": source_ref_changed,
            "staged_stale_reference_occurrences": 0,
            "scan_policy": {
                "included": [
                    "target candidate tree",
                    "repository top-level roots except explicit exclusions",
                ],
                "excluded": [
                    ".git/**",
                    "raw/** immutable artifacts",
                    "source knowledge root (replaced by target candidate)",
                    "resolved plan input",
                    "_meta/knowledge-migration-resolution.json",
                    "journal-bound terminal migration/restore candidate trees",
                    "candidate/log.md append-only history (reported separately)",
                    "symlinks (cascade staging rejects them)",
                    "non-UTF-8 files",
                ],
                "hidden_paths": "included unless explicitly excluded",
            },
            "operations": operations,
            "apply_requires_combined_transaction": True,
        }
        diff = _cascade_diff(operations)
        cascade["diff_sha256"] = hashlib.sha256(diff).hexdigest()
        return cascade, diff
    finally:
        shutil.rmtree(staged)


def _reject_stale_path_references(
    plan: dict,
    repo_root: Path,
    knowledge_root: Path,
    candidate: Path,
    ignored: set[Path],
) -> None:
    findings = _stale_path_references(
        plan, repo_root, knowledge_root, candidate, ignored
    )
    if findings:
        raise ValueError(
            "stale external migration references remain: "
            + "; ".join(
                f"{item['path']}: {item['source_path']} ({item['occurrences']})"
                for item in findings
            )
        )


def _audit_preservation_candidate(
    plan: dict,
    repo_root: Path,
    knowledge_root: Path,
    candidate: Path,
    manifest_verifier: Callable[[Path], dict],
) -> dict:
    pages = []
    total_members = 0
    for operation in plan["operations"]:
        source = knowledge_root.joinpath(*PurePosixPath(operation["source_path"]).parts)
        target = candidate.joinpath(*PurePosixPath(operation["target_path"]).parts)
        instance = parse_markdown(target)
        source_paths = instance["properties"]["source_paths"]
        if len(source_paths) != 1:
            raise ValueError(
                "preservation candidate requires one manifest: "
                f"{operation['target_path']}"
            )
        manifest_path = repo_root / source_paths[0]
        manifest = manifest_verifier(manifest_path)
        payload = manifest_path.parent / manifest["payload"]
        if (
            payload.read_bytes() != _preservation_payload_bytes(source)
            or manifest["source_type"] != "clipping"
            or manifest["source_id"] != _source_id(operation["source_path"])
            or manifest["primary_source"] != _source_locator(operation["source_path"])
            or instance["claims"]
            or instance["relations"]
        ):
            raise ValueError(
                f"preservation lineage audit failed: {operation['source_path']}"
            )
        total_members += len(instance["members"])
        pages.append(
            {
                "source_path": operation["source_path"],
                "target_path": operation["target_path"],
                "source_sha256": operation["source_sha256"],
                "target_sha256": operation["target_sha256"],
                "manifest_path": source_paths[0],
                "payload_exact": True,
                "claims": 0,
                "relations": 0,
                "members": len(instance["members"]),
            }
        )
    return {
        "pages": pages,
        "page_count": len(pages),
        "payload_exact_count": sum(page["payload_exact"] for page in pages),
        "claim_rows": sum(page["claims"] for page in pages),
        "relation_rows": sum(page["relations"] for page in pages),
        "member_rows": total_members,
    }


def _cascade_expected_owner(path: PurePosixPath) -> str:
    if path.as_posix() == (
        "projects/info-sec-engineer-practice/data/generated/past-exams.json"
    ):
        return "generated-past-exams"
    return _cascade_owner(path)


def _decode_cascade_content(operation: dict, state: str) -> bytes:
    try:
        data = base64.b64decode(
            operation[f"{state}_content_base64"], validate=True
        )
    except (KeyError, TypeError, ValueError, binascii.Error) as exc:
        raise ValueError(f"cascade {state} content is invalid") from exc
    if hashlib.sha256(data).hexdigest() != operation[f"{state}_sha256"]:
        raise ValueError(f"cascade {state} content digest mismatch")
    return data


def _resolve_cascade_path(
    repo_root: Path, value: str, *, require_regular: bool = True
) -> Path:
    relative = _safe_relative(value)
    if relative.parts[0] in {".git", "raw", "wiki"}:
        raise ValueError(f"cascade path is outside the mutable allowlist: {value}")
    path = repo_root.joinpath(*relative.parts)
    current = repo_root
    for part in relative.parts[:-1]:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"cascade parent is not a regular directory: {current}")
        if not current.exists() and not require_regular:
            return path
        if not current.is_dir():
            raise ValueError(f"cascade parent is not a regular directory: {current}")
    if not require_regular:
        return path
    try:
        mode = path.lstat().st_mode
    except OSError as exc:
        raise ValueError(f"cascade path is unavailable: {path}") from exc
    if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
        raise ValueError(f"cascade path is not a regular file: {path}")
    return path


def _load_cascade_plan(
    cascade_plan_path: Path,
    confirm_cascade_plan_sha256: str,
    repo_root: Path,
    knowledge_root: Path,
    plan: dict,
    plan_sha256: str,
    *,
    require_live_paths: bool = True,
) -> tuple[dict, str]:
    cascade_plan_path = _outside_knowledge_root(
        knowledge_root, cascade_plan_path, "cascade plan"
    )
    raw = cascade_plan_path.read_bytes()
    cascade_sha256 = hashlib.sha256(raw).hexdigest()
    if confirm_cascade_plan_sha256 != cascade_sha256:
        raise ValueError("cascade plan confirmation digest mismatch")
    try:
        cascade = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("cascade plan is not valid UTF-8 JSON") from exc
    required = {
        "schema_version",
        "migration_plan_sha256",
        "target_tree_sha256",
        "observed_reference_groups",
        "observed_reference_occurrences",
        "active_reference_groups",
        "active_reference_occurrences",
        "historical_exemptions",
        "source_ref_total",
        "source_ref_path_changes",
        "staged_stale_reference_occurrences",
        "scan_policy",
        "operations",
        "apply_requires_combined_transaction",
        "diff_sha256",
    }
    if not isinstance(cascade, dict) or set(cascade) != required:
        raise ValueError("cascade plan shape is invalid")
    if (
        cascade["schema_version"] != "1.0"
        or cascade["migration_plan_sha256"] != plan_sha256
        or cascade["target_tree_sha256"]
        != plan["expected_target_tree_sha256"]
        or cascade["staged_stale_reference_occurrences"] != 0
        or cascade["apply_requires_combined_transaction"] is not True
    ):
        raise ValueError("cascade plan binding is invalid")
    count_fields = {
        "observed_reference_groups",
        "observed_reference_occurrences",
        "active_reference_groups",
        "active_reference_occurrences",
        "source_ref_total",
        "source_ref_path_changes",
    }
    if any(
        not isinstance(cascade[field], int) or cascade[field] < 0
        for field in count_fields
    ):
        raise ValueError("cascade plan count is invalid")
    if not isinstance(cascade["historical_exemptions"], list) or not isinstance(
        cascade["scan_policy"], dict
    ):
        raise ValueError("cascade plan audit metadata is invalid")
    operations = cascade["operations"]
    if not isinstance(operations, list) or not operations:
        raise ValueError("cascade plan operations are invalid")
    paths: list[str] = []
    for operation in operations:
        common = {
            "path",
            "owner",
            "occurrences",
            "action",
            "base_sha256",
            "target_sha256",
            "base_mode",
            "target_mode",
            "base_content_base64",
            "target_content_base64",
        }
        if not isinstance(operation, dict):
            raise ValueError("cascade operation is invalid")
        expected = common | (
            {"command"} if operation.get("action") == "regenerate" else set()
        )
        if set(operation) != expected:
            raise ValueError("cascade operation shape is invalid")
        relative = _safe_relative(operation["path"])
        owner = _cascade_expected_owner(relative)
        if operation["owner"] != owner:
            raise ValueError(f"cascade owner mismatch: {relative}")
        expected_action = (
            "regenerate"
            if owner in {"generated-practice-data", "generated-past-exams"}
            else "replace-paths"
        )
        if operation["action"] != expected_action:
            raise ValueError(f"cascade action mismatch: {relative}")
        if (
            expected_action == "regenerate"
            and operation["command"] != CASCADE_PRACTICE_COMMAND
        ):
            raise ValueError(f"cascade generator command mismatch: {relative}")
        if (
            not isinstance(operation["occurrences"], int)
            or operation["occurrences"] < 0
        ):
            raise ValueError(f"cascade occurrence count is invalid: {relative}")
        for state in ("base", "target"):
            digest = operation[f"{state}_sha256"]
            mode = operation[f"{state}_mode"]
            if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest):
                raise ValueError(f"cascade {state} digest is invalid: {relative}")
            if not isinstance(mode, int) or mode < 0 or mode > 0o7777:
                raise ValueError(f"cascade {state} mode is invalid: {relative}")
            _decode_cascade_content(operation, state)
        if operation["base_sha256"] == operation["target_sha256"] and operation[
            "base_mode"
        ] == operation["target_mode"]:
            raise ValueError(f"cascade operation has no change: {relative}")
        _resolve_cascade_path(
            repo_root,
            relative.as_posix(),
            require_regular=require_live_paths,
        )
        paths.append(relative.as_posix())
    if paths != sorted(paths) or len(paths) != len(set(paths)):
        raise ValueError("cascade operation paths must be unique and sorted")
    if cascade["diff_sha256"] != hashlib.sha256(
        _cascade_diff(operations)
    ).hexdigest():
        raise ValueError("cascade diff digest mismatch")
    return cascade, cascade_sha256


def _external_operation_state(path: Path, operation: dict) -> str:
    try:
        metadata = path.lstat()
    except OSError:
        return "unknown"
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        return "unknown"
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    mode = stat.S_IMODE(metadata.st_mode)
    for state in ("base", "target"):
        if (
            digest == operation[f"{state}_sha256"]
            and mode == operation[f"{state}_mode"]
        ):
            return state
    return "unknown"


def _external_state(cascade: dict, repo_root: Path) -> str:
    states = {
        _external_operation_state(
            _resolve_cascade_path(
                repo_root, operation["path"], require_regular=False
            ),
            operation,
        )
        for operation in cascade["operations"]
    }
    if "unknown" in states:
        return "unknown"
    if len(states) == 1:
        return states.pop()
    return "mixed"


def _replace_external_file(path: Path, data: bytes, mode: int) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.migration.", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            os.fchmod(handle.fileno(), mode)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        fsync_directory(path.parent)
    finally:
        temporary.unlink(missing_ok=True)


def _write_external_state(cascade: dict, repo_root: Path, target_state: str) -> None:
    for operation in cascade["operations"]:
        path = _resolve_cascade_path(repo_root, operation["path"])
        if _external_operation_state(path, operation) == "unknown":
            raise ValueError(f"cascade external file has an unknown state: {path}")
        _replace_external_file(
            path,
            _decode_cascade_content(operation, target_state),
            operation[f"{target_state}_mode"],
        )


def _validate_combined_candidate(
    plan: dict,
    cascade: dict,
    candidate: Path,
    repo_root: Path,
    ignored_live_paths: set[Path],
    candidate_check: Callable[[Path, Path, list[Path]], None],
) -> None:
    staged = Path(tempfile.mkdtemp(prefix="knowledge-combined-migration."))
    try:
        _copy_cascade_stage(
            repo_root,
            staged,
            {candidate},
            knowledge_root=repo_root.joinpath(
                *PurePosixPath(plan["knowledge_root"]).parts
            ),
        )
        shutil.copytree(candidate, staged / "wiki", symlinks=True)
        for operation in cascade["operations"]:
            staged_path = staged.joinpath(*PurePosixPath(operation["path"]).parts)
            _replace_external_file(
                staged_path,
                _decode_cascade_content(operation, "target"),
                operation["target_mode"],
            )
        ignored_staged = {
            (staged / path.relative_to(repo_root)).resolve()
            for path in ignored_live_paths
            if path.is_relative_to(repo_root)
        }
        _reject_stale_path_references(
            plan, staged, staged / "wiki", staged / "wiki", ignored_staged
        )
        canonical_paths = [
            staged.joinpath("wiki", *PurePosixPath(path).parts)
            for path in (
                plan["target_canonical_universe"]
                + plan["source_canonical_universe"]
            )
        ]
        candidate_check(staged / "wiki", staged, canonical_paths)
        if any(
            operation["action"] == "regenerate"
            for operation in cascade["operations"]
        ):
            generator = staged.joinpath(*CASCADE_PRACTICE_GENERATOR.parts)
            completed = subprocess.run(
                [sys.executable, "-B", os.fspath(generator), "--check"],
                cwd=generator.parent.parent,
                check=False,
                capture_output=True,
                text=True,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )
            if completed.returncode:
                raise ValueError(
                    "combined staged generator check failed: "
                    + completed.stderr.strip()
                )
        _reject_stale_path_references(
            plan, staged, staged / "wiki", staged / "wiki", ignored_staged
        )
    finally:
        shutil.rmtree(staged)


def preview_resolved_plan(
    plan_path: Path,
    destination: Path,
    repo_root: Path,
    knowledge_root: Path,
    candidate_check: Callable[[Path, Path, list[Path]], None],
    manifest_verifier: Callable[[Path], dict] | None = None,
) -> dict:
    knowledge_root = _knowledge_root(repo_root, knowledge_root)
    destination = _outside_knowledge_root(
        knowledge_root.resolve(), destination, "preview"
    )
    if destination.exists():
        raise ValueError(f"preview destination already exists: {destination}")
    plan, _, plan_sha = load_resolved_plan(plan_path, repo_root, knowledge_root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    candidate = Path(
        tempfile.mkdtemp(prefix=f".{destination.name}.preview.", dir=destination.parent)
    )
    candidate.rmdir()
    try:
        _build_candidate(plan, knowledge_root, candidate)
        target_tree_sha = build_tree_manifest(candidate)["tree_sha256"]
        if target_tree_sha != plan["expected_target_tree_sha256"]:
            raise ValueError("preview tree digest does not match resolved plan")
        canonical_paths = [
            candidate.joinpath(*PurePosixPath(path).parts)
            for path in plan["target_canonical_universe"]
        ]
        candidate_check(candidate, repo_root, canonical_paths)
        audit_required = plan.get("resolution_mode") == "preservation"
        if audit_required and manifest_verifier is None:
            raise ValueError("preservation preview requires a manifest verifier")
        audit = (
            _audit_preservation_candidate(
                plan, repo_root, knowledge_root, candidate, manifest_verifier
            )
            if audit_required
            else None
        )
        ignored = {plan_path.resolve()}
        impacts = _stale_path_references(
            plan, repo_root, knowledge_root, candidate, ignored
        )
        for impact in impacts:
            impact_path = Path(impact["path"])
            if impact_path.resolve().is_relative_to(candidate.resolve()):
                impact["path"] = str(
                    destination / impact_path.resolve().relative_to(candidate.resolve())
                )
        rename_directory_no_replace(candidate, destination)
        fsync_directory(destination.parent)
    except Exception:
        if candidate.exists():
            shutil.rmtree(candidate)
        raise
    return {
        "schema_version": "1.0",
        "plan_sha256": plan_sha,
        "target_tree_sha256": target_tree_sha,
        "canonical_pages": len(plan["target_canonical_universe"]),
        "structural_verdict": "PASS",
        "preservation_audit": audit,
        "external_reference_findings": impacts,
        "external_reference_occurrences": sum(
            int(item["occurrences"]) for item in impacts
        ),
        "apply_ready": not impacts,
        "preview_root": str(destination),
    }


def apply_resolved_plan(
    plan_path: Path,
    backup_path: Path,
    repo_root: Path,
    knowledge_root: Path,
    confirm_plan_sha256: str,
    journal_path: Path,
    candidate_check: Callable[[Path, Path, list[Path]], None],
    manifest_verifier: Callable[[Path], dict] | None = None,
    cascade_plan_path: Path | None = None,
    confirm_cascade_plan_sha256: str | None = None,
) -> dict:
    knowledge_root = _knowledge_root(repo_root, knowledge_root)
    plan_path = _outside_knowledge_root(
        knowledge_root.resolve(), plan_path, "resolved plan"
    )
    backup_path = _outside_knowledge_root(
        knowledge_root.resolve(), backup_path, "backup"
    )
    journal_path = _journal_path(knowledge_root.resolve(), journal_path)
    plan, raw_plan, plan_sha = load_resolved_plan(plan_path, repo_root, knowledge_root)
    if confirm_plan_sha256 != plan_sha:
        raise ValueError("plan confirmation digest mismatch")
    _verify_backup_binding(backup_path, plan, raw_plan, plan_sha)
    if (cascade_plan_path is None) != (confirm_cascade_plan_sha256 is None):
        raise ValueError(
            "cascade plan and confirmation digest must be provided together"
        )
    cascade: dict | None = None
    cascade_sha256: str | None = None
    if cascade_plan_path is not None and confirm_cascade_plan_sha256 is not None:
        cascade, cascade_sha256 = _load_cascade_plan(
            cascade_plan_path,
            confirm_cascade_plan_sha256,
            repo_root.resolve(),
            knowledge_root.resolve(),
            plan,
            plan_sha,
        )
        cascade_plan_path = cascade_plan_path.resolve()
        if _external_state(cascade, repo_root.resolve()) != "base":
            raise ValueError("combined apply requires all external files at base state")
    if journal_path.exists():
        raise ValueError(f"transaction journal already exists: {journal_path}")
    candidate = Path(
        tempfile.mkdtemp(
            prefix=f".{knowledge_root.name}.migration.",
            dir=knowledge_root.parent,
        )
    )
    candidate.rmdir()
    swapped = False
    external_write_started = False
    conflict = False
    journal = {
        "schema_version": "2.0" if cascade is not None else "1.0",
        "operation": "apply",
        "state": "PREPARED",
        "knowledge_root": str(knowledge_root.resolve()),
        "candidate_root": str(candidate.resolve()),
        "plan_sha256": plan_sha,
        "base_tree_sha256": plan["base_tree_sha256"],
        "target_tree_sha256": plan["expected_target_tree_sha256"],
    }
    if cascade_sha256 is not None:
        journal["cascade_plan_sha256"] = cascade_sha256
    journal_written = False
    try:
        if cascade is None:
            _write_journal(journal_path, journal)
            journal_written = True
        _build_candidate(plan, knowledge_root, candidate)
        if (
            build_tree_manifest(candidate)["tree_sha256"]
            != plan["expected_target_tree_sha256"]
        ):
            raise ValueError("candidate tree digest does not match resolved plan")
        if plan.get("resolution_mode") == "preservation":
            if manifest_verifier is None:
                raise ValueError("preservation apply requires a manifest verifier")
            _audit_preservation_candidate(
                plan, repo_root, knowledge_root, candidate, manifest_verifier
            )
        ignored = {
            plan_path.resolve(),
            backup_path.resolve(),
            journal_path.resolve(),
        }
        if cascade_plan_path is not None:
            ignored.add(cascade_plan_path)
        if cascade is None:
            _reject_stale_path_references(
                plan,
                repo_root.resolve(),
                knowledge_root.resolve(),
                candidate,
                ignored,
            )
            candidate_check(
                candidate,
                repo_root,
                [
                    candidate.joinpath(*PurePosixPath(path).parts)
                    for path in (
                        plan["target_canonical_universe"]
                        + plan["source_canonical_universe"]
                    )
                ],
            )
            _reject_stale_path_references(
                plan,
                repo_root.resolve(),
                knowledge_root.resolve(),
                candidate,
                ignored,
            )
        else:
            _validate_combined_candidate(
                plan,
                cascade,
                candidate,
                repo_root.resolve(),
                ignored,
                candidate_check,
            )
            _write_journal(journal_path, journal)
            journal_written = True
            if _external_state(cascade, repo_root.resolve()) != "base":
                raise ValueError("external files changed after combined validation")
            external_write_started = True
            _write_external_state(cascade, repo_root.resolve(), "target")
            journal["state"] = "EXTERNAL_WRITTEN"
            _write_journal(journal_path, journal)
        exchange_directories(knowledge_root, candidate)
        swapped = True
        journal["state"] = "SWAPPED"
        _write_journal(journal_path, journal)
        current_hash = build_tree_manifest(knowledge_root)["tree_sha256"]
        previous_hash = build_tree_manifest(candidate)["tree_sha256"]
        external_matches = cascade is None or _external_state(
            cascade, repo_root.resolve()
        ) == "target"
        if (
            current_hash != plan["expected_target_tree_sha256"]
            or previous_hash != plan["base_tree_sha256"]
            or not external_matches
        ):
            exchange_directories(knowledge_root, candidate)
            swapped = False
            if cascade is not None and _external_state(
                cascade, repo_root.resolve()
            ) in {"base", "target", "mixed"}:
                _write_external_state(cascade, repo_root.resolve(), "base")
                external_write_started = False
            conflict = True
            journal["state"] = "CONFLICT"
            _write_journal(journal_path, journal)
            raise ValueError(
                "concurrent tree mutation detected; both trees were preserved"
            )
        journal["state"] = "COMMITTED"
        _write_journal(journal_path, journal)
        return journal
    except Exception:
        if swapped:
            exchange_directories(knowledge_root, candidate)
        if external_write_started and cascade is not None:
            external_state = _external_state(cascade, repo_root.resolve())
            if external_state in {"base", "target", "mixed"}:
                _write_external_state(cascade, repo_root.resolve(), "base")
            else:
                conflict = True
                journal["state"] = "CONFLICT"
                _write_journal(journal_path, journal)
        if journal_written and not conflict:
            journal["state"] = "ABORTED"
            _write_journal(journal_path, journal)
        raise


def _load_plan_for_restore(
    plan_path: Path, repo_root: Path, knowledge_root: Path
) -> tuple[dict, bytes, str]:
    raw = plan_path.read_bytes()
    plan = _validate_resolved_document(raw)
    if plan["knowledge_root"] != str(
        knowledge_root.resolve().relative_to(repo_root.resolve())
    ):
        raise ValueError("resolved plan knowledge_root does not match requested root")
    return plan, raw, hashlib.sha256(raw).hexdigest()


def _verify_backup_for_restore(plan_path: Path, backup_path: Path, plan: dict) -> dict:
    raw_plan = plan_path.read_bytes()
    descriptor, embedded_plan, by_name = _backup_members(backup_path)
    if (
        embedded_plan != raw_plan
        or descriptor.get("plan_sha256") != hashlib.sha256(raw_plan).hexdigest()
    ):
        raise ValueError("backup plan binding mismatch")
    tree = descriptor.get("tree_manifest")
    if (
        not isinstance(tree, dict)
        or tree.get("tree_sha256") != plan["base_tree_sha256"]
    ):
        raise ValueError("backup tree binding mismatch")
    _verify_backup_descriptor(backup_path, descriptor, by_name)
    return descriptor


def restore_backup(
    plan_path: Path,
    backup_path: Path,
    repo_root: Path,
    knowledge_root: Path,
    confirm_current_tree_sha256: str,
    journal_path: Path,
    cascade_plan_path: Path | None = None,
    confirm_cascade_plan_sha256: str | None = None,
) -> dict:
    knowledge_root = _knowledge_root(repo_root, knowledge_root)
    plan_path = _outside_knowledge_root(
        knowledge_root.resolve(), plan_path, "resolved plan"
    )
    backup_path = _outside_knowledge_root(
        knowledge_root.resolve(), backup_path, "backup"
    )
    journal_path = _journal_path(knowledge_root.resolve(), journal_path)
    plan, _, plan_sha256 = _load_plan_for_restore(
        plan_path, repo_root, knowledge_root
    )
    current = build_tree_manifest(knowledge_root)["tree_sha256"]
    if (
        current != plan["expected_target_tree_sha256"]
        or confirm_current_tree_sha256 != current
    ):
        raise ValueError("restore rejects a stale or unconfirmed current tree")
    descriptor = _verify_backup_for_restore(plan_path, backup_path, plan)
    if (cascade_plan_path is None) != (confirm_cascade_plan_sha256 is None):
        raise ValueError(
            "cascade plan and confirmation digest must be provided together"
        )
    cascade: dict | None = None
    cascade_sha256: str | None = None
    if cascade_plan_path is not None and confirm_cascade_plan_sha256 is not None:
        cascade, cascade_sha256 = _load_cascade_plan(
            cascade_plan_path,
            confirm_cascade_plan_sha256,
            repo_root.resolve(),
            knowledge_root.resolve(),
            plan,
            plan_sha256,
        )
        if _external_state(cascade, repo_root.resolve()) != "target":
            raise ValueError(
                "combined restore requires all external files at target state"
            )
    if journal_path.exists():
        raise ValueError(f"transaction journal already exists: {journal_path}")
    candidate = Path(
        tempfile.mkdtemp(
            prefix=f".{knowledge_root.name}.restore.",
            dir=knowledge_root.parent,
        )
    )
    candidate.rmdir()
    swapped = False
    external_write_started = False
    conflict = False
    journal = {
        "schema_version": "2.0" if cascade is not None else "1.0",
        "operation": "restore",
        "state": "PREPARED",
        "knowledge_root": str(knowledge_root.resolve()),
        "candidate_root": str(candidate.resolve()),
        "plan_sha256": plan_sha256,
        "base_tree_sha256": plan["expected_target_tree_sha256"],
        "target_tree_sha256": plan["base_tree_sha256"],
    }
    if cascade_sha256 is not None:
        journal["cascade_plan_sha256"] = cascade_sha256
    journal_written = False
    try:
        if cascade is None:
            _write_journal(journal_path, journal)
            journal_written = True
        _write_tree_from_backup(backup_path, descriptor, candidate)
        if build_tree_manifest(candidate)["tree_sha256"] != plan["base_tree_sha256"]:
            raise ValueError("restored candidate tree digest mismatch")
        if cascade is not None:
            _write_journal(journal_path, journal)
            journal_written = True
            if _external_state(cascade, repo_root.resolve()) != "target":
                raise ValueError("external files changed before combined restore")
            external_write_started = True
            _write_external_state(cascade, repo_root.resolve(), "base")
            journal["state"] = "EXTERNAL_WRITTEN"
            _write_journal(journal_path, journal)
        exchange_directories(knowledge_root, candidate)
        swapped = True
        journal["state"] = "SWAPPED"
        _write_journal(journal_path, journal)
        current_hash = build_tree_manifest(knowledge_root)["tree_sha256"]
        previous_hash = build_tree_manifest(candidate)["tree_sha256"]
        external_matches = cascade is None or _external_state(
            cascade, repo_root.resolve()
        ) == "base"
        if (
            current_hash != plan["base_tree_sha256"]
            or previous_hash != plan["expected_target_tree_sha256"]
            or not external_matches
        ):
            exchange_directories(knowledge_root, candidate)
            swapped = False
            if cascade is not None and _external_state(
                cascade, repo_root.resolve()
            ) in {"base", "target", "mixed"}:
                _write_external_state(cascade, repo_root.resolve(), "target")
                external_write_started = False
            conflict = True
            journal["state"] = "CONFLICT"
            _write_journal(journal_path, journal)
            raise ValueError(
                "concurrent tree mutation detected; both trees were preserved"
            )
        journal["state"] = "COMMITTED"
        _write_journal(journal_path, journal)
        return journal
    except Exception:
        if swapped:
            exchange_directories(knowledge_root, candidate)
        if external_write_started and cascade is not None:
            external_state = _external_state(cascade, repo_root.resolve())
            if external_state in {"base", "target", "mixed"}:
                _write_external_state(cascade, repo_root.resolve(), "target")
            else:
                conflict = True
                journal["state"] = "CONFLICT"
                _write_journal(journal_path, journal)
        if journal_written and not conflict:
            journal["state"] = "ABORTED"
            _write_journal(journal_path, journal)
        raise


def recover_transaction(
    journal_path: Path,
    plan_path: Path,
    confirm_plan_sha256: str,
    repo_root: Path,
    knowledge_root: Path,
    cascade_plan_path: Path | None = None,
    confirm_cascade_plan_sha256: str | None = None,
) -> dict:
    knowledge_root = _knowledge_root(repo_root, knowledge_root)
    plan_path = _outside_knowledge_root(knowledge_root, plan_path, "resolved plan")
    journal_path = _journal_path(knowledge_root, journal_path)
    raw_plan = plan_path.read_bytes()
    plan = _validate_resolved_document(raw_plan)
    if plan["knowledge_root"] != str(knowledge_root.relative_to(repo_root.resolve())):
        raise ValueError("resolved plan knowledge_root does not match requested root")
    plan_sha256 = hashlib.sha256(raw_plan).hexdigest()
    if confirm_plan_sha256 != plan_sha256:
        raise ValueError("plan confirmation digest mismatch")
    journal = json.loads(journal_path.read_text(encoding="utf-8"))
    if (
        journal.get("schema_version") == "1.0"
        and set(journal) == TRANSACTION_JOURNAL_V1_FIELDS
    ):
        is_combined = False
    elif (
        journal.get("schema_version") == "2.0"
        and set(journal) == TRANSACTION_JOURNAL_V2_FIELDS
    ):
        is_combined = True
    else:
        raise ValueError("transaction journal shape is invalid")
    allowed_states = {
        "PREPARED",
        "SWAPPED",
        "COMMITTED",
        "ABORTED",
        "CONFLICT",
    }
    if is_combined:
        allowed_states.add("EXTERNAL_WRITTEN")
    if journal["state"] not in allowed_states:
        raise ValueError("transaction journal state is invalid")
    operation = journal["operation"]
    if operation not in {"apply", "restore"}:
        raise ValueError("transaction journal operation is invalid")
    if journal["knowledge_root"] != str(knowledge_root):
        raise ValueError("transaction journal knowledge root is not requested root")
    candidate = Path(journal["candidate_root"])
    candidate_kind = "migration" if operation == "apply" else "restore"
    prefix = f".{knowledge_root.name}.{candidate_kind}."
    if (
        not candidate.is_absolute()
        or candidate.parent != knowledge_root.parent
        or not candidate.name.startswith(prefix)
        or candidate.is_symlink()
    ):
        raise ValueError("transaction journal paths are unsafe")
    if journal["plan_sha256"] != plan_sha256:
        raise ValueError("transaction journal plan binding mismatch")
    current_hash = build_tree_manifest(knowledge_root)["tree_sha256"]
    candidate_hash = (
        build_tree_manifest(candidate)["tree_sha256"] if candidate.is_dir() else None
    )
    base_hash = journal["base_tree_sha256"]
    target_hash = journal["target_tree_sha256"]
    expected_hashes = (
        (plan["base_tree_sha256"], plan["expected_target_tree_sha256"])
        if operation == "apply"
        else (plan["expected_target_tree_sha256"], plan["base_tree_sha256"])
    )
    if (base_hash, target_hash) != expected_hashes:
        raise ValueError("transaction journal tree binding mismatch")
    if journal["state"] == "CONFLICT":
        raise ValueError(
            "conflicted transaction requires manual resolution; trees were preserved"
        )
    if is_combined:
        if cascade_plan_path is None or confirm_cascade_plan_sha256 is None:
            raise ValueError("combined recovery requires cascade plan confirmation")
        cascade, cascade_sha256 = _load_cascade_plan(
            cascade_plan_path,
            confirm_cascade_plan_sha256,
            repo_root.resolve(),
            knowledge_root,
            plan,
            plan_sha256,
            require_live_paths=False,
        )
        if journal["cascade_plan_sha256"] != cascade_sha256:
            raise ValueError("transaction journal cascade binding mismatch")
        external_state = _external_state(cascade, repo_root.resolve())
        if external_state == "unknown":
            journal["state"] = "CONFLICT"
            _write_journal(journal_path, journal)
            raise ValueError(
                "combined transaction has unknown external content; "
                "manual resolution required"
            )
        start_external = "base" if operation == "apply" else "target"
        end_external = "target" if operation == "apply" else "base"
        if journal["state"] == "COMMITTED":
            if (
                current_hash != target_hash
                or candidate_hash != base_hash
                or external_state != end_external
            ):
                raise ValueError("committed combined transaction state is inconsistent")
            return journal
        if current_hash == target_hash and candidate_hash == base_hash:
            exchange_directories(knowledge_root, candidate)
        elif current_hash == base_hash and candidate_hash == target_hash:
            pass
        else:
            journal["state"] = "CONFLICT"
            _write_journal(journal_path, journal)
            raise ValueError(
                "combined transaction tree digests do not match a recoverable state"
            )
        if external_state != start_external:
            _write_external_state(cascade, repo_root.resolve(), start_external)
        if (
            build_tree_manifest(knowledge_root)["tree_sha256"] != base_hash
            or _external_state(cascade, repo_root.resolve()) != start_external
        ):
            journal["state"] = "CONFLICT"
            _write_journal(journal_path, journal)
            raise ValueError("combined rollback verification failed")
        journal["state"] = "ABORTED"
        _write_journal(journal_path, journal)
        return journal
    if cascade_plan_path is not None or confirm_cascade_plan_sha256 is not None:
        raise ValueError("journal v1 does not accept a cascade plan")
    if current_hash == target_hash and candidate_hash == base_hash:
        if journal["state"] == "COMMITTED":
            return journal
        exchange_directories(knowledge_root, candidate)
        journal["state"] = "ABORTED"
        _write_journal(journal_path, journal)
        return journal
    if current_hash == base_hash and candidate_hash == target_hash:
        if journal["state"] == "COMMITTED":
            raise ValueError("committed transaction tree state is inconsistent")
        journal["state"] = "ABORTED"
        _write_journal(journal_path, journal)
        return journal
    if current_hash == target_hash and candidate_hash is None:
        if journal["state"] != "COMMITTED":
            raise ValueError("uncommitted transaction lost its rollback tree")
        return journal
    if current_hash == base_hash and candidate_hash is None:
        if journal["state"] == "COMMITTED":
            raise ValueError("committed transaction tree state is inconsistent")
        journal["state"] = "ABORTED"
        _write_journal(journal_path, journal)
        return journal
    raise ValueError("transaction tree digests do not match a recoverable state")
