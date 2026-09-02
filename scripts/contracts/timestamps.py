from __future__ import annotations

import datetime as dt
import re

CANONICAL_DATETIME_RE = re.compile(
    r"^(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})T"
    r"(?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}):(?P<second>[0-9]{2})"
    r"(?:\.[0-9]+)?(?:Z|[+-](?P<offset_hour>[0-9]{2}):(?P<offset_minute>[0-9]{2}))$"
)
CONTRACT_DATETIME_RE = re.compile(
    r"^(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})[Tt]"
    r"(?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}):(?P<second>[0-9]{2})"
    r"(?:\.[0-9]+)?(?:[Zz]|[+-](?P<offset_hour>[0-9]{2}):(?P<offset_minute>[0-9]{2}))$"
)


def is_canonical_datetime(value: object) -> bool:
    match = CANONICAL_DATETIME_RE.fullmatch(value) if isinstance(value, str) else None
    if match is None:
        return False
    return _valid_datetime_fields(match)


def _valid_datetime_fields(match: re.Match[str]) -> bool:
    try:
        dt.date(
            int(match["year"]),
            int(match["month"]),
            int(match["day"]),
        )
    except ValueError:
        return False
    if (
        int(match["hour"]) > 23
        or int(match["minute"]) > 59
        or int(match["second"]) > 59
    ):
        return False
    if match["offset_hour"] is None:
        return True
    return int(match["offset_hour"]) <= 23 and int(match["offset_minute"]) <= 59


def is_contract_datetime(value: object) -> bool:
    match = CONTRACT_DATETIME_RE.fullmatch(value) if isinstance(value, str) else None
    if match is None:
        return False
    return _valid_datetime_fields(match)
