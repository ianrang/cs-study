#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from knowledge.schema import contract_format_checker  # noqa: E402

CONTRACTS = ROOT / "_meta" / "contracts"
SCHEMA_PATH = CONTRACTS / "canonical-transcript-v1.schema.json"
PIN_PATH = CONTRACTS / "canonical-transcript-v1.pin.json"
FIXTURE_PATH = (
    ROOT / "tests" / "fixtures" / "contracts" / "canonical-transcript-v1.json"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_vendored_contract_pin_and_fixture():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    pin = json.loads(PIN_PATH.read_text(encoding="utf-8"))
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(
        schema, format_checker=contract_format_checker()
    )
    validator.validate(fixture)
    invalid = json.loads(json.dumps(fixture))
    invalid["extraction"]["extracted_at"] = "not-a-date"
    assert list(validator.iter_errors(invalid))
    lowercase = json.loads(json.dumps(fixture))
    lowercase["extraction"]["extracted_at"] = "2026-08-24t00:00:00z"
    assert list(validator.iter_errors(lowercase)) == []
    for value in ("2026-01-01T12:34:60Z", "2016-12-31T23:59:60Z"):
        leap_second = json.loads(json.dumps(fixture))
        leap_second["extraction"]["extracted_at"] = value
        assert list(validator.iter_errors(leap_second))
    assert schema["$id"] == pin["contract_id"]
    assert fixture["schema_version"] == pin["schema_version"]
    assert _sha256(SCHEMA_PATH) == pin["schema_sha256"]
    assert _sha256(FIXTURE_PATH) == pin["fixture_sha256"]


def main() -> int:
    tests = [test_vendored_contract_pin_and_fixture]
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
