import os
import shutil
import stat
import subprocess
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parent.parent
ACTION_REFS = {
    "actions/checkout": "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
    "astral-sh/setup-uv": "astral-sh/setup-uv@20cfd1bf945f4377ade1205e4dbc17946fc9a30d",
}
UV_VERSION = "0.12.9"
EXPECTED_RUNS = (
    "uv python install",
    "uv run --with-requirements requirements-lint.txt python -m pytest -q",
    "uv run --with-requirements requirements-lint.txt python scripts/wiki_ingest.py check --all --target-root wiki --report jsonl",
    "uv run --with-requirements requirements-lint.txt python scripts/wiki_ingest.py materialize --check",
    "uv run --with-requirements requirements-lint.txt python scripts/lint.py --report jsonl",
)


def _assert_workflow_inventory(directory: Path, expected: str) -> None:
    candidates = [*directory.glob("*.yml"), *directory.glob("*.yaml")]
    assert {path.name for path in candidates} == {expected}
    assert (directory / expected).is_file()
    assert not (directory / expected).is_symlink()


def _load_workflow(workflow: str) -> dict:
    document = yaml.load(workflow, Loader=yaml.BaseLoader)
    assert isinstance(document, dict)
    return document


def _assert_required_triggers(workflow: str) -> None:
    document = _load_workflow(workflow)
    assert document["on"] == {"push": "", "pull_request": ""}


def _assert_minimum_permissions(workflow: str) -> None:
    document = _load_workflow(workflow)
    assert document["permissions"] == {"contents": "read"}
    assert "permissions" not in document["jobs"]["verify"]


def _assert_closed_execution_shape(workflow: str) -> None:
    document = _load_workflow(workflow)
    assert set(document) == {"name", "on", "permissions", "jobs"}
    job = document["jobs"]["verify"]
    assert set(job) == {"runs-on", "timeout-minutes", "steps"}
    for step in job["steps"]:
        if "run" in step:
            assert set(step) == {"run"}
        elif str(step.get("uses", "")).startswith("astral-sh/setup-uv@"):
            assert set(step) == {"uses", "with"}
            assert set(step["with"]) == {"version", "enable-cache"}
        else:
            assert set(step) == {"uses"}


def _verify_steps(workflow: str) -> list[dict]:
    document = _load_workflow(workflow)
    steps = document["jobs"]["verify"]["steps"]
    assert isinstance(steps, list)
    assert all(isinstance(step, dict) for step in steps)
    return steps


def _assert_setup_uv_version(workflow: str) -> None:
    steps = _verify_steps(workflow)
    setup_steps = [
        step for step in steps if str(step.get("uses", "")).startswith("astral-sh/setup-uv@")
    ]

    assert len(setup_steps) == 1
    inputs = setup_steps[0].get("with")
    assert isinstance(inputs, dict)
    assert inputs.get("version") == UV_VERSION
    assert [line.strip() for line in workflow.splitlines() if line.strip().startswith("version:")] == [
        f'version: "{UV_VERSION}"'
    ]


def _assert_action_pins(workflow: str) -> None:
    document = _load_workflow(workflow)
    all_uses = [
        step["uses"]
        for job in document["jobs"].values()
        for step in job.get("steps", [])
        if "uses" in step
    ]
    assert sorted(all_uses) == sorted(ACTION_REFS.values())
    steps = _verify_steps(workflow)
    for action, ref in ACTION_REFS.items():
        matches = [
            step.get("uses")
            for step in steps
            if str(step.get("uses", "")).startswith(f"{action}@")
        ]
        assert matches == [ref]


def _assert_verify_runner(workflow: str) -> None:
    document = _load_workflow(workflow)
    job = document["jobs"]["verify"]
    assert job["runs-on"] == "ubuntu-24.04"
    assert job["timeout-minutes"] == "20"


def _assert_verify_sequence(workflow: str) -> None:
    steps = _verify_steps(workflow)
    actual = [step.get("uses", step.get("run")) for step in steps]
    expected = [
        ACTION_REFS["actions/checkout"],
        ACTION_REFS["astral-sh/setup-uv"],
        *EXPECTED_RUNS,
    ]
    assert actual == expected


