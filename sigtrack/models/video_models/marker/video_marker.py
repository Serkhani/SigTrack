from PySide2.QtWidgets import QGraphicsItem, QLabel, QGraphicsPixmapItem, QGraphicsScene
from PySide2.QtGui import QColor, QPixmap
from PySide2.QtCore import QUrl, QRect

from sigtrack.models.video_models.marker.marker_indicator import MarkerIndicator
import sigtrack.resources.compiled.vid_icons_rc


class VideoMarker(QGraphicsPixmapItem):
    def __init__(self, color: QColor):
        self.customPixmap =  QPixmap(":/vidMarker")
        super().__init__(self.customPixmap)
        self.color = color
        self.markerIndicator:MarkerIndicator = MarkerIndicator(self.customPixmap.rect(), color)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
    
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            self.markerIndicator.setPos(value)
        return super().itemChange(change, value)

    def change_text(self, data: list) -> None:
        """
        Change the text when the button is clicked
        """
        self.setToolTip(f"lat: {data[0]} lon: {data[1]}")