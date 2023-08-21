from PySide2.QtCore import Qt
from PySide2.QtGui import (QPainter, QBrush, QPen, QFont, QColor)


class Painter(QPainter):
    def __init__(self):
        QPainter.__init__(self)
        self.brush = QBrush(QColor(Qt.black))
        self.pen = QPen()
        self.font = QFont()
        self.font.setPointSize(50)

    def setFontFamily(self, family):
        self.font.setFamily(family)

    def setFontBold(self, condition):
        self.font.setBold(condition)

    def setFontPointSize(self, size):
        self.font.setPointSize(size)

    def setStrokeWidth(self, width):
        self.pen.setWidth(width)

    def setStrokeColor(self, color):
        self.pen.setColor(color)
        
    def setStrokeStyle(self, style):
        self.pen.setStyle(style)

    def setFillColor(self, color):
        self.brush.setColor(color)

    def setFillStyle(self, style):
        self.brush.setStyle(style)

    def setFillDefault(self):
        self.brush = QBrush(QColor(Qt.black))

    def setStrokeDefault(self):
        self.pen = QPen()

