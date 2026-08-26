from __future__ import annotations

import copy
import datetime as dt
import json
import re
from pathlib import Path

import yaml
from contracts.timestamps import is_canonical_datetime, is_contract_datetime
from jsonschema import Draft202012Validator, FormatChecker

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "_meta" / "knowledge.schema.json"
GENERATED_ROOT_FILES = frozenset({"index.md", "overview.md", "log.md"})
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
DELIMITER_RE = re.compile(r"^:?-{3,}:?$")


class KnowledgeSchemaError(ValueError):
    pass


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
        relative = path.resolve().relative_to(target_root.resolve())
    except ValueError:
        return False
    return (
        path.suffix == ".md"
        and relative.as_posix() not in GENERATED_ROOT_FILES
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


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def validator_for(definition: str) -> Draft202012Validator:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    if definition not in schema.get("$defs", {}):
        raise KnowledgeSchemaError(f"unknown schema definition: {definition}")
    selected = {
        "$schema": schema["$schema"],
        "$ref": f"#/$defs/{definition}",
        "$defs": copy.deepcopy(schema["$defs"]),
    }
    Draft202012Validator.check_schema(selected)
    return Draft202012Validator(selected, format_checker=knowledge_format_checker())


def section_contract(page_type: str) -> list[str]:
    schema = load_schema()
    for condition in schema["$defs"]["DocumentInstance"]["allOf"]:
        declared = condition["if"]["properties"]["properties"]["properties"][
            "page_type"
        ].get("const")
        if declared == page_type:
            return list(condition["then"]["properties"]["ordered_sections"]["const"])
    raise KnowledgeSchemaError(f"unknown page_type section contract: {page_type}")


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
    try:
        loaded = yaml.load("\n".join(lines[1:end]), Loader=_UniqueKeyLoader)
    except yaml.YAMLError as exc:
        raise KnowledgeSchemaError(f"invalid YAML frontmatter: {exc}") from exc
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
    fenced = False
    fence_token = ""
    for index, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            token = stripped[:3]
            if not fenced:
                fenced = True
                fence_token = token
            elif token == fence_token:
                fenced = False
            continue
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


def parse_markdown(path: Path, text: str | None = None) -> dict:
    source = path.read_text(encoding="utf-8") if text is None else text
    properties, body_lines = _parse_frontmatter(source)
    ordered_sections, sections = _section_ranges(body_lines)

    claim_rows = _parse_table(
        sections.get("Claims", []),
        ["id", "primary", "claim", "status", "evidence", "notes"],
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
        sections.get("Relations", []), ["type", "target", "notes"]
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
            sections.get("Members", []), ["member", "role", "rationale"]
        )
        members = [
            {
                "target": _link_target(row["member"]),
                "role": row["role"],
                "rationale": row["rationale"],
            }
            for row in member_rows
        ]

    links = [Path(match).stem for match in WIKILINK_RE.findall("\n".join(body_lines))]
    instance = {
        "id": path.stem,
        "properties": properties,
        "ordered_sections": ordered_sections,
        "claims": claims,
        "relations": relations,
        "members": members,
        "links": links,
    }
    validate_instance(instance, validator_for("DocumentInstance"))
    return instance


def inspect_markdown(path: Path, text: str | None = None) -> tuple[dict, list[str]]:
    source = path.read_text(encoding="utf-8") if text is None else text
    properties, body_lines = _parse_frontmatter(source)
    ordered_sections, _ = _section_ranges(body_lines)
    return properties, ordered_sections


def inspect_headings(path: Path, text: str | None = None) -> list[str]:
    source = path.read_text(encoding="utf-8") if text is None else text
    ordered_sections, _ = _section_ranges(source.splitlines())
    return ordered_sections