def _assert_single_verify_job(workflow: str) -> None:
    document = _load_workflow(workflow)
    assert set(document["jobs"]) == {"verify"}


def test_required_ci_runs_complete_knowledge_checks():
    _assert_workflow_inventory(ROOT / ".github" / "workflows", "knowledge.yml")
    workflow = (ROOT / ".github" / "workflows" / "knowledge.yml").read_text(
        encoding="utf-8"
    )
    _assert_required_triggers(workflow)
    _assert_minimum_permissions(workflow)
    _assert_closed_execution_shape(workflow)

    runs = [step.get("run") for step in _verify_steps(workflow) if "run" in step]
    for command in EXPECTED_RUNS:
        assert runs.count(command) == 1
    _assert_verify_runner(workflow)
    _assert_single_verify_job(workflow)
    _assert_action_pins(workflow)
    _assert_setup_uv_version(workflow)
    _assert_verify_sequence(workflow)
    assert (ROOT / ".python-version").read_text(encoding="utf-8") == "3.12.13\n"
    assert "youtube-script" not in workflow


def test_required_ci_rejects_additional_workflow_file(tmp_path):
    workflows = tmp_path / "workflows"
    workflows.mkdir()
    (workflows / "knowledge.yml").write_text("jobs: {}\n", encoding="utf-8")
    (workflows / "bypass.yaml").write_text("jobs: {}\n", encoding="utf-8")

    with pytest.raises(AssertionError):
        _assert_workflow_inventory(workflows, "knowledge.yml")


@pytest.mark.parametrize("trigger", ["workflow_dispatch", "pull_request_target"])
def test_required_ci_rejects_non_candidate_trigger(trigger):
    workflow = (ROOT / ".github" / "workflows" / "knowledge.yml").read_text(
        encoding="utf-8"
    )
    mutated = workflow.replace("  push:\n  pull_request:\n", f"  {trigger}:\n")

    with pytest.raises(AssertionError):
        _assert_required_triggers(mutated)


@pytest.mark.parametrize("trigger", ["push", "pull_request"])
def test_required_ci_rejects_filtered_candidate_trigger(trigger):
    workflow = (ROOT / ".github" / "workflows" / "knowledge.yml").read_text(
        encoding="utf-8"
    )
    mutated = workflow.replace(
        f"  {trigger}:\n",
        f"  {trigger}:\n    paths:\n      - docs/**\n",
    )

    with pytest.raises(AssertionError):
        _assert_required_triggers(mutated)


@pytest.mark.parametrize("scope", ["top", "job"])
def test_required_ci_rejects_write_permissions(scope):
    workflow = (ROOT / ".github" / "workflows" / "knowledge.yml").read_text(
        encoding="utf-8"
    )
    if scope == "top":
        mutated = workflow.replace("  contents: read\n", "  contents: write\n", 1)
    else:
        mutated = workflow.replace(
            "  verify:\n",
            "  verify:\n    permissions: write-all\n",
            1,
        )

    with pytest.raises(AssertionError):
        _assert_minimum_permissions(mutated)


@pytest.mark.parametrize(
    "scope,key",
    [
        ("job", "if: false"),
        ("job", "continue-on-error: true"),
        ("step", "if: false"),
        ("step", "continue-on-error: true"),
    ],
)
def test_required_ci_rejects_execution_bypass(scope, key):
    workflow = (ROOT / ".github" / "workflows" / "knowledge.yml").read_text(
        encoding="utf-8"
    )
    if scope == "job":
        mutated = workflow.replace("  verify:\n", f"  verify:\n    {key}\n", 1)
    else:
        mutated = workflow.replace(
            "      - run: uv python install\n",
            f"      - run: uv python install\n        {key}\n",
            1,
        )

    with pytest.raises(AssertionError):
        _assert_closed_execution_shape(mutated)


def test_required_ci_rejects_mutable_verify_runner_with_decoy_pin():
    workflow = (ROOT / ".github" / "workflows" / "knowledge.yml").read_text(
        encoding="utf-8"
    )
    mutated = workflow.replace(
        "    runs-on: ubuntu-24.04\n",
        "    runs-on: ubuntu-latest # runs-on: ubuntu-24.04\n",
        1,
    )

    with pytest.raises(AssertionError):
        _assert_verify_runner(mutated)


