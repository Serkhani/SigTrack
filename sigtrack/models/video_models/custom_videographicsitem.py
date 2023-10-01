from PySide2.QtMultimediaWidgets import QGraphicsVideoItem
from PySide2.QtCore import Qt
from PySide2.QtGui import QColor

from sigtrack.models.video_models.marker.video_marker import VideoMarker


class VideoGraphicsItem(QGraphicsVideoItem):
    def __init__(self):
        super().__init__()
        self.setAspectRatioMode(Qt.IgnoreAspectRatio)
    
    def addMarker(self, color: QColor):
        videoMarker = VideoMarker(color)
        # Calculate the position to center the image in the scene
        scene_rect = self.scene().sceneRect()
        image_rect = videoMarker.boundingRect()
        center_x = (scene_rect.width() - image_rect.width()) / 2.0
        center_y = (scene_rect.height() - image_rect.height()) / 2.0
        # Set the position of the videoMarker in the center of the scene
        videoMarker.setPos(center_x, center_y)
        self.scene().addItem(videoMarker)
        self.scene().addItem(videoMarker.markerIndicator)