"""Run the frozen self-check with isolated empty tokeniser cache directories."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import argparse

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--dist-dir", type=Path, default=root / "dist")
parser.add_argument("--report", type=Path, default=root / "docs/offline-packaged.json")
parser.add_argument("--native-window-checks", action="store_true", help="Also run the Windows Qt scale-factor matrix")
args = parser.parse_args()
if sys.platform == "win32":
    executable = args.dist_dir.resolve() / "Tokentra/Tokentra.exe"
elif sys.platform == "darwin":
    executable = args.dist_dir.resolve() / "Tokentra.app/Contents/MacOS/Tokentra"
else:
    executable = args.dist_dir.resolve() / "Tokentra/Tokentra"
with tempfile.TemporaryDirectory(prefix="tokentra-package-check-") as folder:
    environment = os.environ.copy()
    environment.update(TIKTOKEN_CACHE_DIR=str(Path(folder) / "empty-tiktoken"),
                       DATA_GYM_CACHE_DIR=str(Path(folder) / "empty-data-gym"),
                       TEMP=folder, TMP=folder, TMPDIR=folder, PYTHONPATH="", PYTHONHOME="")
    if sys.platform == "win32":
        system = Path(os.environ.get("SystemRoot", "C:/Windows"))
        environment["PATH"] = os.pathsep.join((str(system / "System32"), str(system)))
    fresh_report = Path(folder) / "result.json"
    result = subprocess.run([str(executable), "--offline-check", "--report", str(fresh_report)],
                            cwd=folder, env=environment, timeout=60)
    if result.returncode != 0:
        raise SystemExit(f"Frozen check failed: {result.returncode}")
    report = json.loads(fresh_report.read_text("utf-8"))
    assert report["status"] == "passed"
    report["outside_source_directory"] = True
    report["developer_search_paths_removed"] = True
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2), "utf-8")
    print("Frozen offline check passed, with empty cache paths and network audit hook.")
    if args.native_window_checks:
        if sys.platform != "win32":
            raise SystemExit("The native scale-factor matrix is Windows-specific.")
        for scale in ("1", "1.25", "1.5", "2"):
            environment.update(QT_SCALE_FACTOR=scale, QT_QPA_PLATFORM="windows")
            native_report = Path(folder) / ("native-" + scale + ".json")
            native = subprocess.run([str(executable), "--window-check", "--report", str(native_report)],
                                    cwd=folder, env=environment, timeout=45)
            if native.returncode != 0:
                raise SystemExit(f"Frozen native window check failed at scale {scale}: {native.returncode}")
            data = json.loads(native_report.read_text("utf-8"))
            assert data["status"] == "passed" and data["platform"] == "windows"
            (args.report.parent / ("frozen-windows-scale-" + scale + ".json")).write_text(json.dumps(data, indent=2), "utf-8")
            print(f"Frozen native Windows scale {scale}: passed", flush=True)
