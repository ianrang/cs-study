#!/usr/bin/env python3
"""scripts/ingest.py 단위·엣지 테스트 (pytest 비의존 self-runner).

실행: .venv-lint/bin/python tests/test_ingest.py
검증: best-variant 선택 / 필드 매핑 / null 처리 / verbatim / 멱등·force / atomic 롤백 / 거부 경로.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import ingest  # noqa: E402


def _canonical(**over) -> dict:
    """최소 유효 canonical dict. over 로 부분 override."""
    data = {
        "schema_version": "1.0",
        "video": {
            "url": "https://www.youtube.com/watch?v=ABC123abc-_",
            "id": "ABC123abc-_",
            "title": "제목 T",
            "channel": "채널 C",
            "upload_date": "2019-07-04",
            "duration_seconds": 3999,
            "language": "ko",
        },
        "extraction": {
            "method": "stt",
            "language": "ko",
            "model": "medium",
            "engine": "faster-whisper@1.2.1",
            "extracted_at": "2026-06-04T03:52:29+00:00",
        },
        "segments": [{"start": 0.08, "end": 28.59, "text": "첫 세그먼트 GPT-5 언급"}],
        "full_text": "전체 스크립트 본문 GPT-5 라는 모델명을 포함",
    }
    for k, v in over.items():
        if k in ("video", "extraction") and isinstance(v, dict):
            data[k] = {**data[k], **v}
        else:
            data[k] = v
    return data


def _write(dir_: Path, name: str, data: dict) -> Path:
    p = dir_ / name
    p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return p


# --------------------------------------------------------------------------- #
TESTS = []


def test(fn):
    TESTS.append(fn)
    return fn


@test
def test_select_best_priority():
    """manual > auto_sub > stt (BR-SEL-3)."""
    loaded = [
        (Path("a"), _canonical(extraction={"method": "stt"})),
        (Path("b"), _canonical(extraction={"method": "manual"})),
        (Path("c"), _canonical(extraction={"method": "auto_sub"})),
    ]
    _, data = ingest.select_best(loaded)
    assert data["extraction"]["method"] == "manual", data["extraction"]["method"]


@test
def test_select_best_tiebreak_latest():
    """동률 method 는 extracted_at 최신 (BR-SEL-4)."""
    loaded = [
        (Path("old"), _canonical(extraction={"method": "stt", "extracted_at": "2026-01-01T00:00:00+00:00", "model": "old"})),
        (Path("new"), _canonical(extraction={"method": "stt", "extracted_at": "2026-06-04T00:00:00+00:00", "model": "new"})),
    ]
    _, data = ingest.select_best(loaded)
    assert data["extraction"]["model"] == "new", data["extraction"]["model"]


@test
def test_field_mapping():
    """canonical → raw frontmatter 매핑 (P-MAP-*)."""
    fm = ingest.build_frontmatter(_canonical(), "2026-06-10")
    assert fm["source_type"] == "video"
    assert fm["tier"] == "raw"
    assert fm["source_date"] == "2019-07-04"          # upload_date
    assert fm["last_verified"] == "2026-06-04"          # extracted_at 날짜부
    assert fm["ingested_date"] == "2026-06-10"
    assert fm["stt_model"] == "medium" and fm["stt_engine"] == "faster-whisper@1.2.1"
    # 키 순서 고정 (결정성)
    assert list(fm)[:7] == ["title", "source_url", "source_date", "source_type", "last_verified", "ingested_date", "tier"]


@test
def test_null_title_fallback():
    """title null → video.id (P-MAP-1)."""
    fm = ingest.build_frontmatter(_canonical(video={"title": None}), "2026-06-10")
    assert fm["title"] == "ABC123abc-_", fm["title"]


@test
def test_non_stt_omits_stt_fields():
    """method!=stt 면 stt_model/stt_engine 생략 (P-MAP-9)."""
    fm = ingest.build_frontmatter(_canonical(extraction={"method": "manual"}), "2026-06-10")
    assert "stt_model" not in fm and "stt_engine" not in fm


@test
def test_verbatim_body():
    """full_text + segment text 가 무수정으로 본문에 포함 (BR-BODY-1)."""
    data = _canonical()
    body = ingest.build_body(data)
    assert data["full_text"] in body
    assert data["segments"][0]["text"] in body
    assert "`00:00:00`" in body  # hms 타임스탬프


@test
def test_idempotent_and_force():
    """대상 존재 시 skip, --force 에 재생성 (BR-IDEM-1/2)."""
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "out"
        src = _write(Path(d), "stt.medium.json", _canonical())
        _, _, skipped1 = ingest.ingest(src, out_dir=out, now="2026-06-04")
        assert skipped1 is False
        _, _, skipped2 = ingest.ingest(src, out_dir=out, now="2026-06-04")
        assert skipped2 is True
        _, _, skipped3 = ingest.ingest(src, out_dir=out, now="2026-06-04", force=True)
        assert skipped3 is False


@test
def test_atomic_rollback():
    """둘째(.json) 쓰기 실패 시 .md 롤백 — 부분 산출물 0 (BR-TXN-1)."""
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "out"
        real_replace = ingest.os.replace
        calls = {"n": 0}

        def flaky_replace(a, b):
            calls["n"] += 1
            if calls["n"] == 2:  # json rename
                raise OSError("simulated json write failure")
            return real_replace(a, b)

        ingest.os.replace = flaky_replace
        try:
            raised = False
            try:
                ingest.atomic_commit(out, "VID", "page", _canonical(), force=False)
            except OSError:
                raised = True
            assert raised, "예외가 전파되어야 함"
            assert not (out / "VID.md").exists(), ".md 가 롤백돼야 함"
            assert not (out / "VID.json").exists()
        finally:
            ingest.os.replace = real_replace


@test
def test_invalid_schema_rejected():
    """schema_version 불일치 → IngestError (VR-2)."""
    with tempfile.TemporaryDirectory() as d:
        src = _write(Path(d), "bad.json", _canonical(schema_version="2.0"))
        raised = False
        try:
            ingest.load_canonical(src)
        except ingest.IngestError:
            raised = True
        assert raised


@test
def test_missing_video_id_rejected():
    """video.id 부재 → IngestError (VR-3)."""
    with tempfile.TemporaryDirectory() as d:
        src = _write(Path(d), "noid.json", _canonical(video={"id": ""}))
        raised = False
        try:
            ingest.load_canonical(src)
        except ingest.IngestError:
            raised = True
        assert raised


@test
def test_no_candidates_rejected():
    """디렉토리에 canonical 0건 → IngestError (BR-SEL-5)."""
    with tempfile.TemporaryDirectory() as d:
        empty = Path(d) / "empty"
        empty.mkdir()
        raised = False
        try:
            ingest.resolve_input(empty)
        except ingest.IngestError:
            raised = True
        assert raised


@test
def test_missing_path_rejected():
    """입력 경로 부재 → IngestError (VR-1)."""
    raised = False
    try:
        ingest.resolve_input(Path("/nonexistent/path/xyz"))
    except ingest.IngestError:
        raised = True
    assert raised


def main() -> int:
    passed = failed = 0
    for fn in TESTS:
        try:
            fn()
            passed += 1
            print(f"PASS {fn.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {fn.__name__}: {e}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"ERROR {fn.__name__}: {type(e).__name__}: {e}")
    print(f"\n--- {passed} passed, {failed} failed / {len(TESTS)} ---")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
