from PySide6.QtCore import QSettings


def settings():
    return QSettings("Tokentra", "Tokentra")
