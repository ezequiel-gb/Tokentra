"""Render actual application widgets for review, without persisting sample text."""
import os
from pathlib import Path
import sys
import tempfile
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtCore import QSettings, QEventLoop, QTimer
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
from app.ui.main_window import MainWindow

app = QApplication([])
if sys.platform == "win32" and not QFontDatabase.families():
    # Qt's offscreen plugin has no native Windows font discovery.
    for font in ("segoeui.ttf", "seguisb.ttf", "seguiemj.ttf", "msyh.ttc"):
        QFontDatabase.addApplicationFont(str(Path("C:/Windows/Fonts") / font))
with tempfile.TemporaryDirectory() as directory:
    window = MainWindow(QSettings(str(Path(directory) / "settings.ini"), QSettings.Format.IniFormat))
    window.show()
    window.editor.set_exact_text("Precision begins with the right measure.\n\n"
                                 "A private workspace for prompts, prose and code.\n"
                                 "Count every token locally, with the encoding you choose.\n\n"
                                 "def hello(name):\n    return f'Hello, {name}!'\n\n"
                                 "Hello · Bonjour · こんにちは · مرحباً 👋")
    loop = QEventLoop()
    QTimer.singleShot(1500, loop.quit)
    loop.exec()
    for name, width, height in (("desktop", 1120, 820), ("compact", 680, 540)):
        window.resize(width, height)
        app.processEvents()
        window.grab().save(str(Path("docs") / f"ui-{name}.png"))
    window.set_mode("planning")
    for name, width, height in (("planning-desktop", 1120, 820), ("planning-compact", 680, 540)):
        window.resize(width, height)
        for _ in range(5):
            app.processEvents()
        window.grab().save(str(Path("docs/rc2") / f"{name}.png"))
    window.planning.capacity.setText("50")
    window.planning.allowance.setText("100")
    window.resize(1120, 820)
    for _ in range(5):
        app.processEvents()
    window.grab().save("docs/rc2/planning-overflow.png")
    window.close()
