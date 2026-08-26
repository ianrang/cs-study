from __future__ import annotations

import ctypes
import errno
import os
import sys
import tempfile
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
            os.fsync(handle.fileno())
        try:
            os.link(temp, path)
        except FileExistsError:
            if not path.is_file() or path.read_bytes() != data:
                raise FileExistsError(f"existing output differs: {path}") from None
            return False
        fsync_directory(path.parent)
        return True
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


def rename_directory_no_replace(source: Path, target: Path) -> None:
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
