from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import os
import re
import stat
from collections.abc import Mapping, Sequence
from pathlib import Path

import yaml
from contracts.timestamps import is_canonical_datetime, is_contract_datetime
from jsonschema import Draft202012Validator, FormatChecker

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "_meta" / "knowledge.schema.json"
CANONICAL_ROOT_EXCLUSIONS = frozenset({"index.md", "overview.md"})
TABLE_COLUMNS = {
    "Claims": ("id", "primary", "claim", "status", "evidence", "notes"),
    "Relations": ("type", "target", "notes"),
    "Members": ("member", "role", "rationale"),
}
BASE_TABLE_ORDER = (
    "file.name",
    "title",
    "page_type",
    "summary",
    "date_updated",
)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
DELIMITER_RE = re.compile(r"^:?-{3,}:?$")
TAXONOMY_TAG_HEADING = "## Tag 목록"
TAXONOMY_ENTITY_HEADING = "## Entity 목록"
TAXONOMY_TOKEN_PATTERN = r"[a-z0-9]+(?:[.-][a-z0-9]+)*"
TAXONOMY_VOCAB_RE = re.compile(
    rf"^- `(?P<canonical>{TAXONOMY_TOKEN_PATTERN})`"
    rf"(?: \(alias: (?P<aliases>`{TAXONOMY_TOKEN_PATTERN}`"
    rf"(?:, `{TAXONOMY_TOKEN_PATTERN}`)*)\)| \([^)]*\))?$"
)
TAXONOMY_ALIAS_RE = re.compile(rf"`({TAXONOMY_TOKEN_PATTERN})`")
FENCE_LINE_RE = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})(?P<tail>.*)$")


class KnowledgeSchemaError(ValueError):
    pass


def markdown_fence_mask(lines: Sequence[str]) -> tuple[bool, ...]:
    mask: list[bool] = []
    fence_character = ""
    fence_length = 0
    for line in lines:
        match = FENCE_LINE_RE.fullmatch(line)
        marker = match.group("fence") if match else ""
        character = marker[:1]
        run_length = len(marker)
        tail = match.group("tail") if match else ""
        if not fence_character:
            if marker and not (character == "`" and "`" in tail):
                fence_character = character
                fence_length = run_length
                mask.append(True)
            else:
                mask.append(False)
            continue
        mask.append(True)
        if (
            character == fence_character
            and run_length >= fence_length
            and not tail.strip(" \t")
        ):
            fence_character = ""
            fence_length = 0
    return tuple(mask)


def knowledge_format_checker() -> FormatChecker:
    checker = FormatChecker()
    checker.checks("date-time")(is_canonical_datetime)
    return checker


def contract_format_checker() -> FormatChecker:
    checker = FormatChecker()
    checker.checks("date-time")(is_contract_datetime)
    return checker


def is_canonical_document_path(target_root: Path, path: Path) -> bool:
    """Return whether a Markdown path belongs to the canonical document set."""
    try:
        relative = path.absolute().relative_to(target_root.absolute())
    except ValueError:
        return False
    return (
        path.suffix == ".md"
        and relative.as_posix() not in CANONICAL_ROOT_EXCLUSIONS
        and (not relative.parts or relative.parts[0] != "templates")
    )


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_mapping(
    loader: yaml.Loader, node: yaml.MappingNode, deep: bool = False
) -> dict:
    mapping: dict = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise KnowledgeSchemaError(f"duplicate YAML property: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping
)


def load_unique_yaml(text: str, subject: str) -> object:
    try:
        return yaml.load(text, Loader=_UniqueKeyLoader)
    except yaml.YAMLError as exc:
        raise KnowledgeSchemaError(f"invalid {subject}: {exc}") from exc


def _reject_json_constant(value: str) -> None:
    raise KnowledgeSchemaError(f"non-finite JSON constant: {value}")


