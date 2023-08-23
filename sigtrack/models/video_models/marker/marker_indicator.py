from PySide2.QtWidgets import QGraphicsRectItem, QGraphicsSceneMouseEvent, QColorDialog
from PySide2.QtGui import QColor, QBrush
from PySide2.QtCore import QRectF

class MarkerIndicator(QGraphicsRectItem):
    """
        An indicator for each marker
    """
    
    def __init__(self):
        self.color = QColor()
        self.setRect(QRectF(0.0,0.0,2.0,2.0))
        self.brush:QBrush = QBrush(self.color)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
            show QColor dialog to pick color to be used to indicate the marker
        """        
        color = QColorDialog.getColor(QColor.black, title="Indicator color: ")
        if color.isValid():
            self.color = color
            self.brush.setColor(self.color)
            self.update() #repaint with new color
        return super().mousePressEvent(event)