"""Strict decoding: BOM UTF-8/16/32, otherwise UTF-8. Preserve line endings."""
import codecs
from pathlib import Path


class FileImportError(ValueError):
    pass


def read_text(path: str | Path) -> str:
    try:
        with Path(path).open("rb") as stream:
            prefix = stream.read(4)
        encoding = "utf-8-sig"
        for bom, candidate in ((codecs.BOM_UTF32_LE, "utf-32"),
                               (codecs.BOM_UTF32_BE, "utf-32"),
                               (codecs.BOM_UTF16_LE, "utf-16"),
                               (codecs.BOM_UTF16_BE, "utf-16")):
            if prefix.startswith(bom):
                encoding = candidate
                break
        with Path(path).open("r", encoding=encoding, errors="strict", newline="") as stream:
            text = stream.read()
        if "\0" in text:
            raise FileImportError("This file contains binary NUL characters. Choose a plain-text file.")
        return text
    except UnicodeError as exc:
        raise FileImportError("Cannot decode this file. Use UTF-8, or UTF-16/32 with a byte-order mark.") from exc
    except OSError as exc:
        raise FileImportError("Cannot read this file. Check that it exists and you have access.") from exc