def _load_schema_path(schema_path: Path) -> dict:
    try:
        loaded = json.loads(
            schema_path.read_text(encoding="utf-8"),
            parse_constant=_reject_json_constant,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise KnowledgeSchemaError(f"invalid knowledge schema: {exc}") from exc
    if not isinstance(loaded, dict):
        raise KnowledgeSchemaError("knowledge schema root must be an object")
    return loaded


def load_schema(repo_root: Path = REPO_ROOT) -> dict:
    return _load_schema_path(repo_root / "_meta" / "knowledge.schema.json")


def schema_digest(repo_root: Path = REPO_ROOT) -> str:
    return hashlib.sha256(
        (repo_root / "_meta" / "knowledge.schema.json").read_bytes()
    ).hexdigest()


def load_taxonomy(
    repo_root: Path = REPO_ROOT,
) -> tuple[frozenset[str], dict[str, str], frozenset[str], dict[str, str]]:
    path = repo_root / "_meta" / "taxonomy.md"
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        raise KnowledgeSchemaError(f"invalid taxonomy: {exc}") from exc
    try:
        entity_pattern = load_schema(repo_root)["$defs"]["DocumentInstance"][
            "properties"
        ]["id"]["pattern"]
        entity_canonical_re = re.compile(entity_pattern)
    except (KeyError, TypeError, re.error) as exc:
        raise KnowledgeSchemaError(
            f"invalid DocumentInstance id pattern: {exc}"
        ) from exc
    canonical: dict[str, set[str]] = {"tag": set(), "entity": set()}
    aliases: dict[str, dict[str, str]] = {"tag": {}, "entity": {}}
    section: str | None = None
    headings = {"tag": False, "entity": False}
    for line_number, line in enumerate(lines, start=1):
        if line.startswith(TAXONOMY_TAG_HEADING):
            section = "tag"
            headings[section] = True
            continue
        if line.startswith(TAXONOMY_ENTITY_HEADING):
            section = "entity"
            headings[section] = True
            continue
        if line.startswith("## "):
            section = None
            continue
        if section is None or not line.startswith("- "):
            continue
        match = TAXONOMY_VOCAB_RE.fullmatch(line)
        if match is None:
            raise KnowledgeSchemaError(
                f"invalid taxonomy {section} entry at line {line_number}"
            )
        value = match.group("canonical")
        if section == "entity" and entity_canonical_re.fullmatch(value) is None:
            raise KnowledgeSchemaError(
                f"invalid taxonomy entity canonical at line {line_number}: {value}"
            )
        if value in canonical[section]:
            raise KnowledgeSchemaError(
                f"duplicate taxonomy {section} canonical: {value}"
            )
        canonical[section].add(value)
        for alias in TAXONOMY_ALIAS_RE.findall(match.group("aliases") or ""):
            if alias in aliases[section]:
                raise KnowledgeSchemaError(
                    f"duplicate taxonomy {section} alias: {alias}"
                )
            aliases[section][alias] = value
    if not all(headings.values()):
        raise KnowledgeSchemaError("taxonomy must define tag and entity sections")
    for section_name in ("tag", "entity"):
        conflicts = canonical[section_name].intersection(aliases[section_name])
        if conflicts:
            raise KnowledgeSchemaError(
                f"taxonomy {section_name} canonical/alias collision: "
                f"{sorted(conflicts)[0]}"
            )
    return (
        frozenset(canonical["tag"]),
        dict(sorted(aliases["tag"].items())),
        frozenset(canonical["entity"]),
        dict(sorted(aliases["entity"].items())),
    )


def _page_types_from_schema(schema: dict) -> tuple[str, ...]:
    values = schema["$defs"]["PageType"]["enum"]
    if (
        not isinstance(values, list)
        or not values
        or any(not isinstance(value, str) or not value for value in values)
        or len(values) != len(set(values))
    ):
        raise KnowledgeSchemaError(
            "PageType enum must be a non-empty unique string list"
        )
    return tuple(values)


def page_types(repo_root: Path = REPO_ROOT) -> tuple[str, ...]:
    return _page_types_from_schema(load_schema(repo_root))


def _lifecycle_roots_from_schema(schema: dict) -> tuple[str, ...]:
    try:
        path_properties = schema["$defs"]["PageWrite"]["properties"]
        lifecycle_path = schema["$defs"]["LifecyclePath"]
        pattern = lifecycle_path["pattern"]
    except (KeyError, TypeError) as exc:
        raise KnowledgeSchemaError("LifecycleRoot path pattern is missing") from exc
    lifecycle_ref = {"$ref": "#/$defs/LifecyclePath"}
    expected_source = {"anyOf": [lifecycle_ref, {"type": "null"}]}
    prefix = "^(?:"
    separator = ")/"
    if (
        not isinstance(path_properties, Mapping)
        or not isinstance(lifecycle_path, Mapping)
        or lifecycle_path.get("type") != "string"
        or path_properties.get("source_path") != expected_source
        or path_properties.get("target_path") != lifecycle_ref
        or not isinstance(pattern, str)
        or not pattern.startswith(prefix)
        or separator not in pattern
    ):
        raise KnowledgeSchemaError("LifecycleRoot path reference is invalid")
    alternatives = pattern[len(prefix) :].split(separator, 1)[0]
    values = alternatives.split("|")
    if (
        not alternatives
        or any(not value for value in values)
        or len(values) != len(set(values))
        or any(
            re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value) is None
            for value in values
        )
    ):
        raise KnowledgeSchemaError(
            "LifecycleRoot path pattern must declare unique kebab-case roots"
        )
    try:
        re.compile(pattern)
    except re.error as exc:
        raise KnowledgeSchemaError("LifecycleRoot path pattern is invalid") from exc
    return tuple(values)


