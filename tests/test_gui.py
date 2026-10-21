import time
from PySide6.QtCore import QSettings, QMimeData, Qt
from PySide6.QtGui import QTextCursor
import pytest
from app.ui.main_window import MainWindow
from app.core.counter import count_text
from app.core.workers import Request


@pytest.fixture
def window(qtbot, tmp_path):
    widget = MainWindow(QSettings(str(tmp_path / "settings.ini"), QSettings.Format.IniFormat))
    qtbot.addWidget(widget)
    widget.show()
    qtbot.waitUntil(lambda: widget.result is not None, timeout=15000)
    yield widget
    widget.debounce.stop()
    qtbot.waitUntil(lambda: not widget.queue.active, timeout=15000)


def ready(qtbot, window, expected):
    qtbot.waitUntil(lambda: window.result is not None and window.result.tokens == expected, timeout=15000)


def test_rapid_edits_and_encoding(qtbot, window):
    for text in ("old", "stale", "latest 東京 👋"):
        window.editor.selectAll()
        window.editor.insertPlainText(text)
    window.encoding.setCurrentText("cl100k_base")
    ready(qtbot, window, count_text("latest 東京 👋", "cl100k_base").tokens)
    assert window.result.characters == len("latest 東京 👋")
    old = Request(window.generation - 1, "o200k_base", "old")
    before = window.result
    window._completed(old, count_text("old"), None, "")
    assert window.result is before
    window.copy_tokens()
    from PySide6.QtWidgets import QApplication
    assert QApplication.clipboard().text() == str(before.tokens)
    window.clear()
    assert window.result is None and not window.copy_count.isEnabled()
    ready(qtbot, window, 0)


def test_import_failure_preserves_text(qtbot, window, tmp_path):
    window.editor.insertPlainText("keep this")
    ready(qtbot, window, count_text("keep this").tokens)
    path = tmp_path / "bad.txt"
    path.write_bytes(b"\xff")
    window.import_path(path)
    qtbot.waitUntil(lambda: "decode" in window.status.text())
    assert window.editor.raw == "keep this"
    assert window.result is None


def test_exact_import_and_paste(qtbot, window, tmp_path):
    text = "😀 first\r\nnext\rthird\n"
    path = tmp_path / "good.txt"
    path.write_bytes(text.encode("utf-8"))
    window.import_path(path)
    ready(qtbot, window, count_text(text).tokens)
    assert window.editor.raw == text
    assert window.result.characters == len(text)
    window.editor.moveCursor(QTextCursor.MoveOperation.End)
    mime = QMimeData()
    mime.setText("paste\r\n👋")
    window.editor.insertFromMimeData(mime)
    assert window.editor.raw == text + "paste\r\n👋"
    ready(qtbot, window, count_text(window.editor.raw).tokens)


def test_file_only_leaves_editor_intact(qtbot, window, tmp_path):
    window.editor.insertPlainText("editor")
    path = tmp_path / "large.txt"
    path.write_text("file text " * 1000, encoding="utf-8")
    window.import_path(path, True)
    ready(qtbot, window, count_text("file text " * 1000).tokens)
    assert window.editor.raw == "editor"
    assert "FILE RESULT" in window.source.text()
    window.encoding.setCurrentText("p50k_base")
    ready(qtbot, window, count_text("file text " * 1000, "p50k_base").tokens)
    assert window.editor.raw == "editor"


def test_responsive_during_worker(qtbot, window, monkeypatch):
    from app.core import workers
    original = workers.count_text
    def slow(text, encoding):
        time.sleep(0.25)
        return original(text, encoding)
    monkeypatch.setattr(workers, "count_text", slow)
    window.editor.insertPlainText("background")
    qtbot.waitUntil(lambda: window.queue.active)
    window.clear()
    assert window.editor.raw == ""
    ready(qtbot, window, 0)


def test_window_states_and_settings(qtbot, window):
    window.showMaximized()
    qtbot.waitUntil(window.isMaximized)
    assert window.layout.contentsMargins().left() == 22
    window.showNormal()
    qtbot.waitUntil(lambda: not window.isMaximized())
    assert window.layout.contentsMargins().left() == 30
    window.toggle_fullscreen()
    qtbot.waitUntil(window.isFullScreen)
    window.exit_fullscreen()
    window.resize(680, 540)
    qtbot.wait(30)
    assert window.editor.height() > 60
    window.close()
    assert set(window.preferences.allKeys()) == {"geometry", "encoding", "mode", "context_capacity", "additional_allowance"}


def test_close_waits_without_blocking(qtbot, window, monkeypatch):
    from app.core import workers
    original = workers.count_text
    def slow(text, encoding):
        time.sleep(0.2)
        return original(text, encoding)
    monkeypatch.setattr(workers, "count_text", slow)
    window.editor.insertPlainText("finish")
    qtbot.waitUntil(lambda: window.queue.active)
    window.close()
    assert window.closing
    qtbot.waitUntil(lambda: not window.isVisible(), timeout=5000)


