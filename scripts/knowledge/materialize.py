from __future__ import annotations

import hashlib
import json
import re
import stat
from collections.abc import Mapping
from contextlib import ExitStack
from pathlib import Path

import yaml

from .fs import (
    LeafObservation,
    PathSafetyError,
    VerifiedDirectory,
    managed_temporary_leaf_names,
    observe_regular_leaf_at,
    publish_bytes_no_replace_at,
    remove_observed_leaf_at,
    replace_bytes_atomic_at,
    repository_write_lock,
    verified_directory,
)
from .schema import (
    KnowledgeSchemaError,
    active_domain_for_path,
    canonical_document_paths,
    document_tree_sha256,
    domain_registry,
    generated_contract,
    is_canonical_document_path,
    load_unique_yaml,
    parse_markdown,
    schema_digest,
)

GENERATOR_ID = "cs-study-materializer/1.0"


class MaterializeError(ValueError):
    pass


class _ObsidianBaseDumper(yaml.SafeDumper):
    def increase_indent(self, flow: bool = False, indentless: bool = False):
        return super().increase_indent(flow, indentless=False)

    def ignore_aliases(self, data):
        return True


def _marker_patterns() -> tuple[
    re.Pattern[bytes], re.Pattern[bytes], re.Pattern[bytes]
]:
    identity = re.escape(GENERATOR_ID.encode("utf-8"))
    identity_digest = identity + rb"; schema-sha256: [a-f0-9]{64}"
    markdown = rb"^<!-- generated-by: " + identity_digest + rb" -->$"
    base = (
        rb"\Aformulas:\n  _generated_by: '\""
        + identity_digest
        + rb"\"'\n"
    )
    return (
        re.compile(rb"(?:" + markdown + rb"|" + base + rb")", re.MULTILINE),
        re.compile(markdown, re.MULTILINE),
        re.compile(base, re.MULTILINE),
    )


def _knowledge_root_relative(repo_root: Path, knowledge_root: Path) -> Path:
    try:
        relative = knowledge_root.resolve().relative_to(repo_root.resolve())
    except ValueError as exc:
        raise MaterializeError("knowledge root must be inside repository") from exc
    if relative != Path("wiki"):
        raise MaterializeError("knowledge root must be repo-relative wiki")
    return relative


def _markdown_marker(digest: str) -> str:
    return f"<!-- generated-by: {GENERATOR_ID}; schema-sha256: {digest} -->"


def _base_formula(digest: str) -> str:
    return f'"{GENERATOR_ID}; schema-sha256: {digest}"'


def _generated_text(content: bytes, relative: Path) -> str:
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise MaterializeError(f"generated leaf is not UTF-8: {relative}") from exc


def _canonical_instances(
    repo_root: Path,
    knowledge_root: Path,
    overrides: Mapping[Path, str | None] | None,
) -> list[tuple[Path, dict]]:
    root = knowledge_root.resolve()
    contents: dict[Path, str | None] = {
        path.resolve(): None for path in canonical_document_paths(knowledge_root)
    }
    override_content: dict[Path, str | None] = {}
    for path, content in (overrides or {}).items():
        resolved = path.resolve()
        if not resolved.is_relative_to(root) or not is_canonical_document_path(
            root, resolved
        ):
            raise MaterializeError(f"candidate override escapes knowledge root: {path}")
        override_content[resolved] = content
        if content is None:
            contents.pop(resolved, None)
        else:
            contents[resolved] = content
    records = []
    schema_path = repo_root / "_meta" / "knowledge.schema.json"
    for path in sorted(contents):
        text = override_content.get(path)
        records.append((path, parse_markdown(path, text, schema_path=schema_path)))
    return records


