# from qgis.PyQt.QtWidgets import (QGraphicsView, QGraphicsScene, QVBoxLayout, QHBoxLayout, QWidget, QGraphicsTextItem, QGraphicsRectItem, QToolBar, QUndoStack,
#     QLineEdit, QLabel, QSizePolicy, QPushButton, QFrame, QMenuBar, QAction, qApp, QFileDialog, QMessageBox)
# from qgis.PyQt.QtCore import (Qt, pyqtSignal, QRectF, QRect, QSize, QCoreApplication, QMetaType)
# from qgis.PyQt.QtGui import (QPainterPath, QPainter, QIcon, QPixmap, QImage, QFont, QKeySequence)

from PyQt5.QtWidgets import (QGraphicsView, QGraphicsScene, QVBoxLayout, QHBoxLayout, QWidget, QGraphicsTextItem, QGraphicsRectItem, QToolBar, QUndoStack,
    QLineEdit, QLabel, QSizePolicy, QPushButton, QFrame, QMenuBar, QAction, qApp, QFileDialog, QMessageBox)
from PyQt5.QtCore import (Qt, pyqtSignal, QRectF, QRect, QSize, QCoreApplication, QMetaType)
from PyQt5.QtGui import (QPainterPath, QPainter, QIcon, QBrush, QPen, QColor, QPixmap, QImage, QFont, QKeySequence)


class Painter(QPainter):
    def __init__(self):
        QPainter.__init__(self)
        self.brush = QBrush(QColor(Qt.black))
        self.pen = QPen()
        self.pen.setBrush(self.brush)
#        self.setPen(self.pen)

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
