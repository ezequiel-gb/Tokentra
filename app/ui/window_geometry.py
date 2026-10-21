"""Keep the complete native window frame inside a Qt screen's work area.

All coordinates are Qt logical coordinates, never physical pixels or guessed
taskbar/title-bar sizes. Interactive moves/resizes are deliberately not clamped.
"""
from PySide6.QtCore import QObject, QEvent, QRect, QSize, QTimer, Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QLayout

NORMAL_MINIMUM = QSize(680, 540)
DEFAULT_SIZE = QSize(1040, 760)


def choose_work_area(frame, areas, primary=0):
    """Prefer the largest overlap; use the primary for disconnected coordinates."""
    if not areas:
        return QRect()
    overlaps = [frame.intersected(area) for area in areas]
    weights = [max(0, rect.width()) * max(0, rect.height()) for rect in overlaps]
    if max(weights) == 0:
        return QRect(areas[primary if 0 <= primary < len(areas) else 0])
    return QRect(areas[weights.index(max(weights))])


def fit_frame(frame, available, centre=False, inset=0):
    """Contain an outer frame, including negative-origin and top-taskbar screens."""
    if available.isEmpty():
        return QRect(frame)
    # Insets are a first-launch preference, never allowed to exclude a window.
    x_inset = min(inset, max(0, (available.width() - frame.width()) // 2))
    y_inset = min(inset, max(0, (available.height() - frame.height()) // 2))
    bounds = available.adjusted(x_inset, y_inset, -x_inset, -y_inset)
    result = QRect(frame)
    result.setSize(QSize(min(max(1, frame.width()), bounds.width()),
                         min(max(1, frame.height()), bounds.height())))
    if centre:
        result.moveCenter(bounds.center())
    result.moveLeft(max(bounds.left(), min(result.left(), bounds.right() - result.width() + 1)))
    result.moveTop(max(bounds.top(), min(result.top(), bounds.bottom() - result.height() + 1)))
    return result


class WindowGeometry(QObject):
    def __init__(self, window, preferences):
        super().__init__(window)
        self.window = window
        self.initialising = True
        self.normal_geometry = None
        self.restore_target = None
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.ensure_visible)
        window.installEventFilter(self)
        application = QGuiApplication.instance()
        application.screenAdded.connect(self._screen_added)
        application.screenRemoved.connect(self.schedule)
        for screen in application.screens():
            self._screen_added(screen)
        if window.windowHandle():
            window.windowHandle().screenChanged.connect(self.schedule)

        restored = False
        saved = preferences.value("geometry")
        if saved is not None:
            try:
                restored = window.restoreGeometry(saved)
            except (TypeError, ValueError):
                restored = False  # Damaged settings must not prevent startup.
        maximised = restored and window.isMaximized()
        candidate = window.normalGeometry() if restored else QRect()
        if not candidate.isValid():
            candidate = window.geometry()
        # A saved minimised/full-screen state must not hide the startup controls.
        window.setWindowState(Qt.WindowState.WindowNoState)
        if restored:
            window.setGeometry(candidate)
        else:
            window.resize(DEFAULT_SIZE)
        self.ensure_visible(centre=not restored, inset=16 if not restored else 0)
        self.normal_geometry = QRect(window.geometry())
        self.initialising = False
        if maximised:
            window.setWindowState(Qt.WindowState.WindowMaximized)
        self.schedule()

    def _screen_added(self, screen):
        screen.availableGeometryChanged.connect(self.schedule)
        screen.geometryChanged.connect(self.schedule)
        screen.logicalDotsPerInchChanged.connect(self.schedule)
        self.schedule()

    def work_area(self, frame):
        screens = QGuiApplication.screens()
        primary = QGuiApplication.primaryScreen()
        return choose_work_area(frame, [screen.availableGeometry() for screen in screens],
                                screens.index(primary) if primary in screens else 0)

    def schedule(self, *_):
        self.timer.start(0)

    def eventFilter(self, watched, event):
        if self.initialising:
            return False
        expanded = Qt.WindowState.WindowMinimized | Qt.WindowState.WindowMaximized | Qt.WindowState.WindowFullScreen
        if event.type() == QEvent.Type.WindowStateChange:
            was_expanded = bool(event.oldState() & expanded)
            now_expanded = bool(self.window.windowState() & expanded)
            if not was_expanded and now_expanded:
                # On Windows this event precedes the native resize/move events.
                self.normal_geometry = QRect(self.window.geometry())
            elif was_expanded and not now_expanded and self.normal_geometry is not None:
                # A queued repair can see the old maximised frame while Qt's
                # state already says normal. Restore the captured client rect
                # before containment, rather than clamp that transient frame.
                self.restore_target = QRect(self.normal_geometry)
        elif event.type() in (QEvent.Type.Move, QEvent.Type.Resize):
            if not self.window.windowState() & expanded and self.restore_target is None:
                self.normal_geometry = QRect(self.window.geometry())
        if event.type() in (QEvent.Type.Show, QEvent.Type.WindowStateChange,
                            QEvent.Type.ScreenChangeInternal, QEvent.Type.DevicePixelRatioChange):
            self.schedule()
        return False

    def ensure_visible(self, centre=False, inset=0):
        window = self.window
        if window.isMaximized() or window.isFullScreen() or window.isMinimized():
            # Let the window manager handle reserved regions and fullscreen.
            return
        if self.restore_target is not None:
            target, self.restore_target = self.restore_target, None
            window.setGeometry(target)
        frame = window.frameGeometry()
        client = window.geometry()
        available = self.work_area(frame)
        if available.isEmpty():
            return
        frame_width = max(0, frame.width() - client.width())
        frame_height = max(0, frame.height() - client.height())
        maximum_client = QSize(max(1, available.width() - frame_width),
                               max(1, available.height() - frame_height))
        minimum = QSize(min(NORMAL_MINIMUM.width(), maximum_client.width()),
                        min(NORMAL_MINIMUM.height(), maximum_client.height()))
        layout = window.centralWidget().layout()
        # At high scaling a valid work area can be shorter than the usual
        # minimum. Do not let a layout minimum force the title bar off-screen.
        constrained = minimum != NORMAL_MINIMUM
        layout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint if constrained
                                 else QLayout.SizeConstraint.SetDefaultConstraint)
        if constrained:
            window.centralWidget().setMinimumSize(0, 0)
        window.setMinimumSize(minimum)
        target = fit_frame(frame, available, centre, inset)
        size = QSize(max(1, target.width() - frame_width), max(1, target.height() - frame_height))
        if window.size() != size:
            window.resize(size)
        # QWidget.move() positions the outer frame; setGeometry() positions the
        # client rect, so mixing them here would put the title bar above bounds.
        if window.frameGeometry().topLeft() != target.topLeft():
            window.move(target.topLeft())
        self.normal_geometry = QRect(window.geometry())
