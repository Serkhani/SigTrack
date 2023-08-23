from PySide2.QtWidgets import QGraphicsRectItem
from PySide2.QtGui import QColor, QBrush
from PySide2.QtCore import QRectF

class MarkerIndicator(QGraphicsRectItem):
    """
        An indicator for each marker
    """
    
    def __init__(self, color:QColor):
        self.color = color
        self.setRect(QRectF(0.0,0.0,2.0,2.0))
        self.brush:QBrush = QBrush(self.color)