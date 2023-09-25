from PySide2.QtMultimediaWidgets import QGraphicsVideoItem
from PySide2.QtCore import Qt

from sigtrack.models.video_models.marker.video_marker import VideoMarker


class VideoGraphicsItem(QGraphicsVideoItem):
    def __init__(self):
        super().__init__()
        self.setAspectRatioMode(Qt.IgnoreAspectRatio)
    def addMarker(self):
        videoMarker = VideoMarker()
        self.scene().addItem(videoMarker)

# class VideoWidget(QVideoWidget):
#     def __init__(self, dialog: MarkerPopUp):
#         super().__init__()
#         self.dialog = dialog
#         self.markerPos = None
        
#     def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
#             # put an image marker here
#         if self.dialog.isAddMarker:
#             self.markerPos = event.pos()
#             print(event.pos())  
#         super().mousePressEvent(event)

#     def mouseMoveEvent(self, event: QMouseEvent) -> None:
#         if self.dialog.isAddMarker:
#             mousePos = event.pos()
#             # print(mousePos.x)
#             print(f"moouse.x(): {mousePos.x()} mouse.y: {mousePos.y()}")
#             coordinate = QGeoCoordinate(float(mousePos.x()), float(mousePos.y()))

#             self.dialog.change_text([mousePos.x(), mousePos.y()])
#         super().mouseMoveEvent(event)
