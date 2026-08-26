"""Read-only converter for reconstructed practical-exam Markdown tables."""

from __future__ import annotations

import hashlib
import json
import re
import stat
import sys
import unicodedata
from pathlib import Path

REPO_SCRIPTS = Path(__file__).resolve().parents[3] / "scripts"
sys.path.insert(0, str(REPO_SCRIPTS))

from contracts.timestamps import (  # noqa: E402
    is_canonical_datetime as _is_canonical_timestamp,
)

ROUND_FILE_PATTERN = re.compile(
    r"^(?P<year>\d{4})-(?P<session>\d{2})-practical-(?P<round>\d+)\.md$"
)
ROW_PATTERN = re.compile(r"^\|\s*\d+\s*\|")
RECONSTRUCTION_HEADER = "| no | type | reconstructed prompt | answer | verification |"
VALID_TYPES = {"short", "essay", "practical"}
DISPLAY_BLOCK_TOKEN = re.compile(
    r"\{\{(?P<closing>/)?(?P<kind>code|reference)(?::(?P<language>[^\}]*))?\}\}"
)
DISPLAY_BLOCK_LANGUAGE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CLIPPING_MANIFEST_PATH = re.compile(
    r"^raw/sources/clipping/(?P<source_id>[a-f0-9]{64})/"
    r"(?P<digest>[a-f0-9]{64})/manifest\.json$"
)
CLIPPING_MANIFEST_KEYS = {
    "artifact_digest",
    "created_at",
    "generator",
    "media_type",
    "payload",
    "primary_source",
    "schema_version",
    "size",
    "source_id",
    "source_type",
}


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _frontmatter(lines: list[str], path: Path) -> dict[str, object]:
    if not lines or lines[0] != "---":
        raise ValueError(f"{path}: frontmatter must start with ---")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError(f"{path}: frontmatter closing --- is missing") from error

    result: dict[str, object] = {}
    active_list: str | None = None
    for line in lines[1:end]:
        stripped = line.strip()
        if active_list is not None and stripped.startswith("- "):
            values = result[active_list]
            if isinstance(values, list):
                values.append(stripped[2:].strip().strip('"\''))
            continue
        active_list = None
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"')
        if value:
            result[key] = value
        else:
            result[key] = []
            active_list = key
    if not isinstance(result.get("title"), str) or not result["title"]:
        raise ValueError(f"{path}: frontmatter title is required")
    return result


