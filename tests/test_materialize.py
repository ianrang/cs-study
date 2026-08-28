#!/usr/bin/env python3
from __future__ import annotations

import ast
import hashlib
import json
import shutil
import stat
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import wiki_ingest  # noqa: E402
from knowledge import fs as knowledge_fs  # noqa: E402
from knowledge import materialize  # noqa: E402
from knowledge.check import CheckResult  # noqa: E402
from knowledge.materialize import (  # noqa: E402
    MaterializeError,
    apply_generated,
    generated_drift,
    generated_tree_sha256,
    materialize_input_sha256,
    render_generated,
    validate_generated,
)

FIXTURES = ROOT / "tests" / "fixtures" / "knowledge"


def _setup_repo(tmp_path: Path) -> tuple[Path, Path]:
    repo = tmp_path / "repo"
    meta = repo / "_meta"
    meta.mkdir(parents=True)
    shutil.copy(ROOT / "_meta" / "knowledge.schema.json", meta)
    (meta / "domains.yaml").write_text(
        """version: 1
domains:
  alpha-domain:
    status: active
    label: Alpha Domain
    source_roots: [alpha/]
  beta-domain:
    status: inactive
    label: Beta Domain
    source_roots: []
""",
        encoding="utf-8",
    )
    wiki = repo / "wiki"
    (wiki / "domains" / "alpha-domain").mkdir(parents=True)
    (wiki / "collections").mkdir()
    (wiki / "staging").mkdir()
    (wiki / "templates").mkdir()
    (wiki / "views").mkdir()
    concept = (FIXTURES / "valid-concept.md").read_text(encoding="utf-8")
    concept = concept.replace("title: Contract Fixture Concept", "title: Alpha Page")
    concept = concept.replace(
        "summary: Deterministic parser contract fixture.", "summary: Alpha summary"
    )
    concept = concept.replace(
        "| broader | [[fixture-parent]] | direct outgoing edge |", ""
    )
    (wiki / "domains" / "alpha-domain" / "alpha-page.md").write_text(
        concept, encoding="utf-8"
    )
    collection = (FIXTURES / "valid-collection.md").read_text(encoding="utf-8")
    collection = collection.replace(
        "title: Contract Fixture Collection", "title: Alpha Collection"
    ).replace("summary: Contract collection fixture", "summary: Collection summary")
    collection = collection.replace("valid-concept", "alpha-page")
    (wiki / "collections" / "alpha-collection.md").write_text(
        collection, encoding="utf-8"
    )
    (wiki / "staging" / "draft-page.md").write_text(concept, encoding="utf-8")
    return repo, wiki


def test_render_is_deterministic_and_manifest_is_schema_derived(tmp_path: Path):
    repo, wiki = _setup_repo(tmp_path)

    first = render_generated(repo, wiki)
    second = render_generated(repo, wiki)

    assert first == second
    assert set(first) == {
        Path("wiki/index.md"),
        Path("wiki/overview.md"),
        Path("wiki/views/knowledge-pages.base"),
        *{
            Path(f"wiki/templates/{page_type}.md")
            for page_type in (
                "concept",
                "entity",
                "comparison",
                "benchmark",
                "dataset",
                "method",
                "source-summary",
                "collection",
            )
        },
    }
    digest = hashlib.sha256(
        (repo / "_meta/knowledge.schema.json").read_bytes()
    ).hexdigest()
    markdown_marker = (
        f"<!-- generated-by: cs-study-materializer/1.0; schema-sha256: {digest} -->"
    )
    base_formula = f'"cs-study-materializer/1.0; schema-sha256: {digest}"'
    assert first[Path("wiki/index.md")].decode().splitlines()[0] == markdown_marker
    template_lines = first[Path("wiki/templates/concept.md")].decode().splitlines()
    closing = template_lines.index("---", 1)
    assert template_lines[closing + 1] == markdown_marker
    base = yaml.safe_load(first[Path("wiki/views/knowledge-pages.base")].decode())
    assert base["formulas"] == {"_generated_by": base_formula}
    assert all(value.endswith(b"\n") for value in first.values())
    assert materialize_input_sha256(repo, wiki) == materialize_input_sha256(repo, wiki)
    assert generated_tree_sha256(first) == generated_tree_sha256(second)


