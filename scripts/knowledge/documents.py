from __future__ import annotations

from collections.abc import Mapping, Sequence

import yaml

CLAIMS_HEADER = (
    "| id | primary | claim | status | evidence | notes |",
    "|---|---|---|---|---|---|",
)
RELATIONS_HEADER = (
    "| type | target | notes |",
    "|---|---|---|",
)
MEMBERS_HEADER = (
    "| member | role | rationale |",
    "|---|---|---|",
)


def _demote_level_two_headings(lines: Sequence[str]) -> list[str]:
    rendered: list[str] = []
    fenced = False
    fence_token = ""
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            token = stripped[:3]
            if not fenced:
                fenced = True
                fence_token = token
            elif token == fence_token:
                fenced = False
            rendered.append(line)
        elif not fenced and line.startswith("## "):
            rendered.append(f"#{line}")
        else:
            rendered.append(line)
    return rendered


def _table(lines: Sequence[str]) -> list[str]:
    return ["", *lines, ""]


def render_preserved_document(
    *,
    properties: Mapping[str, object],
    legacy_body_lines: Sequence[str],
    legacy_frontmatter_end_line: int,
    required_sections: Sequence[str],
    source_manifest: str,
    members: Sequence[str],
    path_replacements: Mapping[str, str],
) -> bytes:
    frontmatter = yaml.safe_dump(
        dict(properties),
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    ).rstrip("\n")
    first_section = required_sections[0]
    prefix = ["---", *frontmatter.splitlines(), "---", "", f"## {first_section}"]
    prefix.extend("" for _ in range(max(0, legacy_frontmatter_end_line - len(prefix))))

    body = _demote_level_two_headings(legacy_body_lines)
    if path_replacements:
        body = [replace_paths(line, path_replacements) for line in body]
    lines = [*prefix, *body]
    for section in required_sections[1:]:
        lines.extend(["", f"## {section}"])
        if section == "Members":
            rows = [f"| [[{member}]] |  |  |" for member in members]
            lines.extend(_table([*MEMBERS_HEADER, *rows]))
        elif section == "Claims":
            lines.extend(_table(CLAIMS_HEADER))
        elif section == "Relations":
            lines.extend(_table(RELATIONS_HEADER))
        elif section == "Sources":
            lines.extend(["", f"- `{source_manifest}`", ""])
    return ("\n".join(lines).rstrip() + "\n").encode("utf-8")


def replace_paths(line: str, replacements: Mapping[str, str]) -> str:
    rendered = line
    for source, target in replacements.items():
        source_id = source.rsplit("/", 1)[-1].removesuffix(".md")
        target_id = target.rsplit("/", 1)[-1].removesuffix(".md")
        source_short = source.removeprefix("domains/information-security/")
        target_short = target.removeprefix("domains/information-security/")
        rendered = rendered.replace(f"wiki/{source}", f"wiki/{target}")
        rendered = rendered.replace(source, target)
        if source_short != source:
            rendered = rendered.replace(source_short, target_short)
        if source_id != target_id:
            rendered = rendered.replace(f"[[{source_id}]]", f"[[{target_id}]]")
            rendered = rendered.replace(f"[[{source_id}|", f"[[{target_id}|")
            rendered = rendered.replace(f"[[{source_id}#", f"[[{target_id}#")
    return rendered
