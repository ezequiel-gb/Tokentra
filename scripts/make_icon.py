"""Draw the product's small native icon using Qt, with no runtime image dependency."""
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QImage, QPainter, QColor, QPen, QLinearGradient
from PySide6.QtCore import Qt, QRectF

app = QApplication([])
image = QImage(256, 256, QImage.Format.Format_ARGB32)
image.fill(Qt.GlobalColor.transparent)
painter = QPainter(image)
painter.setRenderHint(QPainter.RenderHint.Antialiasing)
gradient = QLinearGradient(0, 0, 256, 256)
gradient.setColorAt(0, QColor("#245985"))
gradient.setColorAt(1, QColor("#081626"))
painter.setBrush(gradient)
painter.setPen(QPen(QColor("#487FA8"), 3))
painter.drawRoundedRect(QRectF(7, 7, 242, 242), 48, 48)
painter.setPen(QPen(QColor("#A8DFFF"), 17, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
painter.drawLine(65, 82, 191, 82)
painter.drawLine(128, 82, 128, 185)
painter.setPen(QPen(QColor("#3178C6"), 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
painter.drawLine(68, 133, 91, 133)
painter.drawLine(166, 133, 189, 133)
painter.end()
root = Path(__file__).resolve().parents[1] / "app/assets"
image.save(str(root / "icon.png"))
image.save(str(root / "icon.ico"))
