from __future__ import annotations

import hashlib
import json
import re
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

from contracts.privacy import normalize_local_user_paths
from jsonschema import Draft202012Validator

from .fs import (
    confined,
    fsync_directory,
    rename_directory_no_replace,
    write_bytes_fsync,
)
from .schema import (
    REPO_ROOT,
    KnowledgeSchemaError,
    contract_format_checker,
    load_schema,
    validate_instance,
    validator_for,
)

CONTRACT_PATH = (
    REPO_ROOT / "_meta" / "contracts" / "canonical-transcript-v1.schema.json"
)
DEFAULT_RAW_ROOT = REPO_ROOT / "raw"
GENERATOR_NAME = "cs-study-capture"
GENERATOR_VERSION = "1.0"
SAFE_COMPONENT_RE = re.compile(r"^[^/\\]+$")
SAFE_SUFFIX_RE = re.compile(r"^\.[A-Za-z0-9]+$")


class ArtifactError(ValueError):
    pass


@dataclass(frozen=True)
class CaptureResult:
    manifest_path: Path
    created: bool


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _descriptor(path: str, data: bytes, media_type: str) -> dict:
    return {
        "digest": f"sha256:{_digest(data)}",
        "size": len(data),
        "media_type": media_type,
        "path": path,
    }


def _validate_component(label: str, value: str) -> None:
    if value in {"", ".", ".."} or not SAFE_COMPONENT_RE.fullmatch(value):
        raise ArtifactError(f"unsafe {label}: {value!r}")


def _source_types() -> set[str]:
    schema = load_schema()
    values = schema["$defs"]["ArtifactManifest"]["properties"]["source_type"]["enum"]
    return set(values)


def _canonical_transcript(
    data: bytes, *, source_type: str, media_type: str
) -> dict | None:
    if source_type != "video" or media_type != "application/json":
        return None
    try:
        candidate = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(candidate, dict) or "schema_version" not in candidate:
        return None
    schema = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    errors = list(
        Draft202012Validator(
            schema, format_checker=contract_format_checker()
        ).iter_errors(candidate)
    )
    if errors:
        details = "; ".join(error.message for error in errors)
        raise ArtifactError(f"unsupported or invalid canonical transcript: {details}")
    return candidate


def _hms(seconds: float) -> str:
    total = int(seconds)
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def _render_content(transcript: dict) -> bytes:
    video = transcript["video"]
    lines = [
        f"# {video.get('title') or video['id']}",
        "",
        "## Transcript",
        "",
        transcript["full_text"],
        "",
        "## Segments",
        "",
    ]
    lines.extend(
        f"- `{_hms(segment['start'])}` {segment['text']}"
        for segment in transcript["segments"]
    )
    return ("\n".join(lines) + "\n").encode("utf-8")


