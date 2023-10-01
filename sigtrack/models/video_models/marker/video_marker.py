from PySide2.QtWidgets import QGraphicsItem, QLabel, QGraphicsPixmapItem
from PySide2.QtGui import QColor, QPixmap
from PySide2.QtCore import QUrl

from sigtrack.models.video_models.marker.marker_indicator import MarkerIndicator
import sigtrack.resources.compiled.map_rc


class VideoMarker(QGraphicsPixmapItem):
    def __init__(self, color: QColor):
        self.customPixmap =  QPixmap(":/marker")
        super().__init__(self.customPixmap)
        self.color = color
        # self.setPixmap(self.customPixmap)
        # self.pixmapItem = QGraphicsPixmapItem(self.icon)
        self.markerIndicator:MarkerIndicator = MarkerIndicator(self.customPixmap.rect())
        # self.pixmapItem.scene().addr
        self.setFlags(
            # QGraphicsItem.ItemToolTipHasChanged | 
            QGraphicsItem.ItemIsMovable #|
            # QGraphicsItem.ItemIsSelectable 
        )
    
    def addImageAndRect(self):
        # Load the image from the resource file
        pixmap = QPixmap(':/image.png')  # Use the resource path starting with ':/'
        # Create a QGraphicsPixmapItem with the loaded image
        pixmap_item = QGraphicsPixmapItem(pixmap)

        # Calculate the position to center the image in the scene
        scene_rect = self.scene.sceneRect()
        image_rect = pixmap_item.boundingRect()
        center_x = (scene_rect.width() - image_rect.width()) / 2.0
        center_y = (scene_rect.height() - image_rect.height()) / 2.0

        # Set the position of the pixmap_item in the center of the scene
        pixmap_item.setPos(center_x, center_y)

        # Create a QGraphicsRectItem for the colored rectangle
        rect_item = QGraphicsRectItem(center_x, center_y, 200, 100)  # Adjust the size and position as needed
        rect_item.setBrush(self.color)  # Set the rectangle color

        # Add both items to the QGraphicsScene
        self.scene.addItem(pixmap_item)
        self.scene.addItem(rect_item)

    
    def change_text(self, data: list) -> None:
        """
        Change the text when the button is clicked
        """
        self.setToolTip(f"lat: {data[0]} lon: {data[1]}")