from __future__ import annotations

import ctypes
import errno
import fcntl
import hashlib
import os
import re
import secrets
import stat
import sys
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from functools import wraps
from pathlib import Path


class PathSafetyError(ValueError):
    pass


@dataclass(frozen=True)
class VerifiedDirectory:
    path: Path
    descriptor: int
    device: int
    inode: int

    def assert_identity(self) -> None:
        try:
            observed = self.path.lstat()
            opened = os.fstat(self.descriptor)
        except OSError as exc:
            raise PathSafetyError(f"directory changed: {self.path}") from exc
        if (
            not stat.S_ISDIR(observed.st_mode)
            or stat.S_ISLNK(observed.st_mode)
            or (observed.st_dev, observed.st_ino) != (self.device, self.inode)
            or (opened.st_dev, opened.st_ino) != (self.device, self.inode)
        ):
            raise PathSafetyError(f"directory changed: {self.path}")


@dataclass(frozen=True)
class LeafObservation:
    data: bytes
    device: int
    inode: int
    mode: int


@dataclass(frozen=True)
class TemporaryLeaf:
    name: str
    device: int
    inode: int
    mode: int
    sha256: str


MANAGED_TEMPORARY_RE = re.compile(r"^\..+\.[a-f0-9]{24}$")


def is_managed_temporary_leaf_name(name: str) -> bool:
    return MANAGED_TEMPORARY_RE.fullmatch(name) is not None


@contextmanager
def verified_directory(path: Path) -> Iterator[VerifiedDirectory]:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise PathSafetyError(f"target must be a regular directory: {path}") from exc
    try:
        state = os.fstat(descriptor)
        if not stat.S_ISDIR(state.st_mode):
            raise PathSafetyError(f"target must be a regular directory: {path}")
        handle = VerifiedDirectory(path, descriptor, state.st_dev, state.st_ino)
        handle.assert_identity()
        yield handle
    finally:
        os.close(descriptor)


def _observe_regular_leaf_from_descriptor(
    directory: VerifiedDirectory, name: str
) -> LeafObservation | None:
    if Path(name).name != name:
        raise PathSafetyError(f"leaf name must be a basename: {name}")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(name, flags, dir_fd=directory.descriptor)
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise PathSafetyError(f"leaf must be regular non-symlink: {name}") from exc
    try:
        state = os.fstat(descriptor)
        if not stat.S_ISREG(state.st_mode):
            raise PathSafetyError(f"leaf must be regular non-symlink: {name}")
        chunks = []
        while chunk := os.read(descriptor, 1024 * 1024):
            chunks.append(chunk)
        return LeafObservation(
            data=b"".join(chunks),
            device=state.st_dev,
            inode=state.st_ino,
            mode=stat.S_IMODE(state.st_mode),
        )
    finally:
        os.close(descriptor)


def observe_regular_leaf_at(
    directory: VerifiedDirectory, name: str
) -> LeafObservation | None:
    directory.assert_identity()
    return _observe_regular_leaf_from_descriptor(directory, name)


def read_regular_leaf_at(directory: VerifiedDirectory, name: str) -> bytes | None:
    observed = observe_regular_leaf_at(directory, name)
    return None if observed is None else observed.data


def _write_temp_at(
    directory: VerifiedDirectory, name: str, data: bytes, mode: int
) -> TemporaryLeaf:
    for _ in range(128):
        temporary = f".{name}.{secrets.token_hex(12)}"
        try:
            descriptor = os.open(
                temporary,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
                mode,
                dir_fd=directory.descriptor,
            )
            break
        except FileExistsError:
            continue
    else:
        raise FileExistsError(f"cannot allocate temporary leaf: {name}")
    try:
        view = memoryview(data)
        while view:
            written = os.write(descriptor, view)
            view = view[written:]
        os.fchmod(descriptor, mode)
        os.fsync(descriptor)
        state = os.fstat(descriptor)
    except BaseException:
        try:
            os.unlink(temporary, dir_fd=directory.descriptor)
        except FileNotFoundError:
            pass
        raise
    finally:
        os.close(descriptor)
    return TemporaryLeaf(
        name=temporary,
        device=state.st_dev,
        inode=state.st_ino,
        mode=stat.S_IMODE(state.st_mode),
        sha256=hashlib.sha256(data).hexdigest(),
    )