def test_required_ci_rejects_changed_timeout():
    workflow = (ROOT / ".github" / "workflows" / "knowledge.yml").read_text(
        encoding="utf-8"
    )
    mutated = workflow.replace("    timeout-minutes: 20\n", "    timeout-minutes: 360\n", 1)

    with pytest.raises(AssertionError):
        _assert_verify_runner(mutated)


def test_required_ci_rejects_reordered_steps():
    workflow = (ROOT / ".github" / "workflows" / "knowledge.yml").read_text(
        encoding="utf-8"
    )
    checkout = f'      - uses: {ACTION_REFS["actions/checkout"]} # v7.0.1\n'
    final_run = "      - run: uv run --with-requirements requirements-lint.txt python scripts/lint.py --report jsonl\n"
    mutated = workflow.replace(checkout, "", 1).replace(
        final_run,
        final_run + checkout,
        1,
    )

    with pytest.raises(AssertionError):
        _assert_verify_sequence(mutated)


@pytest.mark.parametrize("kind", ["reusable", "runner"])
def test_required_ci_rejects_auxiliary_job(kind):
    workflow = (ROOT / ".github" / "workflows" / "knowledge.yml").read_text(
        encoding="utf-8"
    )
    if kind == "reusable":
        auxiliary = "  auxiliary:\n    uses: evil/example/.github/workflows/reuse.yml@main\n"
    else:
        auxiliary = (
            "  auxiliary:\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            "      - run: true\n"
        )
    mutated = workflow.replace("jobs:\n", "jobs:\n" + auxiliary, 1)

    with pytest.raises(AssertionError):
        _assert_single_verify_job(mutated)


@pytest.mark.parametrize("mutation", ["duplicate", "relocated", "env", "nested"])
def test_required_ci_rejects_uv_version_outside_setup_step(mutation):
    workflow = (ROOT / ".github" / "workflows" / "knowledge.yml").read_text(
        encoding="utf-8"
    )
    version_line = f'          version: "{UV_VERSION}"\n'
    if mutation == "duplicate":
        mutated = workflow.replace(version_line, version_line + "          version: latest\n")
    elif mutation == "relocated":
        mutated = workflow.replace(version_line, "").replace(
            "      - uses: actions/checkout@",
            f'      - with:\n          version: "{UV_VERSION}"\n      - uses: actions/checkout@',
        )
    elif mutation == "env":
        mutated = workflow.replace("        with:\n", "        env:\n")
    else:
        mutated = workflow.replace(
            version_line,
            f'          nested:\n            version: "{UV_VERSION}"\n',
        )

    with pytest.raises(AssertionError):
        _assert_setup_uv_version(mutated)


@pytest.mark.parametrize("action", ["actions/checkout", "astral-sh/setup-uv"])
def test_required_ci_rejects_mutable_action_with_sha_in_comment(action):
    workflow = (ROOT / ".github" / "workflows" / "knowledge.yml").read_text(
        encoding="utf-8"
    )
    expected = next(line for line in workflow.splitlines() if f"uses: {action}@" in line)
    sha_ref = expected.split("@", 1)[1].split(" ", 1)[0]
    mutated = workflow.replace(expected, f"      - uses: {action}@main # {action}@{sha_ref}")

    with pytest.raises(AssertionError):
        _assert_action_pins(mutated)


@pytest.mark.parametrize("action", ["actions/checkout", "astral-sh/setup-uv"])
def test_required_ci_rejects_named_duplicate_action(action):
    workflow = (ROOT / ".github" / "workflows" / "knowledge.yml").read_text(
        encoding="utf-8"
    )
    anchor = next(line for line in workflow.splitlines() if f"uses: {action}@" in line)
    mutated = workflow.replace(
        anchor,
        f"{anchor}\n      - name: duplicate\n        uses: {action}@main",
    )

    with pytest.raises(AssertionError):
        _assert_action_pins(mutated)


