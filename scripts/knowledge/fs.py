from __future__ import annotations

import ctypes
import errno
import fcntl
import os
import stat
import sys
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from functools import wraps
from pathlib import Path


class PathSafetyError(ValueError):
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
