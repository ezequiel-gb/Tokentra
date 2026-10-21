import codecs
import pytest
from app.services.files import read_text, FileImportError


@pytest.mark.parametrize("encoding", ["utf-8", "utf-8-sig", "utf-16", "utf-32"])
def test_exact_decoding(tmp_path, encoding):
    path = tmp_path / "text.txt"
    text = "東京 👋\r\nsecond\rthird\n"
    path.write_bytes(text.encode(encoding))
    assert read_text(path) == text


@pytest.mark.parametrize("data", [b"\xffbad", b"binary\0text", codecs.BOM_UTF16_LE + b"x"])
def test_invalid_file(tmp_path, data):
    path = tmp_path / "invalid.txt"
    path.write_bytes(data)
    with pytest.raises(FileImportError):
        read_text(path)


def test_missing_file(tmp_path):
    with pytest.raises(FileImportError):
        read_text(tmp_path / "absent.txt")
