from PySide2.QtWidgets import QGraphicsView, QGraphicsScene, QGridLayout
from PySide2.QtGui import QResizeEvent, QShowEvent
from PySide2.QtCore import Qt, QSizeF
 
from sigtrack.models.video_models.custom_videographicsitem import VideoGraphicsItem
from sigtrack.controllers.markerpopupCon import MarkerPopUpCon
from sigtrack.models.video_models.marker.video_marker import VideoMarker

class VideoGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.customScene = QGraphicsScene()
        self.setScene(self.customScene)
        self.videoGraphicsItem = VideoGraphicsItem()
        self.customScene.addItem(self.videoGraphicsItem)
        self.markerPopUp = MarkerPopUpCon()
        self.markerPopUp.ui_marker.addMarkerBtn.clicked.connect(self.addMarker)

    def addMarker(self):
        # videoMarker = VideoMarker()
        # self.customScene.addItem(videoMarker.pixmapItem)
        color = self.markerPopUp.marker_model.addMarker()
        self.videoGraphicsItem.addMarker(color)




    def resizeEvent(self, event: QResizeEvent):
        self.customScene.setSceneRect(self.videoGraphicsItem.boundingRect())
        self.fitInView(self.customScene.sceneRect(), Qt.IgnoreAspectRatio)
        super().resizeEvent(event)