from PySide2.QtWidgets import QGraphicsView, QGraphicsScene
from PySide2.QtGui import QResizeEvent, QShowEvent
from PySide2.QtCore import Qt
 
from sigtrack.models.video_models.custom_videographicsitem import VideoGraphicsItem

class VideoGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.videoGraphicsItem = VideoGraphicsItem()
        self.scene.addItem(self.videoGraphicsItem)
        self.setScene(self.scene)

    def resizeEvent(self, event: QResizeEvent):
        # self.fitInView(self.sceneRect(), Qt.IgnoreAspectRatio)
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)
        # self.fitInView(self.sceneRect(), Qt.KeepAspectRatioByExpanding)
        super().resizeEvent(event)


    def showEvent(self, event: QShowEvent):
        # Call fitInView in the showEvent method to ensure it's done when the widget is shown
        self.fitInView(self.sceneRect(), Qt.IgnoreAspectRatio)
        super().showEvent(event)

