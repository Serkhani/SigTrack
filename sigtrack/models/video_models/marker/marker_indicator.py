from PySide2.QtWidgets import QGraphicsRectItem, QGraphicsSceneMouseEvent, QColorDialog
from PySide2.QtGui import QColor, QBrush
from PySide2.QtCore import QRectF

class MarkerIndicator(QGraphicsRectItem):
    """
        An indicator for each marker
    """
    
    def __init__(self, rect:QRectF, color:QColor):
        super().__init__()
        self.color = color
        self.qrect = rect
        self.setRect(QRectF(self.qrect.left()+((self.qrect.right()-self.qrect.left())/2),self.qrect.bottom(),5.0,5.0))
        self.brush:QBrush = QBrush(self.color)
        self.setBrush(self.brush)

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