def _matches_temporary_identity(
    directory: VerifiedDirectory, name: str, temporary: TemporaryLeaf
) -> bool:
    observed = _observe_regular_leaf_from_descriptor(directory, name)
    return observed is not None and (
        observed.device,
        observed.inode,
        observed.mode,
    ) == (temporary.device, temporary.inode, temporary.mode) and (
        hashlib.sha256(observed.data).hexdigest() == temporary.sha256
    )


def _matches_temporary_inode(
    directory: VerifiedDirectory, name: str, temporary: TemporaryLeaf
) -> bool:
    observed = _observe_regular_leaf_from_descriptor(directory, name)
    return observed is not None and (
        observed.device,
        observed.inode,
        observed.mode,
    ) == (temporary.device, temporary.inode, temporary.mode)


def managed_temporary_leaf_names(directory: VerifiedDirectory) -> tuple[str, ...]:
    directory.assert_identity()
    return tuple(
        sorted(
            name
            for name in os.listdir(directory.descriptor)
            if is_managed_temporary_leaf_name(name)
        )
    )


def remove_observed_leaf_at(
    directory: VerifiedDirectory, name: str, expected: LeafObservation
) -> None:
    if observe_regular_leaf_at(directory, name) != expected:
        raise PathSafetyError(f"leaf changed before removal: {directory.path / name}")
    os.unlink(name, dir_fd=directory.descriptor)
    os.fsync(directory.descriptor)


def _exchange_leaf_names(directory: VerifiedDirectory, first: str, second: str) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    first_bytes = os.fsencode(first)
    second_bytes = os.fsencode(second)
    if sys.platform == "darwin":
        operation = libc.renameatx_np
        operation.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint,
        ]
        result = operation(
            directory.descriptor,
            first_bytes,
            directory.descriptor,
            second_bytes,
            0x00000002,
        )
    elif sys.platform.startswith("linux"):
        operation = libc.renameat2
        operation.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint,
        ]
        result = operation(
            directory.descriptor,
            first_bytes,
            directory.descriptor,
            second_bytes,
            2,
        )
    else:
        raise OSError(errno.ENOTSUP, "atomic leaf exchange is unavailable")
    if result != 0:
        error_number = ctypes.get_errno()
        raise OSError(error_number, os.strerror(error_number), directory.path / second)


def publish_bytes_no_replace_at(
    directory: VerifiedDirectory, name: str, data: bytes
) -> bool:
    if read_regular_leaf_at(directory, name) is not None:
        raise FileExistsError(f"existing output differs: {directory.path / name}")
    temporary = _write_temp_at(directory, name, data, 0o644)
    try:
        directory.assert_identity()
        if not _matches_temporary_identity(directory, temporary.name, temporary):
            raise PathSafetyError(f"temporary leaf changed: {temporary.name}")
        os.link(
            temporary.name,
            name,
            src_dir_fd=directory.descriptor,
            dst_dir_fd=directory.descriptor,
            follow_symlinks=False,
        )
        try:
            if not _matches_temporary_identity(directory, name, temporary):
                raise PathSafetyError(f"temporary leaf changed: {temporary.name}")
            os.fsync(directory.descriptor)
            directory.assert_identity()
        except (OSError, PathSafetyError) as commit_error:
            if not _matches_temporary_inode(directory, name, temporary):
                raise OSError(
                    errno.EBUSY,
                    "publish commit indeterminate; observed target differs from "
                    "planned leaf",
                    directory.path / name,
                ) from commit_error
            try:
                os.unlink(name, dir_fd=directory.descriptor)
                os.fsync(directory.descriptor)
            except OSError as rollback_error:
                raise OSError(
                    errno.EIO,
                    "publish commit indeterminate; rollback failed",
                    directory.path / name,
                ) from rollback_error
            raise
        return True
    finally:
        if _matches_temporary_inode(directory, temporary.name, temporary):
            try:
                os.unlink(temporary.name, dir_fd=directory.descriptor)
            except FileNotFoundError:
                pass


