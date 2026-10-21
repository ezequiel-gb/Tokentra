"""Reproducible synthetic engine + GUI benchmark. Run from the project root."""
import json
import os
from pathlib import Path
import platform
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
import psutil
from PySide6.QtCore import QTimer, QEventLoop, QSettings
from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow
import tempfile


def main():
    app = QApplication([])
    process = psutil.Process()
    records = []
    with tempfile.TemporaryDirectory() as folder:
        window = MainWindow(QSettings(str(Path(folder) / "settings.ini"), QSettings.Format.IniFormat))
        window.show()
        loop = QEventLoop()
        window.queue.idle.connect(loop.quit)
        loop.exec()
        for encoding in ("o200k_base", "cl100k_base", "p50k_base"):
            window.encoding.setCurrentText(encoding)
            if window.queue.active:
                loop.exec()
            for target in (100_000, 1_000_000):
                text = " hello" * target
                before = process.memory_info().rss
                load_start = time.perf_counter()
                window.editor.set_exact_text(text)
                load_seconds = time.perf_counter() - load_start
                # Application import uses this same exact-text editor loading path.
                window._changed()
                window.debounce.stop()
                ticks, memory = [], [process.memory_info().rss]
                start = time.perf_counter()
                timer = QTimer()
                def tick():
                    ticks.append(time.perf_counter())
                    memory.append(process.memory_info().rss)
                timer.timeout.connect(tick)
                timer.start(10)
                window._submit()
                loop.exec()
                finish = time.perf_counter()
                timer.stop()
                assert window.result is not None and window.result.tokens == target
                gaps = [b - a for a, b in zip([start] + ticks, ticks + [finish])]
                records.append(dict(encoding=encoding, input_bytes=len(text.encode()),
                                    characters=len(text), tokens=window.result.tokens,
                                    count_seconds=window.result.elapsed,
                                    editor_load_seconds=load_seconds,
                                    gui_heartbeat_ticks=len(ticks),
                                    max_gui_gap_ms=max(gaps) * 1000,
                                    rss_before_mib=before / 2**20,
                                    peak_sampled_rss_mib=max(memory) / 2**20))
                print(json.dumps(records[-1]), flush=True)
        window.close()
    report = dict(platform=platform.platform(), python=sys.version, cpu=platform.processor(),
                  logical_cpus=psutil.cpu_count(), ram_gib=psutil.virtual_memory().total / 2**30,
                  method="Synthetic ' hello' repeated. Encodings warmed. Editor load measured on GUI thread. "
                         "10ms Qt heartbeat during worker count; RSS sampled, not an allocation peak. "
                         "Offscreen Qt on Windows; not a physical-display responsiveness test.", records=records)
    Path("docs/benchmark.json").write_text(json.dumps(report, indent=2), "utf-8")


if __name__ == "__main__":
    main()