@pytest.mark.parametrize("location", ["verify", "other-job"])
def test_required_ci_rejects_unregistered_mutable_action(location):
    workflow = (ROOT / ".github" / "workflows" / "knowledge.yml").read_text(
        encoding="utf-8"
    )
    if location == "verify":
        mutated = workflow.replace(
            "      - run: uv python install\n",
            "      - uses: evil/example@main\n      - run: uv python install\n",
        )
    else:
        other_job = (
            "  auxiliary:\n"
            "    runs-on: ubuntu-24.04\n"
            "    steps:\n"
            "      - uses: evil/example@main\n"
        )
        mutated = workflow.replace("jobs:\n", "jobs:\n" + other_job, 1)

    with pytest.raises(AssertionError):
        _assert_action_pins(mutated)


def test_required_ci_rejects_setup_uv_in_another_job():
    workflow = (ROOT / ".github" / "workflows" / "knowledge.yml").read_text(
        encoding="utf-8"
    )
    setup_block = (
        f'      - uses: {ACTION_REFS["astral-sh/setup-uv"]} # v10.0.1\n'
        "        with:\n"
        f'          version: "{UV_VERSION}"\n'
        "          enable-cache: true\n"
    )
    without_setup = workflow.replace(setup_block, "")
    bootstrap = "  bootstrap:\n    runs-on: ubuntu-24.04\n    steps:\n" + setup_block
    mutated = without_setup.replace("jobs:\n", "jobs:\n" + bootstrap, 1)

    with pytest.raises(AssertionError):
        _assert_setup_uv_version(mutated)


def test_pre_commit_is_executable_and_uses_staged_paths():
    hook = ROOT / ".githooks" / "pre-commit"
    contents = hook.read_text(encoding="utf-8")

    assert stat.S_IMODE(hook.stat().st_mode) == 0o755
    assert '"diff", "--cached"' in contents
    assert '"--name-status", "--no-renames"' in contents
    assert "-z" in contents
    assert 'split(b"\\0")' in contents
    for argument in ("scripts/lint.py", "--report", "jsonl", "--repository-paths"):
        assert f'"{argument}"' in contents
    for test_path in ("tests/test_contract.py", "tests/test_project_boundaries.py"):
        assert f'"{test_path}"' in contents
    assert '"checkout-index"' in contents
    assert "TemporaryDirectory" in contents
    assert '"--repository-paths"' in contents
    assert "check --all" not in contents
    assert "youtube-script" not in contents