def _document_provenance(
    frontmatter: dict[str, object], path: Path, vault_root: Path
) -> str:
    provenance = frontmatter.get("provenance")
    if isinstance(provenance, str) and provenance:
        return provenance
    source_paths = frontmatter.get("source_paths")
    if not isinstance(source_paths, list) or len(source_paths) != 1:
        raise ValueError(f"{path}: frontmatter provenance or one source_paths entry is required")
    manifest_relative = source_paths[0]
    match = (
        CLIPPING_MANIFEST_PATH.fullmatch(manifest_relative)
        if isinstance(manifest_relative, str)
        else None
    )
    if match is None:
        raise ValueError(f"{path}: preservation source manifest path is invalid")
    repo_root = vault_root.parents[2]
    manifest_path = repo_root.joinpath(*Path(manifest_relative).parts)
    current = repo_root
    for part in Path(manifest_relative).parts:
        current /= part
        try:
            mode = current.lstat().st_mode
        except OSError as error:
            raise ValueError(f"{path}: preservation source manifest is unavailable") from error
        if stat.S_ISLNK(mode):
            raise ValueError(f"{path}: preservation bundle symlink is forbidden")
    try:
        manifest_mode = manifest_path.lstat().st_mode
        if not stat.S_ISREG(manifest_mode):
            raise ValueError(f"{path}: preservation source manifest is not regular")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        payload_name = manifest["payload"]
        artifact_digest = manifest["artifact_digest"]
        expected_size = manifest["size"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        raise ValueError(f"{path}: preservation source manifest is invalid") from error
    generator = manifest.get("generator")
    primary_source = manifest.get("primary_source")
    expected_source_id = match["source_id"]
    expected_digest = match["digest"]
    if (
        not isinstance(manifest, dict)
        or set(manifest) != CLIPPING_MANIFEST_KEYS
        or manifest.get("schema_version") != "1.0"
        or manifest.get("source_type") != "clipping"
        or manifest.get("source_id") != expected_source_id
        or artifact_digest != f"sha256:{expected_digest}"
        or manifest.get("media_type") != "text/markdown"
        or payload_name != "payload.md"
        or type(expected_size) is not int
        or expected_size < 0
        or not _is_canonical_timestamp(manifest.get("created_at"))
        or not isinstance(generator, dict)
        or set(generator) != {"name", "version"}
        or not all(isinstance(generator[key], str) and generator[key] for key in generator)
        or not isinstance(primary_source, str)
        or not primary_source
        or hashlib.sha256(
            unicodedata.normalize("NFC", primary_source).encode("utf-8")
        ).hexdigest()
        != expected_source_id
    ):
        raise ValueError(f"{path}: preservation source manifest contract is invalid")
    payload_path = manifest_path.parent / payload_name
    try:
        payload_mode = payload_path.lstat().st_mode
        if not stat.S_ISREG(payload_mode):
            raise ValueError(f"{path}: preservation payload is not regular")
        if {entry.name for entry in manifest_path.parent.iterdir()} != {
            "manifest.json",
            "payload.md",
        }:
            raise ValueError(f"{path}: preservation bundle file set is invalid")
        payload_bytes = payload_path.read_bytes()
        payload_text = payload_bytes.decode("utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise ValueError(f"{path}: preservation payload is unavailable") from error
    if (
        len(payload_bytes) != expected_size
        or hashlib.sha256(payload_bytes).hexdigest() != expected_digest
    ):
        raise ValueError(f"{path}: preservation payload digest mismatch")
    legacy = _frontmatter(payload_text.splitlines(), payload_path)
    legacy_provenance = legacy.get("provenance")
    if not isinstance(legacy_provenance, str) or not legacy_provenance:
        raise ValueError(f"{path}: preserved frontmatter provenance is required")
    return legacy_provenance


def split_markdown_row(line: str, path: Path, line_number: int) -> list[str]:
    """Split a five-cell Markdown table row while preserving escaped pipes."""
    if not line.startswith("|") or not line.endswith("|"):
        raise ValueError(f"{path}:{line_number}: table row must start and end with |")

    cells: list[str] = []
    current: list[str] = []
    index = 1
    while index < len(line) - 1:
        character = line[index]
        if character == "\\" and index + 1 < len(line) - 1 and line[index + 1] == "|":
            current.append("|")
            index += 2
            continue
        if character == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(character)
        index += 1
    cells.append("".join(current).strip())
    if len(cells) != 5 or any(not cell for cell in cells):
        raise ValueError(f"{path}:{line_number}: requires five non-empty cells")
    return cells


def validate_display_blocks(value: str, path: Path, line_number: int, field: str) -> None:
    """Reject ambiguous or unsafe display-block markers before data generation."""
    open_block: tuple[str, int] | None = None
    for marker in DISPLAY_BLOCK_TOKEN.finditer(value):
        kind = marker["kind"]
        language = marker["language"]
        if marker["closing"]:
            if language is not None:
                raise ValueError(f"{path}:{line_number} {field}: closing display block cannot declare a language")
            if open_block is None:
                raise ValueError(f"{path}:{line_number} {field}: closing display block has no opening marker")
            if kind != open_block[0]:
                raise ValueError(f"{path}:{line_number} {field}: display block closing marker does not match opening marker")
            if not value[open_block[1] : marker.start()].strip():
                raise ValueError(f"{path}:{line_number} {field}: display block content must not be empty")
            open_block = None
            continue

        if open_block is not None:
            raise ValueError(f"{path}:{line_number} {field}: display blocks cannot be nested")
        if kind == "reference" and language is not None:
            raise ValueError(f"{path}:{line_number} {field}: reference display block cannot declare a language")
        if language is not None and not DISPLAY_BLOCK_LANGUAGE.fullmatch(language):
            raise ValueError(f"{path}:{line_number} {field}: display block language must be lowercase kebab-case")
        open_block = (kind, marker.end())

    if open_block is not None:
        raise ValueError(f"{path}:{line_number} {field}: display block closing marker is missing")


def parse_round(path: Path, vault_root: Path) -> dict[str, object]:
    match = ROUND_FILE_PATTERN.fullmatch(path.name)
    if not match:
        raise ValueError(f"{path}: filename must be YYYY-SS-practical-NN.md")

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    frontmatter = _frontmatter(lines, path)
    try:
        header_index = lines.index(RECONSTRUCTION_HEADER)
    except ValueError as error:
        raise ValueError(f"{path}: Reconstruction table header is missing") from error

    items: list[dict[str, object]] = []
    numbers: list[int] = []
    for zero_index, line in enumerate(lines[header_index + 2 :], start=header_index + 3):
        if not ROW_PATTERN.match(line):
            if items:
                break
            continue
        number_text, item_type, prompt, answer, verification = split_markdown_row(line, path, zero_index)
        number = int(number_text)
        if item_type not in VALID_TYPES:
            raise ValueError(f"{path}:{zero_index}: unsupported item type {item_type}")
        validate_display_blocks(prompt, path, zero_index, "prompt")
        validate_display_blocks(answer, path, zero_index, "answer")
        numbers.append(number)
        item_id = f"R{match['round']}-Q{number:02d}"
        items.append({
            "id": item_id,
            "number": number,
            "type": item_type,
            "prompt": prompt,
            "answer": answer,
            "verification": verification,
            "sourcePath": str(path.relative_to(vault_root)),
            "sourceLine": zero_index,
            "sourceRef": {
                "path": str(path.relative_to(vault_root)),
                "line": zero_index,
                "excerpt": verification,
                "status": "source-derived",
            },
            "contentDigest": _sha256("\n".join((prompt, answer, verification))),
        })
    if not items:
        raise ValueError(f"{path}: Reconstruction table has no items")
    if numbers != list(range(1, len(numbers) + 1)):
        raise ValueError(f"{path}: item numbers must be contiguous from 1")

    return {
        "roundId": f"R{match['round']}",
        "year": match["year"],
        "session": match["session"],
        "title": frontmatter["title"],
        "documentProvenance": _document_provenance(frontmatter, path, vault_root),
        "status": "source-derived",
        "sourcePath": str(path.relative_to(vault_root)),
        "sourceDigest": _sha256(text),
        "items": items,
    }


def build_past_exam_payload(vault_root: Path) -> dict[str, object]:
    source_root = vault_root / "datasets" / "info-sec-engineer-practical-past-exams" / "01-rounds"
    paths = sorted(source_root.glob("*-practical-*.md"))
    if not paths:
        raise ValueError(f"{source_root}: no practical round Markdown files found")
    rounds = [parse_round(path, vault_root) for path in paths]
    round_ids = [round_data["roundId"] for round_data in rounds]
    item_ids = [item["id"] for round_data in rounds for item in round_data["items"]]
    if len(round_ids) != len(set(round_ids)):
        raise ValueError("past-exam round IDs must be unique")
    if len(item_ids) != len(set(item_ids)):
        raise ValueError("past-exam item IDs must be unique")
    return {
        "version": 1,
        "sourceRoot": str(source_root.relative_to(vault_root)),
        "rounds": rounds,
    }


def validate_past_exam_payload(payload: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict) or payload.get("version") != 1:
        return ["past-exam payload version must be 1"]
    source_root = payload.get("sourceRoot")
    if not isinstance(source_root, str) or not source_root:
        errors.append("past-exam payload requires sourceRoot")
    rounds = payload.get("rounds")
    if not isinstance(rounds, list) or not rounds:
        return ["past-exam payload requires non-empty rounds"]
    item_ids: set[str] = set()
    for round_data in rounds:
        if not isinstance(round_data, dict):
            errors.append("past-exam round must be an object")
            continue
        for field in ("roundId", "year", "session", "title", "documentProvenance", "status", "sourcePath", "sourceDigest"):
            if not isinstance(round_data.get(field), str) or not round_data[field]:
                errors.append(f"past-exam round requires {field}")
        round_id = round_data.get("roundId")
        if not isinstance(round_id, str) or not re.fullmatch(r"R\d+", round_id):
            errors.append(f"{round_id or '<missing>'}: roundId must match R<number>")
        if not isinstance(round_data.get("year"), str) or not re.fullmatch(r"\d{4}", round_data["year"]):
            errors.append(f"{round_id or '<missing>'}: year must be four digits")
        if not isinstance(round_data.get("session"), str) or not re.fullmatch(r"\d{2}", round_data["session"]):
            errors.append(f"{round_id or '<missing>'}: session must be two digits")
        if not isinstance(round_data.get("sourceDigest"), str) or not re.fullmatch(r"[a-f0-9]{64}", round_data["sourceDigest"]):
            errors.append(f"{round_id or '<missing>'}: sourceDigest must be a SHA-256 hex string")
        if round_data.get("status") != "source-derived":
            errors.append(f"{round_data.get('roundId', '<missing>')}: status must be source-derived")
        items = round_data.get("items")
        if not isinstance(items, list) or not items:
            errors.append(f"{round_data.get('roundId', '<missing>')}: requires items")
            continue
        expected_numbers = list(range(1, len(items) + 1))
        actual_numbers = [item.get("number") for item in items if isinstance(item, dict)]
        if actual_numbers != expected_numbers:
            errors.append(f"{round_data.get('roundId', '<missing>')}: item numbers must be contiguous")
        for item in items:
            if not isinstance(item, dict):
                errors.append("past-exam item must be an object")
                continue
            for field in ("id", "type", "prompt", "answer", "verification", "sourcePath", "contentDigest"):
                if not isinstance(item.get(field), str) or not item[field]:
                    errors.append(f"past-exam item requires {field}")
            item_id = item.get("id")
            if not isinstance(item_id, str) or not re.fullmatch(r"R\d+-Q\d{2}", item_id):
                errors.append(f"{item_id or '<missing>'}: item id must match R<number>-Q<number>")
            if item.get("type") not in VALID_TYPES:
                errors.append(f"{item_id or '<missing>'}: invalid type")
            if not isinstance(item.get("sourceLine"), int) or item["sourceLine"] < 1:
                errors.append(f"{item_id or '<missing>'}: invalid sourceLine")
            if not isinstance(item.get("contentDigest"), str) or not re.fullmatch(r"[a-f0-9]{64}", item["contentDigest"]):
                errors.append(f"{item_id or '<missing>'}: contentDigest must be a SHA-256 hex string")
            source_ref = item.get("sourceRef")
            if (
                not isinstance(source_ref, dict)
                or source_ref.get("status") != "source-derived"
                or source_ref.get("path") != item.get("sourcePath")
                or source_ref.get("line") != item.get("sourceLine")
                or source_ref.get("excerpt") != item.get("verification")
            ):
                errors.append(f"{item_id or '<missing>'}: sourceRef must exactly identify the source row")
            if isinstance(item_id, str):
                if item_id in item_ids:
                    errors.append(f"duplicate past-exam item ID: {item_id}")
                item_ids.add(item_id)
    return errors