def _active_records(
    records: list[tuple[Path, dict]],
    repo_root: Path,
    knowledge_root: Path,
    registry: dict[str, dict],
) -> tuple[dict[str, list[tuple[Path, dict]]], list[tuple[Path, dict]]]:
    domains = {name: [] for name in registry}
    collections = []
    root = knowledge_root.resolve()
    for path, instance in records:
        relative = path.resolve().relative_to(root)
        if relative.parts[0] == "domains":
            domain = active_domain_for_path(repo_root, root, path, registry)
            if domain is None:
                raise MaterializeError(f"active page has invalid domain path: {path}")
            domains[domain].append((path, instance))
        elif relative.parts[0] == "collections":
            collections.append((path, instance))
    for pages in domains.values():
        pages.sort(key=lambda item: (item[1]["properties"]["page_type"], item[1]["id"]))
    collections.sort(
        key=lambda item: (item[1]["properties"]["page_type"], item[1]["id"])
    )
    return domains, collections


def _page_entry(repo_root: Path, path: Path, instance: dict) -> str:
    relative = (
        path.resolve().relative_to(repo_root.resolve()).with_suffix("").as_posix()
    )
    properties = instance["properties"]
    return (
        f"- [[{relative}]] — {properties['title']} — {properties['summary']} "
        f"({properties['page_type']})"
    )


def _render_index(
    repo_root: Path,
    registry: dict[str, dict],
    domains: dict[str, list[tuple[Path, dict]]],
    collections: list[tuple[Path, dict]],
    marker: str,
) -> bytes:
    lines = [marker, "", "# Knowledge Index"]
    for name in registry:
        lines.extend(["", f"## {name}", ""])
        entries = domains[name]
        lines.extend(
            [_page_entry(repo_root, path, instance) for path, instance in entries]
            or ["(empty)"]
        )
    lines.extend(["", "## Collections", ""])
    lines.extend(
        [_page_entry(repo_root, path, instance) for path, instance in collections]
        or ["(empty)"]
    )
    return ("\n".join(lines) + "\n").encode("utf-8")


def _render_overview(
    registry: dict[str, dict],
    domains: dict[str, list[tuple[Path, dict]]],
    collections: list[tuple[Path, dict]],
    marker: str,
) -> bytes:
    lines = [
        marker,
        "",
        "# Knowledge Overview",
        "",
        "| domain | label | status | active pages |",
        "|---|---|---|---|",
    ]
    for name, entry in registry.items():
        lines.append(
            f"| [[wiki/index#{name}|{name}]] | {entry['label']} | "
            f"{entry['status']} | {len(domains[name])} |"
        )
    lines.append(
        f"| [[wiki/index#Collections|Collections]] |  | active | {len(collections)} |"
    )
    return ("\n".join(lines) + "\n").encode("utf-8")


def _table_lines(columns: tuple[str, ...]) -> list[str]:
    return [
        "| " + " | ".join(columns) + " |",
        "|" + "|".join("---" for _ in columns) + "|",
    ]


def _render_template(page_type: str, marker: str, contract: dict) -> bytes:
    properties = contract["placeholders"][page_type]
    frontmatter = yaml.safe_dump(
        properties,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    ).rstrip("\n")
    lines = ["---", *frontmatter.splitlines(), "---", marker]
    for section in contract["sections"][page_type]:
        lines.extend(["", f"## {section}", ""])
        if section in {"Claims", "Relations", "Members"}:
            lines.extend(_table_lines(contract["tables"][section]))
    return ("\n".join(lines).rstrip() + "\n").encode("utf-8")


def _dump_base(document: dict) -> bytes:
    return yaml.dump(
        document,
        Dumper=_ObsidianBaseDumper,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    ).encode("utf-8")


def _render_base(registry: dict[str, dict], formula: str, contract: dict) -> bytes:
    table_order = list(contract["base_table_order"])
    views = [{"type": "table", "name": "All active", "order": table_order}]
    for name, entry in registry.items():
        if entry["status"] == "active":
            views.append(
                {
                    "type": "table",
                    "name": entry["label"],
                    "filters": f'file.inFolder("wiki/domains/{name}")',
                    "order": table_order,
                }
            )
    views.append(
        {
            "type": "table",
            "name": "Collections",
            "filters": 'file.inFolder("wiki/collections")',
            "order": table_order,
        }
    )
    document = {
        "formulas": {"_generated_by": formula},
        "filters": {
            "or": [
                'file.inFolder("wiki/domains")',
                'file.inFolder("wiki/collections")',
            ]
        },
        "views": views,
    }
    return _dump_base(document)


