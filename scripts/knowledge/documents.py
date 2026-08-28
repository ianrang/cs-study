from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import stat
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path, PurePosixPath

import yaml

from .fs import (
    fsync_directory,
    publish_bytes_no_replace,
    rename_path_no_replace,
    replace_bytes_atomic,
    repository_write_lock,
)
from .schema import (
    KnowledgeSchemaError,
    active_domains,
    document_tree_sha256,
    parse_markdown,
    schema_digest,
    section_contract,
    table_contract,
    validate_instance,
    validator_for,
)


def _table_header(section: str) -> tuple[str, str]:
    columns = table_contract(section)
    return (
        "| " + " | ".join(columns) + " |",
        "|" + "|".join("---" for _ in columns) + "|",
    )
PAGE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MEMBERS_BODY_RE = re.compile(r"(?ms)(^## Members[ \t]*\r?\n)(.*?)(?=^## |\Z)")
PAGE_PLAN_GENERATOR = {"name": "cs-study", "version": "1.0"}
TABLE_ESCAPE_TRANSLATION = str.maketrans({"\\": "\\\\", "|": "\\|", "\n": " "})
CandidateCheck = Callable[[list[dict]], None]


class PagePlanError(ValueError):
    pass


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
            lines.extend(_table([*_table_header("Members"), *rows]))
        elif section == "Claims":
            lines.extend(_table(_table_header("Claims")))
        elif section == "Relations":
            lines.extend(_table(_table_header("Relations")))
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