def test_index_overview_templates_and_base_follow_canonical_contract(tmp_path: Path):
    repo, wiki = _setup_repo(tmp_path)
    rendered = render_generated(repo, wiki)
    index = rendered[Path("wiki/index.md")].decode()
    overview = rendered[Path("wiki/overview.md")].decode()

    assert index.count("[[wiki/domains/alpha-domain/alpha-page]]") == 1
    assert "Alpha Page" in index and "Alpha summary" in index
    assert "draft-page" not in index
    assert index.index("## alpha-domain") < index.index("## beta-domain")
    assert "[[wiki/collections/alpha-collection]]" in index
    assert (
        "| [[wiki/index#alpha-domain|alpha-domain]] | Alpha Domain | active | 1 |"
        in overview
    )
    assert (
        "| [[wiki/index#beta-domain|beta-domain]] | Beta Domain | inactive | 0 |"
        in overview
    )
    assert "| [[wiki/index#Collections|Collections]] |  | active | 1 |" in overview
    assert "alpha-page" not in overview

    concept = rendered[Path("wiki/templates/concept.md")].decode()
    assert concept.index("title: ''") < concept.index("aliases: []")
    assert concept.index("## Definition") < concept.index("## Sources")
    assert "| id | primary | claim | status | evidence | notes |" in concept
    assert "tier:" not in concept and "domain_confidence:" not in concept
    collection = rendered[Path("wiki/templates/collection.md")].decode()
    assert "| member | role | rationale |" in collection

    base_bytes = rendered[Path("wiki/views/knowledge-pages.base")]
    base_text = base_bytes.decode()
    base = yaml.safe_load(base_text)
    digest = hashlib.sha256(
        (repo / "_meta/knowledge.schema.json").read_bytes()
    ).hexdigest()
    assert base["formulas"] == {
        "_generated_by": f'"cs-study-materializer/1.0; schema-sha256: {digest}"'
    }
    assert base["filters"]["or"] == [
        'file.inFolder("wiki/domains")',
        'file.inFolder("wiki/collections")',
    ]
    assert [view["name"] for view in base["views"]] == [
        "All active",
        "Alpha Domain",
        "Collections",
    ]
    assert all(
        view["order"]
        == [
            "file.name",
            "title",
            "page_type",
            "summary",
            "date_updated",
        ]
        for view in base["views"]
    )
    assert "&id" not in base_text and "*id" not in base_text
    assert "\n  or:\n    - file.inFolder" in base_text
    assert base_text.count("\n    order:\n      - file.name") == len(base["views"])
    assert "_generated_by" not in {
        property_name for view in base["views"] for property_name in view["order"]
    }


def test_independent_validator_rejects_index_and_template_renderer_mutations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repo, wiki = _setup_repo(tmp_path)
    original_index = materialize._render_index

    def omit_active_page(*args, **kwargs):
        return original_index(*args, **kwargs).replace(
            b"- [[wiki/domains/alpha-domain/alpha-page]]",
            b"- [[wiki/domains/alpha-domain/omitted]]",
        )

    monkeypatch.setattr(materialize, "_render_index", omit_active_page)
    with pytest.raises(MaterializeError, match="index"):
        validate_generated(render_generated(repo, wiki), repo, wiki)

    monkeypatch.setattr(materialize, "_render_index", original_index)
    monkeypatch.setattr(materialize, "_render_template", lambda *args: b"not yaml\n")
    with pytest.raises(MaterializeError, match="template"):
        validate_generated(render_generated(repo, wiki), repo, wiki)

    monkeypatch.undo()
    rendered = render_generated(repo, wiki)
    template = Path("wiki/templates/concept.md")
    rendered[template] = rendered[template].replace(
        b"title: ''\n", b"title: ''\ntitle: ''\n", 1
    )
    with pytest.raises(MaterializeError, match="template YAML"):
        validate_generated(rendered, repo, wiki)


def test_independent_validator_rejects_active_record_common_mode_mutation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repo, wiki = _setup_repo(tmp_path)
    original = materialize._active_records

    def omit_domain_pages(*args, **kwargs):
        domains, collections = original(*args, **kwargs)
        return {name: [] for name in domains}, collections

    monkeypatch.setattr(materialize, "_active_records", omit_domain_pages)
    rendered = render_generated(repo, wiki)

    with pytest.raises(MaterializeError, match="index"):
        validate_generated(rendered, repo, wiki)


def test_validator_rejects_relocated_base_marker(tmp_path: Path):
    repo, wiki = _setup_repo(tmp_path)
    rendered = render_generated(repo, wiki)
    base_path = Path("wiki/views/knowledge-pages.base")
    base = yaml.safe_load(rendered[base_path])
    marker = base.pop("formulas")
    base["views"][0]["formulas"] = marker
    rendered[base_path] = yaml.safe_dump(base, sort_keys=False).encode()

    with pytest.raises(MaterializeError, match="Base marker"):
        validate_generated(rendered, repo, wiki)


