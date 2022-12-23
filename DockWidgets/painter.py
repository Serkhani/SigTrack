# from qgis.PyQt.QtWidgets import (QGraphicsView, QGraphicsScene, QVBoxLayout, QHBoxLayout, QWidget, QGraphicsTextItem, QGraphicsRectItem, QToolBar, QUndoStack,
#     QLineEdit, QLabel, QSizePolicy, QPushButton, QFrame, QMenuBar, QAction, qApp, QFileDialog, QMessageBox)
# from qgis.PyQt.QtCore import (Qt, pyqtSignal, QRectF, QRect, QSize, QCoreApplication, QMetaType)
# from qgis.PyQt.QtGui import (QPainterPath, QPainter, QIcon, QPixmap, QImage, QFont, QKeySequence)

from PySide2.QtCore import Qt
from PySide2.QtGui import (QPainter, QBrush, QPen, QColor)


class Painter(QPainter):
    def __init__(self):
        QPainter.__init__(self)
        self.brush = QBrush(QColor(Qt.black))
        self.pen = QPen()

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

