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
VERIFIED_VIDEO_CLAIM_TABLE = CLAIM_TABLE.replace(
    "| claimed | raw/sources/video/x.md |",
    "| verified | raw/sources/video/x.md |",
)


def _wiki_frontmatter(**overrides):
    fm = {
        "title": "Test",
        "tier": "llm-synthesis",
        "page_type": "concept",
        "domain": "information-security",
        "domain_confidence": "high",
        "shared_scope": "domain",
        "tags": [],
        "status": "active",
        "date_created": "2026-07-12",
        "date_updated": "2026-07-12",
        "source_paths": ["AGENTS.md"],
        "source_count": 1,
        "provenance": "extracted",
        "summary": "test",
        "evergreen": False,
    }
    fm.update(overrides)
    return fm

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


@test
def test_system_pages_still_reject_broken_links():
    findings = lint.check_axis_5_integrity_broken_links(
        REPO_ROOT / "wiki" / "overview.md",
        "[[wiki/domains/does-not-exist/overview]]",
    )
    assert any("broken link" in finding.message for finding in findings)


@test
def test_wikilink_resolver_tries_repo_root_before_local_path():
    findings = lint.check_axis_5_integrity_broken_links(WIKI_SOURCE_PATH, "[[AGENTS.md]]")
    assert findings == []


@test
def test_wikilink_resolver_strips_heading_suffix():
    findings = lint.check_axis_5_integrity_broken_links(WIKI_SOURCE_PATH, "[[AGENTS.md#Mission]]")
    assert findings == []


@test
def test_directory_link_requires_overview_or_index():
    findings = lint.check_axis_5_integrity_broken_links(
        WIKI_SOURCE_PATH,
        "[[wiki/domains/information-security]]",
    )
    assert any("broken link" in finding.message for finding in findings)


@test
def test_claim_table_requires_derived_frontmatter_fields():
    findings = lint.check_claim_table(WIKI_SOURCE_PATH, CLAIM_TABLE, {})
    messages = [finding.message for finding in findings]
    assert any("verification_status 누락" in message for message in messages)
    assert any("claim_status_counts 누락" in message for message in messages)


@test
def test_video_only_evidence_cannot_be_verified():
    fm = {
        "verification_status": "verified",
        "claim_status_counts": {
            "claimed": 0,
            "corroborated": 0,
            "verified": 1,
            "rejected": 0,
        },
    }
    findings = lint.check_claim_table(WIKI_SOURCE_PATH, VERIFIED_VIDEO_CLAIM_TABLE, fm)
    assert any("영상 단독 evidence" in finding.message for finding in findings)


@test
def test_unreviewed_external_url_cannot_be_verified():
    table = VERIFIED_VIDEO_CLAIM_TABLE.replace(
        "raw/sources/video/x.md",
        "https://www.youtube.com/watch?v=x",
    )
    fm = {
        "verification_status": "verified",
        "claim_status_counts": {"claimed": 0, "corroborated": 0, "verified": 1, "rejected": 0},
    }
    findings = lint.check_claim_table(WIKI_SOURCE_PATH, table, fm)
    assert any("verified evidence 부재 또는 허용 경로 이탈" in finding.message for finding in findings)


@test
def test_curated_raw_source_can_support_verified_claim():
    table = VERIFIED_VIDEO_CLAIM_TABLE.replace(
        "raw/sources/video/x.md",
        "raw/sources/web/information-security-exam-references/kisa-ismsp-criteria-guide-2023-11.md",
    )
    fm = {
        "verification_status": "verified",
        "claim_status_counts": {"claimed": 0, "corroborated": 0, "verified": 1, "rejected": 0},
    }
    assert lint.check_claim_table(WIKI_SOURCE_PATH, table, fm) == []


@test
def test_verified_evidence_must_exist_without_path_traversal():
    fm = {
        "verification_status": "verified",
        "claim_status_counts": {"claimed": 0, "corroborated": 0, "verified": 1, "rejected": 0},
    }
    for evidence in (
        "raw/sources/web/does-not-exist.md",
        "raw/sources/web/../../video/x.md",
    ):
        table = VERIFIED_VIDEO_CLAIM_TABLE.replace("raw/sources/video/x.md", evidence)
        findings = lint.check_claim_table(WIKI_SOURCE_PATH, table, fm)
        assert any("verified evidence 부재 또는 허용 경로 이탈" in finding.message for finding in findings)


@test
def test_wiki_frontmatter_types_and_enums_are_validated():
    fm = _wiki_frontmatter(
        tier="raw",
        page_type="study-guide",
        domain_confidence="certain",
        shared_scope="local",
        tags="security",
        status="done",
        source_paths="AGENTS.md",
        source_count="1",
        provenance="generated",
        evergreen="false",
        title=[],
        summary={},
        date_created="not-a-date",
        date_updated=42,
    )
    findings = lint.check_wiki_required_fields(WIKI_SOURCE_PATH, fm)
    assert len(findings) >= 14


@test
def test_draft_status_is_valid_for_domain_drafts():
    findings = lint.check_wiki_required_fields(WIKI_SOURCE_PATH, _wiki_frontmatter(status="draft"))
    assert findings == []




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
