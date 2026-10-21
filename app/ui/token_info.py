"""Compact, standard Qt help for the token result, including keyboard focus."""
from PySide6.QtCore import QPoint, Qt, QTimer, QEvent
from PySide6.QtWidgets import QToolButton, QToolTip


TOKEN_INFORMATION = (
    "Tokens are counted using the selected OpenAI encoding. "
    "Special-token strings are treated as ordinary text. "
    "Results exclude conversation formatting, hidden instructions and other processing overhead."
)


class TokenInformation(QToolButton):
    def __init__(self):
        super().__init__()
        self.setObjectName("tokenInformation")
        self.setText("i")
        self.setFixedSize(20, 20)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAccessibleName("About text token counts")
        self.setAccessibleDescription(TOKEN_INFORMATION)
        # Rich-text detection enables Qt's automatic tooltip wrapping. Qt also
        # positions the tooltip within the screen rather than the parent panel.
        self.setToolTip("<qt>" + TOKEN_INFORMATION + "</qt>")
        self.clicked.connect(self.show_information)

    def show_information(self):
        QToolTip.showText(self.mapToGlobal(QPoint(0, self.height() + 4)),
                          self.toolTip(), self)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        # Qt's tooltip event filter dismisses tips during the focus event.
        # Present it after that event, and only if focus is still here.
        QTimer.singleShot(0, self.show_focused_information)

    def show_focused_information(self):
        if self.hasFocus() and self.isVisible():
            self.show_information()

    def focusOutEvent(self, event):
        QToolTip.hideText()
        super().focusOutEvent(event)

    def leaveEvent(self, event):
        QToolTip.hideText()
        super().leaveEvent(event)

    def hideEvent(self, event):
        QToolTip.hideText()
        super().hideEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            QToolTip.hideText()
            event.accept()
        else:
            super().keyPressEvent(event)

    def event(self, event):
        if (event.type() == QEvent.Type.ShortcutOverride and event.key() == Qt.Key.Key_Escape
                and self.hasFocus() and QToolTip.isVisible()):
            event.accept()
            return True
        return super().event(event)