def test_apply_rejects_markerless_existing_base(tmp_path: Path):
    repo, wiki = _setup_repo(tmp_path)
    base = wiki / "views/knowledge-pages.base"
    base.write_text("filters: {}\nviews: []\n", encoding="utf-8")

    with pytest.raises(MaterializeError, match="markerless"):
        apply_generated(repo, wiki)

    assert base.read_text(encoding="utf-8") == "filters: {}\nviews: []\n"


@pytest.mark.parametrize("location", ["existing", "managed-temp"])
@pytest.mark.parametrize("marker_shape", ["unquoted", "relocated"])
def test_apply_preserves_noncanonical_base_ownership_claim(
    tmp_path: Path, location: str, marker_shape: str
):
    repo, wiki = _setup_repo(tmp_path)
    digest = hashlib.sha256(
        (repo / "_meta/knowledge.schema.json").read_bytes()
    ).hexdigest()
    formula = f'"cs-study-materializer/1.0; schema-sha256: {digest}"'
    if marker_shape == "unquoted":
        content = (
            "formulas:\n"
            f"  _generated_by: cs-study-materializer/1.0; schema-sha256: {digest}\n"
            "filters: {}\nviews: []\n"
        )
    else:
        content = (
            "filters: {}\nviews: []\nformulas:\n"
            f"  _generated_by: '{formula}'\n"
        )
    if location == "existing":
        target = wiki / "views/knowledge-pages.base"
    else:
        target = wiki / "views" / f".knowledge-pages.base.{'d' * 24}"
    target.write_text(content, encoding="utf-8")

    if location == "existing":
        with pytest.raises(MaterializeError, match="markerless"):
            apply_generated(repo, wiki)
    else:
        assert apply_generated(repo, wiki)["created"] == 11

    assert target.read_text(encoding="utf-8") == content


def test_apply_replaces_canonical_base_with_stale_schema_digest(tmp_path: Path):
    repo, wiki = _setup_repo(tmp_path)
    rendered = render_generated(repo, wiki)
    for relative, content in rendered.items():
        (repo / relative).write_bytes(content)
    base = wiki / "views/knowledge-pages.base"
    digest = hashlib.sha256(
        (repo / "_meta/knowledge.schema.json").read_bytes()
    ).hexdigest()
    base.write_bytes(base.read_bytes().replace(digest.encode(), b"a" * 64, 1))

    assert apply_generated(repo, wiki)["replaced"] == 1
    assert base.read_bytes() == rendered[Path("wiki/views/knowledge-pages.base")]


def test_schema_page_type_change_automatically_changes_template_manifest(
    tmp_path: Path,
):
    repo, wiki = _setup_repo(tmp_path)
    schema_path = repo / "_meta/knowledge.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    schema["$defs"]["PageType"]["enum"].append("procedure")
    schema["$defs"]["DocumentInstance"]["allOf"].append(
        {
            "if": {
                "properties": {
                    "properties": {"properties": {"page_type": {"const": "procedure"}}}
                }
            },
            "then": {
                "properties": {
                    "ordered_sections": {
                        "const": ["Steps", "Claims", "Relations", "Sources"]
                    }
                }
            },
        }
    )
    schema_path.write_text(json.dumps(schema), encoding="utf-8")

    rendered = render_generated(repo, wiki)

    assert Path("wiki/templates/procedure.md") in rendered
    assert "## Steps" in rendered[Path("wiki/templates/procedure.md")].decode()
    assert len(rendered) == 12


def test_check_is_no_write_and_reports_missing_or_changed_leaf(tmp_path: Path):
    repo, wiki = _setup_repo(tmp_path)
    rendered = render_generated(repo, wiki)
    before = list(repo.rglob("*"))

    assert generated_drift(repo, wiki) != ()
    assert list(repo.rglob("*")) == before

    for relative, content in rendered.items():
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    assert generated_drift(repo, wiki) == ()
    (repo / "wiki/index.md").write_text("changed\n", encoding="utf-8")
    assert any("wiki/index.md" in item for item in generated_drift(repo, wiki))