def page_plan_bytes(plan: dict) -> bytes:
    return (
        json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def _canonical_digest(value: object) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _relative_page(knowledge_root: Path, path: Path) -> str:
    try:
        relative = path.resolve().relative_to(knowledge_root.resolve())
    except ValueError as exc:
        raise PagePlanError(f"page path escapes knowledge root: {path}") from exc
    value = relative.as_posix()
    pure = PurePosixPath(value)
    if (
        pure.is_absolute()
        or ".." in pure.parts
        or "." in pure.parts
        or "\\" in value
        or path.suffix != ".md"
    ):
        raise PagePlanError(f"invalid page path: {path}")
    return value


def _knowledge_root_name(repo_root: Path, knowledge_root: Path) -> str:
    try:
        relative = knowledge_root.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError as exc:
        raise PagePlanError("knowledge root must be inside repository") from exc
    if relative != "wiki":
        raise PagePlanError("knowledge root must be repo-relative wiki")
    return relative


def write_set_overrides(
    knowledge_root: Path, write_set: list[dict]
) -> dict[Path, str | None]:
    overrides: dict[Path, str | None] = {}
    for entry in write_set:
        source = entry["source_path"]
        target = entry["target_path"]
        if source is not None and source != target:
            overrides[knowledge_root / source] = None
        overrides[knowledge_root / target] = entry["content"]
    return overrides


def _build_page_plan(
    *,
    operation: str,
    operation_input: dict,
    write_set: list[dict],
    repo_root: Path,
    knowledge_root: Path,
    requires_review_approval: bool = False,
    review_verdicts: list[dict] | None = None,
) -> dict:
    base_tree = document_tree_sha256(knowledge_root)
    target_tree = document_tree_sha256(
        knowledge_root, write_set_overrides(knowledge_root, write_set)
    )
    plan = {
        "schema_version": "1.0",
        "operation": operation,
        "knowledge_root": _knowledge_root_name(repo_root, knowledge_root),
        "schema_sha256": schema_digest(repo_root),
        "base_tree_sha256": base_tree,
        "target_tree_sha256": target_tree,
        "input_sha256": _canonical_digest(operation_input),
        "generator": dict(PAGE_PLAN_GENERATOR),
        "requires_review_approval": requires_review_approval,
        "review_verdicts": review_verdicts or [],
        "operation_input": operation_input,
        "write_set": write_set,
    }
    try:
        validate_instance(
            plan,
            validator_for(
                "PageWritePlan", repo_root / "_meta" / "knowledge.schema.json"
            ),
        )
    except (KnowledgeSchemaError, OSError, ValueError) as exc:
        if isinstance(exc, PagePlanError):
            raise
        raise PagePlanError(str(exc)) from exc
    return plan


def _escape_table(value: object) -> str:
    return str(value).translate(TABLE_ESCAPE_TRANSLATION)


def _member_row(item: Mapping[str, object]) -> str:
    values = (f"[[{item['target']}]]", item["role"], item["rationale"])
    escaped = [str(value).translate(TABLE_ESCAPE_TRANSLATION) for value in values]
    return "| " + " | ".join(escaped) + " |"


def _relation_row(item: Mapping[str, object]) -> str:
    values = (item["type"], f"[[{item['target']}]]", item["notes"])
    escaped = [str(value).translate(TABLE_ESCAPE_TRANSLATION) for value in values]
    return "| " + " | ".join(escaped) + " |"


def _render_semantic_plan(plan: dict, page_id: str, now: str) -> str:
    required = section_contract(plan["page_type"])
    generated = {"Claims", "Relations", "Sources", "Members"}
    expected_sections = [heading for heading in required if heading not in generated]
    supplied_sections = [section["heading"] for section in plan["sections"]]
    if supplied_sections != expected_sections:
        raise PagePlanError(
            "semantic sections must be exactly "
            f"{expected_sections}: {supplied_sections}"
        )
    if plan["page_type"] != "collection" and plan["members"]:
        raise PagePlanError("members are only allowed for collection pages")
    properties = {
        "title": plan["title"],
        "page_type": plan["page_type"],
        "tags": plan["tags"],
        "date_created": now,
        "date_updated": now,
        "source_paths": plan["source_paths"],
        "summary": plan["summary"],
    }
    frontmatter = yaml.safe_dump(
        properties,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    ).rstrip("\n")
    section_bodies = {item["heading"]: item["body"] for item in plan["sections"]}
    lines = ["---", *frontmatter.splitlines(), "---"]
    for heading in required:
        lines.extend(["", f"## {heading}", ""])
        if heading in section_bodies:
            lines.extend(section_bodies[heading].rstrip().splitlines())
        elif heading == "Members":
            lines.extend(_table_header("Members"))
            lines.extend(_member_row(item) for item in plan["members"])
        elif heading == "Claims":
            lines.extend(_table_header("Claims"))
            lines.extend(
                "| "
                + " | ".join(
                    [
                        _escape_table(item["id"]),
                        str(item["primary"]).lower(),
                        _escape_table(item["text"]),
                        _escape_table(item["status"]),
                        _escape_table(item["evidence"]),
                        _escape_table(item["notes"]),
                    ]
                )
                + " |"
                for item in plan["claims"]
            )
        elif heading == "Relations":
            lines.extend(_table_header("Relations"))
            lines.extend(_relation_row(item) for item in plan["relations"])
        elif heading == "Sources":
            lines.extend(f"- `{path}`" for path in plan["source_paths"])
    rendered = "\n".join(lines).rstrip() + "\n"
    parse_markdown(Path(f"{page_id}.md"), rendered)
    return rendered


def _write_entry(
    action: str,
    source_path: str | None,
    target_path: str,
    content: str,
    base_content: str | None,
    base_sha256: str | None,
    base_mode: int | None,
) -> dict:
    return {
        "action": action,
        "source_path": source_path,
        "target_path": target_path,
        "base_sha256": base_sha256,
        "target_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "base_mode": base_mode,
        "target_mode": 0o644 if base_mode is None else base_mode,
        "base_content": base_content,
        "content": content,
    }


def build_synthesize_plan(
    *,
    semantic_plan_path: Path,
    source_paths: list[str],
    page_id: str,
    now: str,
    repo_root: Path,
    knowledge_root: Path,
) -> dict:
    try:
        semantic = json.loads(semantic_plan_path.read_text(encoding="utf-8"))
        validate_instance(
            semantic,
            validator_for(
                "SemanticPlan", repo_root / "_meta" / "knowledge.schema.json"
            ),
        )
    except (OSError, json.JSONDecodeError, KnowledgeSchemaError) as exc:
        raise PagePlanError(f"invalid SemanticPlan: {exc}") from exc
    if semantic["source_paths"] != source_paths:
        raise PagePlanError("CLI and SemanticPlan source paths must exact match")
    if semantic["domain"] not in active_domains(repo_root):
        raise PagePlanError(f"domain is not an active domain: {semantic['domain']}")
    if not PAGE_ID_RE.fullmatch(page_id):
        raise PagePlanError(f"invalid page ID: {page_id}")
    try:
        parsed_date = dt.date.fromisoformat(now)
    except ValueError as exc:
        raise PagePlanError(f"invalid --now date: {now}") from exc
    if parsed_date.isoformat() != now:
        raise PagePlanError(f"--now must be canonical YYYY-MM-DD: {now}")
    target_relative = f"staging/{semantic['domain']}/{page_id}.md"
    target = knowledge_root / target_relative
    if target.exists() or target.is_symlink():
        raise PagePlanError(f"synthesize target already exists: {target}")
    content = _render_semantic_plan(semantic, page_id, now)
    entry = _write_entry("create", None, target_relative, content, None, None, None)
    plan = _build_page_plan(
        operation="synthesize",
        operation_input={
            "semantic_plan_sha256": hashlib.sha256(
                semantic_plan_path.read_bytes()
            ).hexdigest(),
            "source_paths": source_paths,
            "page_id": page_id,
            "now": now,
        },
        write_set=[entry],
        repo_root=repo_root,
        knowledge_root=knowledge_root,
    )
    return plan


def _existing_page(knowledge_root: Path, path: Path) -> tuple[str, str, dict]:
    relative = _relative_page(knowledge_root, path)
    if not path.is_file() or path.is_symlink():
        raise PagePlanError(f"source page must be a regular file: {path}")
    try:
        content = path.read_bytes().decode("utf-8")
        instance = parse_markdown(path, content)
    except (OSError, UnicodeDecodeError, KnowledgeSchemaError) as exc:
        raise PagePlanError(f"invalid source page: {exc}") from exc
    return relative, content, instance


def _move_plan(
    *,
    operation: str,
    source: Path,
    target_dir: Path,
    repo_root: Path,
    knowledge_root: Path,
    requires_review_approval: bool,
    operation_input: dict,
    review_verdicts: list[dict] | None = None,
) -> dict:
    source_relative, content, _ = _existing_page(knowledge_root, source)
    if not target_dir.is_dir() or target_dir.is_symlink():
        raise PagePlanError(f"target directory must already exist: {target_dir}")
    target = target_dir / source.name
    target_relative = _relative_page(knowledge_root, target)
    if target.resolve() == source.resolve():
        write_set: list[dict] = []
    else:
        if target.exists() or target.is_symlink():
            raise PagePlanError(f"move target already exists: {target}")
        write_set = [
            _write_entry(
                "move",
                source_relative,
                target_relative,
                content,
                None,
                hashlib.sha256(content.encode("utf-8")).hexdigest(),
                stat.S_IMODE(source.stat().st_mode),
            )
        ]
    return _build_page_plan(
        operation=operation,
        operation_input=operation_input,
        write_set=write_set,
        repo_root=repo_root,
        knowledge_root=knowledge_root,
        requires_review_approval=requires_review_approval,
        review_verdicts=review_verdicts,
    )


def _validate_review_verdicts(instance: dict, verdicts: list[dict]) -> None:
    primary = {claim["id"]: claim for claim in instance["claims"] if claim["primary"]}
    if [row.get("claim_id") for row in verdicts] != sorted(primary):
        raise PagePlanError("review verdicts must exactly cover primary claims")
    for row in verdicts:
        claim = primary[row["claim_id"]]
        verdict = row.get("verdict")
        if claim["status"] == "claimed" or verdict == "insufficient":
            raise PagePlanError("claimed or insufficient primary claim cannot promote")
        supported = claim["status"] in {"corroborated", "verified"}
        contradicted = claim["status"] == "rejected"
        if (verdict == "support") != supported or (
            (verdict == "contradiction") != contradicted
        ):
            raise PagePlanError("review verdict and claim status do not match")


def build_promote_plan(
    draft: Path,
    target_dir: Path,
    *,
    review_verdicts_path: Path,
    repo_root: Path,
    knowledge_root: Path,
) -> dict:
    source_relative = _relative_page(knowledge_root, draft)
    if not source_relative.startswith("staging/"):
        raise PagePlanError("promote source must be a staging draft")
    target_relative = _relative_page(knowledge_root, target_dir / draft.name)
    if not target_relative.startswith(("domains/", "collections/")):
        raise PagePlanError("promote target must be an active lifecycle directory")
    _, _, instance = _existing_page(knowledge_root, draft)
    try:
        verdicts = json.loads(review_verdicts_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PagePlanError(f"invalid review verdicts: {exc}") from exc
    if not isinstance(verdicts, list) or any(
        not isinstance(row, dict) for row in verdicts
    ):
        raise PagePlanError("review verdicts must be an array of objects")
    if [row.get("claim_id") for row in verdicts] != sorted(
        str(row.get("claim_id", "")) for row in verdicts
    ):
        raise PagePlanError("review verdict input must be sorted by claim_id")
    _validate_review_verdicts(instance, verdicts)
    verdict_digest = _canonical_digest(verdicts)
    plan = _move_plan(
        operation="promote",
        source=draft,
        target_dir=target_dir,
        repo_root=repo_root,
        knowledge_root=knowledge_root,
        requires_review_approval=True,
        operation_input={
            "source_path": source_relative,
            "target_path": target_relative,
            "review_verdicts_sha256": verdict_digest,
        },
        review_verdicts=verdicts,
    )
    return plan


def _lifecycle(relative: str) -> str:
    first = PurePosixPath(relative).parts[0]
    if first not in {"staging", "domains", "collections", "archive"}:
        raise PagePlanError(f"page is outside a lifecycle root: {relative}")
    return first


def build_move_plan(
    page: Path,
    target_dir: Path,
    *,
    repo_root: Path,
    knowledge_root: Path,
) -> dict:
    source_relative = _relative_page(knowledge_root, page)
    target_relative = _relative_page(knowledge_root, target_dir / page.name)
    if _lifecycle(source_relative) != _lifecycle(target_relative):
        raise PagePlanError("move must remain in the same lifecycle root")
    plan = _move_plan(
        operation="move",
        source=page,
        target_dir=target_dir,
        repo_root=repo_root,
        knowledge_root=knowledge_root,
        requires_review_approval=False,
        operation_input={
            "source_path": source_relative,
            "target_path": target_relative,
        },
    )
    return plan


def _replace_members(content: str, members: Sequence[dict]) -> str:
    match = MEMBERS_BODY_RE.search(content)
    if match is None:
        raise PagePlanError("collection Members section is missing")
    replacement = "\n".join(
        [
            "",
            *_table_header("Members"),
            *(_member_row(item) for item in members),
            "",
            "",
        ]
    )
    return content[: match.start(2)] + replacement + content[match.end(2) :]


def _collection_plan(
    *,
    operation: str,
    collection: Path,
    members: Sequence[dict],
    input_value: object,
    repo_root: Path,
    knowledge_root: Path,
) -> dict:
    relative, content, instance = _existing_page(knowledge_root, collection)
    if instance["properties"]["page_type"] != "collection":
        raise PagePlanError("collection command requires page_type collection")
    rendered = _replace_members(content, members)
    if rendered == content:
        write_set: list[dict] = []
    else:
        write_set = [
            _write_entry(
                "replace",
                relative,
                relative,
                rendered,
                content,
                hashlib.sha256(content.encode("utf-8")).hexdigest(),
                stat.S_IMODE(collection.stat().st_mode),
            )
        ]
    return _build_page_plan(
        operation=operation,
        operation_input=input_value,
        write_set=write_set,
        repo_root=repo_root,
        knowledge_root=knowledge_root,
    )


def build_collection_add_member_plan(
    collection: Path,
    member: str,
    *,
    before: str | None,
    after: str | None,
    order_by_id: bool,
    repo_root: Path,
    knowledge_root: Path,
) -> dict:
    relative, _, instance = _existing_page(knowledge_root, collection)
    existing = list(instance["members"])
    targets = [item["target"] for item in existing]
    if len(targets) != len(set(targets)):
        raise PagePlanError("duplicate collection member in source page")
    if member in targets:
        raise PagePlanError(f"duplicate collection member: {member}")
    if sum((before is not None, after is not None, order_by_id)) != 1:
        raise PagePlanError("select exactly one collection ordering policy")
    added = {"target": member, "role": "", "rationale": ""}
    if order_by_id:
        updated = sorted([*existing, added], key=lambda item: item["target"])
    else:
        anchor = before if before is not None else after
        if anchor not in targets:
            raise PagePlanError(f"collection ordering anchor is not a member: {anchor}")
        index = targets.index(anchor) + int(after is not None)
        updated = [*existing[:index], added, *existing[index:]]
    plan = _collection_plan(
        operation="collection-add-member",
        collection=collection,
        members=updated,
        input_value={
            "collection_path": relative,
            "member": member,
            "before": before,
            "after": after,
            "order_by_id": order_by_id,
        },
        repo_root=repo_root,
        knowledge_root=knowledge_root,
    )
    return plan


def build_collection_reorder_plan(
    collection: Path,
    members: list[str],
    *,
    repo_root: Path,
    knowledge_root: Path,
) -> dict:
    relative, _, instance = _existing_page(knowledge_root, collection)
    targets = [item["target"] for item in instance["members"]]
    if len(targets) != len(set(targets)):
        raise PagePlanError("duplicate collection member in source page")
    existing = {item["target"]: item for item in instance["members"]}
    if len(members) != len(set(members)) or set(members) != set(existing):
        raise PagePlanError("reorder must provide the exact member set once")
    plan = _collection_plan(
        operation="collection-reorder",
        collection=collection,
        members=[existing[target] for target in members],
        input_value={"collection_path": relative, "members": members},
        repo_root=repo_root,
        knowledge_root=knowledge_root,
    )
    return plan


def load_page_write_plan(path: Path, repo_root: Path) -> tuple[bytes, dict]:
    try:
        raw = path.read_bytes()
        plan = json.loads(raw)
        validate_instance(
            plan,
            validator_for(
                "PageWritePlan", repo_root / "_meta" / "knowledge.schema.json"
            ),
        )
    except (OSError, json.JSONDecodeError, KnowledgeSchemaError) as exc:
        raise PagePlanError(f"invalid PageWritePlan: {exc}") from exc
    return raw, plan


def _validate_plan_operation(plan: dict, entry: dict) -> None:
    expected_actions = {
        "synthesize": "create",
        "promote": "move",
        "collection-add-member": "replace",
        "collection-reorder": "replace",
        "move": "move",
    }
    if expected_actions[plan["operation"]] != entry["action"]:
        raise PagePlanError("operation and page action do not match")
    source = entry["source_path"]
    target = entry["target_path"]
    operation_input = plan["operation_input"]
    if plan["operation"] in {"promote", "move"} and (
        operation_input["source_path"] != source
        or operation_input["target_path"] != target
    ):
        raise PagePlanError("operation input paths do not match write-set")
    if plan["operation"].startswith("collection-") and (
        operation_input["collection_path"] != source or source != target
    ):
        raise PagePlanError("collection operation input path does not match write-set")
    if plan["operation"] == "synthesize":
        operation_input = plan["operation_input"]
        instance = parse_markdown(Path(target), entry["content"])
        properties = instance["properties"]
        if _lifecycle(target) != "staging":
            raise PagePlanError("synthesize target must be staging")
        if (
            PurePosixPath(target).stem != operation_input["page_id"]
            or properties["source_paths"] != operation_input["source_paths"]
            or properties["date_created"] != operation_input["now"]
            or properties["date_updated"] != operation_input["now"]
        ):
            raise PagePlanError("synthesize operation input does not match target page")
    if plan["operation"] == "promote":
        if source is None or _lifecycle(source) != "staging":
            raise PagePlanError("promote source must be staging")
        if _lifecycle(target) not in {"domains", "collections"}:
            raise PagePlanError("promote target must be active")
    if plan["operation"] == "move":
        if source is None or _lifecycle(source) != _lifecycle(target):
            raise PagePlanError("move must remain in the same lifecycle root")


def _outside_members_section(content: str) -> tuple[str, str]:
    match = MEMBERS_BODY_RE.search(content)
    if match is None:
        raise PagePlanError("collection Members section is missing")
    return content[: match.start(2)], content[match.end(2) :]


def _validate_collection_delta(
    plan: dict, path: Path, source_content: str, content: str
) -> None:
    if _outside_members_section(source_content) != _outside_members_section(content):
        raise PagePlanError("collection delta must preserve raw bytes outside Members")
    before = parse_markdown(path, source_content)["members"]
    after = parse_markdown(path, content)["members"]
    before_targets = [row["target"] for row in before]
    if len(before_targets) != len(set(before_targets)):
        raise PagePlanError("duplicate collection member in source page")
    operation_input = plan["operation_input"]
    if plan["operation"] == "collection-add-member":
        member = operation_input["member"]
        added = [row for row in after if row["target"] == member]
        preserved = [row for row in after if row["target"] != member]
        if (
            added != [{"target": member, "role": "", "rationale": ""}]
            or preserved != before
            or len(after) != len(before) + 1
        ):
            raise PagePlanError("collection add-member delta is invalid")
        if operation_input["order_by_id"]:
            expected = sorted([*before, added[0]], key=lambda row: row["target"])
        else:
            anchor = operation_input["before"] or operation_input["after"]
            try:
                index = before_targets.index(anchor)
            except ValueError as exc:
                raise PagePlanError(
                    "collection ordering anchor is not a member"
                ) from exc
            index += int(operation_input["after"] is not None)
            expected = [*before[:index], added[0], *before[index:]]
        if after != expected:
            raise PagePlanError("collection add-member ordering delta is invalid")
    else:
        try:
            requested = operation_input["members"]
            if len(requested) != len(before_targets) or set(requested) != set(
                before_targets
            ):
                raise PagePlanError("collection reorder requires the exact member set")
            expected = [
                next(row for row in before if row["target"] == target)
                for target in requested
            ]
        except StopIteration as exc:
            raise PagePlanError("collection reorder delta is invalid") from exc
        if after != expected:
            raise PagePlanError("collection reorder delta is invalid")


def _validate_noop_operation(plan: dict, knowledge_root: Path) -> None:
    operation_input = plan["operation_input"]
    if plan["operation"] == "collection-reorder":
        collection = knowledge_root / operation_input["collection_path"]
        _relative_page(knowledge_root, collection)
        if not collection.is_file() or collection.is_symlink():
            raise PagePlanError("no-op collection page is missing")
        instance = parse_markdown(collection)
        if instance["properties"]["page_type"] != "collection":
            raise PagePlanError("no-op collection operation requires a collection page")
        if [row["target"] for row in instance["members"]] != operation_input["members"]:
            raise PagePlanError("no-op collection order does not match operation input")
        return
    if plan["operation"] == "move":
        source = operation_input["source_path"]
        target = operation_input["target_path"]
        if source != target or _lifecycle(source) != _lifecycle(target):
            raise PagePlanError("no-op move requires one unchanged lifecycle path")
        page = knowledge_root / source
        _relative_page(knowledge_root, page)
        if not page.is_file() or page.is_symlink():
            raise PagePlanError("no-op move source page is missing")
        return
    raise PagePlanError(f"{plan['operation']} does not permit a no-op plan")


def _leaf_matches(path: Path, content: bytes, mode: int) -> bool | None:
    try:
        return (
            path.is_file()
            and not path.is_symlink()
            and path.read_bytes() == content
            and stat.S_IMODE(path.stat().st_mode) == mode
        )
    except OSError:
        return None


def _apply_page_write_plan_unlocked(
    plan_path: Path,
    confirmation: str,
    *,
    repo_root: Path,
    knowledge_root: Path,
    candidate_check: CandidateCheck,
    expected_operation: str | None = None,
    review_approved: bool = False,
) -> bool:
    raw, plan = load_page_write_plan(plan_path, repo_root)
    if hashlib.sha256(raw).hexdigest() != confirmation:
        raise PagePlanError("plan confirmation SHA-256 does not match exact bytes")
    if _knowledge_root_name(repo_root, knowledge_root) != plan["knowledge_root"]:
        raise PagePlanError("plan knowledge root does not match requested root")
    if schema_digest(repo_root) != plan["schema_sha256"]:
        raise PagePlanError("stale plan schema digest")
    if plan["generator"] != PAGE_PLAN_GENERATOR:
        raise PagePlanError("unsupported page plan generator")
    if expected_operation is not None and plan["operation"] != expected_operation:
        raise PagePlanError("invoked command and plan operation do not match")
    if plan["requires_review_approval"] and not review_approved:
        raise PagePlanError("explicit review approval is required")
    if _canonical_digest(plan["operation_input"]) != plan["input_sha256"]:
        raise PagePlanError("operation input digest does not match plan")
    if plan["operation"] == "promote" and _canonical_digest(
        plan["review_verdicts"]
    ) != plan["operation_input"]["review_verdicts_sha256"]:
        raise PagePlanError("review verdict digest does not match operation input")
    write_set = plan["write_set"]
    candidate_check(write_set)
    current_tree = document_tree_sha256(knowledge_root)
    if not write_set:
        _validate_noop_operation(plan, knowledge_root)
        if plan["target_tree_sha256"] != plan["base_tree_sha256"]:
            raise PagePlanError("no-op plan target tree differs from base tree")
        if current_tree != plan["base_tree_sha256"]:
            raise PagePlanError("stale plan base tree digest")
        return False
    entry = write_set[0]
    source = (
        knowledge_root / entry["source_path"]
        if entry["source_path"] is not None
        else None
    )
    target = knowledge_root / entry["target_path"]
    _relative_page(knowledge_root, target)
    content_bytes = entry["content"].encode("utf-8")
    if hashlib.sha256(content_bytes).hexdigest() != entry["target_sha256"]:
        raise PagePlanError("target content digest does not match plan")
    _validate_plan_operation(plan, entry)
    if entry["action"] == "create":
        if (
            source is not None
            or entry["base_sha256"] is not None
            or entry["base_mode"] is not None
            or entry["base_content"] is not None
            or entry["target_mode"] != 0o644
        ):
            raise PagePlanError("create plan must use an absent base and mode 0644")
    else:
        base_content = entry["base_content"]
        base_payload = entry["content"] if entry["action"] == "move" else base_content
        if (
            entry["action"] == "move"
            and entry["base_sha256"] != entry["target_sha256"]
        ):
            raise PagePlanError("move must preserve source bytes")
        if (
            entry["base_mode"] is None
            or entry["target_mode"] != entry["base_mode"]
            or (entry["action"] == "replace" and not isinstance(base_content, str))
            or (entry["action"] == "move" and base_content is not None)
            or not isinstance(base_payload, str)
            or hashlib.sha256(base_payload.encode("utf-8")).hexdigest()
            != entry["base_sha256"]
        ):
            raise PagePlanError(
                "replace/move base content and target mode must preserve source"
            )
    if current_tree == plan["target_tree_sha256"]:
        if _leaf_matches(target, content_bytes, entry["target_mode"]) is not True:
            raise PagePlanError("target tree matches but target page bytes differ")
        if entry["action"] == "move" and source is not None and (
            source.exists() or source.is_symlink()
        ):
            raise PagePlanError("target tree matches but move source still exists")
        if plan["operation"] == "promote":
            _validate_review_verdicts(
                parse_markdown(target, entry["content"]), plan["review_verdicts"]
            )
        if plan["operation"].startswith("collection-"):
            _validate_collection_delta(
                plan, target, entry["base_content"], entry["content"]
            )
        return False
    if current_tree != plan["base_tree_sha256"]:
        raise PagePlanError("stale plan base tree digest")
    if entry["action"] == "create":
        if target.exists() or target.is_symlink():
            raise PagePlanError("create target collision")
    else:
        if source is None:
            raise PagePlanError("replace/move plan requires a source")
        _relative_page(knowledge_root, source)
        if not source.is_file() or source.is_symlink():
            raise PagePlanError("source page is missing")
        if hashlib.sha256(source.read_bytes()).hexdigest() != entry["base_sha256"]:
            raise PagePlanError("stale source page digest")
        if stat.S_IMODE(source.stat().st_mode) != entry["base_mode"]:
            raise PagePlanError("stale source page mode")
        if entry["action"] == "replace" and source.resolve() != target.resolve():
            raise PagePlanError("replace source and target path must match")
        if entry["action"] == "move":
            if source.stem != target.stem:
                raise PagePlanError("move must preserve page ID")
            if target.exists() or target.is_symlink():
                raise PagePlanError("move target collision")
            if source.read_bytes() != content_bytes:
                raise PagePlanError("move must preserve source bytes")
    if plan["operation"].startswith("collection-"):
        if (
            source is None
            or parse_markdown(source)["properties"]["page_type"] != "collection"
        ):
            raise PagePlanError("collection operation requires a collection page")
        _validate_collection_delta(
            plan, source, entry["base_content"], entry["content"]
        )
    if plan["operation"] == "promote":
        _validate_review_verdicts(parse_markdown(source), plan["review_verdicts"])
    overrides = write_set_overrides(knowledge_root, write_set)
    if document_tree_sha256(knowledge_root, overrides) != plan["target_tree_sha256"]:
        raise PagePlanError("target tree digest does not match candidate")
    if document_tree_sha256(knowledge_root) != plan["base_tree_sha256"]:
        raise PagePlanError("stale plan base tree after candidate validation")
    if source is not None and (
        hashlib.sha256(source.read_bytes()).hexdigest() != entry["base_sha256"]
        or stat.S_IMODE(source.stat().st_mode) != entry["base_mode"]
    ):
        raise PagePlanError("stale source bytes or mode after candidate validation")
    previous_content = source.read_bytes() if source is not None else None
    if entry["action"] == "create":
        changed = publish_bytes_no_replace(target, content_bytes)
    elif entry["action"] == "replace":
        replace_bytes_atomic(target, content_bytes)
        changed = True
    else:
        rename_path_no_replace(source, target)
        changed = True
    post_tree_error: Exception | None = None
    try:
        post_tree_matches = (
            document_tree_sha256(knowledge_root) == plan["target_tree_sha256"]
        )
    except (KnowledgeSchemaError, OSError) as exc:
        post_tree_error = exc
        post_tree_matches = False
    if not post_tree_matches:
        target_is_planned_leaf = _leaf_matches(
            target, content_bytes, entry["target_mode"]
        )
        if target_is_planned_leaf is None:
            raise PagePlanError(
                "apply state indeterminate; planned target leaf could not be observed"
            )
        if not target_is_planned_leaf:
            raise PagePlanError(
                "apply state indeterminate; observed target differs from planned leaf; "
                f"source_exists={source.exists() if source is not None else False}; "
                f"target_exists={target.exists() or target.is_symlink()}"
            )
        if entry["action"] == "move" and source is not None and source.exists():
            raise PagePlanError(
                "apply state indeterminate; move source reappeared before rollback; "
                f"source_exists=True; target_exists={target.exists()}"
            )
        try:
            if entry["action"] == "create":
                target.unlink()
                fsync_directory(target.parent)
            elif entry["action"] == "replace" and previous_content is not None:
                replace_bytes_atomic(target, previous_content)
            elif source is not None and not source.exists():
                rename_path_no_replace(target, source)
        except OSError as exc:
            raise PagePlanError(
                "apply state indeterminate; own leaf rollback failed; "
                f"source_exists={source.exists() if source is not None else False}; "
                f"target_exists={target.exists() or target.is_symlink()}"
            ) from exc
        try:
            if entry["action"] == "create":
                base_restored = not target.exists() and not target.is_symlink()
            elif entry["action"] == "replace" and previous_content is not None:
                base_restored = _leaf_matches(
                    target, previous_content, entry["base_mode"]
                )
            else:
                base_bytes = (
                    entry["content"]
                    if entry["action"] == "move"
                    else entry["base_content"]
                ).encode("utf-8")
                base_restored = (
                    source is not None
                    and _leaf_matches(source, base_bytes, entry["base_mode"]) is True
                    and not target.exists()
                    and not target.is_symlink()
                )
        except OSError as exc:
            raise PagePlanError(
                "apply state indeterminate; rollback state could not be observed"
            ) from exc
        if base_restored is None:
            raise PagePlanError(
                "apply state indeterminate; rollback state could not be observed"
            )
        if not base_restored:
            raise PagePlanError(
                "apply state indeterminate; rollback did not restore exact base; "
                f"source_exists={source.exists() if source is not None else False}; "
                f"target_exists={target.exists() or target.is_symlink()}"
            )
        raise PagePlanError(
            "applied tree digest differs from plan; own leaf rolled back"
        ) from post_tree_error
    return changed


def apply_page_write_plan(
    plan_path: Path,
    confirmation: str,
    *,
    repo_root: Path,
    knowledge_root: Path,
    candidate_check: CandidateCheck,
    expected_operation: str | None = None,
    review_approved: bool = False,
) -> bool:
    try:
        with repository_write_lock(repo_root):
            return _apply_page_write_plan_unlocked(
                plan_path,
                confirmation,
                repo_root=repo_root,
                knowledge_root=knowledge_root,
                candidate_check=candidate_check,
                expected_operation=expected_operation,
                review_approved=review_approved,
            )
    except BlockingIOError as exc:
        raise PagePlanError("repository writer lock is already held") from exc
