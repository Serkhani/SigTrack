from PySide2.QtWidgets import QGraphicsItem, QLabel
from PySide2.QtGui import QColor
from PySide2.QtCore import QUrl

from sigtrack.models.video_models.marker.marker_indicator import MarkerIndicator
import sigtrack.resources.compiled.map_rc


class VideoMarker(QGraphicsItem):
    def __init__(self):
        super().__init__()
        self.icon =  QUrl("qrc://:/marker")
        self.markerIndicator:MarkerIndicator = MarkerIndicator()
        self.setFlags(
            QGraphicsItem.ItemToolTipHasChanged | 
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemIsSelectable 
        )
    
    def change_text(self, data: list) -> None:
        """
        Change the text when the button is clicked
        """
        self.setToolTip(f"lat: {data[0]} lon: {data[1]}")