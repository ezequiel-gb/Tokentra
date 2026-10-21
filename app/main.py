import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from pathlib import Path
from app.ui.main_window import MainWindow
from app import DISPLAY_VERSION
from app.services.windows import initialise_windows


def main():
    initialise_windows()
    if "--ui-check" in sys.argv:
        from app.ui_check import run
        return run()
    if "--window-check" in sys.argv:
        from app.window_check import run
        return run()
    if "--offline-check" in sys.argv:
        from app.offline_check import run
        return run()
    application = QApplication(sys.argv)
    application.setApplicationName("Tokentra")
    application.setOrganizationName("Tokentra")
    application.setApplicationVersion(DISPLAY_VERSION)
    application.setWindowIcon(QIcon(str(Path(__file__).parent / "assets/icon.png")))
    window = MainWindow()
    window.show()
    return application.exec()


if __name__ == "__main__":
    sys.exit(main())