def test_selection_paste_and_unicode_edit(qtbot, window):
    window.editor.set_exact_text("😀a\r\nb")
    cursor = window.editor.textCursor()
    cursor.setPosition(2)  # Qt positions count UTF-16 units.
    cursor.setPosition(3, QTextCursor.MoveMode.KeepAnchor)
    window.editor.setTextCursor(cursor)
    window.editor.insertPlainText("X")
    assert window.editor.raw == "😀X\r\nb"
    window.editor.selectAll()
    mime = QMimeData()
    mime.setText("replacement\r\n東京")
    window.editor.insertFromMimeData(mime)
    assert window.editor.raw == "replacement\r\n東京"
    ready(qtbot, window, count_text(window.editor.raw).tokens)


def test_worker_queue_keeps_only_latest(qtbot, window, monkeypatch):
    from app.core import workers
    original = workers.count_text
    seen = []
    def slow(text, encoding):
        seen.append(text)
        time.sleep(0.1)
        return original(text, encoding)
    monkeypatch.setattr(workers, "count_text", slow)
    for i, text in enumerate(("first", "discard me", "last")):
        window.queue.submit(Request(-100 - i, "o200k_base", text))
    qtbot.waitUntil(lambda: not window.queue.active, timeout=5000)
    assert seen == ["first", "last"]

def test_planning_shared_result_without_recount(qtbot, window, monkeypatch):
    window.editor.set_exact_text("Hello world!")
    ready(qtbot, window, count_text("Hello world!").tokens)
    generation = window.generation
    result = window.result
    def forbidden(*args, **kwargs):
        raise AssertionError("Scenario changes must not tokenise again")
    monkeypatch.setattr(window.queue, "submit", forbidden)
    window.set_mode("planning")
    window.planning.capacity.setText("10")
    window.planning.allowance.setText("20")
    assert window.planning.allocation.planned == result.tokens + 20
    assert window.planning.allocation.unallocated == -10 - result.tokens
    assert "exceeds" in window.planning.interpretation.text()
    window.planning.capacity.setText("0")
    assert window.planning.allocation is None
    assert window.planning.validation.text()
    window.planning.capacity.setText("1,000")
    window.planning.allowance.setText("0")
    assert window.planning.allocation.unallocated == 1000 - result.tokens
    window.set_mode("counter")
    assert window.result is result and window.generation == generation
    assert window.editor.raw == "Hello world!"


def test_planning_pending_and_preferences(qtbot, window):
    window.set_mode("planning")
    window.planning.capacity.setText(str(10**50))
    window.planning.allowance.setText("0")
    window.editor.set_exact_text("new text")
    assert window.planning.allocation is None
    ready(qtbot, window, count_text("new text").tokens)
    assert window.planning.allocation.capacity == 10**50
    window.close()
    assert window.preferences.value("context_capacity") == str(10**50)
    assert window.preferences.value("mode") == "planning"
    restored = MainWindow(window.preferences)
    qtbot.addWidget(restored)
    assert restored.mode == "planning"
    assert restored.planning.capacity.text() == f'{10**50:,}'
    qtbot.waitUntil(lambda: not restored.queue.active, timeout=15000)
    restored.close()

def test_planning_corrupt_preferences_and_compact_navigation(qtbot, tmp_path):
    preferences = QSettings(str(tmp_path / 'bad.ini'), QSettings.Format.IniFormat)
    preferences.setValue('context_capacity', '-1')
    preferences.setValue('additional_allowance', 'invalid')
    preferences.setValue('mode', 'unknown')
    widget = MainWindow(preferences)
    qtbot.addWidget(widget)
    widget.show()
    assert widget.mode == 'counter'
    assert widget.planning.capacity.text() == '128,000'
    assert widget.planning.allowance.text() == '8,000'
    widget.set_mode('planning')
    widget.resize(680, 540)
    qtbot.wait(30)
    widget.planning.capacity.setFocus()
    widget.planning.ensureWidgetVisible(widget.planning.capacity)
    qtbot.wait(30)
    assert widget.planning.viewport().rect().intersects(widget.planning.capacity.rect().translated(
        widget.planning.capacity.mapTo(widget.planning.viewport(), widget.planning.capacity.rect().topLeft())))
    assert widget.editor.height() > 60
    assert widget.planning.horizontalScrollBar().maximum() == 0
    qtbot.waitUntil(lambda: not widget.queue.active, timeout=15000)
    widget.close()

def test_planning_latest_encoding_clear_and_error(qtbot, window):
    window.set_mode('planning')
    for text in ('obsolete', 'latest 東京 👋'):
        window.editor.set_exact_text(text)
    window.encoding.setCurrentText('cl100k_base')
    ready(qtbot, window, count_text('latest 東京 👋', 'cl100k_base').tokens)
    plan = window.planning.allocation
    assert plan.transcript == window.result.tokens
    window._completed(Request(window.generation - 1, 'o200k_base', 'obsolete'), count_text('obsolete'), '', '')
    assert window.planning.allocation is plan
    window.clear()
    assert window.planning.allocation is None
    ready(qtbot, window, 0)
    assert window.planning.allocation.transcript == 0
    window._invalidate()
    window._completed(Request(window.generation, 'cl100k_base', ''), None, '', 'Counting failed safely')
    assert window.planning.allocation is None
    assert 'Counting failed safely' in window.planning.interpretation.text()