def _manifest_bytes(manifest: dict) -> bytes:
    return (
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def _verify_bundle(bundle: Path, expected: dict | None = None) -> dict:
    manifest_path = bundle / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        validate_instance(manifest, validator_for("ArtifactManifest"))
    except (OSError, json.JSONDecodeError, KnowledgeSchemaError) as exc:
        raise ArtifactError(
            f"corrupt artifact manifest: {manifest_path}: {exc}"
        ) from exc
    if expected is not None:
        comparable_manifest = {
            key: value for key, value in manifest.items() if key != "created_at"
        }
        comparable_expected = {
            key: value for key, value in expected.items() if key != "created_at"
        }
        if comparable_manifest != comparable_expected:
            raise ArtifactError(f"existing artifact manifest differs: {manifest_path}")

    descriptors = [
        {
            "digest": manifest["artifact_digest"],
            "size": manifest["size"],
            "path": manifest["payload"],
        }
    ]
    if "content" in manifest:
        descriptors.append(manifest["content"])
    descriptors.extend(manifest.get("assets", []))
    expected_names = {"manifest.json"}
    for descriptor in descriptors:
        item = confined(bundle, bundle / descriptor["path"])
        data = item.read_bytes()
        if descriptor["digest"] != f"sha256:{_digest(data)}" or descriptor[
            "size"
        ] != len(data):
            raise ArtifactError(f"artifact descriptor mismatch: {item}")
        expected_names.add(descriptor["path"])
    actual_names = {path.name for path in bundle.iterdir()}
    if actual_names != expected_names:
        raise ArtifactError(
            "artifact bundle file set mismatch: "
            f"expected={sorted(expected_names)} actual={sorted(actual_names)}"
        )
    return manifest


def verify_manifest(manifest_path: Path) -> dict:
    if manifest_path.name != "manifest.json":
        raise ArtifactError(f"artifact manifest filename is invalid: {manifest_path}")
    return _verify_bundle(manifest_path.parent)


def capture(
    artifact: Path,
    *,
    source_type: str,
    source_id: str,
    primary_source: str,
    media_type: str,
    created_at: str,
    raw_root: Path = DEFAULT_RAW_ROOT,
    expected_sha256: str | None = None,
) -> CaptureResult:
    if not artifact.is_file():
        raise ArtifactError(f"capture requires one explicit file: {artifact}")
    _validate_component("source_type", source_type)
    _validate_component("source_id", source_id)
    if source_type not in _source_types():
        raise ArtifactError(f"unsupported source_type: {source_type}")
    if not primary_source or not media_type:
        raise ArtifactError("primary_source and media_type must be non-empty")

    payload_bytes = artifact.read_bytes()
    if source_type == "clipping" and media_type == "text/markdown":
        try:
            payload_bytes = normalize_local_user_paths(payload_bytes)
        except ValueError as exc:
            raise ArtifactError(str(exc)) from exc
    digest = _digest(payload_bytes)
    if expected_sha256 is not None and digest != expected_sha256:
        raise ArtifactError(
            "artifact digest differs from approved digest: "
            f"{digest} != {expected_sha256}"
        )
    suffix = (
        artifact.suffix.lower() if SAFE_SUFFIX_RE.fullmatch(artifact.suffix) else ""
    )
    payload_name = f"payload{suffix}"
    transcript = _canonical_transcript(
        payload_bytes,
        source_type=source_type,
        media_type=media_type,
    )
    if transcript is not None and (
        source_type != "video" or transcript["video"]["id"] != source_id
    ):
        raise ArtifactError(
            "canonical transcript identity differs from capture source identity"
        )

    manifest = {
        "schema_version": "1.0",
        "source_type": source_type,
        "source_id": source_id,
        "artifact_digest": f"sha256:{digest}",
        "media_type": media_type,
        "size": len(payload_bytes),
        "payload": payload_name,
        "created_at": created_at,
        "generator": {"name": GENERATOR_NAME, "version": GENERATOR_VERSION},
        "primary_source": primary_source,
    }
    content_bytes = _render_content(transcript) if transcript is not None else None
    if content_bytes is not None:
        manifest["content"] = _descriptor("content.md", content_bytes, "text/markdown")
    try:
        validate_instance(manifest, validator_for("ArtifactManifest"))
    except KnowledgeSchemaError as exc:
        raise ArtifactError(f"invalid artifact manifest: {exc}") from exc

    source_root = confined(raw_root, raw_root / "sources" / source_type / source_id)
    final = confined(source_root, source_root / digest)
    if final.exists():
        _verify_bundle(final, manifest)
        return CaptureResult(final / "manifest.json", created=False)

    source_root.mkdir(parents=True, exist_ok=True)
    temp = Path(tempfile.mkdtemp(prefix=".capture-", dir=source_root))
    created = True
    try:
        write_bytes_fsync(temp / payload_name, payload_bytes)
        if content_bytes is not None:
            write_bytes_fsync(temp / "content.md", content_bytes)
        write_bytes_fsync(temp / "manifest.json", _manifest_bytes(manifest))
        _verify_bundle(temp, manifest)
        fsync_directory(temp)
        try:
            rename_directory_no_replace(temp, final)
        except OSError:
            if not final.exists():
                raise
            _verify_bundle(final, manifest)
            created = False
        fsync_directory(source_root)
    finally:
        if temp.exists():
            shutil.rmtree(temp)
    return CaptureResult(final / "manifest.json", created=created)


def capture_asset(
    asset: Path,
    *,
    source_id: str,
    media_type: str,
    created_at: str,
    raw_root: Path = DEFAULT_RAW_ROOT,
) -> CaptureResult:
    if not asset.is_file():
        raise ArtifactError(f"asset capture requires one explicit file: {asset}")
    _validate_component("source_id", source_id)
    if not media_type:
        raise ArtifactError("media_type must be non-empty")
    data = asset.read_bytes()
    digest = _digest(data)
    suffix = asset.suffix.lower() if SAFE_SUFFIX_RE.fullmatch(asset.suffix) else ""
    payload_name = f"asset{suffix}"
    manifest = {
        "schema_version": "1.0",
        "source_id": source_id,
        "asset_digest": f"sha256:{digest}",
        "media_type": media_type,
        "size": len(data),
        "payload": payload_name,
        "created_at": created_at,
        "generator": {"name": GENERATOR_NAME, "version": GENERATOR_VERSION},
    }
    try:
        validate_instance(manifest, validator_for("AssetManifest"))
    except KnowledgeSchemaError as exc:
        raise ArtifactError(f"invalid asset manifest: {exc}") from exc

    source_root = confined(raw_root, raw_root / "assets" / source_id)
    final = confined(source_root, source_root / digest)

    def verify(bundle: Path) -> None:
        try:
            existing = json.loads(
                (bundle / "manifest.json").read_text(encoding="utf-8")
            )
            validate_instance(existing, validator_for("AssetManifest"))
            payload = bundle / existing["payload"]
            payload_data = payload.read_bytes()
        except (OSError, json.JSONDecodeError, KnowledgeSchemaError) as exc:
            raise ArtifactError(f"corrupt asset bundle: {bundle}: {exc}") from exc
        comparable_existing = {
            key: value for key, value in existing.items() if key != "created_at"
        }
        comparable_manifest = {
            key: value for key, value in manifest.items() if key != "created_at"
        }
        if comparable_existing != comparable_manifest or payload_data != data:
            raise ArtifactError(f"existing asset bundle differs: {bundle}")
        if {path.name for path in bundle.iterdir()} != {"manifest.json", payload_name}:
            raise ArtifactError(f"asset bundle file set mismatch: {bundle}")

    if final.exists():
        verify(final)
        return CaptureResult(final / "manifest.json", created=False)
    source_root.mkdir(parents=True, exist_ok=True)
    temp = Path(tempfile.mkdtemp(prefix=".asset-", dir=source_root))
    created = True
    try:
        write_bytes_fsync(temp / payload_name, data)
        write_bytes_fsync(temp / "manifest.json", _manifest_bytes(manifest))
        verify(temp)
        fsync_directory(temp)
        try:
            rename_directory_no_replace(temp, final)
        except OSError:
            if not final.exists():
                raise
            verify(final)
            created = False
        fsync_directory(source_root)
    finally:
        if temp.exists():
            shutil.rmtree(temp)
    return CaptureResult(final / "manifest.json", created=created)
