#!/usr/bin/env python3
"""scripts/pipeline.py 오케스트레이터 테스트 (pytest 비의존 self-runner).

실행: .venv-lint/bin/python tests/test_pipeline.py
검증: 설정 로드 / 경로 회수 / 실패·미출력 거부 / extract→ingest 오케스트레이션 / wiki 게이트 정지.
subprocess(ytscript) 는 monkeypatch — 실 추출 없이 결정적.
"""
from __future__ import annotations

import io
import json
import sys
import tempfile
import types
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import pipeline  # noqa: E402


def _canonical_file(dir_: Path, name: str = "stt.medium.json") -> Path:
    data = {
        "schema_version": "1.0",
        "video": {"url": "https://youtu.be/X", "id": "VIDID00001", "title": "T",
                   "channel": "C", "upload_date": "2020-01-01", "duration_seconds": 10, "language": "ko"},
        "extraction": {"method": "stt", "language": "ko", "model": "medium",
                        "engine": "faster-whisper@1.2.1", "extracted_at": "2026-06-04T00:00:00+00:00"},
        "segments": [{"start": 0.0, "end": 1.0, "text": "본문"}],
        "full_text": "전체 본문",
    }
    p = dir_ / name
    p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return p


def _fake_proc(returncode: int, stdout: str = "", stderr: str = ""):
    return types.SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)


TESTS = []


def test(fn):
    TESTS.append(fn)
    return fn


@test
def test_load_config():
    with tempfile.TemporaryDirectory() as d:
        cfg = Path(d) / "pipeline.yaml"
        cfg.write_text("extractor:\n  source: stt\ningest:\n  force: true\n", encoding="utf-8")
        c = pipeline.load_config(cfg)
        assert c["extractor"]["source"] == "stt"
        assert c["ingest"]["force"] is True


@test
def test_flag_value():
    assert pipeline._flag_value(["ko", "en"]) == "ko,en"
    assert pipeline._flag_value("medium") == "medium"
    assert pipeline._flag_value(8) == "8"


@test
def test_run_extractor_captures_path(monkeypatch_target=None):
    """ytscript stdout 마지막 줄을 canonical 경로로 회수."""
    with tempfile.TemporaryDirectory() as d:
        proj = Path(d)
        jp = _canonical_file(proj, "c.json")
        real = pipeline.subprocess.run
        pipeline.subprocess.run = lambda *a, **k: _fake_proc(0, stdout=f"{jp}\n", stderr="skip\n")
        try:
            got = pipeline.run_extractor("URL", {"project": str(proj)})
            assert got == jp, got
        finally:
            pipeline.subprocess.run = real


@test
def test_run_extractor_failure():
    with tempfile.TemporaryDirectory() as d:
        real = pipeline.subprocess.run
        pipeline.subprocess.run = lambda *a, **k: _fake_proc(2, stdout="", stderr="[자막 없음]\n")
        try:
            raised = False
            try:
                pipeline.run_extractor("URL", {"project": d})
            except pipeline.PipelineError:
                raised = True
            assert raised
        finally:
            pipeline.subprocess.run = real


@test
def test_run_extractor_no_path():
    with tempfile.TemporaryDirectory() as d:
        real = pipeline.subprocess.run
        pipeline.subprocess.run = lambda *a, **k: _fake_proc(0, stdout="\n", stderr="")
        try:
            raised = False
            try:
                pipeline.run_extractor("URL", {"project": d})
            except pipeline.PipelineError:
                raised = True
            assert raised
        finally:
            pipeline.subprocess.run = real


@test
def test_orchestration_extract_then_ingest():
    """run() 가 추출 경로를 받아 ingest 까지 수행 (extract 는 monkeypatch)."""
    with tempfile.TemporaryDirectory() as d:
        src_dir = Path(d) / "src"
        src_dir.mkdir()
        jp = _canonical_file(src_dir)
        out = Path(d) / "out"
        real = pipeline.run_extractor
        pipeline.run_extractor = lambda url, ex: jp
        try:
            cfg = {"extractor": {}, "ingest": {"out": str(out)}, "wiki": {}}
            md, jsonp, skipped = pipeline.run("URL", cfg)
            assert md.exists() and md.name == "VIDID00001.md"
            assert jsonp.exists() and jsonp.name == "VIDID00001.json"
            assert skipped is False
            assert "전체 본문" in md.read_text(encoding="utf-8")  # verbatim
        finally:
            pipeline.run_extractor = real


@test
def test_wiki_gate_stops_with_message():
    """wiki.enabled=true 여도 자동 합성 안 함 — 게이트 안내만(stderr)."""
    with tempfile.TemporaryDirectory() as d:
        src_dir = Path(d) / "src"
        src_dir.mkdir()
        jp = _canonical_file(src_dir)
        out = Path(d) / "out"
        real_ex = pipeline.run_extractor
        pipeline.run_extractor = lambda url, ex: jp
        real_err = sys.stderr
        sys.stderr = io.StringIO()
        try:
            cfg = {"extractor": {}, "ingest": {"out": str(out)}, "wiki": {"enabled": True}}
            pipeline.run("URL", cfg)
            captured = sys.stderr.getvalue()
        finally:
            sys.stderr = real_err
            pipeline.run_extractor = real_ex
        assert "wiki stage" in captured and "사람 review 게이트" in captured


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
