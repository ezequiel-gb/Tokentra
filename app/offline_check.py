"""Explicit diagnostic mode. Never records user text or runs in normal startup."""
import json
from pathlib import Path
import sys
import tempfile


def deny_network(event, args):
    if event in ("socket.connect", "socket.getaddrinfo", "socket.gethostbyname", "socket.gethostbyaddr"):
        raise RuntimeError("Unexpected network access")


def run():
    sys.addaudithook(deny_network)
    from app.core.counter import count_text
    from app.core.tokenizer import ENCODINGS
    from app.services.files import read_text
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QSettings, QEventLoop, QTimer
    from app.ui.main_window import MainWindow
    application = QApplication.instance() or QApplication(["Tokentra", "-platform", "offscreen"])
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder) / "sample.txt"
        path.write_bytes("Hello world!\r\n東京 👋".encode("utf-8"))
        expected = {"o200k_base": 6, "cl100k_base": 8, "p50k_base": 11}
        results = {name: count_text(read_text(path), name).tokens for name in ENCODINGS}
        assert results == expected
        window = MainWindow(QSettings(str(Path(folder) / "preferences.ini"), QSettings.Format.IniFormat))
        def wait_for_result():
            loop = QEventLoop()
            timeout = QTimer()
            timeout.setSingleShot(True)
            timeout.timeout.connect(loop.quit)
            window.queue.idle.connect(loop.quit)
            timeout.start(10000)
            if window.result is None:
                loop.exec()
            window.queue.idle.disconnect(loop.quit)
            timeout.stop()
            if window.result is None:
                raise RuntimeError("Offline GUI counting did not finish")
        wait_for_result()
        for name in ENCODINGS:
            window.encoding.setCurrentText(name)
            window.import_path(path)
            wait_for_result()
            assert window.result.encoding == name
            assert window.result.tokens == expected[name]
            assert window.editor.raw == read_text(path)
        generation = window.generation
        raw = window.editor.raw
        window.set_mode("planning")
        window.planning.capacity.setText("100")
        window.planning.allowance.setText("200")
        assert window.planning.allocation.unallocated == 100 - expected[name] - 200
        assert window.planning.allocation.excess == expected[name] + 100
        window.set_mode("counter")
        assert window.generation == generation and window.editor.raw == raw
        window.close()
        preferences = window.preferences
        assert set(preferences.allKeys()) == {"geometry", "encoding", "mode", "context_capacity", "additional_allowance"}
    report = dict(status="passed", network="Python socket connections and DNS denied",
                  encodings=results, gui_startup=True, imported_file=True,
                  gui_encoding_switches=True, planning=True, persisted_keys=preferences.allKeys())
    if "--report" in sys.argv:
        Path(sys.argv[sys.argv.index("--report") + 1]).write_text(json.dumps(report, indent=2), "utf-8")
    elif sys.stdout is not None:
        print(json.dumps(report, indent=2))
    return 0
