from __future__ import annotations

import re

LOCAL_USER_HOME = "<local-user-home>"
APPLE_USER_HOME_RE = re.compile(r"/Users/[^/\\<>{}\r\n]+/")
WINDOWS_USER_HOME_RE = re.compile(
    r"[A-Za-z]:\\Users\\[^/\\<>{}\r\n]+\\", re.IGNORECASE
)


def normalize_local_user_paths(data: bytes) -> bytes:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("privacy normalization requires UTF-8 text") from exc
    normalized = APPLE_USER_HOME_RE.sub(f"{LOCAL_USER_HOME}/", text)
    normalized = WINDOWS_USER_HOME_RE.sub(f"{LOCAL_USER_HOME}\\\\", normalized)
    return normalized.encode("utf-8")