def _validation_instances(
    repo_root: Path,
    knowledge_root: Path,
    overrides: Mapping[Path, str | None] | None,
) -> list[tuple[Path, dict]]:
    root = knowledge_root.resolve()
    contents = {path.resolve(): None for path in canonical_document_paths(root)}
    for path, content in (overrides or {}).items():
        resolved = path.resolve()
        if not resolved.is_relative_to(root) or not is_canonical_document_path(
            root, resolved
        ):
            raise MaterializeError(
                f"validation override escapes knowledge root: {path}"
            )
        if content is None:
            contents.pop(resolved, None)
        else:
            contents[resolved] = content
    schema_path = repo_root / "_meta/knowledge.schema.json"
    return [
        (path, parse_markdown(path, contents[path], schema_path=schema_path))
        for path in sorted(contents)
    ]


def _validation_active_records(
    records: list[tuple[Path, dict]],
    repo_root: Path,
    knowledge_root: Path,
    registry: dict[str, dict],
) -> tuple[dict[str, list[tuple[Path, dict]]], list[tuple[Path, dict]]]:
    domains = {name: [] for name in registry}
    collections = []
    root = knowledge_root.resolve()
    for path, instance in records:
        relative = path.resolve().relative_to(root)
        if relative.parts[0] == "domains":
            domain = active_domain_for_path(repo_root, root, path, registry)
            if domain is None:
                raise MaterializeError(f"active page has invalid domain path: {path}")
            domains[domain].append((path, instance))
        elif relative.parts[0] == "collections":
            collections.append((path, instance))
    for pages in domains.values():
        pages.sort(key=lambda item: (item[1]["properties"]["page_type"], item[1]["id"]))
    collections.sort(
        key=lambda item: (item[1]["properties"]["page_type"], item[1]["id"])
    )
    return domains, collections


