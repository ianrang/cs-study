#!/usr/bin/env python3
"""SemanticWritePlan JSON Schema tests (pytest 비의존 self-runner).

실행: .venv-lint/bin/python tests/test_wiki_ingest_schema.py
검증: valid semantic input / forbidden write fields / empty claims reject.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "_meta" / "wiki-ingest-write-plan.schema.json"


def _schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _validator() -> Draft202012Validator:
    schema = _schema()
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _valid_plan(**overrides) -> dict:
    plan = {
        "schema_version": "wiki-ingest-plan.v1",
        "raw_path": "raw/sources/video/ABC123abc-_.md",
        "video_id": "ABC123abc-_",
        "domain_decision": {
            "domain": "developer-tools",
            "confidence": "high",
            "rationale": "영상 주제가 CLI 기반 개발 도구 사용법이다.",
            "source": "write_plan",
        },
        "source_summary": {
            "title": "영상 제목 기반 source summary",
            "summary": "영상은 개발 도구 사용 흐름을 설명한다.",
            "main_claims": ["영상은 X라고 주장한다."],
        },
        "claims": [
            {
                "id": "C1",
                "primary": True,
                "claim": "영상은 X라고 주장한다.",
                "status": "claimed",
                "evidence": "raw/sources/video/ABC123abc-_.md",
                "notes": "추가 검증 필요",
            }
        ],
        "candidates": [
            {
                "kind": "concept",
                "slug": "model-context-protocol",
                "label": "Model Context Protocol",
                "status": "existing",
                "matched_path": "wiki/domains/developer-tools/concepts/model-context-protocol.md",
                "reason": "기존 wiki page 와 slug 일치",
            }
        ],
    }
    for key, value in overrides.items():
        if key in plan and isinstance(plan[key], dict) and isinstance(value, dict):
            plan[key] = {**plan[key], **value}
        else:
            plan[key] = value
    return plan


TESTS = []


def _register(fn):
    TESTS.append(fn)
    return fn


@_register
def test_valid_semantic_write_plan():
    """B안: semantic fields 만 포함한 plan 은 schema valid."""
    _validator().validate(_valid_plan())


@_register
def test_rejects_file_write_fields():
    """LLM/사람 입력에 writes 같은 파일 write 계획이 들어오면 reject."""
    plan = _valid_plan(writes=[{"path": "wiki/index.md", "content": "bad"}])
    errors = list(_validator().iter_errors(plan))
    assert errors, "expected additionalProperties violation"
    assert any(error.validator == "additionalProperties" for error in errors)


@_register
def test_rejects_empty_claims():
    """wiki source summary 는 claim table 원천 claim 을 최소 1개 가져야 한다."""
    plan = _valid_plan(claims=[])
    errors = list(_validator().iter_errors(plan))
    assert errors, "expected minItems violation"
    assert any(list(error.path) == ["claims"] and error.validator == "minItems" for error in errors)


@_register
def test_rejects_derived_frontmatter_fields():
    """derived roll-up/frontmatter 는 validator 가 재계산하므로 plan 에 넣을 수 없다."""
    plan = _valid_plan(verification_status="claimed", claim_status_counts={"claimed": 1})
    errors = list(_validator().iter_errors(plan))
    assert errors, "expected additionalProperties violation"
    assert any(error.validator == "additionalProperties" for error in errors)


@_register
def test_rejects_redundant_new_candidate_status():
    """신규 후보는 review-needed로 단일화하고 별도 new 상태를 허용하지 않는다."""
    plan = _valid_plan()
    plan["candidates"][0]["status"] = "new"
    errors = list(_validator().iter_errors(plan))
    assert errors, "expected candidate status enum violation"
    assert any(error.validator == "enum" for error in errors)


@_register
def test_rejects_non_mvp_candidate_kind():
    """MVP 후보는 concept/entity로 제한하고 다른 page type은 허용하지 않는다."""
    plan = _valid_plan()
    plan["candidates"][0]["kind"] = "method"
    errors = list(_validator().iter_errors(plan))
    assert errors, "expected candidate kind enum violation"
    assert any(error.validator == "enum" for error in errors)


@_register
def test_requires_candidate_matched_path_key():
    """matched_path는 nullable이지만 key 자체는 항상 존재해야 한다."""
    plan = _valid_plan()
    del plan["candidates"][0]["matched_path"]
    errors = list(_validator().iter_errors(plan))
    assert errors, "expected candidate required-key violation"
    assert any(error.validator == "required" for error in errors)


@_register
def test_requires_claim_notes_key_but_allows_empty_value():
    plan = _valid_plan()
    plan["claims"][0]["notes"] = ""
    _validator().validate(plan)
    del plan["claims"][0]["notes"]
    errors = list(_validator().iter_errors(plan))
    assert errors, "expected claim notes required-key violation"
    assert any(error.validator == "required" for error in errors)


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
