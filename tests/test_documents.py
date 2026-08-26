import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from knowledge.documents import render_preserved_document  # noqa: E402
from knowledge.schema import parse_markdown, section_contract  # noqa: E402


def _properties(page_type: str, source_manifest: str) -> dict:
    return {
        "title": "보존 변환 fixture",
        "page_type": page_type,
        "tags": ["architecture"],
        "date_created": "2026-08-24",
        "date_updated": "2026-08-24",
        "source_paths": [source_manifest],
        "summary": "보존 변환을 검증한다.",
    }


def test_renderer_is_deterministic_and_preserves_legacy_body_line_positions():
    manifest = "raw/sources/clipping/fixture/" + "a" * 64 + "/manifest.json"
    body = ["", "# Legacy", "", "## Legacy Section", "", "근거 문장"]
    arguments = {
        "properties": _properties("method", manifest),
        "legacy_body_lines": body,
        "legacy_frontmatter_end_line": 20,
        "required_sections": section_contract("method"),
        "source_manifest": manifest,
        "members": [],
        "path_replacements": {},
    }
    first = render_preserved_document(**arguments)
    second = render_preserved_document(**arguments)
    assert first == second
    rendered_lines = first.decode("utf-8").splitlines()
    assert rendered_lines[20:] == [
        "",
        "# Legacy",
        "",
        "### Legacy Section",
        "",
        "근거 문장",
        "",
        "## Algorithm",
        "",
        "## Implementation",
        "",
        "## Trade-offs",
        "",
        "## Open Questions",
        "",
        "## Claims",
        "",
        "| id | primary | claim | status | evidence | notes |",
        "|---|---|---|---|---|---|",
        "",
        "",
        "## Relations",
        "",
        "| type | target | notes |",
        "|---|---|---|",
        "",
        "",
        "## Sources",
        "",
        f"- `{manifest}`",
    ]


def test_renderer_preserves_approved_collection_member_order(tmp_path: Path):
    manifest = "raw/sources/clipping/fixture/" + "b" * 64 + "/manifest.json"
    members = [f"member-{index:02d}" for index in range(1, 53)]
    rendered = render_preserved_document(
        properties=_properties("collection", manifest),
        legacy_body_lines=["", "Legacy collection body."],
        legacy_frontmatter_end_line=20,
        required_sections=section_contract("collection"),
        source_manifest=manifest,
        members=members,
        path_replacements={},
    )
    page = tmp_path / "fixture-collection.md"
    page.write_bytes(rendered)
    instance = parse_markdown(page)
    assert [member["target"] for member in instance["members"]] == members
    assert instance["claims"] == []
    assert instance["relations"] == []


def test_renderer_rewrites_only_approved_moved_path_tokens():
    manifest = "raw/sources/clipping/fixture/" + "c" * 64 + "/manifest.json"
    rendered = render_preserved_document(
        properties=_properties("source-summary", manifest),
        legacy_body_lines=[
            "old/path.md",
            "wiki/old/path.md",
            "[[path]] [[path|label]] [[path#heading]]",
            "old/pathology.md",
        ],
        legacy_frontmatter_end_line=20,
        required_sections=section_contract("source-summary"),
        source_manifest=manifest,
        members=[],
        path_replacements={"old/path.md": "new/new-path.md"},
    ).decode("utf-8")
    assert "new/new-path.md" in rendered
    assert "wiki/new/new-path.md" in rendered
    assert "[[new-path]] [[new-path|label]] [[new-path#heading]]" in rendered
    assert "old/pathology.md" in rendered
