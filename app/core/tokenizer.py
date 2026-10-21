"""Construct official tiktoken encodings exclusively from bundled local data.

No registry lookup, URL loader or development cache is used at runtime.
"""
import base64
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import threading

import tiktoken

ENCODINGS = ("o200k_base", "cl100k_base", "p50k_base")
ASSETS = Path(__file__).resolve().parents[1] / "assets/tokenizers"
_lock = threading.RLock()


@lru_cache(maxsize=3)
def _load(name: str) -> tiktoken.Encoding:
    if name not in ENCODINGS:
        raise ValueError("Unsupported encoding")
    try:
        entry = json.loads((ASSETS / "manifest.json").read_text("utf-8"))["encodings"][name]
        data = (ASSETS / entry["file"]).read_bytes()
        if hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise ValueError("Tokenizer asset integrity check failed")
        ranks = {base64.b64decode(token): int(rank) for token, rank in
                 (line.split() for line in data.splitlines() if line)}
        return tiktoken.Encoding(mergeable_ranks=ranks, **entry["definition"])
    except (OSError, KeyError, ValueError) as exc:
        raise RuntimeError("Local tokeniser assets are missing or damaged. Reinstall Tokentra.") from exc


def get_encoding(name: str) -> tiktoken.Encoding:
    # Prevent duplicate initialisation when library clients call concurrently.
    with _lock:
        return _load(name)
