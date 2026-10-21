"""Keep original CRLF/CR and pasted text while Qt displays normalised newlines."""
from PySide6.QtWidgets import QPlainTextEdit


def raw_offset(text, qt_position):
    index = units = 0
    while index < len(text) and units < qt_position:
        character = text[index]
        if character == "\r" and text[index:index + 2] == "\r\n":
            index += 2
        else:
            index += 1
        units += 2 if ord(character) > 0xFFFF else 1
    return index


class TextEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.raw = ""
        self.setting = False
        self.pasting = None
        self.document().contentsChange.connect(self._contents_changed)
        self.setAcceptDrops(True)
        self.setPlaceholderText("Paste, type or import your text here…\n\nEverything stays on your device.")
        self.setAccessibleName("Text workspace")

    def set_exact_text(self, text):
        self.setting = True
        try:
            self.setPlainText(text)
            self.raw = text
        finally:
            self.setting = False

    def insertFromMimeData(self, source):
        self.pasting = source.text() if source.hasText() else None
        try:
            super().insertFromMimeData(source)
        finally:
            self.pasting = None

    def _contents_changed(self, position, removed, added):
        if self.setting:
            return
        start = raw_offset(self.raw, position)
        end = raw_offset(self.raw, position + removed)
        if self.pasting is not None:
            inserted = self.pasting
        else:
            display = self.toPlainText().encode("utf-16-le", errors="surrogatepass")
            inserted = display[position * 2:(position + added) * 2].decode("utf-16-le", errors="surrogatepass")
        self.raw = self.raw[:start] + inserted + self.raw[end:]