def test_canonical_page_marker_text_is_not_an_unexpected_generated_leaf(
    tmp_path: Path,
):
    repo, wiki = _setup_repo(tmp_path)
    page = wiki / "domains/alpha-domain/alpha-page.md"
    page.write_text(
        page.read_text(encoding="utf-8").replace(
            "Definition body.",
            "Definition body.\n\n<!-- generated-by: cs-study-materializer/1.0; "
            f"schema-sha256: {'a' * 64} -->",
        ),
        encoding="utf-8",
    )
    for relative, content in render_generated(repo, wiki).items():
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    assert generated_drift(repo, wiki) == ()


def test_apply_preflight_rejects_markerless_symlink_and_unknown_generated_leaf(
    tmp_path: Path,
):
    repo, wiki = _setup_repo(tmp_path)
    index = repo / "wiki/index.md"
    index.write_text("human owned\n", encoding="utf-8")
    with pytest.raises(MaterializeError, match="markerless"):
        apply_generated(repo, wiki)
    assert index.read_text(encoding="utf-8") == "human owned\n"
    assert not (repo / "wiki/overview.md").exists()

    index.unlink()
    target = repo / "outside.md"
    target.write_text("outside\n", encoding="utf-8")
    index.symlink_to(target)
    with pytest.raises(MaterializeError, match="regular non-symlink"):
        apply_generated(repo, wiki)
    assert target.read_text(encoding="utf-8") == "outside\n"

    index.unlink()
    unknown = repo / "wiki/templates/unknown.md"
    unknown.parent.mkdir(parents=True, exist_ok=True)
    unknown.write_text(
        "<!-- generated-by: cs-study-materializer/1.0; schema-sha256: "
        + "a" * 64
        + " -->\n",
        encoding="utf-8",
    )
    with pytest.raises(MaterializeError, match="unexpected generated leaf"):
        apply_generated(repo, wiki)