def validate_generated(
    expected: Mapping[Path, bytes],
    repo_root: Path,
    knowledge_root: Path,
    overrides: Mapping[Path, str | None] | None = None,
) -> None:
    contract = generated_contract(repo_root)
    page_type_set = set(contract["page_types"])
    expected_paths = {
        Path("wiki/index.md"),
        Path("wiki/overview.md"),
        Path("wiki/views/knowledge-pages.base"),
        *{Path(f"wiki/templates/{name}.md") for name in page_type_set},
    }
    if set(expected) != expected_paths:
        raise MaterializeError("generated manifest path set differs from schema")
    digest = schema_digest(repo_root)
    markdown_marker = _markdown_marker(digest).encode()
    base_formula = _base_formula(digest)
    _, markdown_marker_re, base_marker_re = _marker_patterns()
    for path, content in expected.items():
        marker_re = base_marker_re if path.suffix == ".base" else markdown_marker_re
        if len(marker_re.findall(content)) != 1:
            if path.suffix == ".base":
                raise MaterializeError("invalid generated Base marker")
            raise MaterializeError(f"invalid generated marker: {path}")
        if not content.endswith(b"\n"):
            raise MaterializeError(f"generated leaf lacks final newline: {path}")
    registry = domain_registry(repo_root)
    records = _validation_instances(repo_root, knowledge_root, overrides)
    domains, collections = _validation_active_records(
        records, repo_root, knowledge_root, registry
    )

    index_path = Path("wiki/index.md")
    index_lines = _generated_text(expected[index_path], index_path).splitlines()
    required_index = [markdown_marker.decode(), "", "# Knowledge Index"]
    for name in registry:
        required_index.extend(["", f"## {name}", ""])
        entries = []
        for path, instance in domains[name]:
            relative = (
                path.resolve()
                .relative_to(repo_root.resolve())
                .with_suffix("")
                .as_posix()
            )
            properties = instance["properties"]
            entries.append(
                f"- [[{relative}]] — {properties['title']} — {properties['summary']} "
                f"({properties['page_type']})"
            )
        required_index.extend(entries or ["(empty)"])
    required_index.extend(["", "## Collections", ""])
    collection_entries = []
    for path, instance in collections:
        relative = (
            path.resolve().relative_to(repo_root.resolve()).with_suffix("").as_posix()
        )
        properties = instance["properties"]
        collection_entries.append(
            f"- [[{relative}]] — {properties['title']} — {properties['summary']} "
            f"({properties['page_type']})"
        )
    required_index.extend(collection_entries or ["(empty)"])
    if index_lines != required_index:
        raise MaterializeError(
            "generated index differs from canonical active page coverage"
        )

    overview_lines = [
        markdown_marker.decode(),
        "",
        "# Knowledge Overview",
        "",
        "| domain | label | status | active pages |",
        "|---|---|---|---|",
    ]
    for name, entry in registry.items():
        overview_lines.append(
            f"| [[wiki/index#{name}|{name}]] | {entry['label']} | {entry['status']} | "
            f"{len(domains[name])} |"
        )
    overview_lines.append(
        f"| [[wiki/index#Collections|Collections]] |  | active | {len(collections)} |"
    )
    if (
        _generated_text(
            expected[Path("wiki/overview.md")], Path("wiki/overview.md")
        ).splitlines()
        != overview_lines
    ):
        raise MaterializeError("generated overview differs from domain registry counts")

    for page_type in contract["page_types"]:
        relative = Path(f"wiki/templates/{page_type}.md")
        lines = _generated_text(expected[relative], relative).splitlines()
        try:
            closing = lines.index("---", 1)
            properties = load_unique_yaml(
                "\n".join(lines[1:closing]), "generated template YAML"
            )
        except (ValueError, KnowledgeSchemaError) as exc:
            raise MaterializeError(
                f"invalid generated template YAML: {relative}"
            ) from exc
        property_names = (
            *contract["required_properties"],
            *contract["optional_properties"],
        )
        if not isinstance(properties, dict) or tuple(properties) != property_names:
            raise MaterializeError(f"generated template properties differ: {relative}")
        if properties != contract["placeholders"][page_type]:
            raise MaterializeError(
                f"generated template placeholders differ: {relative}"
            )
        if closing + 1 >= len(lines) or lines[closing + 1] != markdown_marker.decode():
            raise MaterializeError(f"generated template marker differs: {relative}")
        body = lines[closing + 2 :]
        headings = [line[3:] for line in body if line.startswith("## ")]
        if headings != list(contract["sections"][page_type]):
            raise MaterializeError(f"generated template sections differ: {relative}")
        required_body = []
        for section in contract["sections"][page_type]:
            required_body.extend(["", f"## {section}", ""])
            if section in contract["tables"]:
                columns = contract["tables"][section]
                required_body.extend(
                    [
                        "| " + " | ".join(columns) + " |",
                        "|" + "|".join("---" for _ in columns) + "|",
                    ]
                )
        while required_body and required_body[-1] == "":
            required_body.pop()
        if body != required_body:
            raise MaterializeError(f"generated template body differs: {relative}")

    try:
        base_path = Path("wiki/views/knowledge-pages.base")
        base_text = _generated_text(expected[base_path], base_path)
        base = load_unique_yaml(base_text, "generated Base YAML")
    except KnowledgeSchemaError as exc:
        raise MaterializeError(f"invalid generated Base YAML: {exc}") from exc
    table_order = list(contract["base_table_order"])
    required_views = [{"type": "table", "name": "All active", "order": table_order}]
    required_views.extend(
        {
            "type": "table",
            "name": entry["label"],
            "filters": f'file.inFolder("wiki/domains/{name}")',
            "order": table_order,
        }
        for name, entry in registry.items()
        if entry["status"] == "active"
    )
    required_views.append(
        {
            "type": "table",
            "name": "Collections",
            "filters": 'file.inFolder("wiki/collections")',
            "order": table_order,
        }
    )
    required_base = {
        "formulas": {"_generated_by": base_formula},
        "filters": {
            "or": [
                'file.inFolder("wiki/domains")',
                'file.inFolder("wiki/collections")',
            ]
        },
        "views": required_views,
    }
    if base != required_base:
        if not isinstance(base, dict) or base.get("formulas") != required_base["formulas"]:
            raise MaterializeError("invalid generated Base marker")
        raise MaterializeError("invalid generated Base document")
    if expected[base_path] != _dump_base(required_base):
        raise MaterializeError("generated Base serialization is not canonical")