def _hook_repo(tmp_path: Path) -> tuple[Path, dict[str, str]]:
    repo = tmp_path / "repo"
    hook = repo / ".githooks" / "pre-commit"
    fake_bin = repo / "fake-bin"
    scripts = repo / "scripts"
    tests = repo / "tests"
    hook.parent.mkdir(parents=True)
    fake_bin.mkdir()
    scripts.mkdir()
    tests.mkdir()
    (repo / "wiki").mkdir()
    (repo / "raw").mkdir()
    (repo / "_meta").mkdir()
    hook.write_bytes((ROOT / ".githooks" / "pre-commit").read_bytes())
    hook.chmod(0o755)
    (scripts / "lint.py").write_text(
        "from pathlib import Path\n"
        "import os\n"
        "import sys\n"
        "if marker := os.environ.get('LINT_MARKER'):\n"
        "    Path(marker).touch()\n"
        "if sys.argv[-1:] == ['wiki']:\n"
        "    raise SystemExit(31 if Path('wiki/repair.md').read_text() == 'broken\\n' else 0)\n"
        "if any(value.endswith('/link.md') for value in sys.argv):\n"
        "    raise SystemExit(0 if Path('untracked-target.md').exists() else 29)\n"
        "if '--leading.md' in sys.argv:\n"
        "    raise SystemExit(42)\n"
        "if '--paths' in sys.argv and any(value.startswith('docs/') for value in sys.argv):\n"
        "    raise SystemExit(46)\n"
        "if '--report' in sys.argv and '--paths' not in sys.argv and '--repository-paths' not in sys.argv:\n"
        "    if not Path('raw/delete.md').exists():\n"
        "        raise SystemExit(47)\n"
        "    if Path('raw/invalid.md').exists():\n"
        "        raise SystemExit(49)\n"
        "    if any(path.exists() and path.read_text() == 'INVALID\\n' for path in (Path('_meta/invalid.md'), Path('AGENTS.md'))):\n"
        "        raise SystemExit(49)\n"
        "    if not Path('_meta/delete.md').exists():\n"
        "        raise SystemExit(48)\n"
        "    if os.environ.get('EXPECT_REPAIR_FAILURE') and Path('wiki/repair.md').read_text() == 'broken\\n':\n"
        "        raise SystemExit(31)\n"
        "raise SystemExit(0)\n",
        encoding="utf-8",
    )
    uv = fake_bin / "uv"
    uv.write_text(
        "#!/bin/sh\n"
        "[ -z \"${UV_LOG:-}\" ] || printf '%s\\n' \"$*\" >> \"$UV_LOG\"\n"
        "if [ -n \"${FAIL_UV_ON_INVALID_REQUIREMENTS:-}\" ] && [ \"${2:-}\" = --with-requirements ] && grep -q INVALID \"$3\"; then exit 43; fi\n"
        "if [ -n \"${FAIL_UV_ON_INVALID_PYTHON_VERSION:-}\" ] && grep -q INVALID .python-version; then exit 44; fi\n"
        "case \" $* \" in *\" python -m pytest \"*)\n"
        "  if [ -n \"${FAIL_PYTEST_ON_INVALID:-}\" ] && grep -q INVALID tests/test_contract.py; then exit 41; fi\n"
        "  [ -n \"${RUN_REAL_PYTEST:-}\" ] || exit 0;;\n"
        "esac\n"
        "while [ \"$1\" != python ]; do shift; done\n"
        "shift\n"
        "exec python3 \"$@\"\n",
        encoding="utf-8",
    )
    uv.chmod(0o755)
    (repo / "note.md").write_text("valid\n", encoding="utf-8")
    (repo / "requirements-lint.txt").write_text("valid\n", encoding="utf-8")
    (repo / ".python-version").write_text("3.12.13\n", encoding="utf-8")
    (tests / "test_contract.py").write_text(
        "def test_contract():\n    assert True\n", encoding="utf-8"
    )
    (tests / "test_project_boundaries.py").write_text(
        "import subprocess\n"
        "def test_git_context():\n"
        "    result = subprocess.run(['git', 'rev-parse', '--show-toplevel'], check=False)\n"
        "    assert result.returncode == 0\n",
        encoding="utf-8",
    )
    (repo / "wiki" / "page.md").write_text("valid\n", encoding="utf-8")
    (repo / "wiki" / "repair.md").write_text("broken\n", encoding="utf-8")
    (repo / "raw" / "delete.md").write_text("valid\n", encoding="utf-8")
    (repo / "_meta" / "delete.md").write_text("valid\n", encoding="utf-8")
    (repo / "AGENTS.md").write_text("valid\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "test"], cwd=repo, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.invalid"],
        cwd=repo,
        check=True,
    )
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "baseline"], cwd=repo, check=True)
    env = os.environ.copy()
    env["PATH"] = f"{fake_bin}{os.pathsep}{env['PATH']}"
    return repo, env


def _install_faulting_git(repo: Path, env: dict[str, str]) -> None:
    actual_git = shutil.which("git")
    assert actual_git is not None
    fake_git = repo / "fake-bin" / "git"
    fake_git.write_text(
        "#!/bin/sh\n"
        "if [ \"$1\" = diff ] && [ -n \"${FAKE_GIT_MODE:-}\" ]; then\n"
        "  case \"$FAKE_GIT_MODE\" in\n"
        "    fail) exit 37;;\n"
        "    malformed) printf 'M\\000'; exit 0;;\n"
        "    non_utf8) printf 'M\\000\\377.md\\000'; exit 0;;\n"
        "  esac\n"
        "fi\n"
        "if [ \"$1\" = checkout-index ] && [ \"${FAKE_GIT_MODE:-}\" = checkout_fail ]; then\n"
        "  exit 38\n"
        "fi\n"
        f'exec "{actual_git}" "$@"\n',
        encoding="utf-8",
    )
    fake_git.chmod(0o755)


