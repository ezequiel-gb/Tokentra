"""Build-time only: download official BPE tables and capture official definitions.

Never imported by the application. Each download must match tiktoken's SHA-256.
Run again only when upgrading the pinned tiktoken version and review the diff.
"""
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen
from unittest.mock import patch

from tiktoken_ext import openai_public
from importlib.metadata import version

ROOT = Path(__file__).resolve().parents[1] / "app/assets/tokenizers"


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    definitions = {}
    for name in ("o200k_base", "cl100k_base", "p50k_base"):
        captured = {}

        def capture(url, expected_hash):
            captured.update(url=url, sha256=expected_hash)
            return {}

        with patch.object(openai_public, "load_tiktoken_bpe", capture):
            definition = getattr(openai_public, name)()
        definition.pop("mergeable_ranks")
        data = urlopen(captured["url"], timeout=60).read()
        if hashlib.sha256(data).hexdigest() != captured["sha256"]:
            raise ValueError(f"Asset integrity check failed: {name}")
        filename = name + ".tiktoken"
        (ROOT / filename).write_bytes(data)
        definitions[name] = dict(definition=definition, file=filename, **captured)
        print(f"Verified {name}: {len(data):,} bytes")
    (ROOT / "manifest.json").write_text(
        json.dumps(dict(tiktoken_version=version("tiktoken"), encodings=definitions), indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