def render_generated(
    repo_root: Path,
    knowledge_root: Path,
    overrides: Mapping[Path, str | None] | None = None,
) -> dict[Path, bytes]:
    _knowledge_root_relative(repo_root, knowledge_root)
    try:
        contract = generated_contract(repo_root)
        registry = domain_registry(repo_root)
        records = _canonical_instances(repo_root, knowledge_root, overrides)
        domains, collections = _active_records(
            records, repo_root, knowledge_root, registry
        )
        digest = schema_digest(repo_root)
        markdown_marker = _markdown_marker(digest)
        base_formula = _base_formula(digest)
        rendered = {
            Path("wiki/index.md"): _render_index(
                repo_root, registry, domains, collections, markdown_marker
            ),
            Path("wiki/overview.md"): _render_overview(
                registry, domains, collections, markdown_marker
            ),
            Path("wiki/views/knowledge-pages.base"): _render_base(
                registry, base_formula, contract
            ),
        }
        for page_type in contract["page_types"]:
            rendered[Path(f"wiki/templates/{page_type}.md")] = _render_template(
                page_type, markdown_marker, contract
            )
        ordered = dict(sorted(rendered.items(), key=lambda item: item[0].as_posix()))
        return ordered
    except (
        KeyError,
        OSError,
        TypeError,
        UnicodeDecodeError,
        yaml.YAMLError,
        KnowledgeSchemaError,
    ) as exc:
        raise MaterializeError(f"cannot render generated surface: {exc}") from exc


