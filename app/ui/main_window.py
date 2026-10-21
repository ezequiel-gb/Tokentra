import sys

from PySide6.QtCore import Qt, QTimer, QSignalBlocker, QEvent
from PySide6.QtGui import QAction, QKeySequence, QGuiApplication
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QComboBox, QFrame, QProgressBar, QFileDialog, QButtonGroup)
from app.core.tokenizer import ENCODINGS
from app.core.workers import WorkerQueue, Request
from app.services.settings import settings
from app.ui.editor import TextEditor
from app.ui.theme import STYLE
from app.ui.window_geometry import WindowGeometry
from app.ui.planning import ModeStack, PlanningDashboard
from app.ui.token_info import TokenInformation


class MainWindow(QMainWindow):
    def __init__(self, preferences=None):
        super().__init__()
        self.preferences = preferences if preferences is not None else settings()
        self.generation = 0
        self.result = None
        self.file_path = None
        self.file_only = False
        self.closing = False
        self.setWindowTitle("Tokentra | Precision Token Counter")
        self.setMinimumSize(680, 540)
        self.setStyleSheet(STYLE)
        self.shell = QWidget(objectName="shell")
        self.setCentralWidget(self.shell)
        self.layout = QVBoxLayout(self.shell)
        self.layout.setContentsMargins(30, 26, 30, 22)
        self.layout.setSpacing(12)

        header = QHBoxLayout()
        branding = QVBoxLayout()
        branding.setSpacing(4)
        branding.addWidget(QLabel("TOKENTRA", objectName="brand"))
        self.brand_caption = QLabel("PRECISION TOKEN COUNTER", objectName="eyebrow")
        branding.addWidget(self.brand_caption)
        header.addLayout(branding)
        header.addStretch()
        privacy = QLabel("●  LOCAL & OFFLINE", objectName="eyebrow")
        privacy.setToolTip("No accounts, telemetry, automatic text saving or network requests.")
        header.addWidget(privacy)
        self.layout.addLayout(header)

        navigation = QHBoxLayout()
        self.mode_buttons = QButtonGroup(self)
        self.counter_mode = self.button("Token Counter", lambda: self.set_mode("counter"), "modeButton")
        self.planning_mode = self.button("Context Planning", lambda: self.set_mode("planning"), "modeButton")
        for button in (self.counter_mode, self.planning_mode):
            button.setCheckable(True)
            self.mode_buttons.addButton(button)
            navigation.addWidget(button)
        navigation.addStretch()
        navigation.addWidget(QLabel("Shared text workspace", objectName="muted"))
        self.layout.addLayout(navigation)

        controls = QHBoxLayout()
        controls.setSpacing(10)
        controls.addWidget(QLabel("Tokeniser"))
        self.encoding = QComboBox()
        self.encoding.addItems(ENCODINGS)
        self.encoding.setAccessibleName("OpenAI encoding")
        selected = self.preferences.value("encoding", "o200k_base")
        self.encoding.setCurrentText(selected if selected in ENCODINGS else "o200k_base")
        controls.addWidget(self.encoding)
        controls.addStretch()
        self.import_button = self.button("Import text", lambda: self.choose_file(False), "primary")
        controls.addWidget(self.import_button)
        self.file_button = self.button("Count file", lambda: self.choose_file(True))
        self.file_button.setToolTip("Count a file without loading it into the editor. Exact whole-text counting; requires RAM.")
        controls.addWidget(self.file_button)
        self.layout.addLayout(controls)

        workspace = QHBoxLayout()
        workspace.addWidget(QLabel("TEXT WORKSPACE", objectName="eyebrow"))
        workspace.addStretch()
        self.source = QLabel("Plain text · nothing saved", objectName="muted")
        workspace.addWidget(self.source)
        self.layout.addLayout(workspace)
        self.editor = TextEditor()
        self.editor.setMinimumHeight(80)
        self.layout.addWidget(self.editor, 1)

        actions = QHBoxLayout()
        self.paste_button = self.button("Paste", self.paste)
        self.copy_button = self.button("Copy text", self.copy_text)
        self.clear_button = self.button("Clear", self.clear)
        for button in (self.paste_button, self.copy_button, self.clear_button):
            actions.addWidget(button)
        actions.addStretch()
        self.status = QLabel("Ready", objectName="muted")
        self.status.setAccessibleName("Processing status")
        self.status.setWordWrap(True)
        self.status.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        actions.addWidget(self.status, 1)
        self.layout.addLayout(actions)

        panel = QFrame(objectName="panel")
        dashboard = QHBoxLayout(panel)
        self.metrics_layout = dashboard
        dashboard.setContentsMargins(22, 14, 22, 16)
        dashboard.setSpacing(24)
        self.token_information = TokenInformation()
        self.tokens = self.metric(dashboard, "TEXT TOKENS", "tokenValue", self.token_information)
        self.words = self.metric(dashboard, "WORDS", "metricValue")
        self.characters = self.metric(dashboard, "CHARACTERS", "metricValue")
        dashboard.addStretch()
        self.copy_count = self.button("Copy count", self.copy_tokens)
        dashboard.addWidget(self.copy_count)
        self.results_stack = ModeStack()
        self.results_stack.setMinimumHeight(100)
        self.results_stack.addWidget(panel)
        self.planning = PlanningDashboard(self.preferences)
        self.results_stack.addWidget(self.planning)
        self.layout.addWidget(self.results_stack)
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(3)
        self.progress.setVisible(False)
        self.layout.addWidget(self.progress)

        self.queue = WorkerQueue(self)
        self.queue.completed.connect(self._completed)
        self.queue.idle.connect(self._idle)
        self.debounce = QTimer(self)
        self.debounce.setSingleShot(True)
        self.debounce.setInterval(220)
        self.debounce.timeout.connect(self._submit)
        self.editor.textChanged.connect(self._changed)
        self.encoding.currentTextChanged.connect(self._encoding_changed)
        self.shortcut(QKeySequence.StandardKey.Open, lambda: self.choose_file(False))
        self.shortcut(QKeySequence("Ctrl+Shift+C" if sys.platform != "darwin" else "Meta+Shift+C"), self.copy_tokens)
        self.shortcut(QKeySequence("Ctrl+L" if sys.platform != "darwin" else "Meta+L"), self.clear)
        self.shortcut(QKeySequence("F11"), self.toggle_fullscreen)
        self.shortcut(QKeySequence("Escape"), self.exit_fullscreen)
        self.shortcut(QKeySequence.StandardKey.Quit, self.close)
        self.set_mode("planning" if self.preferences.value("mode", "counter") == "planning" else "counter")
        self._window_finish()
        self.window_geometry = WindowGeometry(self, self.preferences)
        self._invalidate()
        self._submit()  # Verify default assets even with an empty editor.

    @staticmethod
    def button(text, callback, name=""):
        button = QPushButton(text)
        button.setObjectName(name)
        button.setAccessibleName(text)
        button.clicked.connect(callback)
        return button

    @staticmethod
    def metric(layout, name, style, information=None):
        column = QVBoxLayout()
        column.setSpacing(3)
        heading = QHBoxLayout()
        heading.setSpacing(7)
        heading.addWidget(QLabel(name, objectName="eyebrow"))
        if information is not None:
            heading.addWidget(information)
        heading.addStretch()
        column.addLayout(heading)
        value = QLabel("0", objectName=style)
        value.setAccessibleName(name)
        value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        column.addWidget(value)
        layout.addLayout(column)
        return value

    def shortcut(self, key, callback):
        action = QAction(self)
        action.setShortcut(key)
        action.triggered.connect(callback)
        self.addAction(action)

    def _invalidate(self):
        self.generation += 1
        self.result = None
        self.queue.discard_pending()
        for metric in (self.tokens, self.words, self.characters):
            metric.setText("…")
        self.copy_count.setEnabled(False)
        self.progress.setVisible(True)
        self.status.setText("Waiting for latest text…")
        self.planning.set_tokens(None, "Waiting for the latest text count…")

    def _changed(self):
        self.file_path = None
        self.file_only = False
        self.source.setText("Plain text · nothing saved")
        self._invalidate()
        self.debounce.start()

    def _encoding_changed(self):
        self._invalidate()
        self.debounce.stop()
        self._submit()

    def _submit(self):
        self.status.setText("Reading and counting…" if self.file_path else "Counting locally…")
        self.queue.submit(Request(self.generation, self.encoding.currentText(),
                                  "" if self.file_path else self.editor.raw,
                                  self.file_path, self.file_only))

    def _completed(self, request, result, text, error):
        if request.generation != self.generation:
            return
        self.progress.setVisible(False)
        if error:
            self.status.setText(error)
            self.file_path = None
            self.file_only = False
            self.planning.set_tokens(None, error)
            return
        if request.path and not request.file_only:
            try:
                with QSignalBlocker(self.editor):
                    self.editor.set_exact_text(text)
            except MemoryError:
                self.status.setText("Not enough memory to display this document. Use Count file.")
                self.file_path = None
                self.planning.set_tokens(None, "Not enough memory to display the imported text.")
                return
            self.file_path = None  # Future encoding changes count this in-memory snapshot.
            self.source.setText("Imported text · original line endings")
        elif request.file_only:
            self.source.setText("FILE RESULT · editor edits return to text")
        self.result = result
        self.planning.set_tokens(None if request.file_only else result.tokens,
            "Count file is a separate result. Edit or import text into the shared workspace to plan it." if request.file_only else "")
        self.tokens.setText(f"{result.tokens:,}")
        self.words.setText(f"{result.words:,}")
        self.characters.setText(f"{result.characters:,}")
        self.copy_count.setEnabled(True)
        self.status.setText(f"{result.encoding} · {result.elapsed * 1000:,.0f} ms" +
                            (" · file result" if request.file_only else " · up to date"))

    def paste(self):
        self.editor.setFocus()
        self.editor.paste()

    def set_mode(self, mode):
        self.mode = "planning" if mode == "planning" else "counter"
        self.results_stack.setCurrentIndex(1 if self.mode == "planning" else 0)
        self.counter_mode.setChecked(self.mode == "counter")
        self.planning_mode.setChecked(self.mode == "planning")
        # The counter keeps the editor dominant. Planning shares the available
        # height with its dashboard, without a fixed cap or a second editor.
        self.layout.setStretchFactor(self.editor, 1)
        self.layout.setStretchFactor(self.results_stack, 3 if self.mode == "planning" else 0)
        self.results_stack.updateGeometry()

    def copy_text(self):
        QApplication.clipboard().setText(self.editor.raw)

    def copy_tokens(self):
        if self.result is not None:
            QApplication.clipboard().setText(str(self.result.tokens))

    def clear(self):
        self.debounce.stop()
        with QSignalBlocker(self.editor):
            self.editor.set_exact_text("")
        self._changed()
        self.editor.setFocus()

    def choose_file(self, file_only):
        path, _ = QFileDialog.getOpenFileName(self, "Count file" if file_only else "Import plain text",
                                             "", "Plain text (*.txt);;Text files (*)")
        if path:
            self.import_path(path, file_only)

    def import_path(self, path, file_only=False):
        self.debounce.stop()
        self._invalidate()
        self.file_path = str(path)
        self.file_only = file_only
        self._submit()

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.exit_fullscreen()
        else:
            self.was_maximised = self.isMaximized()
            self.showFullScreen()

    def exit_fullscreen(self):
        if self.isFullScreen():
            self.showMaximized() if getattr(self, "was_maximised", False) else self.showNormal()

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == QEvent.Type.WindowStateChange and hasattr(self, "layout"):
            self._window_finish()

    def _window_finish(self):
        expanded = self.isMaximized() or self.isFullScreen()
        self._adapt_spacing()
        # Native decorations retain OS dragging, resizing, snapping and accessibility.
        # DWM handles real outside corners on Windows 11, including square maximisation.
        if sys.platform == "win32":
            try:
                import ctypes
                preference = ctypes.c_int(1 if expanded else 2)  # DONOTROUND / ROUND
                ctypes.windll.dwmapi.DwmSetWindowAttribute(int(self.winId()), 33,
                                                          ctypes.byref(preference), 4)
                dark = ctypes.c_int(1)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(int(self.winId()), 20, ctypes.byref(dark), 4)
            except (OSError, AttributeError):
                pass  # Older Windows keeps reliable native rectangular chrome.

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "metrics_layout"):
            self._adapt_spacing()

    def _adapt_spacing(self):
        # At high DPI a laptop can expose less than 400 logical pixels of
        # height. Reclaim decoration/spacing before sacrificing a text line or
        # letting the dashboard extend beyond the window's visible bounds.
        compact = self.height() < 500
        very_short = self.height() < 400
        expanded = self.isMaximized() or self.isFullScreen()
        margin = 22 if expanded or compact else 30
        vertical = 4 if very_short else 8
        self.layout.setContentsMargins(margin, vertical if compact else (22 if expanded else 26),
                                       margin, vertical if compact else 22)
        self.layout.setSpacing((2 if very_short else 4) if compact else 12)
        self.brand_caption.setVisible(not compact)
        self.metrics_layout.setContentsMargins(22, 8 if compact else 14, 22, 8 if compact else 16)

    def closeEvent(self, event):
        if self.queue.active:
            self.closing = True
            self.debounce.stop()
            self.queue.stop()
            self.setEnabled(False)
            self.status.setText("Finishing active calculation before closing…")
            event.ignore()
            return
        self.preferences.setValue("geometry", self.saveGeometry())
        self.preferences.setValue("encoding", self.encoding.currentText())
        self.preferences.setValue("mode", self.mode)
        self.planning.save_preferences(self.preferences)
        self.preferences.sync()
        event.accept()

    def _idle(self):
        if self.closing:
            self.close()
