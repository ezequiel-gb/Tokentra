import pytest
from PySide6.QtCore import QByteArray, QRect, QSettings, Qt
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QGuiApplication
from app.ui.main_window import MainWindow
from app.ui.window_geometry import WindowGeometry, choose_work_area, fit_frame


@pytest.mark.parametrize("area,frame", [
    (QRect(0, 0, 1920, 1040), QRect(200, -200, 1000, 800)),
    (QRect(0, 48, 1920, 1032), QRect(10, 0, 1000, 800)),
    (QRect(80, 0, 1840, 1080), QRect(0, 20, 1000, 800)),
    (QRect(-1920, 0, 1920, 1040), QRect(-2300, -50, 2200, 1200)),
    (QRect(0, 0, 960, 500), QRect(0, 0, 1120, 820)),
    (QRect(0, 0, 683, 360), QRect(600, -700, 1120, 820)),
])
def test_full_frame_containment(area, frame):
    repaired = fit_frame(frame, area)
    assert area.contains(repaired)
    assert fit_frame(repaired, area) == repaired


def test_partial_overlap_is_not_enough():
    area = QRect(0, 40, 1280, 680)
    frame = QRect(100, -600, 1000, 820)
    assert area.intersects(frame)  # The old guard accepted this inaccessible title bar.
    assert not area.contains(frame)
    assert area.contains(fit_frame(frame, area))


def test_valid_geometry_is_preserved():
    frame = QRect(160, 100, 900, 650)
    assert fit_frame(frame, QRect(0, 0, 1920, 1040)) == frame


def test_screen_choice_and_disconnection():
    left, primary = QRect(-1600, 0, 1600, 860), QRect(0, 40, 1920, 1000)
    assert choose_work_area(QRect(-1400, 50, 1000, 700), [left, primary], 1) == left
    assert choose_work_area(QRect(-1400, 50, 1000, 700), [primary]) == primary
    assert choose_work_area(QRect(99999, -9999, 1000, 700), [left, primary], 1) == primary


def create_window(qtbot, tmp_path, monkeypatch, area, saved=None):
    monkeypatch.setattr(WindowGeometry, "work_area", lambda self, frame: QRect(area))
    preferences = QSettings(str(tmp_path / "geometry.ini"), QSettings.Format.IniFormat)
    if saved is not None:
        preferences.setValue("geometry", saved)
    window = MainWindow(preferences)
    qtbot.addWidget(window)
    window.show()
    qtbot.waitUntil(lambda: window.result is not None, timeout=15000)
    return window


@pytest.mark.parametrize("area", [QRect(0, 40, 1280, 680), QRect(35, 20, 900, 530), QRect(0, 0, 683, 360)])
def test_first_show_complete_native_frame(qtbot, tmp_path, monkeypatch, area):
    window = create_window(qtbot, tmp_path, monkeypatch, area)
    assert area.contains(window.frameGeometry())
    assert not window.windowFlags() & Qt.WindowType.FramelessWindowHint


@pytest.mark.parametrize("saved", [QByteArray(b"damaged geometry"), "wrong settings type"])
def test_corrupt_settings_fall_back(qtbot, tmp_path, monkeypatch, saved):
    area = QRect(0, 32, 1100, 720)
    window = create_window(qtbot, tmp_path, monkeypatch, area, saved)
    assert area.contains(window.frameGeometry())


def test_restored_partial_frame_is_clamped(qtbot, tmp_path, monkeypatch):
    # Isolate the application's guard from Qt's own platform-dependent restore repair.
    def restore(window, saved):
        window.resize(1200, 900)
        window.move(100, -400)
        return True
    monkeypatch.setattr(MainWindow, "restoreGeometry", restore)
    area = QRect(20, 48, 960, 520)
    window = create_window(qtbot, tmp_path, monkeypatch, area, QByteArray(b"simulated saved state"))
    assert area.contains(window.frameGeometry())


def test_valid_saved_geometry_roundtrip(qtbot, tmp_path, monkeypatch):
    # Qt itself validates restoreGeometry against the real test screen before
    # our injected work-area policy runs, so keep this roundtrip on that screen.
    area = QGuiApplication.primaryScreen().availableGeometry()
    window = create_window(qtbot, tmp_path, monkeypatch, area)
    window.resize(700, 580)
    window.move(area.left() + 30, area.top() + 50)
    qtbot.wait(10)
    before = window.geometry()
    window.close()
    other = MainWindow(window.preferences)
    qtbot.addWidget(other)
    other.show()
    qtbot.waitUntil(lambda: other.result is not None, timeout=15000)
    assert other.geometry() == before


def test_screen_change_and_restore_are_repaired(qtbot, tmp_path, monkeypatch):
    area = QRect(0, 0, 1600, 1000)
    window = create_window(qtbot, tmp_path, monkeypatch, area)
    reduced = QRect(20, 40, 900, 520)
    monkeypatch.setattr(window.window_geometry, "work_area", lambda frame: reduced)
    window.move(1200, -100)
    window.window_geometry.schedule()  # QScreen geometry/disconnection/DPI signals use this path.
    qtbot.waitUntil(lambda: reduced.contains(window.frameGeometry()))
    window.showMaximized()
    qtbot.waitUntil(window.isMaximized)
    window.showNormal()
    qtbot.waitUntil(lambda: not window.isMaximized() and reduced.contains(window.frameGeometry()))
    window.toggle_fullscreen()
    window.exit_fullscreen()
    qtbot.waitUntil(lambda: reduced.contains(window.frameGeometry()))


def test_saved_minimised_state_does_not_hide_startup(qtbot, tmp_path, monkeypatch):
    holder = QWidget()
    holder.resize(800, 600)
    holder.setWindowState(Qt.WindowState.WindowMinimized)
    saved = holder.saveGeometry()
    window = create_window(qtbot, tmp_path, monkeypatch, QRect(0, 0, 1280, 900), saved)
    assert not window.isMinimized()


def test_maximise_restore_preserves_normal_rect(qtbot, tmp_path, monkeypatch):
    area = QGuiApplication.primaryScreen().availableGeometry()
    window = create_window(qtbot, tmp_path, monkeypatch, area)
    window.resize(700, 580)
    window.move(area.left() + 30, area.top() + 50)
    before = window.geometry()
    window.showMaximized()
    qtbot.waitUntil(window.isMaximized)
    window.showNormal()
    qtbot.waitUntil(lambda: not window.window_geometry.timer.isActive())
    assert window.geometry() == before


def test_saved_maximised_geometry_has_valid_normal_restore(qtbot, tmp_path, monkeypatch):
    area = QGuiApplication.primaryScreen().availableGeometry()
    window = create_window(qtbot, tmp_path, monkeypatch, area)
    window.resize(700, 580)
    window.move(area.left() + 30, area.top() + 50)
    before = window.geometry()
    window.showMaximized()
    window.close()
    other = MainWindow(window.preferences)
    qtbot.addWidget(other)
    other.show()
    qtbot.waitUntil(lambda: other.result is not None, timeout=15000)
    assert other.isMaximized()
    other.showNormal()
    qtbot.waitUntil(lambda: not other.window_geometry.timer.isActive())
    assert other.geometry() == before