def materialize_input_sha256(
    repo_root: Path,
    knowledge_root: Path,
    overrides: Mapping[Path, str | None] | None = None,
) -> str:
    try:
        value = {
            "canonical_tree_sha256": document_tree_sha256(knowledge_root, overrides),
            "domain_registry_sha256": hashlib.sha256(
                (repo_root / "_meta" / "domains.yaml").read_bytes()
            ).hexdigest(),
            "generator": GENERATOR_ID,
            "options": {},
            "schema_sha256": schema_digest(repo_root),
        }
    except (KnowledgeSchemaError, OSError) as exc:
        raise MaterializeError(f"cannot identify materialize input: {exc}") from exc
    encoded = json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def generated_tree_sha256(expected: Mapping[Path, bytes]) -> str:
    manifest = [
        {
            "path": path.as_posix(),
            "sha256": hashlib.sha256(content).hexdigest(),
        }
        for path, content in sorted(
            expected.items(), key=lambda item: item[0].as_posix()
        )
    ]
    encoded = json.dumps(
        manifest, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _generated_marker_paths(repo_root: Path, knowledge_root: Path) -> set[Path]:
    marker_re, _, _ = _marker_patterns()
    paths = set()
    candidates = list(knowledge_root.glob("*"))
    for namespace in (knowledge_root / "templates", knowledge_root / "views"):
        if namespace.is_dir() and not namespace.is_symlink():
            candidates.extend(namespace.rglob("*"))
    for path in candidates:
        try:
            mode = path.lstat().st_mode
        except OSError:
            continue
        if stat.S_ISREG(mode) and marker_re.search(path.read_bytes()):
            paths.add(path.resolve().relative_to(repo_root.resolve()))
    return paths


def generated_drift(repo_root: Path, knowledge_root: Path) -> tuple[str, ...]:
    expected = render_generated(repo_root, knowledge_root)
    validate_generated(expected, repo_root, knowledge_root)
    findings = []
    for relative, content in expected.items():
        path = repo_root / relative
        try:
            mode = path.lstat().st_mode
        except FileNotFoundError:
            findings.append(f"missing generated leaf: {relative.as_posix()}")
            continue
        if not stat.S_ISREG(mode) or stat.S_ISLNK(mode):
            findings.append(f"generated leaf is not regular: {relative.as_posix()}")
        elif path.read_bytes() != content:
            findings.append(f"generated bytes differ: {relative.as_posix()}")
    for relative in sorted(
        _generated_marker_paths(repo_root, knowledge_root) - set(expected)
    ):
        findings.append(f"unexpected generated leaf: {relative.as_posix()}")
    return tuple(findings)


def _preflight_apply(
    repo_root: Path,
    knowledge_root: Path,
    expected: dict[Path, bytes],
    directories: Mapping[Path, VerifiedDirectory],
) -> dict[Path, LeafObservation | None]:
    marker_re, markdown_marker_re, base_marker_re = _marker_patterns()
    for directory in directories.values():
        for name in managed_temporary_leaf_names(directory):
            temporary = observe_regular_leaf_at(directory, name)
            if temporary is not None and marker_re.search(temporary.data):
                remove_observed_leaf_at(directory, name, temporary)
    unexpected = _generated_marker_paths(repo_root, knowledge_root) - set(expected)
    if unexpected:
        joined = ", ".join(path.as_posix() for path in sorted(unexpected))
        raise MaterializeError(f"unexpected generated leaf: {joined}")
    for directory in directories.values():
        directory.assert_identity()
    observed: dict[Path, LeafObservation | None] = {}
    for relative in expected:
        parent_relative = relative.parent
        existing = observe_regular_leaf_at(directories[parent_relative], relative.name)
        observed[relative] = existing
        if existing is None:
            continue
        marker_pattern = (
            base_marker_re if relative.suffix == ".base" else markdown_marker_re
        )
        if len(marker_pattern.findall(existing.data)) != 1:
            raise MaterializeError(f"refusing markerless generated leaf: {relative}")
    return observed


def apply_generated(repo_root: Path, knowledge_root: Path) -> dict[str, int | str]:
    input_sha256 = materialize_input_sha256(repo_root, knowledge_root)
    expected = render_generated(repo_root, knowledge_root)
    validate_generated(expected, repo_root, knowledge_root)
    created = replaced = unchanged = 0
    with repository_write_lock(repo_root):
        if materialize_input_sha256(repo_root, knowledge_root) != input_sha256:
            raise MaterializeError("materialize input changed before apply")
        rerendered = render_generated(repo_root, knowledge_root)
        validate_generated(rerendered, repo_root, knowledge_root)
        if rerendered != expected:
            raise MaterializeError("materialize input changed before apply")
        try:
            with ExitStack() as stack:
                parent_paths = sorted({relative.parent for relative in expected})
                directories = {
                    relative: stack.enter_context(
                        verified_directory(repo_root / relative)
                    )
                    for relative in parent_paths
                }
                observed = _preflight_apply(
                    repo_root, knowledge_root, expected, directories
                )
                for relative, content in expected.items():
                    directory = directories[relative.parent]
                    previous = observed[relative]
                    if previous is None:
                        publish_bytes_no_replace_at(directory, relative.name, content)
                        created += 1
                    elif previous.data == content:
                        if (
                            observe_regular_leaf_at(directory, relative.name)
                            != previous
                        ):
                            raise PathSafetyError(
                                f"generated leaf changed after preflight: {relative}"
                            )
                        unchanged += 1
                    else:
                        replace_bytes_atomic_at(
                            directory, relative.name, previous, content
                        )
                        replaced += 1
        except PathSafetyError as exc:
            raise MaterializeError(str(exc)) from exc
    return {
        "created": created,
        "input_sha256": input_sha256,
        "output_tree_sha256": generated_tree_sha256(expected),
        "replaced": replaced,
        "unchanged": unchanged,
    }
