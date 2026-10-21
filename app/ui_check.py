"""Explicit synthetic UI regression diagnostic; never uses normal preferences."""
import json
from pathlib import Path
import sys
import tempfile
import time


def run():
    from PySide6.QtCore import QEventLoop, QPoint, QSettings, Qt, QTimer
    from PySide6.QtGui import QFontDatabase
    from PySide6.QtWidgets import QApplication, QLabel, QToolTip
    from app import DISPLAY_VERSION
    from app.core.counter import count_text
    from app.offline_check import deny_network
    from app.ui.main_window import MainWindow
    from app.ui.token_info import TOKEN_INFORMATION

    sys.addaudithook(deny_network)
    application = QApplication.instance() or QApplication(["Tokentra UI verification"])
    if sys.platform == "win32" and not QFontDatabase.families():
        for name in ("segoeui.ttf", "seguisb.ttf", "seguiemj.ttf", "msyh.ttc"):
            QFontDatabase.addApplicationFont("C:/Windows/Fonts/" + name)
    report_path = Path(sys.argv[sys.argv.index("--report") + 1])
    output = report_path.parent
    output.mkdir(parents=True, exist_ok=True)
    records = []

    def settle(milliseconds=100):
        loop = QEventLoop()
        QTimer.singleShot(milliseconds, loop.quit)
        loop.exec()

    with tempfile.TemporaryDirectory() as folder:
        window = MainWindow(QSettings(str(Path(folder) / "ui.ini"), QSettings.Format.IniFormat))
        try:
            window.show()
            sample = "Precision begins with the right measure.\n\nA private workspace for prompts, prose and code.\nHello · Bonjour · 東京 · مرحباً 👋"
            window.editor.set_exact_text(sample)
            deadline = time.monotonic() + 15
            while window.result is None and time.monotonic() < deadline:
                settle(20)
            assert window.result and window.result.tokens == count_text(sample).tokens
            generation, result = window.generation, window.result
            assert not any("Exact raw-text counts ·" in label.text() for label in window.findChildren(QLabel))
            assert window.token_information.accessibleDescription() == TOKEN_INFORMATION
            startup_size = [window.width(), window.height()]
            for mode in ("counter", "planning"):
                window.set_mode(mode)
                settle()
                assert window.editor.height() >= 80
                assert window.editor.viewport().height() >= window.editor.fontMetrics().height()
                assert window.shell.rect().contains(window.results_stack.geometry()), "Startup dashboard outside client bounds"
                window.grab().save(str(output / f"startup-{mode}.png"))
            for width, height in ((680, 540), (1040, 760), (1120, 820), (1440, 900), (1920, 1080)):
                window.resize(width, height)
                window.set_mode("counter")
                settle()
                editor_height = window.editor.height()
                assert window.editor.height() >= 80
                assert window.editor.viewport().height() >= window.editor.fontMetrics().height()
                assert window.shell.rect().contains(window.results_stack.geometry())
                if width in (680, 1120):
                    window.grab().save(str(output / f"counter-{width}.png"))
                window.set_mode("planning")
                settle()
                assert window.editor.height() >= 80
                assert window.editor.viewport().height() >= window.editor.fontMetrics().height()
                assert window.shell.rect().contains(window.results_stack.geometry())
                assert window.editor.raw == sample and window.result is result and window.generation == generation
                assert window.editor.height() <= editor_height, "Planning must not take space away from its dashboard"
                window.planning.capacity.setText("128,000")
                window.planning.allowance.setText("8,000")
                window.planning.set_tokens(result.tokens)
                settle()
                if width in (680, 1040, 1120, 1440):
                    window.grab().save(str(output / f"planning-{width}.png"))
                for number in (1000, 8000, 128000, 1000000, 10000000):
                    window.planning.capacity.setText(str(number * 2))
                    window.planning.allowance.setText("0")
                    window.planning.set_tokens(number)
                    settle(30)
                    widths = {}
                    for key, value in window.planning.values.items():
                        expected = number * 2 if key == "capacity" else number
                        assert value.text() == f"{expected:,}"
                        required = value.fontMetrics().horizontalAdvance(value.text())
                        assert value.contentsRect().width() >= required + 2, (width, number, key, value.width(), required)
                        assert value.height() >= value.fontMetrics().height()
                        widths[key] = dict(width=value.width(), text_pixels=required)
                    assert window.planning.horizontalScrollBar().maximum() == 0
                    records.append(dict(size=[window.width(), window.height()], value=number,
                                        columns=window.planning._columns, labels=widths))
            window.resize(1120, 820)
            window.set_mode("planning")
            window.planning.capacity.setText("128,000")
            window.planning.allowance.setText("8,000")
            window.planning.set_tokens(result.tokens)
            settle()
            planning_scroll_max = window.planning.verticalScrollBar().maximum()
            window.set_mode("counter")
            settle()
            window.activateWindow()
            window.token_information.setFocus(Qt.FocusReason.TabFocusReason)
            settle()
            assert window.token_information.hasFocus() and QToolTip.isVisible(), f"focus={window.token_information.hasFocus()}, tooltip={QToolTip.isVisible()}"
            tip = next(widget for widget in application.topLevelWidgets() if widget.inherits("QTipLabel"))
            assert window.token_information.screen().availableGeometry().contains(tip.frameGeometry())
            tip.grab().save(str(output / "token-information.png"))
            window.copy_count.setFocus(Qt.FocusReason.TabFocusReason)
            settle(400)
            assert not QToolTip.isVisible()
            window.copy_tokens()
            assert application.clipboard().text() == str(result.tokens)
            data = dict(status="passed", version=DISPLAY_VERSION, platform=application.platformName(),
                        device_pixel_ratio=window.devicePixelRatioF(), numeric_layouts=records,
                        startup_client_size=startup_size, startup_content_contained=True,
                        keyboard_tooltip=True, tooltip_within_screen=True, tooltip_dismissal=True,
                        shared_editor_and_result=True, footer_removed=True,
                        planning_scroll_max_at_1120x820=planning_scroll_max,
                        scope="Actual Qt widget rendering with synthetic input and isolated settings. Logical resizes and Qt scale factors, not physical display reconfiguration.")
        except Exception as error:
            data = dict(status="failed", error=f"{type(error).__name__}: {error}", diagnostic_line=error.__traceback__.tb_lineno, numeric_layouts=records)
        finally:
            deadline = time.monotonic() + 15
            while window.queue.active and time.monotonic() < deadline:
                settle(20)
            window.close()
    report_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    if sys.stdout:
        print(json.dumps({key: value for key, value in data.items() if key != "numeric_layouts"}, indent=2))
    return 0 if data["status"] == "passed" else 1