def replace_bytes_atomic_at(
    directory: VerifiedDirectory,
    name: str,
    expected_previous: LeafObservation,
    data: bytes,
) -> None:
    observed = observe_regular_leaf_at(directory, name)
    if observed != expected_previous:
        raise PathSafetyError(f"leaf changed after preflight: {directory.path / name}")
    temporary = _write_temp_at(directory, name, data, expected_previous.mode)
    cleanup_temporary = True
    try:
        directory.assert_identity()
        if observe_regular_leaf_at(directory, name) != expected_previous:
            raise PathSafetyError(
                f"leaf changed after preflight: {directory.path / name}"
            )
        if not _matches_temporary_identity(directory, temporary.name, temporary):
            raise PathSafetyError(f"temporary leaf changed: {temporary.name}")
        _exchange_leaf_names(directory, temporary.name, name)
        displaced = _observe_regular_leaf_from_descriptor(directory, temporary.name)
        target_is_exact = _matches_temporary_identity(directory, name, temporary)
        if displaced != expected_previous or not target_is_exact:
            if not _matches_temporary_inode(directory, name, temporary):
                cleanup_temporary = False
                raise OSError(
                    errno.EBUSY,
                    "replace commit indeterminate; target changed before rollback",
                    directory.path / name,
                )
            cleanup_temporary = False
            try:
                _exchange_leaf_names(directory, temporary.name, name)
                os.fsync(directory.descriptor)
                cleanup_temporary = True
            except OSError as rollback_error:
                raise OSError(
                    errno.EIO,
                    "replace conflict rollback failed",
                    directory.path / name,
                ) from rollback_error
            raise PathSafetyError(
                f"leaf changed after preflight: {directory.path / name}"
            )
        try:
            os.fsync(directory.descriptor)
            directory.assert_identity()
        except (OSError, PathSafetyError) as commit_error:
            displaced = _observe_regular_leaf_from_descriptor(directory, temporary.name)
            if displaced != expected_previous or not _matches_temporary_inode(
                directory, name, temporary
            ):
                cleanup_temporary = displaced == expected_previous
                raise OSError(
                    errno.EBUSY,
                    "replace commit indeterminate; observed target differs from "
                    "planned leaf",
                    directory.path / name,
                ) from commit_error
            cleanup_temporary = False
            try:
                _exchange_leaf_names(directory, temporary.name, name)
                os.fsync(directory.descriptor)
                cleanup_temporary = True
            except OSError as rollback_error:
                raise OSError(
                    errno.EIO,
                    "replace commit indeterminate; rollback failed",
                    directory.path / name,
                ) from rollback_error
            raise
    finally:
        cleanup_observation = _observe_regular_leaf_from_descriptor(
            directory, temporary.name
        )
        cleanup_is_owned = cleanup_observation == expected_previous or (
            cleanup_observation is not None
            and (
                cleanup_observation.device,
                cleanup_observation.inode,
                cleanup_observation.mode,
            )
            == (temporary.device, temporary.inode, temporary.mode)
        )
        if cleanup_temporary and cleanup_is_owned:
            try:
                os.unlink(temporary.name, dir_fd=directory.descriptor)
            except FileNotFoundError:
                pass


def confined(root: Path, candidate: Path) -> Path:
    resolved_root = root.resolve()
    resolved = candidate.resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise PathSafetyError(f"path escapes root: {candidate}") from exc
    return resolved