@pytest.mark.parametrize('number', [1000, 8000, 128000, 1000000, 10000000])
@pytest.mark.parametrize('width', [680, 900, 1120])
def test_planning_numbers_fit_complete_cards(qtbot, window, number, width):
    window.resize(width, 820)
    window.set_mode('planning')
    window.planning.capacity.setText(str(number * 2))
    window.planning.allowance.setText('0')
    window.planning.set_tokens(number)
    qtbot.wait(30)
    for key, label in window.planning.values.items():
        assert label.text() == f'{number * 2 if key == "capacity" else number:,}'
        assert label.contentsRect().width() >= label.fontMetrics().horizontalAdvance(label.text()) + 2
        assert label.height() >= label.fontMetrics().height()
    widths = [frame.width() for frame in window.planning.card_frames]
    assert max(widths) - min(widths) <= 1
    assert window.planning.horizontalScrollBar().maximum() == 0
    # Exercise the requested capacity itself as well as the larger card values.
    window.planning.capacity.setText(str(number))
    qtbot.wait(20)
    capacity = window.planning.values['capacity']
    assert capacity.text() == f'{number:,}'
    assert capacity.contentsRect().width() >= capacity.fontMetrics().horizontalAdvance(capacity.text()) + 2


def test_contextual_help_and_no_footer(qtbot, window):
    from PySide6.QtWidgets import QApplication, QLabel, QToolTip
    from PySide6.QtGui import QHelpEvent
    from PySide6.QtCore import QEvent
    from app.ui.token_info import TOKEN_INFORMATION
    assert not any('Exact raw-text counts ·' in label.text() for label in window.findChildren(QLabel))
    info = window.token_information
    assert info.accessibleDescription() == TOKEN_INFORMATION
    assert TOKEN_INFORMATION in info.toolTip()
    window.activateWindow()
    info.setFocus(Qt.FocusReason.TabFocusReason)
    qtbot.waitUntil(QToolTip.isVisible)
    qtbot.keyClick(info, Qt.Key.Key_Escape)
    qtbot.waitUntil(lambda: not QToolTip.isVisible())
    window.copy_count.setFocus()
    event = QHelpEvent(QEvent.Type.ToolTip, info.rect().center(), info.mapToGlobal(info.rect().center()))
    QApplication.sendEvent(info, event)
    qtbot.waitUntil(QToolTip.isVisible)
    QApplication.sendEvent(info, QEvent(QEvent.Type.Leave))
    qtbot.waitUntil(lambda: not QToolTip.isVisible())
    info.setFocus(Qt.FocusReason.TabFocusReason)
    qtbot.waitUntil(QToolTip.isVisible)
    window.set_mode('planning')
    qtbot.waitUntil(lambda: not QToolTip.isVisible())


def test_mode_sensitive_proportions(qtbot, window):
    window.resize(1120, 820)
    window.editor.set_exact_text('shared text')
    ready(qtbot, window, count_text('shared text').tokens)
    qtbot.wait(30)
    editor = window.editor
    before = editor.height()
    result, generation = window.result, window.generation
    window.set_mode('planning')
    qtbot.wait(50)
    assert 80 <= editor.height() < before
    assert window.results_stack.height() > editor.height()
    assert window.planning.verticalScrollBar().maximum() == 0
    window.set_mode('counter')
    qtbot.wait(30)
    assert window.editor is editor and editor.height() == before
    assert editor.raw == 'shared text' and window.result is result and window.generation == generation

@pytest.mark.parametrize('mode', ['counter', 'planning'])
@pytest.mark.parametrize('height', [368, 391])
def test_short_high_dpi_layout_stays_inside_window(qtbot, window, mode, height):
    from PySide6.QtWidgets import QLayout
    window.setMinimumSize(0, 0)
    window.layout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
    window.resize(642, height)
    window.set_mode(mode)
    qtbot.wait(60)
    bounds = window.shell.rect()
    assert window.editor.height() >= 80
    assert bounds.contains(window.editor.geometry())
    assert bounds.contains(window.results_stack.geometry())
    assert not window.brand_caption.isVisible()
    if mode == 'planning':
        window.activateWindow()
        window.planning.values['unallocated'].setFocus()
        qtbot.wait(20)
        for control in (window.planning.capacity, window.planning.allowance):
            qtbot.keyClick(window.focusWidget(), Qt.Key.Key_Tab)
            qtbot.wait(40)
            assert control.hasFocus()
            rectangle = control.rect().translated(control.mapTo(window.planning.viewport(), control.rect().topLeft()))
            assert window.planning.viewport().rect().contains(rectangle)
    window.resize(1040, 760)
    qtbot.wait(30)
    assert window.brand_caption.isVisible()
