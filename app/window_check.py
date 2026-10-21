"""Explicit native window smoke test using isolated synthetic preferences only."""
import json
from pathlib import Path
import sys
import tempfile
import time


def windows_visible_bounds(window):
    """Read physical visible-frame/work-area bounds, avoiding Qt DPI rounding."""
    import ctypes
    from ctypes import wintypes
    class MonitorInfo(ctypes.Structure):
        _fields_ = [("size", wintypes.DWORD), ("monitor", wintypes.RECT),
                    ("work", wintypes.RECT), ("flags", wintypes.DWORD)]
    user = ctypes.windll.user32
    user.MonitorFromWindow.argtypes = [wintypes.HWND, wintypes.DWORD]
    user.MonitorFromWindow.restype = wintypes.HANDLE
    user.GetMonitorInfoW.argtypes = [wintypes.HANDLE, ctypes.POINTER(MonitorInfo)]
    user.GetMonitorInfoW.restype = wintypes.BOOL
    info = MonitorInfo()
    info.size = ctypes.sizeof(info)
    monitor = user.MonitorFromWindow(int(window.winId()), 2)
    if not user.GetMonitorInfoW(monitor, ctypes.byref(info)):
        raise OSError("Cannot inspect native monitor work area")
    visible = wintypes.RECT()
    dwm = ctypes.windll.dwmapi
    dwm.DwmGetWindowAttribute.argtypes = [wintypes.HWND, wintypes.DWORD, wintypes.LPVOID, wintypes.DWORD]
    if dwm.DwmGetWindowAttribute(int(window.winId()), 9, ctypes.byref(visible), ctypes.sizeof(visible)) != 0:
        raise OSError("Cannot inspect DWM visible frame")
    bounds = lambda rect: [rect.left, rect.top, rect.right, rect.bottom]
    contained = (info.work.left <= visible.left and info.work.top <= visible.top
                 and info.work.right >= visible.right and info.work.bottom >= visible.bottom)
    return dict(visible_physical=bounds(visible), work_physical=bounds(info.work), contained=contained)


def _run():
    from PySide6.QtCore import QByteArray, QEventLoop, QSettings, QTimer, QObject, QEvent
    from PySide6.QtWidgets import QApplication, QWidget
    from app.offline_check import deny_network
    from app.ui.main_window import MainWindow
    sys.addaudithook(deny_network)
    application = QApplication.instance() or QApplication(["Tokentra window verification"])

    def wait_until(predicate, seconds=10):
        deadline = time.monotonic() + seconds
        while not predicate():
            if time.monotonic() > deadline:
                raise AssertionError("Window verification timed out")
            loop = QEventLoop()
            QTimer.singleShot(20, loop.quit)
            loop.exec()
        # Process the queued post-show/frame/state repair as well.
        application.processEvents()

    def snapshot(window, name):
        frame, area = window.frameGeometry(), window.screen().availableGeometry()
        assert area.contains(frame), f"{name}: outer frame is outside work area"
        return dict(case=name, frame=frame.getRect(), available=area.getRect(),
                    device_pixel_ratio=window.devicePixelRatioF())

    records = []
    class Trace(QObject):
        def eventFilter(self, watched, event):
            if event.type() in (QEvent.Type.Move, QEvent.Type.Resize, QEvent.Type.WindowStateChange):
                records.append(dict(event=event.type().name, state=watched.windowState().value,
                                    client=watched.geometry().getRect(), frame=watched.frameGeometry().getRect(),
                                    normal=watched.normalGeometry().getRect()))
            return False
    with tempfile.TemporaryDirectory() as folder:
        for name in ("first-launch", "valid-saved", "invalid-saved", "oversized-saved", "corrupt-saved"):
            preferences = QSettings(str(Path(folder) / (name + ".ini")), QSettings.Format.IniFormat)
            if name == "corrupt-saved":
                preferences.setValue("geometry", QByteArray(b"invalid"))
            elif name != "first-launch":
                holder = QWidget()
                area = application.primaryScreen().availableGeometry()
                holder.resize(720, 560)
                holder.move(area.left() + 32, area.top() + 32)
                if name == "invalid-saved":
                    holder.move(-20000, -20000)
                elif name == "oversized-saved":
                    holder.resize(area.width() * 2, area.height() * 2)
                    holder.move(area.left(), area.top() - 400)
                preferences.setValue("geometry", holder.saveGeometry())
                holder.close()
            window = MainWindow(preferences)
            trace = Trace(window)
            window.installEventFilter(trace)
            window.show()
            wait_until(lambda: window.result is not None and not window.window_geometry.timer.isActive())
            records.append(snapshot(window, name))
            if name == "first-launch":
                before = window.geometry()
                window.showMaximized()
                wait_until(window.isMaximized)
                # Qt's state flag precedes the DWM animation. Inspect the
                # settled physical frame, including when launched hidden by
                # an installer verification harness.
                if sys.platform == "win32":
                    def maximised_frame_ready():
                        bounds = windows_visible_bounds(window)
                        visible, work = bounds["visible_physical"], bounds["work_physical"]
                        return bounds["contained"] and visible == work
                    wait_until(maximised_frame_ready)
                physical = windows_visible_bounds(window) if sys.platform == "win32" else None
                if physical is not None:
                    assert physical["contained"], f"Visible maximised frame outside work area: {physical}"
                records.append(dict(case="maximised", frame=window.frameGeometry().getRect(),
                                    client=window.geometry().getRect(), available=window.screen().availableGeometry().getRect(),
                                    native_bounds=physical))
                window.showNormal()
                wait_until(lambda: not window.isMaximized() and not window.window_geometry.timer.isActive())
                records.append(snapshot(window, "restored"))
                assert window.geometry() == before, f"Restore changed normal geometry: {before.getRect()} -> {window.geometry().getRect()}: {records}"
                window.showMinimized()
                wait_until(window.isMinimized)
                window.showNormal()
                wait_until(lambda: not window.isMinimized() and not window.window_geometry.timer.isActive())
                records.append(snapshot(window, "reopened"))
                window.toggle_fullscreen()
                wait_until(window.isFullScreen)
                window.exit_fullscreen()
                wait_until(lambda: not window.isFullScreen() and not window.window_geometry.timer.isActive())
                records.append(snapshot(window, "left-fullscreen"))
                window.resize(max(window.minimumWidth(), window.width() - 40),
                              max(window.minimumHeight(), window.height() - 40))
                window.window_geometry.ensure_visible()
                records.append(snapshot(window, "resized"))
            window.close()
            assert set(preferences.allKeys()) == {"geometry", "encoding", "mode", "context_capacity", "additional_allowance"}
    result = dict(status="passed", platform=application.platformName(), records=records,
                  scope="Programmatic native Qt transitions; not physical monitor/scaling reconfiguration or manual dragging")
    if "--report" in sys.argv:
        Path(sys.argv[sys.argv.index("--report") + 1]).write_text(json.dumps(result, indent=2), "utf-8")
    elif sys.stdout is not None:
        print(json.dumps(result, indent=2))
    return 0


def run():
    try:
        return _run()
    except Exception as error:
        # Explicit diagnostics use synthetic settings and return a structured
        # failure instead of leaving a frozen-GUI traceback dialog open.
        if "--report" in sys.argv:
            Path(sys.argv[sys.argv.index("--report") + 1]).write_text(
                json.dumps(dict(status="failed", error=str(error)), indent=2), "utf-8")
        elif sys.stderr is not None:
            print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(run())
