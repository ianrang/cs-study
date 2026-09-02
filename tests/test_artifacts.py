#!/usr/bin/env python3
import hashlib
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from knowledge import artifacts, fs as knowledge_fs  # noqa: E402
from knowledge.check import artifact_replay_findings  # noqa: E402
from wiki_ingest import _utc_now  # noqa: E402

FIXTURE = ROOT / "tests" / "fixtures" / "contracts" / "canonical-transcript-v1.json"
NOW = "2026-08-21T00:00:00+00:00"


def _capture(source: Path, raw: Path, source_id: str = "fixture-video"):
    return artifacts.capture(
        source,
        source_type="video",
        source_id=source_id,
        primary_source="https://www.youtube.com/watch?v=fixture-video",
        media_type="application/json",
        created_at=NOW,
        raw_root=raw,
    )


def _tree(root: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_same_payload_is_byte_identical_no_op():
    with tempfile.TemporaryDirectory() as directory:
        raw = Path(directory) / "raw"
        first = _capture(FIXTURE, raw)
        before = _tree(raw)
        second = artifacts.capture(
            FIXTURE,
            source_type="video",
            source_id="fixture-video",
            primary_source="https://www.youtube.com/watch?v=fixture-video",
            media_type="application/json",
            created_at="2026-08-22T00:00:00+00:00",
            raw_root=raw,
        )
        assert first.created is True
        assert second.created is False
        assert first.manifest_path == second.manifest_path
        assert _tree(raw) == before
        assert (
            artifact_replay_findings(
                before,
                _tree(raw),
                second_created=second.created,
            )
            == []
        )


def test_replay_checker_rejects_byte_drift_or_created_revision():
    findings = artifact_replay_findings(
        {"manifest.json": b"before"},
        {"manifest.json": b"after"},
        second_created=True,
    )
    assert len(findings) == 1
    assert findings[0]["rule_id"] == "VR-KP-021"


def test_expected_digest_mismatch_writes_nothing():
    with tempfile.TemporaryDirectory() as directory:
        raw = Path(directory) / "raw"
        try:
            artifacts.capture(
                FIXTURE,
                source_type="video",
                source_id="fixture-video",
                primary_source="https://www.youtube.com/watch?v=fixture-video",
                media_type="application/json",
                created_at=NOW,
                raw_root=raw,
                expected_sha256="0" * 64,
            )
        except artifacts.ArtifactError as exc:
            assert "approved digest" in str(exc)
        else:
            raise AssertionError("unapproved artifact bytes were captured")
        assert not raw.exists()


def test_invalid_created_at_writes_nothing_and_corrupt_replay_is_rejected():
    with tempfile.TemporaryDirectory() as directory:
        raw = Path(directory) / "raw"
        try:
            artifacts.capture(
                FIXTURE,
                source_type="video",
                source_id="fixture-video",
                primary_source="https://www.youtube.com/watch?v=fixture-video",
                media_type="application/json",
                created_at="not-a-date",
                raw_root=raw,
            )
        except artifacts.ArtifactError as exc:
            assert "date-time" in str(exc)
        else:
            raise AssertionError("invalid created_at was captured")
        assert not raw.exists()

        result = _capture(FIXTURE, raw)
        manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
        manifest["created_at"] = "not-a-date"
        result.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        try:
            _capture(FIXTURE, raw)
        except artifacts.ArtifactError as exc:
            assert "date-time" in str(exc)
        else:
            raise AssertionError("invalid existing created_at was accepted")


def test_invalid_transcript_leap_second_writes_nothing():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        raw = root / "raw"
        transcript = json.loads(FIXTURE.read_text(encoding="utf-8"))
        transcript["extraction"]["extracted_at"] = "2026-01-01T12:34:60Z"
        source = root / "invalid.json"
        source.write_text(json.dumps(transcript), encoding="utf-8")
        try:
            artifacts.capture(
                source,
                source_type="video",
                source_id="fixture-video",
                primary_source="https://www.youtube.com/watch?v=fixture-video",
                media_type="application/json",
                created_at=NOW,
                raw_root=raw,
            )
        except artifacts.ArtifactError as exc:
            assert "date-time" in str(exc)
        else:
            raise AssertionError("invalid transcript leap second was captured")
        assert not raw.exists()


def test_default_activity_time_uses_canonical_utc_z():
    value = _utc_now()
    assert value.endswith("Z")
    assert "+00:00" not in value


def test_different_payload_creates_revision_without_mutating_old():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        raw = root / "raw"
        first = _capture(FIXTURE, raw)
        first_bytes = _tree(first.manifest_path.parent)
        changed = json.loads(FIXTURE.read_text(encoding="utf-8"))
        changed["full_text"] = "new revision"
        changed_path = root / "changed.json"
        changed_path.write_text(
            json.dumps(changed, ensure_ascii=False), encoding="utf-8"
        )
        second = _capture(changed_path, raw)
        assert first.manifest_path.parent != second.manifest_path.parent
        assert _tree(first.manifest_path.parent) == first_bytes
        assert len(list((raw / "sources" / "video" / "fixture-video").iterdir())) == 2


def test_clipping_capture_hashes_and_stores_privacy_normalized_bytes():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        raw = root / "raw"
        source = root / "source.md"
        source.write_text(
            "local source: /Users/alice/Downloads/evidence.pdf\n",
            encoding="utf-8",
        )
        expected = b"local source: <local-user-home>/Downloads/evidence.pdf\n"
        result = artifacts.capture(
            source,
            source_type="clipping",
            source_id="fixture-clipping",
            primary_source="wiki/fixture.md",
            media_type="text/markdown",
            created_at=NOW,
            raw_root=raw,
            expected_sha256=hashlib.sha256(expected).hexdigest(),
        )
        manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
        assert manifest["artifact_digest"] == (
            f"sha256:{hashlib.sha256(expected).hexdigest()}"
        )
        assert (result.manifest_path.parent / "payload.md").read_bytes() == expected
        assert "/Users/alice/" in source.read_text(encoding="utf-8")


def test_existing_corruption_is_rejected_without_repair():
    with tempfile.TemporaryDirectory() as directory:
        raw = Path(directory) / "raw"
        result = _capture(FIXTURE, raw)
        payload = result.manifest_path.parent / "payload.json"
        payload.write_text("corrupt", encoding="utf-8")
        try:
            _capture(FIXTURE, raw)
        except artifacts.ArtifactError as exc:
            assert "descriptor mismatch" in str(exc)
        else:
            raise AssertionError("corrupt bundle accepted")
        assert payload.read_text(encoding="utf-8") == "corrupt"


def test_payload_symlink_is_rejected_before_read():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        raw = root / "raw"
        result = _capture(FIXTURE, raw)
        payload = result.manifest_path.parent / "payload.json"
        external = root / "external.json"
        external.write_bytes(payload.read_bytes())
        payload.unlink()
        payload.symlink_to(external)

        try:
            artifacts.verify_manifest(result.manifest_path, raw_root=raw)
        except artifacts.ArtifactError as exc:
            assert "regular non-symlink" in str(exc)
        else:
            raise AssertionError("payload symlink accepted")


def test_manifest_symlink_is_rejected_before_read():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        raw = root / "raw"
        result = _capture(FIXTURE, raw)
        external = root / "external-manifest.json"
        result.manifest_path.replace(external)
        result.manifest_path.symlink_to(external)

        try:
            artifacts.verify_manifest(result.manifest_path, raw_root=raw)
        except artifacts.ArtifactError as exc:
            assert "regular non-symlink" in str(exc)
        else:
            raise AssertionError("manifest symlink accepted")


def test_bundle_ancestor_symlink_is_rejected_from_raw_root():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        raw = root / "raw"
        result = _capture(FIXTURE, raw)
        source_type = raw / "sources" / "video"
        external = root / "external-video"
        source_type.replace(external)
        source_type.symlink_to(external, target_is_directory=True)

        try:
            artifacts.verify_manifest(result.manifest_path, raw_root=raw)
        except artifacts.ArtifactError as exc:
            assert "regular non-symlink" in str(exc)
        else:
            raise AssertionError("bundle ancestor symlink accepted")


def test_bundle_swap_during_verification_is_rejected():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        raw = root / "raw"
        result = _capture(FIXTURE, raw)
        bundle = result.manifest_path.parent
        original = root / "original-bundle"
        external = root / "external-bundle"
        external.mkdir()
        for name in ("manifest.json", "payload.json", "content.md"):
            (external / name).write_bytes(f"ATTACK-{name}".encode())

        real_read = knowledge_fs.os.read
        nonempty_reads = 0

        def swap_after_bundle_reads(descriptor: int, size: int) -> bytes:
            nonlocal nonempty_reads
            data = real_read(descriptor, size)
            if data:
                nonempty_reads += 1
                if nonempty_reads == 3:
                    bundle.replace(original)
                    bundle.symlink_to(external, target_is_directory=True)
            return data

        knowledge_fs.os.read = swap_after_bundle_reads
        try:
            try:
                artifacts.verify_manifest(result.manifest_path, raw_root=raw)
            except artifacts.ArtifactError:
                pass
            else:
                raise AssertionError("bundle replacement was accepted")
        finally:
            knowledge_fs.os.read = real_read


def test_payload_traversal_is_rejected_by_manifest_schema_before_read():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        raw = root / "raw"
        result = _capture(FIXTURE, raw)
        manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
        manifest["payload"] = "../external.json"
        result.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        (result.manifest_path.parent.parent / "external.json").write_bytes(
            (result.manifest_path.parent / "payload.json").read_bytes()
        )

        try:
            artifacts.verify_manifest(result.manifest_path, raw_root=raw)
        except artifacts.ArtifactError as exc:
            assert "does not match" in str(exc)
        else:
            raise AssertionError("payload traversal accepted")


def test_directory_input_is_rejected():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        try:
            _capture(root, root / "raw")
        except artifacts.ArtifactError as exc:
            assert "one explicit file" in str(exc)
        else:
            raise AssertionError("directory input accepted")


def test_failure_before_commit_leaves_no_final_or_temp_bundle():
    with tempfile.TemporaryDirectory() as directory:
        raw = Path(directory) / "raw"
        real_write = artifacts.write_bytes_fsync
        calls = {"count": 0}

        def fail_second(path, data):
            calls["count"] += 1
            if calls["count"] == 2:
                raise OSError("injected write failure")
            real_write(path, data)

        artifacts.write_bytes_fsync = fail_second
        try:
            try:
                _capture(FIXTURE, raw)
            except OSError as exc:
                assert "injected" in str(exc)
            else:
                raise AssertionError("injected failure did not propagate")
        finally:
            artifacts.write_bytes_fsync = real_write
        source_root = raw / "sources" / "video" / "fixture-video"
        assert not source_root.exists() or list(source_root.iterdir()) == []


def test_source_capture_does_not_replace_competing_empty_directory():
    with tempfile.TemporaryDirectory() as directory:
        raw = Path(directory) / "raw"
        real_commit = artifacts.rename_path_no_replace

        def inject_competitor(source, target):
            Path(target).mkdir()
            return real_commit(source, target)

        artifacts.rename_path_no_replace = inject_competitor
        try:
            try:
                _capture(FIXTURE, raw)
            except artifacts.ArtifactError as exc:
                assert "corrupt artifact manifest" in str(exc)
            else:
                raise AssertionError("competing source directory was replaced")
        finally:
            artifacts.rename_path_no_replace = real_commit
        source_root = raw / "sources" / "video" / "fixture-video"
        final = next(
            path for path in source_root.iterdir() if not path.name.startswith(".")
        )
        assert list(final.iterdir()) == []


def test_asset_capture_does_not_replace_competing_empty_directory():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        raw = root / "raw"
        asset = root / "frame.jpg"
        asset.write_bytes(b"image")
        real_commit = artifacts.rename_path_no_replace

        def inject_competitor(source, target):
            Path(target).mkdir()
            return real_commit(source, target)

        artifacts.rename_path_no_replace = inject_competitor
        try:
            try:
                artifacts.capture_asset(
                    asset,
                    source_id="fixture-video",
                    media_type="image/jpeg",
                    created_at=NOW,
                    raw_root=raw,
                )
            except artifacts.ArtifactError as exc:
                assert "corrupt asset bundle" in str(exc)
            else:
                raise AssertionError("competing asset directory was replaced")
        finally:
            artifacts.rename_path_no_replace = real_commit
        source_root = raw / "assets" / "fixture-video"
        final = next(
            path for path in source_root.iterdir() if not path.name.startswith(".")
        )
        assert list(final.iterdir()) == []


def test_manifest_describes_exact_payload_and_normalized_content():
    with tempfile.TemporaryDirectory() as directory:
        result = _capture(FIXTURE, Path(directory) / "raw")
        manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
        payload = result.manifest_path.parent / manifest["payload"]
        content = result.manifest_path.parent / manifest["content"]["path"]
        assert (
            manifest["artifact_digest"]
            == f"sha256:{hashlib.sha256(payload.read_bytes()).hexdigest()}"
        )
        assert manifest["size"] == len(payload.read_bytes())
        assert (
            manifest["content"]["digest"]
            == f"sha256:{hashlib.sha256(content.read_bytes()).hexdigest()}"
        )


def test_transcript_source_identity_mismatch_is_rejected():
    with tempfile.TemporaryDirectory() as directory:
        try:
            _capture(FIXTURE, Path(directory) / "raw", source_id="other-video")
        except artifacts.ArtifactError as exc:
            assert "identity differs" in str(exc)
        else:
            raise AssertionError("identity mismatch accepted")


def test_non_video_json_with_schema_version_is_captured_as_generic_payload():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        source = root / "web.json"
        source.write_text(
            '{"schema_version":"external.v1","value":1}\n', encoding="utf-8"
        )
        result = artifacts.capture(
            source,
            source_type="web",
            source_id="fixture-web",
            primary_source="https://example.invalid/data.json",
            media_type="application/json",
            created_at=NOW,
            raw_root=root / "raw",
        )
        manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
        assert "content" not in manifest


def test_asset_same_bytes_no_op_and_changed_bytes_new_revision():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        raw = root / "raw"
        first_path = root / "frame.jpg"
        first_path.write_bytes(b"first-image")
        first = artifacts.capture_asset(
            first_path,
            source_id="fixture-video",
            media_type="image/jpeg",
            created_at=NOW,
            raw_root=raw,
        )
        repeated = artifacts.capture_asset(
            first_path,
            source_id="fixture-video",
            media_type="image/jpeg",
            created_at="2026-08-22T00:00:00+00:00",
            raw_root=raw,
        )
        first_tree = _tree(first.manifest_path.parent)
        second_path = root / "changed.jpg"
        second_path.write_bytes(b"second-image")
        changed = artifacts.capture_asset(
            second_path,
            source_id="fixture-video",
            media_type="image/jpeg",
            created_at=NOW,
            raw_root=raw,
        )
        assert (
            first.created is True
            and repeated.created is False
            and changed.created is True
        )
        assert first.manifest_path.parent != changed.manifest_path.parent
        assert _tree(first.manifest_path.parent) == first_tree


def test_existing_asset_payload_symlink_is_rejected_before_read():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        raw = root / "raw"
        source = root / "frame.jpg"
        source.write_bytes(b"image")
        result = artifacts.capture_asset(
            source,
            source_id="fixture-video",
            media_type="image/jpeg",
            created_at=NOW,
            raw_root=raw,
        )
        payload = result.manifest_path.parent / "asset.jpg"
        external = root / "external.jpg"
        external.write_bytes(payload.read_bytes())
        payload.unlink()
        payload.symlink_to(external)

        try:
            artifacts.capture_asset(
                source,
                source_id="fixture-video",
                media_type="image/jpeg",
                created_at=NOW,
                raw_root=raw,
            )
        except artifacts.ArtifactError as exc:
            assert "regular non-symlink" in str(exc)
        else:
            raise AssertionError("asset payload symlink accepted")


def test_asset_bundle_swap_during_verification_is_rejected():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        raw = root / "raw"
        source = root / "frame.jpg"
        source.write_bytes(b"image")
        result = artifacts.capture_asset(
            source,
            source_id="fixture-video",
            media_type="image/jpeg",
            created_at=NOW,
            raw_root=raw,
        )
        bundle = result.manifest_path.parent
        original = root / "original-asset-bundle"
        external = root / "external-asset-bundle"
        external.mkdir()
        for name in ("manifest.json", "asset.jpg"):
            (external / name).write_bytes(f"ATTACK-{name}".encode())

        real_read = knowledge_fs.os.read
        nonempty_reads = 0

        def swap_after_bundle_reads(descriptor: int, size: int) -> bytes:
            nonlocal nonempty_reads
            data = real_read(descriptor, size)
            if data:
                nonempty_reads += 1
                if nonempty_reads == 2:
                    bundle.replace(original)
                    bundle.symlink_to(external, target_is_directory=True)
            return data

        knowledge_fs.os.read = swap_after_bundle_reads
        try:
            try:
                artifacts.capture_asset(
                    source,
                    source_id="fixture-video",
                    media_type="image/jpeg",
                    created_at=NOW,
                    raw_root=raw,
                )
            except artifacts.ArtifactError:
                pass
            else:
                raise AssertionError("asset bundle replacement was accepted")
        finally:
            knowledge_fs.os.read = real_read


def main() -> int:
    tests = [
        value for name, value in sorted(globals().items()) if name.startswith("test_")
    ]
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