def write_bytes_fsync(path: Path, data: bytes) -> None:
    with path.open("xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def publish_bytes_no_replace(path: Path, data: bytes) -> bool:
    """Atomically publish bytes without replacing a competing destination."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.is_file() and path.read_bytes() == data:
            return False
        raise FileExistsError(f"existing output differs: {path}")
    descriptor, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temp = Path(temp_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fchmod(handle.fileno(), 0o644)
            os.fsync(handle.fileno())
        try:
            os.link(temp, path)
        except FileExistsError:
            if not path.is_file() or path.read_bytes() != data:
                raise FileExistsError(f"existing output differs: {path}") from None
            return False
        try:
            fsync_directory(path.parent)
        except OSError as commit_error:
            try:
                published = path.lstat()
                temporary = temp.lstat()
                target_is_published_leaf = (
                    (published.st_dev, published.st_ino)
                    == (temporary.st_dev, temporary.st_ino)
                    and path.read_bytes() == data
                    and stat.S_IMODE(published.st_mode) == 0o644
                )
            except OSError:
                target_is_published_leaf = False
            if target_is_published_leaf:
                try:
                    path.unlink()
                    fsync_directory(path.parent)
                except OSError as rollback_error:
                    raise OSError(
                        errno.EIO,
                        "publish commit indeterminate; rollback failed",
                        path,
                    ) from rollback_error
                raise commit_error
            raise OSError(
                errno.EBUSY,
                "publish commit indeterminate; observed target differs from "
                "planned leaf",
                path,
            ) from commit_error
        return True
    finally:
        temp.unlink(missing_ok=True)


def replace_bytes_atomic(path: Path, data: bytes) -> None:
    if not path.is_file() or path.is_symlink():
        raise FileNotFoundError(f"replace target must be a regular file: {path}")
    previous = path.read_bytes()
    previous_mode = stat.S_IMODE(path.stat().st_mode)
    descriptor, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temp = Path(temp_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fchmod(handle.fileno(), previous_mode)
            os.fsync(handle.fileno())
        os.replace(temp, path)
        try:
            fsync_directory(path.parent)
        except OSError as commit_error:
            try:
                target_is_replacement = (
                    path.is_file()
                    and not path.is_symlink()
                    and path.read_bytes() == data
                    and stat.S_IMODE(path.stat().st_mode) == previous_mode
                )
            except OSError:
                target_is_replacement = False
            if target_is_replacement:
                rollback_fd, rollback_name = tempfile.mkstemp(
                    prefix=f".{path.name}.rollback.", dir=path.parent
                )
                rollback = Path(rollback_name)
                try:
                    with os.fdopen(rollback_fd, "wb") as handle:
                        handle.write(previous)
                        handle.flush()
                        os.fchmod(handle.fileno(), previous_mode)
                        os.fsync(handle.fileno())
                    os.replace(rollback, path)
                    fsync_directory(path.parent)
                except OSError as rollback_error:
                    raise OSError(
                        errno.EIO,
                        "replace commit indeterminate; rollback failed",
                        path,
                    ) from rollback_error
                finally:
                    rollback.unlink(missing_ok=True)
                raise commit_error
            raise OSError(
                errno.EBUSY,
                "replace commit indeterminate; observed target differs from "
                "planned leaf",
                path,
            ) from commit_error
    finally:
        temp.unlink(missing_ok=True)


def fsync_directory(path: Path) -> None:
    descriptor = os.open(str(path), os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def fsync_file(path: Path) -> None:
    descriptor = os.open(str(path), os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def chmod_fsync(path: Path, mode: int) -> None:
    descriptor = os.open(str(path), os.O_RDONLY)
    try:
        os.fchmod(descriptor, mode)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _rename_path_no_replace_syscall(source: Path, target: Path) -> None:
    source_bytes = os.fsencode(source)
    target_bytes = os.fsencode(target)
    libc = ctypes.CDLL(None, use_errno=True)
    if sys.platform == "darwin":
        operation = libc.renamex_np
        operation.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
        result = operation(source_bytes, target_bytes, 0x00000004)
    elif sys.platform.startswith("linux"):
        try:
            operation = libc.renameat2
        except AttributeError as exc:
            raise OSError(
                errno.ENOTSUP, "atomic no-replace directory rename is unavailable"
            ) from exc
        operation.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint,
        ]
        result = operation(-100, source_bytes, -100, target_bytes, 1)
    elif sys.platform == "win32":
        os.rename(source, target)
        return
    else:
        raise OSError(
            errno.ENOTSUP, "atomic no-replace directory rename is unavailable"
        )
    if result != 0:
        error_number = ctypes.get_errno()
        raise OSError(error_number, os.strerror(error_number), target)


def rename_path_no_replace(source: Path, target: Path) -> None:
    source_state = source.lstat()
    source_bytes = source.read_bytes() if stat.S_ISREG(source_state.st_mode) else None
    source_mode = stat.S_IMODE(source_state.st_mode)
    _rename_path_no_replace_syscall(source, target)
    try:
        fsync_directory(source.parent)
        if source.parent.resolve() != target.parent.resolve():
            fsync_directory(target.parent)
    except OSError as commit_error:
        target_is_committed_source = False
        try:
            if (target.exists() or target.is_symlink()) and not source.exists():
                observed = target.lstat()
                target_is_committed_source = (
                    (observed.st_dev, observed.st_ino)
                    == (source_state.st_dev, source_state.st_ino)
                    and stat.S_IMODE(observed.st_mode) == source_mode
                    and (source_bytes is None or target.read_bytes() == source_bytes)
                )
        except OSError:
            target_is_committed_source = False
        if not target_is_committed_source:
            raise OSError(
                errno.EBUSY,
                "rename commit indeterminate; observed target differs from source",
                target,
            ) from commit_error
        try:
            _rename_path_no_replace_syscall(target, source)
            fsync_directory(source.parent)
            if source.parent.resolve() != target.parent.resolve():
                fsync_directory(target.parent)
        except OSError as rollback_error:
            raise OSError(
                errno.EIO,
                "rename commit indeterminate; rollback failed",
                target,
            ) from rollback_error
        raise commit_error


@contextmanager
def repository_write_lock(repo_root: Path) -> Iterator[None]:
    descriptor = os.open(str(repo_root), os.O_RDONLY)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield
    finally:
        os.close(descriptor)


def repository_locked(repo_argument_index: int):
    def decorate(function):
        @wraps(function)
        def locked(*args, **kwargs):
            repo_root = kwargs.get("repo_root")
            if repo_root is None:
                repo_root = args[repo_argument_index]
            with repository_write_lock(Path(repo_root)):
                return function(*args, **kwargs)

        return locked

    return decorate


def exchange_directories(left: Path, right: Path) -> None:
    if left.resolve().parent != right.resolve().parent:
        raise OSError(errno.EXDEV, "atomic directory exchange requires a common parent")
    left_bytes = os.fsencode(left)
    right_bytes = os.fsencode(right)
    libc = ctypes.CDLL(None, use_errno=True)
    if sys.platform == "darwin":
        operation = libc.renamex_np
        operation.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
        result = operation(left_bytes, right_bytes, 0x00000002)
    elif sys.platform.startswith("linux"):
        try:
            operation = libc.renameat2
        except AttributeError as exc:
            raise OSError(
                errno.ENOTSUP, "atomic directory exchange is unavailable"
            ) from exc
        operation.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint,
        ]
        result = operation(-100, left_bytes, -100, right_bytes, 2)
    else:
        raise OSError(errno.ENOTSUP, "atomic directory exchange is unavailable")
    if result != 0:
        error_number = ctypes.get_errno()
        raise OSError(error_number, os.strerror(error_number), right)
    fsync_directory(left.resolve().parent)
