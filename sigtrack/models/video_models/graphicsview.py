from PySide2.QtWidgets import QGraphicsView, QGraphicsScene, QGridLayout
from PySide2.QtGui import QResizeEvent, QShowEvent
from PySide2.QtCore import Qt, QSizeF
 
from sigtrack.models.video_models.custom_videographicsitem import VideoGraphicsItem
from sigtrack.controllers.markerpopupCon import MarkerPopUpCon

class VideoGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.customScene = QGraphicsScene()
        self.setScene(self.customScene)
        self.videoGraphicsItem = VideoGraphicsItem()
        self.customScene.addItem(self.videoGraphicsItem)
        self.markerPopUp = MarkerPopUpCon()
        self.markerPopUp.ui_marker.addMarkerBtn.clicked.connect(self.markerPopUp.marker_model.addMarker)

    def resizeEvent(self, event: QResizeEvent):
        self.customScene.setSceneRect(self.videoGraphicsItem.boundingRect())
        self.fitInView(self.customScene.sceneRect(), Qt.IgnoreAspectRatio)
        super().resizeEvent(event)