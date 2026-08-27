#!/usr/bin/env python3
import contextlib
import hashlib
import io
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import wiki_ingest  # noqa: E402
from knowledge.artifacts import capture  # noqa: E402
from knowledge.check import (  # noqa: E402
    RULE_REGISTRY,
    CheckResult,
    check_target,
    contract_findings,
    rule_coverage_findings,
)

TRANSCRIPT = ROOT / "tests" / "fixtures" / "contracts" / "canonical-transcript-v1.json"
CONCEPT = ROOT / "tests" / "fixtures" / "knowledge" / "valid-concept.md"
NOW = "2026-08-21T00:00:00+00:00"
FIXTURE_MANIFEST = (
    "raw/sources/video/fixture-video/"
    "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/manifest.json"
)


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if path.is_file():
            digest.update(str(path.relative_to(root)).encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()


def _setup() -> tuple[tempfile.TemporaryDirectory, Path, Path, str]:
    temporary = tempfile.TemporaryDirectory()
    repo = Path(temporary.name)
    manifest = capture(
        TRANSCRIPT,
        source_type="video",
        source_id="fixture-video",
        primary_source="https://www.youtube.com/watch?v=fixture-video",
        media_type="application/json",
        created_at=NOW,
        raw_root=repo / "raw",
    ).manifest_path
    relative_manifest = str(manifest.resolve().relative_to(repo.resolve()))
    target = repo / "wiki"
    (target / "staging").mkdir(parents=True)
    return temporary, repo, target, relative_manifest


def _write_concept(
    target: Path,
    page_id: str,
    manifest: str,
    relation_row: str = "",
    subdir: str = "staging",
) -> Path:
    text = CONCEPT.read_text(encoding="utf-8").replace(FIXTURE_MANIFEST, manifest)
    text = text.replace("title: Contract Fixture Concept", f"title: {page_id}")
    text = text.replace(
        "| broader | [[fixture-parent]] | direct outgoing edge |",
        relation_row,
    )
    path = target / subdir / f"{page_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_valid_target_has_separate_structural_and_semantic_verdicts():
    temporary, repo, target, manifest = _setup()
    try:
        _write_concept(target, "valid-concept", manifest)
        result = check_target(target, repo_root=repo)
        assert result.structural_verdict == "PASS", result.findings
        assert result.semantic_review == "not-performed"
    finally:
        temporary.cleanup()


def test_all_and_changed_use_same_rules_and_findings():
    temporary, repo, target, manifest = _setup()
    try:
        page = _write_concept(target, "valid-concept", manifest)
        all_result = check_target(target, repo_root=repo, mode="all")
        changed_result = check_target(
            target, repo_root=repo, mode="changed", changed_paths=[page]
        )
        assert all_result.findings == changed_result.findings
    finally:
        temporary.cleanup()


def test_changed_mode_excludes_unrelated_finding_and_includes_direct_inbound():
    temporary, repo, target, manifest = _setup()
    try:
        changed = _write_concept(target, "changed-page", manifest)
        _write_concept(
            target,
            "inbound-page",
            manifest,
            "| related | [[changed-page]] | invalid owner on direct inbound edge |",
        )
        _write_concept(
            target,
            "unrelated-page",
            manifest,
            "| broader | [[missing-page]] | unrelated defect |",
        )
        result = check_target(
            target,
            repo_root=repo,
            mode="changed",
            changed_paths=[changed],
        )
        finding_paths = {Path(item["path"]).stem for item in result.findings}
        assert "unrelated-page" not in finding_paths
        assert "inbound-page" in finding_paths
    finally:
        temporary.cleanup()


def test_checker_is_no_write():
    temporary, repo, target, manifest = _setup()
    try:
        _write_concept(target, "valid-concept", manifest)
        before = _tree_hash(repo)
        check_target(target, repo_root=repo)
        assert _tree_hash(repo) == before
    finally:
        temporary.cleanup()


def test_broken_link_is_high_finding():
    temporary, repo, target, manifest = _setup()
    try:
        _write_concept(
            target,
            "valid-concept",
            manifest,
            "| broader | [[missing-page]] | direct outgoing edge |",
        )
        result = check_target(target, repo_root=repo)
        assert any(item["rule_id"] == "VR-KP-008" for item in result.findings)
        assert result.structural_verdict == "FAIL"
    finally:
        temporary.cleanup()


def test_duplicate_basename_is_rejected():
    temporary, repo, target, manifest = _setup()
    try:
        _write_concept(target, "duplicate-page", manifest, subdir="staging/a")
        _write_concept(target, "duplicate-page", manifest, subdir="staging/b")
        result = check_target(target, repo_root=repo)
        assert sum(item["rule_id"] == "VR-KP-007" for item in result.findings) == 2
    finally:
        temporary.cleanup()


def test_typed_relation_cycle_is_rejected():
    temporary, repo, target, manifest = _setup()
    try:
        _write_concept(target, "page-a", manifest, "| broader | [[page-b]] | edge |")
        _write_concept(target, "page-b", manifest, "| broader | [[page-a]] | edge |")
        result = check_target(target, repo_root=repo)
        assert sum(item["rule_id"] == "VR-KP-013" for item in result.findings) == 2
    finally:
        temporary.cleanup()


def test_related_edge_owner_is_lexicographically_smaller_page():
    temporary, repo, target, manifest = _setup()
    try:
        _write_concept(target, "page-a", manifest)
        _write_concept(target, "page-z", manifest, "| related | [[page-a]] | edge |")
        result = check_target(target, repo_root=repo)
        assert any(item["rule_id"] == "VR-KP-012" for item in result.findings)
    finally:
        temporary.cleanup()


def test_non_collection_page_under_collections_is_rejected():
    temporary, repo, target, manifest = _setup()
    try:
        _write_concept(target, "valid-concept", manifest, subdir="collections")
        result = check_target(target, repo_root=repo)
        assert any(item["rule_id"] == "VR-KP-014" for item in result.findings)
    finally:
        temporary.cleanup()


def test_empty_target_is_not_a_structural_pass():
    with tempfile.TemporaryDirectory() as directory:
        target = Path(directory) / "wiki"
        target.mkdir()
        result = check_target(target)
        assert result.structural_verdict == "FAIL"
        assert any(item["rule_id"] == "VR-KP-004" for item in result.findings)


def test_full_check_excludes_generated_root_pages_and_templates():
    temporary, repo, target, manifest = _setup()
    try:
        _write_concept(target, "valid-concept", manifest)
        for filename in ("index.md", "overview.md", "log.md"):
            (target / filename).write_text("invalid generated page\n", encoding="utf-8")
        (target / "templates").mkdir()
        (target / "templates" / "invalid.md").write_text(
            "invalid template\n", encoding="utf-8"
        )
        result = check_target(target, repo_root=repo, mode="all")
        assert result.structural_verdict == "PASS", result.findings
        assert result.exclusions == (
            ".git",
            ".venv",
            "__pycache__",
            "index.md",
            "log.md",
            "node_modules",
            "overview.md",
            "templates/**",
            "venv",
        )
    finally:
        temporary.cleanup()


def test_full_check_includes_hidden_canonical_markdown():
    temporary, repo, target, _ = _setup()
    try:
        hidden = target / ".active-hidden"
        hidden.mkdir()
        page = hidden / "broken.md"
        page.write_text("# Broken\n", encoding="utf-8")

        result = check_target(target, repo_root=repo, mode="all")

        assert result.structural_verdict == "FAIL"
        assert any(Path(item["path"]) == page for item in result.findings)
    finally:
        temporary.cleanup()


def test_p2_t5_validation_rules_are_active_and_executable():
    for rule_id in ("VR-KP-015", "VR-KP-016", "VR-KP-022"):
        assert RULE_REGISTRY[rule_id] == ("active", "page-command-contract")
    assert not any(
        finding["subject_id"] in {"VR-KP-015", "VR-KP-016", "VR-KP-022"}
        for finding in rule_coverage_findings()
    )


def _run_check_cli(result: CheckResult, report: str) -> tuple[int, list[str]]:
    original = wiki_ingest.check_target
    wiki_ingest.check_target = lambda *args, **kwargs: result
    try:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            return_code = wiki_ingest.main(
                [
                    "check",
                    "--all",
                    "--target-root",
                    str(ROOT / "wiki"),
                    "--report",
                    report,
                ]
            )
    finally:
        wiki_ingest.check_target = original
    return return_code, output.getvalue().splitlines()


def test_check_text_report_includes_exclusions():
    result = CheckResult(
        structural_verdict="PASS",
        semantic_review="not-performed",
        mode="all",
        exclusions=(".git", "templates/**"),
        findings=(),
    )

    return_code, output = _run_check_cli(result, "text")

    assert return_code == 0
    assert "exclusions=.git,templates/**" in output


def test_check_jsonl_report_includes_exclusions():
    result = CheckResult(
        structural_verdict="PASS",
        semantic_review="not-performed",
        mode="all",
        exclusions=(".git", "templates/**"),
        findings=(),
    )

    return_code, output = _run_check_cli(result, "jsonl")

    assert return_code == 0
    assert json.loads(output[-1])["result"]["exclusions"] == [
        ".git",
        "templates/**",
    ]


def test_architecture_check_includes_cli_entrypoint():
    from knowledge.check import architecture_findings

    with tempfile.TemporaryDirectory() as directory:
        repo = Path(directory)
        package = repo / "scripts" / "knowledge"
        package.mkdir(parents=True)
        (package / "__init__.py").write_text("", encoding="utf-8")
        (repo / "scripts" / "wiki_ingest.py").write_text(
            "import ytscript\n", encoding="utf-8"
        )
        findings = architecture_findings(repo)
        assert any("wiki_ingest -> ytscript" in item["message"] for item in findings)


def test_target_dag_contract_covers_current_non_transitional_edges():
    import ast
    import re

    architecture = (ROOT / "docs" / "wiki-ingest-architecture.md").read_text(
        encoding="utf-8"
    )
    dag_block = architecture.split("목표 module DAG:", 1)[1]
    dag_block = dag_block.split("```text", 1)[1].split("```", 1)[0]
    parsed_edges = re.findall(
        r"^\s*([a-z_]+\.py)\s*->\s*([a-z_]+\.py)\s*$",
        dag_block,
        re.MULTILINE,
    )
    target_edges = set(parsed_edges)
    target_modules = {module for edge in target_edges for module in edge}

    assert len(target_modules) == 10
    assert len(parsed_edges) == 14
    assert len(target_edges) == 14
    assert ("check.py", "fs.py") in target_edges

    adjacency = {module: set() for module in target_modules}
    for source, target in target_edges:
        adjacency[source].add(target)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(module: str) -> None:
        assert module not in visiting, f"target DAG cycle at {module}"
        if module in visited:
            return
        visiting.add(module)
        for target in adjacency[module]:
            visit(target)
        visiting.remove(module)
        visited.add(module)

    for module in target_modules:
        visit(module)

    def longest_path(module: str) -> int:
        targets = adjacency[module]
        return 0 if not targets else 1 + max(longest_path(target) for target in targets)

    assert max(longest_path(module) for module in target_modules) == 3

    scripts_root = ROOT / "scripts"
    python_paths = list((scripts_root / "knowledge").glob("*.py"))
    python_paths.append(scripts_root / "contracts" / "privacy.py")
    python_paths.append(scripts_root / "wiki_ingest.py")
    current_modules = {path.stem for path in python_paths if path.stem != "__init__"}
    current_edges: set[tuple[str, str]] = set()
    for path in python_paths:
        if path.stem == "__init__":
            continue
        source = f"{path.stem}.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            modules: list[str] = []
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules = [node.module]
            for module in modules:
                target_stem = module.split(".")[-1]
                if target_stem in current_modules:
                    current_edges.add((source, f"{target_stem}.py"))

    non_transitional_edges = {
        edge
        for edge in current_edges
        if "migration.py" not in edge
        and edge != ("wiki_ingest.py", "fs.py")
    }
    assert ("check.py", "fs.py") in non_transitional_edges
    assert non_transitional_edges <= target_edges, sorted(
        non_transitional_edges - target_edges
    )
    expected_transition_edges = {
        ("wiki_ingest.py", "artifacts.py"),
        ("wiki_ingest.py", "check.py"),
        ("wiki_ingest.py", "documents.py"),
        ("wiki_ingest.py", "fs.py"),
        ("wiki_ingest.py", "migration.py"),
        ("artifacts.py", "fs.py"),
        ("artifacts.py", "privacy.py"),
        ("artifacts.py", "schema.py"),
        ("check.py", "fs.py"),
        ("check.py", "graph.py"),
        ("check.py", "schema.py"),
        ("documents.py", "fs.py"),
        ("documents.py", "schema.py"),
        ("migration.py", "documents.py"),
        ("migration.py", "fs.py"),
        ("migration.py", "privacy.py"),
        ("migration.py", "schema.py"),
    }
    assert current_edges == expected_transition_edges, sorted(
        current_edges.symmetric_difference(expected_transition_edges)
    )
    current_adjacency = {module: set() for module in current_modules}
    for source, target in current_edges:
        current_adjacency[Path(source).stem].add(Path(target).stem)

    def current_longest_path(module: str, visiting: set[str]) -> int:
        assert module not in visiting, f"current DAG cycle at {module}"
        next_visiting = visiting | {module}
        targets = current_adjacency[module]
        return (
            0
            if not targets
            else 1
            + max(current_longest_path(target, next_visiting) for target in targets)
        )

    assert max(current_longest_path(module, set()) for module in current_modules) == 3


def test_project_timestamp_boundary_is_exact_and_one_way():
    import ast

    converter = (
        ROOT
        / "projects"
        / "info-sec-engineer-practice"
        / "scripts"
        / "past_exam_converter.py"
    )
    converter_tree = ast.parse(converter.read_text(encoding="utf-8"))
    imports = set()
    for node in ast.walk(converter_tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    assert {name for name in imports if name.startswith("contracts.")} == {
        "contracts.timestamps"
    }
    assert not any(name.startswith("knowledge.") for name in imports)

    knowledge_paths = list((ROOT / "scripts" / "knowledge").glob("*.py"))
    reverse_imports = []
    for path in knowledge_paths:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            else:
                names = []
            reverse_imports.extend(
                (path.name, name)
                for name in names
                if name.startswith("projects.") or name == "past_exam_converter"
            )
        source = path.read_text(encoding="utf-8")
        assert "past_exam_converter" not in source
    assert reverse_imports == []

    build_entry = converter.parent / "build-practice-data.py"
    contract_paths = [
        path
        for path in (ROOT / "scripts" / "contracts").glob("*.py")
        if path.stem != "__init__"
    ]
    combined_paths = [
        path for path in knowledge_paths if path.stem != "__init__"
    ] + [
        ROOT / "scripts" / "wiki_ingest.py",
        *contract_paths,
        build_entry,
        converter,
    ]
    combined_modules = {path.stem for path in combined_paths}
    combined_edges = set()
    for path in combined_paths:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            else:
                names = []
            for name in names:
                target = name.split(".")[-1]
                if target in combined_modules:
                    combined_edges.add((path.stem, target))
    migration_source = (ROOT / "scripts" / "knowledge" / "migration.py").read_text(
        encoding="utf-8"
    )

    def command_dependency(source: str) -> str:
        tree = ast.parse(source)
        planner = next(
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "build_reference_cascade_plan"
        )
        constants = {
            target.id: node.value.args[0].value
            for node in ast.walk(tree)
            if isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance((target := node.targets[0]), ast.Name)
            and target.id == "CASCADE_PRACTICE_GENERATOR"
            and isinstance(node.value, ast.Call)
            and node.value.args
            and isinstance(node.value.args[0], ast.Constant)
            and isinstance(node.value.args[0].value, str)
        }
        assert set(constants) == {"CASCADE_PRACTICE_GENERATOR"}
        assignments = {
            target.id: ast.unparse(node.value)
            for node in ast.walk(planner)
            if isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance((target := node.targets[0]), ast.Name)
            and target.id in {"generator", "baseline_generator"}
        }
        assert set(assignments) == {"generator", "baseline_generator"}
        assert all(
            "CASCADE_PRACTICE_GENERATOR.parts" in value
            for value in assignments.values()
        )
        subprocess_targets = []
        for node in ast.walk(planner):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "subprocess"
                and node.func.attr == "run"
                and node.args
                and isinstance(node.args[0], ast.List)
            ):
                path_args = [
                    element.args[0].id
                    for element in node.args[0].elts
                    if isinstance(element, ast.Call)
                    and isinstance(element.func, ast.Attribute)
                    and isinstance(element.func.value, ast.Name)
                    and element.func.value.id == "os"
                    and element.func.attr == "fspath"
                    and element.args
                    and isinstance(element.args[0], ast.Name)
                ]
                assert len(path_args) == 1
                subprocess_targets.extend(path_args)
        assert sorted(subprocess_targets) == ["baseline_generator", "generator"]
        return Path(constants["CASCADE_PRACTICE_GENERATOR"]).stem

    command_target = command_dependency(migration_source)
    assert command_target == "build-practice-data"
    retargeted = migration_source.replace(
        "os.fspath(generator)", "os.fspath(repo_root / 'other.py')", 1
    )
    try:
        command_dependency(retargeted)
    except AssertionError:
        pass
    else:
        raise AssertionError("retargeted generator command edge was accepted")
    combined_edges.add(("migration", command_target))
    assert len(combined_modules) == 12
    assert len(combined_edges) == 21
    assert ("migration", "build-practice-data") in combined_edges
    assert ("build-practice-data", "past_exam_converter") in combined_edges
    assert ("past_exam_converter", "timestamps") in combined_edges
    assert {
        source for source, target in combined_edges if target == "past_exam_converter"
    } == {"build-practice-data"}
    adjacency = {module: set() for module in combined_modules}
    for source, target in combined_edges:
        adjacency[source].add(target)

    def longest(module: str, visiting: set[str]) -> int:
        assert module not in visiting, f"combined DAG cycle at {module}"
        return 0 if not adjacency[module] else 1 + max(
            longest(target, visiting | {module}) for target in adjacency[module]
        )

    assert max(longest(module, set()) for module in combined_modules) == 4
    business_logic = (ROOT / "docs" / "wiki-ingest-business-logic.md").read_text(
        encoding="utf-8"
    )
    assert (
        "목표 core+contract edge set exact(10 modules·14 edges)·전환 command-inclusive "
        "12 modules·21 edges·cycle 0·최대 dependency edge chain 4"
        in business_logic
    )


def test_page_apply_candidate_call_path_does_not_gain_an_edge():
    import ast

    sources = {
        "wiki_ingest": ROOT / "scripts" / "wiki_ingest.py",
        "documents": ROOT / "scripts" / "knowledge" / "documents.py",
        "check": ROOT / "scripts" / "knowledge" / "check.py",
        "schema": ROOT / "scripts" / "knowledge" / "schema.py",
    }
    functions = {}
    for module, path in sources.items():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        functions.update(
            {
                (module, node.name): node
                for node in tree.body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            }
        )

    expected_path = (
        ("wiki_ingest", "main"),
        ("wiki_ingest", "_apply_page_plan"),
        ("documents", "apply_page_write_plan"),
        ("documents", "_apply_page_write_plan_unlocked"),
        ("wiki_ingest", "_check_page_candidate"),
        ("check", "check_target"),
        ("schema", "parse_markdown"),
        ("schema", "_parse_table"),
        ("schema", "_split_table_row"),
    )
    assert len(expected_path) == 9
    assert len(expected_path) - 1 == 8

    concrete_edges = (
        (expected_path[0], expected_path[1]),
        (expected_path[1], expected_path[2]),
        (expected_path[2], expected_path[3]),
        (expected_path[4], expected_path[5]),
        (expected_path[5], expected_path[6]),
        (expected_path[6], expected_path[7]),
        (expected_path[7], expected_path[8]),
    )
    for source, target in concrete_edges:
        called_names = {
            call.func.id
            for call in ast.walk(functions[source])
            if isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
        }
        assert target[1] in called_names, f"missing call edge: {source} -> {target}"

    apply_calls = [
        call
        for call in ast.walk(functions[("wiki_ingest", "_apply_page_plan")])
        if isinstance(call, ast.Call)
        and isinstance(call.func, ast.Name)
        and call.func.id == "apply_page_write_plan"
    ]
    assert len(apply_calls) == 1
    candidate_bindings = [
        keyword.value
        for keyword in apply_calls[0].keywords
        if keyword.arg == "candidate_check"
    ]
    assert len(candidate_bindings) == 1
    assert isinstance(candidate_bindings[0], ast.Name)
    assert candidate_bindings[0].id == "_check_page_candidate"

    unlocked = functions[("documents", "_apply_page_write_plan_unlocked")]
    callback_calls = {
        call.func.id
        for call in ast.walk(unlocked)
        if isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
    }
    assert "candidate_check" in callback_calls
    architecture = (ROOT / "docs" / "wiki-ingest-architecture.md").read_text(
        encoding="utf-8"
    )
    assert "함수 9개 직렬(= edge 8)" in architecture


def test_corrupt_evidence_is_rejected():
    temporary, repo, target, manifest = _setup()
    try:
        _write_concept(target, "valid-concept", manifest)
        descriptor = json.loads((repo / manifest).read_text(encoding="utf-8"))
        (repo / manifest).parent.joinpath(descriptor["payload"]).write_bytes(b"corrupt")
        result = check_target(target, repo_root=repo)
        assert any(item["rule_id"] == "VR-KP-009" for item in result.findings)
    finally:
        temporary.cleanup()


def test_corrupt_normalized_content_is_rejected():
    temporary, repo, target, manifest = _setup()
    try:
        _write_concept(target, "valid-concept", manifest)
        descriptor = json.loads((repo / manifest).read_text(encoding="utf-8"))
        (repo / manifest).parent.joinpath(descriptor["content"]["path"]).write_bytes(
            b"corrupt"
        )
        result = check_target(target, repo_root=repo)
        assert any(item["rule_id"] == "VR-KP-009" for item in result.findings)
    finally:
        temporary.cleanup()


def test_changed_mode_rejects_path_outside_target():
    temporary, repo, target, manifest = _setup()
    try:
        _write_concept(target, "valid-concept", manifest)
        outside = repo / "outside.md"
        outside.write_text("outside", encoding="utf-8")
        try:
            check_target(
                target, repo_root=repo, mode="changed", changed_paths=[outside]
            )
        except ValueError as exc:
            assert "under target root" in str(exc)
        else:
            raise AssertionError("outside changed path accepted")
    finally:
        temporary.cleanup()


def test_changed_mode_detects_broken_inbound_link_after_deletion():
    temporary, repo, target, manifest = _setup()
    try:
        deleted = _write_concept(target, "deleted-page", manifest)
        _write_concept(
            target,
            "inbound-page",
            manifest,
            "| broader | [[deleted-page]] | direct inbound edge |",
        )
        deleted.unlink()
        result = check_target(
            target,
            repo_root=repo,
            mode="changed",
            changed_paths=[deleted],
        )
        assert any(
            item["rule_id"] == "VR-KP-008" and Path(item["path"]).stem == "inbound-page"
            for item in result.findings
        )
    finally:
        temporary.cleanup()


def test_rule_coverage_fails_closed_for_missing_and_unimplemented_rule():
    registry = dict(RULE_REGISTRY)
    del registry["VR-KP-011"]
    registry["VR-KP-012"] = ("active", "unknown-check")
    findings = rule_coverage_findings(registry)
    assert {finding["subject_id"] for finding in findings} == {"VR-KP-011", "VR-KP-012"}


def test_contract_checker_rejects_pin_digest_drift():
    import shutil

    with tempfile.TemporaryDirectory() as directory:
        repo = Path(directory)
        shutil.copytree(ROOT / "_meta" / "contracts", repo / "_meta" / "contracts")
        fixture_root = repo / "tests" / "fixtures" / "contracts"
        fixture_root.mkdir(parents=True)
        shutil.copy(TRANSCRIPT, fixture_root / TRANSCRIPT.name)
        pin = repo / "_meta" / "contracts" / "canonical-transcript-v1.pin.json"
        data = json.loads(pin.read_text(encoding="utf-8"))
        data["fixture_sha256"] = "0" * 64
        pin.write_text(json.dumps(data), encoding="utf-8")
        findings = contract_findings(repo)
        assert len(findings) == 1
        assert findings[0]["rule_id"] == "VR-KP-001"


def main() -> int:
    tests = [
        value for name, value in sorted(globals().items()) if name.startswith("test_")
    ]
    failed = 0
    for test in tests:
        try:
            test()
            print(f"PASS {test.__name__}")
        except Exception as exc:
            failed += 1
            print(f"FAIL {test.__name__}: {exc}")
    print(f"\n--- {len(tests) - failed} passed, {failed} failed / {len(tests)} ---")
    return int(bool(failed))


if __name__ == "__main__":
    sys.exit(main())
