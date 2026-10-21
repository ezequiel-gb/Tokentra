import json
import os
from pathlib import Path
import subprocess
import sys


def test_fresh_process_offline_gui_and_file_import(tmp_path):
    report = tmp_path / "offline.json"
    environment = os.environ.copy()
    environment.update(TEMP=str(tmp_path), TMP=str(tmp_path), TMPDIR=str(tmp_path),
                       TIKTOKEN_CACHE_DIR=str(tmp_path / "empty-cache"),
                       DATA_GYM_CACHE_DIR=str(tmp_path / "empty-data-gym-cache"))
    result = subprocess.run([sys.executable, "-m", "app.main", "--offline-check", "--report", str(report)],
                            cwd=Path(__file__).resolve().parents[1], env=environment,
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
    data = json.loads(report.read_text("utf-8"))
    assert data["encodings"] == {"o200k_base": 6, "cl100k_base": 8, "p50k_base": 11}
    assert data["gui_encoding_switches"]
    assert data["persisted_keys"] == ["additional_allowance", "context_capacity", "encoding", "geometry", "mode"]
    assert not (tmp_path / "empty-cache").exists()
