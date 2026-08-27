import stat
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from knowledge import fs  # noqa: E402


def test_publish_bytes_no_replace_is_atomic_and_idempotent():
    with tempfile.TemporaryDirectory() as directory:
        output = Path(directory) / "plan.json"
        assert fs.publish_bytes_no_replace(output, b"approved\n") is True
        assert fs.publish_bytes_no_replace(output, b"approved\n") is False
        try:
            fs.publish_bytes_no_replace(output, b"different\n")
        except FileExistsError:
            pass
        else:
            raise AssertionError("different bytes replaced an approved output")
        assert output.read_bytes() == b"approved\n"


def test_publish_bytes_no_replace_preserves_competing_writer():
    with tempfile.TemporaryDirectory() as directory:
        output = Path(directory) / "plan.json"
        real_link = fs.os.link

        def competing_link(source: Path, target: Path) -> None:
            Path(target).write_bytes(b"competitor\n")
            real_link(source, target)

        fs.os.link = competing_link
        try:
            try:
                fs.publish_bytes_no_replace(output, b"approved\n")
            except FileExistsError:
                pass
            else:
                raise AssertionError("competing output was replaced")
        finally:
            fs.os.link = real_link
        assert output.read_bytes() == b"competitor\n"


def test_replace_bytes_atomic_preserves_previous_bytes_when_replace_fails():
    with tempfile.TemporaryDirectory() as directory:
        output = Path(directory) / "page.md"
        output.write_bytes(b"before\n")
        real_replace = fs.os.replace

        def fail_replace(source: Path, target: Path) -> None:
            raise OSError("injected replace failure")

        fs.os.replace = fail_replace
        try:
            try:
                fs.replace_bytes_atomic(output, b"after\n")
            except OSError as exc:
                assert "injected replace failure" in str(exc)
            else:
                raise AssertionError("injected replace failure was ignored")
        finally:
            fs.os.replace = real_replace
        assert output.read_bytes() == b"before\n"
        assert list(output.parent.glob(f".{output.name}.*")) == []


def test_rename_path_no_replace_moves_without_overwriting_target():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        source = root / "source.md"
        target = root / "target.md"
        source.write_bytes(b"source\n")
        target.write_bytes(b"target\n")
        try:
            fs.rename_path_no_replace(source, target)
        except OSError:
            pass
        else:
            raise AssertionError("existing target was overwritten")
        assert source.read_bytes() == b"source\n"
        assert target.read_bytes() == b"target\n"


def test_publish_and_replace_preserve_canonical_modes():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        created = root / "created.md"
        assert fs.publish_bytes_no_replace(created, b"created\n") is True
        assert stat.S_IMODE(created.stat().st_mode) == 0o644

        existing = root / "existing.md"
        existing.write_bytes(b"before\n")
        existing.chmod(0o640)
        fs.replace_bytes_atomic(existing, b"after\n")
        assert existing.read_bytes() == b"after\n"
        assert stat.S_IMODE(existing.stat().st_mode) == 0o640


def test_leaf_primitives_rollback_after_first_post_commit_fsync_failure():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        real_fsync = fs.fsync_directory
        calls = 0

        def fail_once(path: Path) -> None:
            nonlocal calls
            calls += 1
            if calls == 1:
                raise OSError("injected post-commit fsync failure")
            real_fsync(path)

        fs.fsync_directory = fail_once
        try:
            created = root / "created.md"
            try:
                fs.publish_bytes_no_replace(created, b"created\n")
            except OSError:
                pass
            else:
                raise AssertionError("injected create fsync failure was ignored")
            assert not created.exists()

            calls = 0
            replaced = root / "replaced.md"
            replaced.write_bytes(b"before\n")
            replaced.chmod(0o640)
            try:
                fs.replace_bytes_atomic(replaced, b"after\n")
            except OSError:
                pass
            else:
                raise AssertionError("injected replace fsync failure was ignored")
            assert replaced.read_bytes() == b"before\n"
            assert stat.S_IMODE(replaced.stat().st_mode) == 0o640

            calls = 0
            source = root / "source.md"
            target = root / "target.md"
            source.write_bytes(b"source\n")
            source.chmod(0o600)
            try:
                fs.rename_path_no_replace(source, target)
            except OSError:
                pass
            else:
                raise AssertionError("injected move fsync failure was ignored")
            assert source.read_bytes() == b"source\n"
            assert stat.S_IMODE(source.stat().st_mode) == 0o600
            assert not target.exists()
        finally:
            fs.fsync_directory = real_fsync


def test_rename_post_commit_failure_does_not_move_external_target_to_source():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        source = root / "source.md"
        target = root / "target.md"
        source.write_bytes(b"base\n")
        real_fsync = fs.fsync_directory
        calls = 0

        def replace_target_then_fail(path: Path) -> None:
            nonlocal calls
            calls += 1
            if calls == 1:
                target.write_bytes(b"external\n")
                raise OSError("injected post-commit failure")
            real_fsync(path)

        fs.fsync_directory = replace_target_then_fail
        try:
            try:
                fs.rename_path_no_replace(source, target)
            except OSError as exc:
                assert "indeterminate" in str(exc)
            else:
                raise AssertionError("external target conflict was ignored")
        finally:
            fs.fsync_directory = real_fsync
        assert not source.exists()
        assert target.read_bytes() == b"external\n"


