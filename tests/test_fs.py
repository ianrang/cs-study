import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from knowledge import fs  # noqa: E402


def test_publish_bytes_no_replace_is_atomic_and_idempotent():
    with tempfile.TemporaryDirectory() as directory:
        output = Path(directory) / "plan.json"
        assert fs.publish_bytes_no_replace(output, b"approved\n") is True
        assert fs.publish_bytes_no_replace(output, b"approved\n") is False
        try:
            fs.publish_bytes_no_replace(output, b"different\n")
        except FileExistsError:
            pass
        else:
            raise AssertionError("different bytes replaced an approved output")
        assert output.read_bytes() == b"approved\n"


def test_publish_bytes_no_replace_preserves_competing_writer():
    with tempfile.TemporaryDirectory() as directory:
        output = Path(directory) / "plan.json"
        real_link = fs.os.link

        def competing_link(source: Path, target: Path) -> None:
            Path(target).write_bytes(b"competitor\n")
            real_link(source, target)

        fs.os.link = competing_link
        try:
            try:
                fs.publish_bytes_no_replace(output, b"approved\n")
            except FileExistsError:
                pass
            else:
                raise AssertionError("competing output was replaced")
        finally:
            fs.os.link = real_link
        assert output.read_bytes() == b"competitor\n"
