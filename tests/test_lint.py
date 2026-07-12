#!/usr/bin/env python3
"""wiki lint claim table 회귀 테스트 (pytest 비의존 self-runner)."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LINT_PATH = REPO_ROOT / "scripts" / "lint.py"


def _load_lint_module():
    spec = importlib.util.spec_from_file_location("wiki_lint", LINT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load lint module: {LINT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lint = _load_lint_module()
WIKI_SOURCE_PATH = REPO_ROOT / "wiki" / "domains" / "test" / "sources" / "video.md"
CLAIM_TABLE = """## Claims

| id | primary | claim | status | evidence | notes |
|---|---|---|---|---|---|
| C1 | true | 영상은 X라고 주장한다. | claimed | raw/sources/video/x.md | 검증 필요 |
"""

TESTS = []


def test(fn):
    TESTS.append(fn)
    return fn


@test
def test_claim_status_counts_non_mapping_returns_finding():
    """잘못된 count 타입은 예외가 아니라 HIGH finding이어야 한다."""
    fm = {
        "verification_status": "claimed",
        "claim_status_counts": "invalid",
    }
    findings = lint.check_claim_table(WIKI_SOURCE_PATH, CLAIM_TABLE, fm)
    assert any("claim_status_counts 형식 오류" in finding.message for finding in findings)


@test
def test_claim_status_counts_requires_exact_status_keys():
    fm = {
        "verification_status": "claimed",
        "claim_status_counts": {"claimed": 1},
    }
    findings = lint.check_claim_table(WIKI_SOURCE_PATH, CLAIM_TABLE, fm)
    assert any("claim_status_counts key 오류" in finding.message for finding in findings)


@test
def test_claim_status_counts_requires_non_negative_integers():
    fm = {
        "verification_status": "claimed",
        "claim_status_counts": {
            "claimed": 1,
            "corroborated": 0,
            "verified": 0,
            "rejected": -1,
        },
    }
    findings = lint.check_claim_table(WIKI_SOURCE_PATH, CLAIM_TABLE, fm)
    assert any("claim_status_counts 값 오류" in finding.message for finding in findings)


@test
def test_claim_status_counts_must_match_claim_table():
    fm = {
        "verification_status": "claimed",
        "claim_status_counts": {
            "claimed": 0,
            "corroborated": 1,
            "verified": 0,
            "rejected": 0,
        },
    }
    findings = lint.check_claim_table(WIKI_SOURCE_PATH, CLAIM_TABLE, fm)
    assert any("claim_status_counts 불일치" in finding.message for finding in findings)


@test
def test_valid_claim_rollup_has_no_findings():
    fm = {
        "verification_status": "claimed",
        "claim_status_counts": {
            "claimed": 1,
            "corroborated": 0,
            "verified": 0,
            "rejected": 0,
        },
    }
    assert lint.check_claim_table(WIKI_SOURCE_PATH, CLAIM_TABLE, fm) == []


@test
def test_no_primary_claims_roll_up_to_claimed():
    rows = [
        {
            "id": "C1",
            "primary": "false",
            "claim": "보조 주장",
            "status": "verified",
            "evidence": "https://example.com/evidence",
            "notes": "",
        }
    ]
    rollup, counts = lint.calculate_claim_rollup(rows)
    assert rollup == "claimed"
    assert counts == {"claimed": 0, "corroborated": 0, "verified": 1, "rejected": 0}


def main() -> int:
    passed = 0
    failed = 0
    for fn in TESTS:
        try:
            fn()
            print(f"PASS {fn.__name__}")
            passed += 1
        except Exception as exc:
            print(f"FAIL {fn.__name__}: {exc}")
            failed += 1
    print(f"\n--- {passed} passed, {failed} failed / {len(TESTS)} ---")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