def test_create_and_replace_post_commit_conflicts_are_preserved():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        real_fsync = fs.fsync_directory

        created = root / "created.md"
        calls = 0

        def change_created_mode_then_fail(path: Path) -> None:
            nonlocal calls
            calls += 1
            if calls == 1:
                created.chmod(0o600)
                raise OSError("injected create conflict")
            real_fsync(path)

        fs.fsync_directory = change_created_mode_then_fail
        try:
            try:
                fs.publish_bytes_no_replace(created, b"created\n")
            except OSError as exc:
                assert "indeterminate" in str(exc)
            else:
                raise AssertionError("create conflict was ignored")
        finally:
            fs.fsync_directory = real_fsync
        assert created.read_bytes() == b"created\n"
        assert stat.S_IMODE(created.stat().st_mode) == 0o600

        deleted = root / "deleted.md"
        calls = 0

        def delete_created_then_fail(path: Path) -> None:
            nonlocal calls
            calls += 1
            if calls == 1:
                deleted.unlink()
                raise OSError("injected create deletion")
            real_fsync(path)

        fs.fsync_directory = delete_created_then_fail
        try:
            try:
                fs.publish_bytes_no_replace(deleted, b"deleted\n")
            except OSError as exc:
                assert "indeterminate" in str(exc)
            else:
                raise AssertionError("create deletion conflict was ignored")
        finally:
            fs.fsync_directory = real_fsync
        assert not deleted.exists()

        replaced = root / "replaced.md"
        replaced.write_bytes(b"before\n")
        calls = 0

        def replace_content_then_fail(path: Path) -> None:
            nonlocal calls
            calls += 1
            if calls == 1:
                replaced.write_bytes(b"external\n")
                raise OSError("injected replace conflict")
            real_fsync(path)

        fs.fsync_directory = replace_content_then_fail
        try:
            try:
                fs.replace_bytes_atomic(replaced, b"after\n")
            except OSError as exc:
                assert "indeterminate" in str(exc)
            else:
                raise AssertionError("replace conflict was ignored")
        finally:
            fs.fsync_directory = real_fsync
        assert replaced.read_bytes() == b"external\n"


def test_post_commit_rollback_failure_is_reported_indeterminate():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        real_fsync = fs.fsync_directory
        calls = 0

        def fail_every_fsync(path: Path) -> None:
            nonlocal calls
            calls += 1
            raise OSError(f"injected fsync failure {calls}: {path}")

        fs.fsync_directory = fail_every_fsync
        try:
            created = root / "created.md"
            try:
                fs.publish_bytes_no_replace(created, b"created\n")
            except OSError as exc:
                assert "indeterminate" in str(exc)
            else:
                raise AssertionError("create rollback fsync failure was ignored")

            replaced = root / "replaced.md"
            replaced.write_bytes(b"before\n")
            try:
                fs.replace_bytes_atomic(replaced, b"after\n")
            except OSError as exc:
                assert "indeterminate" in str(exc)
            else:
                raise AssertionError("replace rollback fsync failure was ignored")
        finally:
            fs.fsync_directory = real_fsync


def test_post_commit_observation_failure_is_reported_indeterminate(
    monkeypatch: pytest.MonkeyPatch,
):
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        real_fsync = fs.fsync_directory
        real_read_bytes = Path.read_bytes

        replaced = root / "replaced.md"
        replaced.write_bytes(b"before\n")
        replace_reads = 0

        def fail_replace_observation(path: Path) -> bytes:
            nonlocal replace_reads
            if path == replaced:
                replace_reads += 1
                if replace_reads == 2:
                    raise PermissionError("injected replace observation failure")
            return real_read_bytes(path)

        monkeypatch.setattr(Path, "read_bytes", fail_replace_observation)

        def fail_fsync(path: Path) -> None:
            raise OSError(f"injected post-commit: {path}")

        monkeypatch.setattr(fs, "fsync_directory", fail_fsync)
        with pytest.raises(OSError, match="indeterminate"):
            fs.replace_bytes_atomic(replaced, b"after\n")
        assert real_read_bytes(replaced) == b"after\n"

        monkeypatch.setattr(Path, "read_bytes", real_read_bytes)
        source = root / "source.md"
        target = root / "target.md"
        source.write_bytes(b"source\n")

        def fail_move_observation(path: Path) -> bytes:
            if path == target:
                raise PermissionError("injected move observation failure")
            return real_read_bytes(path)

        monkeypatch.setattr(Path, "read_bytes", fail_move_observation)
        with pytest.raises(OSError, match="indeterminate"):
            fs.rename_path_no_replace(source, target)
        assert not source.exists()
        assert real_read_bytes(target) == b"source\n"
        monkeypatch.setattr(fs, "fsync_directory", real_fsync)


def test_repository_write_lock_is_nonblocking_and_process_scoped():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        with fs.repository_write_lock(root):
            try:
                with fs.repository_write_lock(root):
                    pass
            except BlockingIOError:
                pass
            else:
                raise AssertionError("second repository writer acquired the same lock")


def test_repository_write_lock_blocks_a_separate_process():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        command = (
            "import sys; from pathlib import Path; "
            "sys.path.insert(0, sys.argv[2]); "
            "from knowledge.fs import repository_write_lock; "
            "\ntry:\n with repository_write_lock(Path(sys.argv[1])): pass"
            "\nexcept BlockingIOError:\n raise SystemExit(23)"
        )
        with fs.repository_write_lock(root):
            result = subprocess.run(
                [sys.executable, "-c", command, str(root), str(ROOT / "scripts")],
                check=False,
                capture_output=True,
                text=True,
            )
        assert result.returncode == 23, result.stderr