def lifecycle_roots(repo_root: Path = REPO_ROOT) -> tuple[str, ...]:
    return _lifecycle_roots_from_schema(load_schema(repo_root))


def _property_contract_from_schema(
    schema: dict,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    properties = schema["$defs"]["Properties"]
    declared = properties["properties"]
    required = properties["required"]
    if (
        not isinstance(declared, dict)
        or not isinstance(required, list)
        or len(required) != len(set(required))
        or any(name not in declared for name in required)
    ):
        raise KnowledgeSchemaError("invalid Properties schema contract")
    optional = [name for name in declared if name not in required]
    return tuple(required), tuple(optional)


def property_contract(
    repo_root: Path = REPO_ROOT,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    return _property_contract_from_schema(load_schema(repo_root))


def table_contract(section: str) -> list[str]:
    try:
        return list(TABLE_COLUMNS[section])
    except KeyError as exc:
        raise KnowledgeSchemaError(f"unknown table section: {section}") from exc


def canonical_document_paths(target_root: Path) -> tuple[Path, ...]:
    root = target_root.absolute()
    try:
        root_mode = root.lstat().st_mode
    except OSError as exc:
        raise KnowledgeSchemaError(
            f"knowledge root must be an existing directory: {target_root}"
        ) from exc
    if not stat.S_ISDIR(root_mode) or stat.S_ISLNK(root_mode):
        raise KnowledgeSchemaError("knowledge root must be a non-symlink directory")

    def fail_traversal(error: OSError) -> None:
        location = error.filename or root
        raise KnowledgeSchemaError(
            f"knowledge traversal unavailable: {location}"
        ) from error

    paths: list[Path] = []
    try:
        for current, directory_names, file_names in os.walk(
            root, followlinks=False, onerror=fail_traversal
        ):
            current_path = Path(current)
            for name in directory_names:
                directory = current_path / name
                try:
                    mode = directory.lstat().st_mode
                except OSError as exc:
                    raise KnowledgeSchemaError(
                        f"knowledge traversal entry unavailable: {directory}"
                    ) from exc
                if name.endswith(".md"):
                    raise KnowledgeSchemaError(
                        "Markdown entry must be a regular non-symlink file: "
                        f"{directory}"
                    )
                if not stat.S_ISDIR(mode) or stat.S_ISLNK(mode):
                    raise KnowledgeSchemaError(
                        f"knowledge traversal directory must be regular: {directory}"
                    )
            for name in file_names:
                if not name.endswith(".md"):
                    continue
                path = current_path / name
                try:
                    mode = path.lstat().st_mode
                except OSError as exc:
                    raise KnowledgeSchemaError(
                        f"knowledge traversal entry unavailable: {path}"
                    ) from exc
                if not stat.S_ISREG(mode) or stat.S_ISLNK(mode):
                    raise KnowledgeSchemaError(
                        f"Markdown entry must be a regular non-symlink file: {path}"
                    )
                if is_canonical_document_path(root, path):
                    paths.append(path)
    except OSError as exc:
        fail_traversal(exc)
    return tuple(sorted(paths))


def document_tree_sha256(
    target_root: Path,
    overrides: Mapping[Path, str | None] | None = None,
) -> str:
    root = target_root.absolute()
    documents = {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in canonical_document_paths(root)
    }
    for path, content in (overrides or {}).items():
        resolved = path.absolute()
        try:
            relative = resolved.relative_to(root).as_posix()
        except ValueError as exc:
            raise KnowledgeSchemaError(
                f"document override escapes root: {path}"
            ) from exc
        if not is_canonical_document_path(root, resolved):
            raise KnowledgeSchemaError(f"invalid document override path: {path}")
        if content is None:
            documents.pop(relative, None)
        else:
            documents[relative] = content.encode("utf-8")
    manifest = [
        {"path": path, "sha256": hashlib.sha256(documents[path]).hexdigest()}
        for path in sorted(documents)
    ]
    encoded = json.dumps(
        manifest,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def domain_registry(repo_root: Path = REPO_ROOT) -> dict[str, dict]:
    registry_path = repo_root / "_meta" / "domains.yaml"
    try:
        registry = load_unique_yaml(
            registry_path.read_text(encoding="utf-8"), "domain registry"
        )
        if not isinstance(registry, dict) or registry.get("version") != 1:
            raise KnowledgeSchemaError("domain registry version must be 1")
        domains = registry["domains"]
    except (OSError, UnicodeDecodeError, KeyError, TypeError, yaml.YAMLError) as exc:
        raise KnowledgeSchemaError(f"invalid domain registry: {exc}") from exc
    if not isinstance(domains, dict):
        raise KnowledgeSchemaError("domain registry domains must be a mapping")
    if any(not isinstance(name, str) for name in domains):
        raise KnowledgeSchemaError("domain registry keys must be strings")
    validated: dict[str, dict] = {}
    for name, value in sorted(domains.items()):
        if not isinstance(name, str) or not re.fullmatch(
            r"[a-z0-9]+(?:-[a-z0-9]+)*", name
        ):
            raise KnowledgeSchemaError(f"invalid domain registry key: {name}")
        if not isinstance(value, dict) or set(value) != {
            "status",
            "label",
            "source_roots",
        }:
            raise KnowledgeSchemaError(f"invalid domain registry entry: {name}")
        status_value = value["status"]
        label = value["label"]
        source_roots = value["source_roots"]
        if status_value not in {"active", "inactive"}:
            raise KnowledgeSchemaError(f"invalid domain status: {name}")
        if not isinstance(label, str) or not label or re.search(r"[\r\n|]", label):
            raise KnowledgeSchemaError(f"invalid domain label: {name}")
        if (
            not isinstance(source_roots, list)
            or any(
                not isinstance(root, str)
                or not root
                or root.startswith(("/", "\\"))
                or "\\" in root
                or ".." in Path(root).parts
                for root in source_roots
            )
            or len(source_roots) != len(set(source_roots))
        ):
            raise KnowledgeSchemaError(f"invalid domain source_roots: {name}")
        validated[name] = {
            "status": status_value,
            "label": label,
            "source_roots": list(source_roots),
        }
    return validated


def active_domains(repo_root: Path = REPO_ROOT) -> frozenset[str]:
    return frozenset(
        name
        for name, value in domain_registry(repo_root).items()
        if value["status"] == "active"
    )


def active_domain_for_path(
    repo_root: Path,
    target_root: Path,
    path: Path,
    registry: Mapping[str, Mapping[str, object]] | None = None,
) -> str | None:
    relative = path.absolute().relative_to(target_root.absolute())
    if not relative.parts or relative.parts[0] != "domains":
        return None
    if len(relative.parts) < 3:
        raise KnowledgeSchemaError(f"active page has invalid domain path: {path}")
    domain = relative.parts[1]
    selected = domain_registry(repo_root) if registry is None else registry
    if domain not in selected:
        raise KnowledgeSchemaError(f"active page has unregistered domain path: {path}")
    if selected[domain]["status"] != "active":
        raise KnowledgeSchemaError(f"active page is under inactive domain: {domain}")
    return domain


def validator_for(
    definition: str, schema_path: Path = SCHEMA_PATH
) -> Draft202012Validator:
    schema = _load_schema_path(schema_path)
    if definition not in schema.get("$defs", {}):
        raise KnowledgeSchemaError(f"unknown schema definition: {definition}")
    selected = {
        "$schema": schema["$schema"],
        "$ref": f"#/$defs/{definition}",
        "$defs": copy.deepcopy(schema["$defs"]),
    }
    Draft202012Validator.check_schema(selected)
    return Draft202012Validator(selected, format_checker=knowledge_format_checker())


def _section_contract_from_schema(page_type: str, schema: dict) -> list[str]:
    for condition in schema["$defs"]["DocumentInstance"]["allOf"]:
        declared = condition["if"]["properties"]["properties"]["properties"][
            "page_type"
        ].get("const")
        if declared == page_type:
            return list(condition["then"]["properties"]["ordered_sections"]["const"])
    raise KnowledgeSchemaError(f"unknown page_type section contract: {page_type}")


def section_contract(page_type: str, repo_root: Path = REPO_ROOT) -> list[str]:
    return _section_contract_from_schema(page_type, load_schema(repo_root))


def generated_contract(repo_root: Path = REPO_ROOT) -> dict:
    schema = load_schema(repo_root)
    types = _page_types_from_schema(schema)
    required, optional = _property_contract_from_schema(schema)
    return {
        "base_table_order": BASE_TABLE_ORDER,
        "page_types": types,
        "required_properties": required,
        "optional_properties": optional,
        "placeholders": {
            page_type: {
                name: (
                    page_type
                    if name == "page_type"
                    else []
                    if name in {"tags", "aliases", "source_paths"}
                    else ""
                )
                for name in (*required, *optional)
            }
            for page_type in types
        },
        "sections": {
            page_type: tuple(_section_contract_from_schema(page_type, schema))
            for page_type in types
        },
        "tables": {name: tuple(columns) for name, columns in TABLE_COLUMNS.items()},
    }


def validate_instance(instance: dict, validator: Draft202012Validator) -> None:
    errors = sorted(
        validator.iter_errors(instance),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    if errors:
        details = "; ".join(
            f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
            for error in errors
        )
        raise KnowledgeSchemaError(details)


def _parse_frontmatter(text: str) -> tuple[dict, list[str]]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise KnowledgeSchemaError("YAML frontmatter opening delimiter missing")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise KnowledgeSchemaError(
            "YAML frontmatter closing delimiter missing"
        ) from exc
    loaded = load_unique_yaml("\n".join(lines[1:end]), "YAML frontmatter")
    if not isinstance(loaded, dict):
        raise KnowledgeSchemaError("YAML frontmatter must be a mapping")
    properties = {}
    for key, value in loaded.items():
        if isinstance(value, (dt.date, dt.datetime)):
            value = value.isoformat()
        elif isinstance(value, list):
            value = [
                item.isoformat() if isinstance(item, (dt.date, dt.datetime)) else item
                for item in value
            ]
        properties[key] = value
    for key, value in properties.items():
        if isinstance(value, dict) or (
            isinstance(value, list)
            and any(isinstance(item, (dict, list)) for item in value)
        ):
            raise KnowledgeSchemaError(
                f"property must be flat scalar or scalar list: {key}"
            )
    return properties, lines[end + 1 :]


def _section_ranges(lines: list[str]) -> tuple[list[str], dict[str, list[str]]]:
    headings: list[tuple[str, int]] = []
    for index, (line, fenced) in enumerate(zip(lines, markdown_fence_mask(lines))):
        if not fenced and line.startswith("## "):
            headings.append((line[3:].strip(), index))
    sections: dict[str, list[str]] = {}
    for offset, (heading, start) in enumerate(headings):
        if heading in sections:
            raise KnowledgeSchemaError(f"duplicate level-2 section: {heading}")
        end = headings[offset + 1][1] if offset + 1 < len(headings) else len(lines)
        sections[heading] = lines[start + 1 : end]
    return [heading for heading, _ in headings], sections


def _split_table_row(line: str) -> list[str]:
    if not line.startswith("|") or not line.endswith("|"):
        raise KnowledgeSchemaError(f"table row must start and end with pipe: {line}")
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in line[1:-1]:
        if escaped:
            current.append(char)
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    if escaped:
        current.append("\\")
    cells.append("".join(current).strip())
    return cells


def _parse_table(lines: list[str], expected: list[str]) -> list[dict[str, str]]:
    nonempty = [line.strip() for line in lines if line.strip()]
    if len(nonempty) < 2:
        raise KnowledgeSchemaError(f"table missing for columns: {expected}")
    header = _split_table_row(nonempty[0])
    delimiter = _split_table_row(nonempty[1])
    if [cell.lower() for cell in header] != expected:
        raise KnowledgeSchemaError(f"table columns must be exactly: {expected}")
    if len(delimiter) != len(expected) or not all(
        DELIMITER_RE.fullmatch(cell) for cell in delimiter
    ):
        raise KnowledgeSchemaError("invalid Markdown table delimiter row")
    rows: list[dict[str, str]] = []
    for line in nonempty[2:]:
        cells = _split_table_row(line)
        if len(cells) != len(expected):
            raise KnowledgeSchemaError(f"table row column count mismatch: {line}")
        rows.append(dict(zip(expected, cells)))
    return rows


def _link_target(value: str) -> str:
    match = WIKILINK_RE.fullmatch(value.strip())
    if not match:
        raise KnowledgeSchemaError(f"expected exact wikilink: {value}")
    return Path(match.group(1)).stem


def parse_markdown(
    path: Path,
    text: str | None = None,
    *,
    schema_path: Path = SCHEMA_PATH,
) -> dict:
    source = path.read_text(encoding="utf-8") if text is None else text
    properties, body_lines = _parse_frontmatter(source)
    ordered_sections, sections = _section_ranges(body_lines)

    claim_rows = _parse_table(
        sections.get("Claims", []),
        table_contract("Claims"),
    )
    claims = []
    for row in claim_rows:
        if row["primary"] not in {"true", "false"}:
            raise KnowledgeSchemaError("claim primary must be lowercase true or false")
        claims.append(
            {
                "id": row["id"],
                "primary": row["primary"] == "true",
                "text": row["claim"],
                "status": row["status"],
                "evidence": row["evidence"],
                "notes": row["notes"],
            }
        )

    relation_rows = _parse_table(
        sections.get("Relations", []), table_contract("Relations")
    )
    relations = [
        {
            "type": row["type"],
            "target": _link_target(row["target"]),
            "notes": row["notes"],
        }
        for row in relation_rows
    ]

    members = []
    if properties.get("page_type") == "collection":
        member_rows = _parse_table(
            sections.get("Members", []), table_contract("Members")
        )
        members = [
            {
                "target": _link_target(row["member"]),
                "role": row["role"],
                "rationale": row["rationale"],
            }
            for row in member_rows
        ]

    links = [
        Path(match).stem
        for line, fenced in zip(body_lines, markdown_fence_mask(body_lines))
        if not fenced
        for match in WIKILINK_RE.findall(line)
    ]
    instance = {
        "id": path.stem,
        "properties": properties,
        "ordered_sections": ordered_sections,
        "claims": claims,
        "relations": relations,
        "members": members,
        "links": links,
    }
    validate_instance(instance, validator_for("DocumentInstance", schema_path))
    return instance