def test_pre_commit_rejects_staged_markdown_masked_by_worktree(tmp_path):
    repo, env = _hook_repo(tmp_path)
    note = repo / "note.md"
    note.write_text("staged invalid\n", encoding="utf-8")
    subprocess.run(["git", "add", "note.md"], cwd=repo, check=True)
    note.write_text("worktree valid\n", encoding="utf-8")

    result = subprocess.run(
        [repo / ".githooks" / "pre-commit"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "staged/worktree Markdown mismatch" in result.stderr


def test_pre_commit_accepts_delete_only_and_empty_staged_sets(tmp_path):
    repo, env = _hook_repo(tmp_path)
    hook = repo / ".githooks" / "pre-commit"

    empty = subprocess.run(
        [hook], cwd=repo, env=env, capture_output=True, text=True, check=False
    )
    assert empty.returncode == 0

    (repo / "note.md").unlink()
    subprocess.run(["git", "add", "note.md"], cwd=repo, check=True)
    deleted = subprocess.run(
        [hook], cwd=repo, env=env, capture_output=True, text=True, check=False
    )
    assert deleted.returncode == 0


def test_pre_commit_rejects_staged_deletion_restored_in_worktree(tmp_path):
    repo, env = _hook_repo(tmp_path)
    note = repo / "note.md"
    note.unlink()
    subprocess.run(["git", "add", "note.md"], cwd=repo, check=True)
    note.write_text("restored\n", encoding="utf-8")

    result = subprocess.run(
        [repo / ".githooks" / "pre-commit"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "staged/worktree Markdown mismatch" in result.stderr


def test_pre_commit_routes_wiki_deletion_to_full_wiki_lint(tmp_path):
    repo, env = _hook_repo(tmp_path)
    (repo / "wiki" / "page.md").rename(repo / "wiki" / "page.txt")
    (repo / "wiki" / "repair.md").write_text("repaired\n", encoding="utf-8")
    (repo / "note.md").write_text("changed\n", encoding="utf-8")
    subprocess.run(
        ["git", "add", "-A", "wiki/page.md", "wiki/page.txt", "note.md"],
        cwd=repo,
        check=True,
    )
    env["EXPECT_REPAIR_FAILURE"] = "1"

    result = subprocess.run(
        [repo / ".githooks" / "pre-commit"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 31


def test_pre_commit_lints_staged_markdown_without_untracked_targets(tmp_path):
    repo, env = _hook_repo(tmp_path)
    (repo / "raw" / "link.md").write_text("[[untracked-target]]\n", encoding="utf-8")
    subprocess.run(["git", "add", "raw/link.md"], cwd=repo, check=True)
    (repo / "untracked-target.md").write_text("target\n", encoding="utf-8")

    result = subprocess.run(
        [repo / ".githooks" / "pre-commit"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 29


def test_pre_commit_routes_non_wiki_lint_scope_deletion_to_full_lint(tmp_path):
    repo, env = _hook_repo(tmp_path)
    (repo / "raw" / "delete.md").unlink()
    subprocess.run(["git", "add", "raw/delete.md"], cwd=repo, check=True)

    result = subprocess.run(
        [repo / ".githooks" / "pre-commit"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 47


@pytest.mark.parametrize(
    "invalid_path", ["raw/invalid.md", "_meta/invalid.md", "AGENTS.md"]
)
def test_pre_commit_combines_wiki_deletion_with_other_lint_scope_changes(
    tmp_path, invalid_path
):
    repo, env = _hook_repo(tmp_path)
    (repo / "wiki" / "page.md").rename(repo / "wiki" / "page.txt")
    (repo / invalid_path).write_text("INVALID\n", encoding="utf-8")
    subprocess.run(
        ["git", "add", "-A", "wiki/page.md", "wiki/page.txt", invalid_path],
        cwd=repo,
        check=True,
    )

    result = subprocess.run(
        [repo / ".githooks" / "pre-commit"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 49


def test_pre_commit_combines_wiki_and_other_lint_scope_deletions(tmp_path):
    repo, env = _hook_repo(tmp_path)
    (repo / "wiki" / "page.md").rename(repo / "wiki" / "page.txt")
    (repo / "_meta" / "delete.md").unlink()
    subprocess.run(
        ["git", "add", "-A", "wiki/page.md", "wiki/page.txt", "_meta/delete.md"],
        cwd=repo,
        check=True,
    )

    result = subprocess.run(
        [repo / ".githooks" / "pre-commit"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 48


def test_pre_commit_preserves_space_and_newline_in_staged_markdown_paths(tmp_path):
    repo, env = _hook_repo(tmp_path)
    for name in ("has space.md", "line\nbreak.md"):
        (repo / name).write_text("valid\n", encoding="utf-8")
    subprocess.run(
        ["git", "add", "has space.md", "line\nbreak.md"], cwd=repo, check=True
    )

    result = subprocess.run(
        [repo / ".githooks" / "pre-commit"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0


def test_pre_commit_treats_leading_hyphen_as_a_path(tmp_path):
    repo, env = _hook_repo(tmp_path)
    (repo / "--leading.md").write_text("valid\n", encoding="utf-8")
    subprocess.run(["git", "add", "--", "--leading.md"], cwd=repo, check=True)

    result = subprocess.run(
        [repo / ".githooks" / "pre-commit"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0


def test_pre_commit_skips_markdown_outside_repository_lint_scope(tmp_path):
    repo, env = _hook_repo(tmp_path)
    (repo / "docs").mkdir()
    (repo / "docs" / "design.md").write_text("[[example-id]]\n", encoding="utf-8")
    subprocess.run(["git", "add", "docs/design.md"], cwd=repo, check=True)

    result = subprocess.run(
        [repo / ".githooks" / "pre-commit"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0


def test_pre_commit_runs_fast_tests_from_index_snapshot(tmp_path):
    repo, env = _hook_repo(tmp_path)
    contract_test = repo / "tests" / "test_contract.py"
    contract_test.write_text("INVALID\n", encoding="utf-8")
    subprocess.run(["git", "add", "tests/test_contract.py"], cwd=repo, check=True)
    contract_test.write_text("def test_contract():\n    assert True\n", encoding="utf-8")
    env["FAIL_PYTEST_ON_INVALID"] = "1"

    result = subprocess.run(
        [repo / ".githooks" / "pre-commit"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0


def test_pre_commit_snapshot_tests_have_git_context(tmp_path):
    repo, env = _hook_repo(tmp_path)
    env["RUN_REAL_PYTEST"] = "1"

    result = subprocess.run(
        [repo / ".githooks" / "pre-commit"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0


def test_pre_commit_bootstraps_before_reading_snapshot_requirements(tmp_path):
    repo, env = _hook_repo(tmp_path)
    (repo / "requirements-lint.txt").write_text("INVALID\n", encoding="utf-8")
    env["FAIL_UV_ON_INVALID_REQUIREMENTS"] = "1"

    result = subprocess.run(
        [repo / ".githooks" / "pre-commit"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0


def test_pre_commit_bootstraps_before_reading_snapshot_python_version(tmp_path):
    repo, env = _hook_repo(tmp_path)
    (repo / ".python-version").write_text("INVALID\n", encoding="utf-8")
    env["FAIL_UV_ON_INVALID_PYTHON_VERSION"] = "1"

    result = subprocess.run(
        [repo / ".githooks" / "pre-commit"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0


@pytest.mark.parametrize("mode", ["fail", "malformed", "non_utf8"])
def test_pre_commit_fails_closed_on_invalid_git_inventory(tmp_path, mode):
    repo, env = _hook_repo(tmp_path)
    _install_faulting_git(repo, env)
    marker = tmp_path / "lint-ran"
    env["FAKE_GIT_MODE"] = mode
    env["LINT_MARKER"] = str(marker)

    result = subprocess.run(
        [repo / ".githooks" / "pre-commit"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert not marker.exists()


def test_pre_commit_fails_closed_when_index_snapshot_cannot_be_created(tmp_path):
    repo, env = _hook_repo(tmp_path)
    _install_faulting_git(repo, env)
    marker = tmp_path / "lint-ran"
    uv_log = tmp_path / "uv.log"
    env["FAKE_GIT_MODE"] = "checkout_fail"
    env["LINT_MARKER"] = str(marker)
    env["UV_LOG"] = str(uv_log)

    result = subprocess.run(
        [repo / ".githooks" / "pre-commit"],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 38
    assert not marker.exists()
    assert not uv_log.exists()
