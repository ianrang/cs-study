#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from contracts.privacy import normalize_local_user_paths  # noqa: E402


def test_normalize_local_user_paths_is_deterministic_and_idempotent():
    source = (
        b"/Users/alice/Downloads/a.pdf\n"
        b"/home/bob/study/b.pdf\n"
        b"C:\\Users\\carol\\Desktop\\c.pdf\n"
        b"D:\\Users\\Carol Smith\\Documents\\d.pdf\n"
    )
    expected = (
        b"<local-user-home>/Downloads/a.pdf\n"
        b"/home/bob/study/b.pdf\n"
        b"<local-user-home>\\Desktop\\c.pdf\n"
        b"<local-user-home>\\Documents\\d.pdf\n"
    )
    normalized = normalize_local_user_paths(source)
    assert normalized == expected
    assert normalize_local_user_paths(normalized) == normalized


def test_normalize_local_user_paths_preserves_non_personal_absolute_paths():
    source = (
        b"/home/service/output.txt\n"
        b"/tmp/output.txt\n/var/log/system.log\nC:\\ProgramData\\x.log\n"
    )
    assert normalize_local_user_paths(source) == source


def test_normalize_local_user_paths_rejects_non_utf8_payload():
    try:
        normalize_local_user_paths(b"\xff")
    except ValueError as exc:
        assert "UTF-8" in str(exc)
    else:
        raise AssertionError("non-UTF-8 text payload was accepted")
