from PySide2.QtWidgets import QGraphicsView, QGraphicsScene, QGridLayout
from PySide2.QtGui import QResizeEvent, QShowEvent
from PySide2.QtCore import Qt, QSizeF
 
from sigtrack.models.video_models.custom_videographicsitem import VideoGraphicsItem

class VideoGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.scene.clear()
        self.videoGraphicsItem = VideoGraphicsItem()
        self.scene.addItem(self.videoGraphicsItem)
        self.scene.setSceneRect(self.videoGraphicsItem.boundingRect())
        self.setScene(self.scene)
        self.fitInView(self.scene.sceneRect(), Qt.IgnoreAspectRatio)

    def resizeEvent(self, event: QResizeEvent):
        self.scene.setSceneRect(self.videoGraphicsItem.boundingRect())
        self.fitInView(self.scene.sceneRect(), Qt.IgnoreAspectRatio)
        super().resizeEvent(event)