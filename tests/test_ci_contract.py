import os
import shutil
import stat
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parent.parent


def test_required_ci_runs_complete_knowledge_checks():
    workflow = (ROOT / ".github" / "workflows" / "knowledge.yml").read_text(
        encoding="utf-8"
    )

    for command in (
        "uv python install",
        "python -m pytest -q",
        "python scripts/wiki_ingest.py check --all --target-root wiki --report jsonl",
        "python scripts/wiki_ingest.py materialize --check",
        "python scripts/lint.py --report jsonl",
    ):
        assert workflow.count(command) == 1
    assert "runs-on: ubuntu-24.04" in workflow
    assert "actions/checkout@11d5960a326750d5838078e36cf38b85af677262" in workflow
    assert "astral-sh/setup-uv@d0cc045d04ccac9d8b7881df0226f9e82c39688e" in workflow
    assert (ROOT / ".python-version").read_text(encoding="utf-8") == "3.12.13\n"
    assert "youtube-script" not in workflow


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