def test_apply_rejects_generated_parent_symlink_before_external_write(tmp_path: Path):
    repo, wiki = _setup_repo(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    (wiki / "templates").rmdir()
    (wiki / "templates").symlink_to(outside, target_is_directory=True)

    with pytest.raises(MaterializeError, match="regular"):
        apply_generated(repo, wiki)

    assert list(outside.iterdir()) == []


def test_apply_rejects_parent_swap_after_preflight_without_external_write(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repo, wiki = _setup_repo(tmp_path)
    outside = tmp_path / "outside"
    outside.mkdir()
    original = materialize._preflight_apply

    def swap_parent(*args, **kwargs):
        result = original(*args, **kwargs)
        (wiki / "templates").rename(wiki / "templates-detached")
        (wiki / "templates").symlink_to(outside, target_is_directory=True)
        return result

    monkeypatch.setattr(materialize, "_preflight_apply", swap_parent)
    with pytest.raises(MaterializeError, match="directory changed"):
        apply_generated(repo, wiki)
    assert list(outside.iterdir()) == []


def test_apply_rejects_leaf_swap_after_preflight_and_preserves_human_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repo, wiki = _setup_repo(tmp_path)
    for relative, content in render_generated(repo, wiki).items():
        (repo / relative).write_bytes(content)
    index = wiki / "index.md"
    index.write_bytes(index.read_bytes() + b"stale\n")
    original = materialize._preflight_apply

    def swap_leaf(*args, **kwargs):
        result = original(*args, **kwargs)
        index.write_text("human replacement\n", encoding="utf-8")
        return result

    monkeypatch.setattr(materialize, "_preflight_apply", swap_leaf)
    with pytest.raises(MaterializeError, match="leaf changed"):
        apply_generated(repo, wiki)
    assert index.read_text(encoding="utf-8") == "human replacement\n"


def test_apply_rejects_leaf_swap_at_atomic_exchange_and_preserves_human_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repo, wiki = _setup_repo(tmp_path)
    for relative, content in render_generated(repo, wiki).items():
        (repo / relative).write_bytes(content)
    index = wiki / "index.md"
    index.write_bytes(index.read_bytes() + b"stale\n")
    original = knowledge_fs._exchange_leaf_names
    injected = False

    def swap_after_final_check(directory, first: str, second: str):
        nonlocal injected
        if second == "index.md" and not injected:
            injected = True
            index.write_text("human-after-final-check\n", encoding="utf-8")
        return original(directory, first, second)

    monkeypatch.setattr(knowledge_fs, "_exchange_leaf_names", swap_after_final_check)
    with pytest.raises(MaterializeError, match="leaf changed"):
        apply_generated(repo, wiki)
    assert index.read_text(encoding="utf-8") == "human-after-final-check\n"


def test_temp_file_failure_leaves_no_leaf_and_exact_replay_converges(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repo, wiki = _setup_repo(tmp_path)
    original = knowledge_fs.os.fsync
    injected = False

    def fail_first_fsync(descriptor: int):
        nonlocal injected
        if not injected:
            injected = True
            raise OSError("injected temp fsync failure")
        return original(descriptor)

    monkeypatch.setattr(knowledge_fs.os, "fsync", fail_first_fsync)
    with pytest.raises(OSError, match="injected temp fsync failure"):
        apply_generated(repo, wiki)
    assert list(wiki.glob(".index.md.*")) == []

    monkeypatch.setattr(knowledge_fs.os, "fsync", original)
    assert apply_generated(repo, wiki)["created"] == 11
    assert generated_drift(repo, wiki) == ()


@pytest.mark.parametrize("operation", ["publish", "replace"])
def test_temp_content_mutation_before_commit_never_publishes_corrupt_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, operation: str
):
    repo, wiki = _setup_repo(tmp_path)
    rendered = render_generated(repo, wiki)
    index = wiki / "index.md"
    if operation == "replace":
        for relative, content in rendered.items():
            (repo / relative).write_bytes(content)
        previous = index.read_bytes() + b"stale\n"
        index.write_bytes(previous)
        original = knowledge_fs._exchange_leaf_names
        injected = False

        def mutate_then_exchange(directory, first: str, second: str):
            nonlocal injected
            if second == "index.md" and not injected:
                injected = True
                descriptor = knowledge_fs.os.open(
                    first,
                    knowledge_fs.os.O_WRONLY | knowledge_fs.os.O_TRUNC,
                    dir_fd=directory.descriptor,
                )
                try:
                    knowledge_fs.os.write(descriptor, b"corrupt\n")
                finally:
                    knowledge_fs.os.close(descriptor)
            return original(directory, first, second)

        monkeypatch.setattr(
            knowledge_fs, "_exchange_leaf_names", mutate_then_exchange
        )
    else:
        previous = None
        original_link = knowledge_fs.os.link

        def mutate_then_link(source, target, **kwargs):
            if target == "index.md":
                descriptor = knowledge_fs.os.open(
                    source,
                    knowledge_fs.os.O_WRONLY | knowledge_fs.os.O_TRUNC,
                    dir_fd=kwargs["src_dir_fd"],
                )
                try:
                    knowledge_fs.os.write(descriptor, b"corrupt\n")
                finally:
                    knowledge_fs.os.close(descriptor)
            return original_link(source, target, **kwargs)

        monkeypatch.setattr(knowledge_fs.os, "link", mutate_then_link)

    with pytest.raises((MaterializeError, knowledge_fs.PathSafetyError)):
        apply_generated(repo, wiki)
    if previous is None:
        assert not index.exists()
    else:
        assert index.read_bytes() == previous
    assert b"corrupt" not in index.read_bytes() if index.exists() else True


def test_managed_temp_leftover_does_not_block_exact_replay(tmp_path: Path):
    repo, wiki = _setup_repo(tmp_path)
    rendered = render_generated(repo, wiki)
    owned_temp = wiki / f".index.md.{'a' * 24}"
    owned_temp.write_bytes(rendered[Path("wiki/index.md")])
    owned_base_temp = wiki / "views" / f".knowledge-pages.base.{'c' * 24}"
    owned_base_temp.write_bytes(rendered[Path("wiki/views/knowledge-pages.base")])
    markerless_temp = wiki / f".index.md.{'b' * 24}"
    markerless_temp.write_bytes(b"human temporary bytes\n")

    result = apply_generated(repo, wiki)

    assert result["created"] == 11
    assert not owned_temp.exists()
    assert not owned_base_temp.exists()
    assert markerless_temp.read_bytes() == b"human temporary bytes\n"
    assert generated_drift(repo, wiki) == ()


def test_check_reports_managed_marker_temp_until_apply_recovers(tmp_path: Path):
    repo, wiki = _setup_repo(tmp_path)
    rendered = render_generated(repo, wiki)
    for relative, content in rendered.items():
        (repo / relative).write_bytes(content)
    owned_temp = wiki / f".index.md.{'a' * 24}"
    owned_temp.write_bytes(rendered[Path("wiki/index.md")])

    assert any(".index.md" in finding for finding in generated_drift(repo, wiki))
    apply_generated(repo, wiki)
    assert not owned_temp.exists()
    assert generated_drift(repo, wiki) == ()


def test_cleanup_unlink_failure_converges_on_next_replay(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repo, wiki = _setup_repo(tmp_path)
    original = knowledge_fs.os.unlink
    injected = False

    def fail_first_temp_cleanup(path, *args, **kwargs):
        nonlocal injected
        if not injected and str(path).startswith(".index.md."):
            injected = True
            raise OSError("injected cleanup unlink failure")
        return original(path, *args, **kwargs)

    monkeypatch.setattr(knowledge_fs.os, "unlink", fail_first_temp_cleanup)
    with pytest.raises(OSError, match="injected cleanup unlink failure"):
        apply_generated(repo, wiki)
    assert len(list(wiki.glob(".index.md.*"))) == 1

    monkeypatch.setattr(knowledge_fs.os, "unlink", original)
    result = apply_generated(repo, wiki)
    assert result["created"] == 10
    assert result["unchanged"] == 1
    assert list(wiki.glob(".index.md.*")) == []
    assert generated_drift(repo, wiki) == ()


@pytest.mark.parametrize("operation", ["publish", "replace"])
def test_post_commit_failure_preserves_same_bytes_competing_inode(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, operation: str
):
    repo, wiki = _setup_repo(tmp_path)
    rendered = render_generated(repo, wiki)
    index = wiki / "index.md"
    if operation == "replace":
        for relative, content in rendered.items():
            (repo / relative).write_bytes(content)
        index.write_bytes(index.read_bytes() + b"stale\n")
    target_bytes = rendered[Path("wiki/index.md")]
    original = knowledge_fs.os.fsync
    injected = False

    def replace_target_then_fail(descriptor: int):
        nonlocal injected
        if not injected and stat.S_ISDIR(knowledge_fs.os.fstat(descriptor).st_mode):
            injected = True
            index.unlink()
            index.write_bytes(target_bytes)
            index.chmod(0o600)
            raise OSError("injected directory fsync failure")
        return original(descriptor)

    monkeypatch.setattr(knowledge_fs.os, "fsync", replace_target_then_fail)
    with pytest.raises(OSError, match="indeterminate"):
        apply_generated(repo, wiki)
    assert index.read_bytes() == target_bytes
    assert stat.S_IMODE(index.stat().st_mode) == 0o600
    assert not list(wiki.glob(".index.md.*"))


def test_partial_leaf_failure_is_detected_and_exact_replay_converges(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repo, wiki = _setup_repo(tmp_path)
    original = materialize.publish_bytes_no_replace_at
    calls = 0

    def fail_second(directory, name: str, data: bytes) -> bool:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("injected leaf failure")
        return original(directory, name, data)

    monkeypatch.setattr(materialize, "publish_bytes_no_replace_at", fail_second)
    with pytest.raises(OSError, match="injected leaf failure"):
        apply_generated(repo, wiki)
    assert generated_drift(repo, wiki)

    monkeypatch.setattr(materialize, "publish_bytes_no_replace_at", original)
    first = apply_generated(repo, wiki)
    second = apply_generated(repo, wiki)
    assert first["created"] == 10
    assert second["created"] == second["replaced"] == 0
    assert second["unchanged"] == 11
    assert second["input_sha256"] == first["input_sha256"]
    assert second["output_tree_sha256"] == first["output_tree_sha256"]
    assert generated_drift(repo, wiki) == ()


def test_apply_rechecks_rendered_input_inside_repository_lock(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repo, wiki = _setup_repo(tmp_path)
    original = materialize.render_generated
    calls = 0

    def change_after_initial_render(*args, **kwargs):
        nonlocal calls
        calls += 1
        rendered = original(*args, **kwargs)
        if calls == 2:
            rendered = dict(rendered)
            rendered[Path("wiki/index.md")] += b"changed\n"
        return rendered

    monkeypatch.setattr(materialize, "render_generated", change_after_initial_render)
    with pytest.raises(MaterializeError, match="index|input changed before apply"):
        apply_generated(repo, wiki)
    assert not (wiki / "index.md").exists()


def test_invalid_domain_registry_fails_before_render(tmp_path: Path):
    repo, wiki = _setup_repo(tmp_path)
    (repo / "_meta/domains.yaml").write_text(
        "version: 1\ndomains:\n  Bad_Name:\n    status: active\n"
        "    label: Bad\n    source_roots: []\n",
        encoding="utf-8",
    )
    with pytest.raises(MaterializeError, match="domain registry"):
        render_generated(repo, wiki)


def test_inactive_domain_page_fails_checker_and_materializer(tmp_path: Path):
    repo, wiki = _setup_repo(tmp_path)
    (wiki / "domains" / "beta-domain").mkdir()
    (wiki / "domains" / "alpha-domain" / "alpha-page.md").rename(
        wiki / "domains" / "beta-domain" / "alpha-page.md"
    )

    with pytest.raises(MaterializeError, match="inactive domain"):
        render_generated(repo, wiki)
    result = wiki_ingest.check_target(
        wiki, repo_root=repo, mode="all", include_repository_contracts=False
    )
    assert result.structural_verdict == "FAIL"
    assert any("inactive domain" in finding["message"] for finding in result.findings)


def test_invalid_utf8_domain_registry_fails_both_public_boundaries(tmp_path: Path):
    repo, wiki = _setup_repo(tmp_path)
    (repo / "_meta/domains.yaml").write_bytes(b"\xff")

    with pytest.raises(MaterializeError, match="domain registry"):
        render_generated(repo, wiki)
    result = wiki_ingest.check_target(
        wiki, repo_root=repo, mode="all", include_repository_contracts=False
    )
    assert result.structural_verdict == "FAIL"
    assert any("domain registry" in finding["message"] for finding in result.findings)


def test_display_text_contract_rejects_multiline_and_table_separator(tmp_path: Path):
    repo, wiki = _setup_repo(tmp_path)
    page = wiki / "domains/alpha-domain/alpha-page.md"
    page.write_text(
        page.read_text(encoding="utf-8").replace(
            "title: Alpha Page", "title: |-\n  Alpha\n  Page"
        ),
        encoding="utf-8",
    )
    with pytest.raises(MaterializeError, match="title"):
        render_generated(repo, wiki)

    page.write_text(
        page.read_text(encoding="utf-8").replace(
            "title: |-\n  Alpha\n  Page", "title: Alpha Page"
        ),
        encoding="utf-8",
    )
    registry = repo / "_meta/domains.yaml"
    registry.write_text(
        registry.read_text(encoding="utf-8").replace(
            "label: Alpha Domain", "label: Alpha | Domain"
        ),
        encoding="utf-8",
    )
    with pytest.raises(MaterializeError, match="domain label"):
        render_generated(repo, wiki)


@pytest.mark.parametrize(
    ("property_name", "replacement"),
    [
        ("title", "title: |+\n  Alpha Page"),
        ("summary", "summary: |+\n  Alpha summary\n"),
    ],
)
def test_display_text_contract_rejects_trailing_line_break(
    tmp_path: Path, property_name: str, replacement: str
):
    repo, wiki = _setup_repo(tmp_path)
    page = wiki / "domains/alpha-domain/alpha-page.md"
    original = (
        "title: Alpha Page"
        if property_name == "title"
        else "summary: Alpha summary"
    )
    page.write_text(
        page.read_text(encoding="utf-8").replace(original, replacement),
        encoding="utf-8",
    )

    with pytest.raises(MaterializeError, match=property_name):
        render_generated(repo, wiki)


@pytest.mark.parametrize(
    "schema_bytes",
    [b"{ invalid", b'{"non_finite": NaN}', b"\xff"],
)
def test_schema_loader_fails_closed_at_materializer_boundary(
    tmp_path: Path, schema_bytes: bytes
):
    repo, wiki = _setup_repo(tmp_path)
    (repo / "_meta/knowledge.schema.json").write_bytes(schema_bytes)

    with pytest.raises(MaterializeError, match="cannot render generated surface"):
        render_generated(repo, wiki)


def test_generator_identity_has_one_runtime_owner(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repo, wiki = _setup_repo(tmp_path)
    monkeypatch.setattr(materialize, "GENERATOR_ID", "cs-study-materializer/1.1")

    rendered = render_generated(repo, wiki)

    validate_generated(rendered, repo, wiki)
    assert b"generated-by: cs-study-materializer/1.1" in rendered[Path("wiki/index.md")]


def test_materialize_command_call_graph_max_depth_is_exactly_ratcheted():
    module_paths = {
        name: ROOT / f"scripts/knowledge/{name}.py"
        for name in ("materialize", "schema", "fs")
    }
    functions = {}
    imports = {name: {} for name in module_paths}
    for module, path in module_paths.items():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, ast.ImportFrom) and node.module:
                target_module = node.module.split(".")[-1]
                if target_module in module_paths:
                    imports[module].update(
                        {
                            alias.asname or alias.name: f"{target_module}.{alias.name}"
                            for alias in node.names
                        }
                    )
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions[f"{module}.{node.name}"] = node
    edges = {name: set() for name in functions}
    for qualified, function in functions.items():
        module = qualified.split(".", 1)[0]
        for node in ast.walk(function):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
                continue
            local = f"{module}.{node.func.id}"
            target = local if local in functions else imports[module].get(node.func.id)
            if target in functions:
                edges[qualified].add(target)

    def maximum_edges(name: str, visiting: frozenset[str] = frozenset()) -> int:
        assert name not in visiting, f"materialize call cycle at {name}"
        return max(
            (1 + maximum_edges(target, visiting | {name}) for target in edges[name]),
            default=0,
        )

    core_roots = ("materialize.apply_generated", "materialize.generated_drift")
    core_max = max(maximum_edges(root) for root in core_roots)
    main = ast.parse((ROOT / "scripts/wiki_ingest.py").read_text(encoding="utf-8"))
    main_node = next(
        node
        for node in main.body
        if isinstance(node, ast.FunctionDef) and node.name == "main"
    )
    main_calls = {
        node.func.id
        for node in ast.walk(main_node)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert {"apply_generated", "generated_drift"} <= main_calls
    command_targets = {
        f"materialize.{name}"
        for name in main_calls
        if f"materialize.{name}" in functions
    }
    command_max = max(1 + maximum_edges(target) for target in command_targets)
    assert core_max == 5
    assert command_max == 6


def test_cli_materialize_check_and_apply_have_distinct_write_semantics(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repo, wiki = _setup_repo(tmp_path)
    monkeypatch.setattr(wiki_ingest, "REPO_ROOT", repo)

    assert wiki_ingest.main(["materialize", "--check"]) == 1
    assert not (wiki / "index.md").exists()
    assert wiki_ingest.main(["materialize"]) == 0
    assert wiki_ingest.main(["materialize", "--check"]) == 0


def test_cli_repository_check_executes_generated_parity_rules(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    repo, wiki = _setup_repo(tmp_path)
    monkeypatch.setattr(wiki_ingest, "REPO_ROOT", repo)
    apply_generated(repo, wiki)
    (wiki / "index.md").write_bytes((wiki / "index.md").read_bytes() + b"stale\n")

    assert (
        wiki_ingest.main(
            ["check", "--all", "--target-root", str(wiki), "--report", "jsonl"]
        )
        == 1
    )
    lines = capsys.readouterr().out.splitlines()
    findings = [json.loads(line) for line in lines[:-1]]
    finding = next(item for item in findings if item["rule_id"] == "VR-KP-018")
    result = json.loads(lines[-1])["result"]
    assert result["structural_verdict"] == "FAIL"
    assert finding in result["findings"]


def test_page_candidate_checks_base_parity_then_canonical_then_candidate_coverage(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repo, wiki = _setup_repo(tmp_path)
    calls = []
    monkeypatch.setattr(wiki_ingest, "REPO_ROOT", repo)
    monkeypatch.setattr(
        wiki_ingest,
        "generated_drift",
        lambda *args: calls.append("base-parity") or (),
    )
    monkeypatch.setattr(
        wiki_ingest,
        "check_target",
        lambda *args, **kwargs: (
            calls.append("canonical-overlay")
            or CheckResult("PASS", "not-performed", "all", (), ())
        ),
    )
    monkeypatch.setattr(
        wiki_ingest,
        "render_generated",
        lambda *args, **kwargs: calls.append("candidate-coverage") or {},
    )
    monkeypatch.setattr(
        wiki_ingest,
        "validate_generated",
        lambda *args, **kwargs: calls.append("candidate-validation"),
    )

    wiki_ingest._check_page_candidate([])

    assert calls == [
        "base-parity",
        "canonical-overlay",
        "candidate-coverage",
        "candidate-validation",
    ]


def test_page_candidate_rejects_repository_drift_before_canonical_check(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    repo, _ = _setup_repo(tmp_path)
    canonical_called = False
    monkeypatch.setattr(wiki_ingest, "REPO_ROOT", repo)
    monkeypatch.setattr(
        wiki_ingest, "generated_drift", lambda *args: ("generated bytes differ",)
    )

    def observe_canonical(*args, **kwargs):
        nonlocal canonical_called
        canonical_called = True

    monkeypatch.setattr(wiki_ingest, "check_target", observe_canonical)
    with pytest.raises(ValueError, match="generated repository drift"):
        wiki_ingest._check_page_candidate([])
    assert canonical_called is False
