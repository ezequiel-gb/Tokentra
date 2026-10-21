from pathlib import Path
from unittest.mock import patch
import pytest
import tiktoken
from tiktoken.load import load_tiktoken_bpe
from tiktoken_ext import openai_public
from app.core.counter import count_text
from app.core.tokenizer import ASSETS, ENCODINGS, get_encoding

CASES = ["", " \t\n", " leading and trailing ", "a\r\nb\rc\n\n\n", "!?.,;:()[]{}",
         "中文 日本語 한국어 العربية हिन्दी", "👩🏽‍💻🌍 e\u0301 é", "def f(x):\n    return x + 1\n",
         "<|endoftext|> <|fim_prefix|> <|endofprompt|>", "text 123\n" * 20000]


@pytest.fixture(scope="module", params=ENCODINGS)
def reference(request):
    name = request.param
    # Official constructor with the official local loader: independent reference.
    with patch.object(openai_public, "load_tiktoken_bpe",
                      lambda url, expected_hash: load_tiktoken_bpe(str(ASSETS / (name + ".tiktoken")), expected_hash)):
        encoding = tiktoken.Encoding(**getattr(openai_public, name)())
    return name, encoding


@pytest.mark.parametrize("text", CASES, ids=["empty", "whitespace", "edges", "line-endings", "punctuation",
                                          "multilingual", "emoji", "code", "special-looking", "large"])
def test_matches_official_reference(reference, text):
    name, encoding = reference
    result = count_text(text, name)
    assert result.tokens == len(encoding.encode(text, disallowed_special=()))
    assert result.words == len(text.split())
    assert result.characters == len(text)
    assert result.encoding == name


def test_unsupported_encoding():
    with pytest.raises(ValueError):
        get_encoding("not-openai")


def test_damaged_asset_fails_locally(tmp_path, monkeypatch):
    from app.core import tokenizer
    tokenizer._load.cache_clear()
    monkeypatch.setattr(tokenizer, "ASSETS", tmp_path)
    with pytest.raises(RuntimeError, match="missing or damaged"):
        get_encoding("o200k_base")


@pytest.mark.parametrize("text,points,units", [
    ("A😀B", 3, 4),
    ("e\u0301", 2, 2),
    ("👩🏽‍💻", 4, 7),
    ("😀" * 9 + "a" * 578, 587, 596),
    ("&amp; 😀\r\n", 9, 10),
], ids=["supplementary", "combining", "emoji-sequence", "587-codepoints-596-units", "literal-entity-crlf"])
def test_unicode_codepoints_not_utf16(reference, text, points, units):
    # Independent fixtures: the original 251-token sample was not supplied.
    name, official = reference
    assert len(text) == points
    assert len(text.encode("utf-16-le")) // 2 == units
    result = count_text(text, name)
    assert result.characters == points
    assert result.tokens == len(official.encode(text, disallowed_special=()))
