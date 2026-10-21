"""Whole-text prose/code/Unicode baseline plus editor and worker responsiveness."""
import json
import argparse
import os
from pathlib import Path
import platform
import sys
import tempfile
import threading
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
import psutil
from PySide6.QtCore import QEventLoop, QSettings, QTimer
from PySide6.QtWidgets import QApplication
from app.core.counter import count_text
from app.ui.main_window import MainWindow

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ("Reliable measurements help us prepare a desktop release. Spaces, punctuation and line endings matter.\n"
          "def calculate_total(values):\n    return sum(value * 1.25 for value in values)\n"
          "Latin Ελληνικά Кириллица العربية עברית 中文 日本語 한국어 हिन्दी ∑ € £ 😀 👩🏽‍💻\r\n\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, default=ROOT / 'docs/rc2/benchmark.json')
    args = parser.parse_args()
    application = QApplication([])
    process = psutil.Process()
    records = []
    temporary_root = ROOT / ".verification-tmp"
    temporary_root.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=temporary_root) as folder:
        window = MainWindow(QSettings(str(Path(folder) / "settings.ini"), QSettings.Format.IniFormat))
        window.show()
        loop = QEventLoop()
        window.queue.idle.connect(loop.quit)
        loop.exec()
        for encoding in ("o200k_base", "cl100k_base", "p50k_base"):
            window.encoding.setCurrentText(encoding)
            if window.queue.active:
                loop.exec()
            unit_count = count_text(CORPUS, encoding).tokens
            for target in (100_000, 1_000_000):
                text = CORPUS * max(1, round(target / unit_count))
                expected = count_text(text, encoding).tokens
                samples = [process.memory_info().rss]
                stopped = threading.Event()
                def sample():
                    while not stopped.wait(0.005):
                        samples.append(process.memory_info().rss)
                sampler = threading.Thread(target=sample, daemon=True)
                sampler.start()
                before = time.perf_counter()
                window.editor.set_exact_text(text)
                load_seconds = time.perf_counter() - before
                window._changed()
                window.debounce.stop()
                ticks = []
                timer = QTimer()
                timer.timeout.connect(lambda: ticks.append(time.perf_counter()))
                timer.start(10)
                before_count = time.perf_counter()
                window._submit()
                loop.exec()
                finished = time.perf_counter()
                timer.stop()
                assert window.result is not None and window.result.tokens == expected
                count_seconds = window.result.elapsed
                # Measure one ordinary edit at the end of the loaded document too.
                from PySide6.QtGui import QTextCursor
                window.editor.moveCursor(QTextCursor.MoveOperation.End)
                edit_start = time.perf_counter()
                window.editor.insertPlainText("!")
                edit_seconds = time.perf_counter() - edit_start
                window.debounce.stop()
                stopped.set()
                sampler.join()
                gaps = [b - a for a, b in zip([before_count] + ticks, ticks + [finished])]
                records.append(dict(encoding=encoding, target_tokens=target, tokens=expected,
                                    characters=len(text), input_bytes=len(text.encode("utf-8")),
                                    count_seconds=count_seconds,
                                    worker_roundtrip_seconds=finished - before_count,
                                    editor_load_seconds=load_seconds, editor_end_edit_seconds=edit_seconds,
                                    heartbeat_ticks=len(ticks), max_gui_gap_ms=max(gaps) * 1000,
                                    peak_sampled_rss_mib=max(samples) / 2**20,
                                    cumulative_peak_working_set_mib=getattr(process.memory_info(), "peak_wset", 0) / 2**20))
                print(json.dumps(records[-1]), flush=True)
        window.close()
    output = args.report
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(dict(platform=platform.platform(), python=platform.python_version(),
        logical_cpus=psutil.cpu_count(), ram_gib=psutil.virtual_memory().total / 2**30,
        corpus=CORPUS, method="Repeated mixed prose, Python, multilingual Unicode and CRLF. Whole-string counting, "
        "warm encodings. RSS sampled every 5ms on a separate Python thread across load/count/end-edit; not a precise peak. "
        "10ms GUI heartbeat only during worker count. Offscreen Qt, not a physical responsiveness test.", records=records), indent=2), "utf-8")


if __name__ == "__main__":
    main()
