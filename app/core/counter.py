from dataclasses import dataclass
import re
from time import perf_counter

from app.core.tokenizer import get_encoding


@dataclass(frozen=True)
class Counts:
    tokens: int
    words: int
    characters: int
    encoding: str
    elapsed: float


def count_text(text: str, encoding: str = "o200k_base") -> Counts:
    started = perf_counter()
    # encode_ordinary never interprets special-token-looking input as control tokens.
    tokens = len(get_encoding(encoding).encode_ordinary(text))
    words = sum(1 for _ in re.finditer(r"\S+", text))
    return Counts(tokens, words, len(text), encoding, perf_counter() - started)
