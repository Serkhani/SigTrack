from PySide2.QtGui import QMouseEvent
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtWidgets import QGraphicsSceneMouseEvent #, QGraphicsScene
from PySide2.QtPositioning import QGeoCoordinate
from sigtrack.views.videoview.latlon_dialog import MarkerPopUp

class VideoWidget(QVideoWidget):
    def __init__(self, dialog: MarkerPopUp):
        super().__init__()
        self.dialog = dialog
        self.markerPos = None
        
    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
            # put an image marker here
        if self.dialog.isAddMarker:
            self.markerPos = event.pos()
            print(event.pos())  
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.dialog.isAddMarker:
            mousePos = event.pos()
            # print(mousePos.x)
            print(f"moouse.x(): {mousePos.x()} mouse.y: {mousePos.y()}")
            coordinate = QGeoCoordinate(float(mousePos.x()), float(mousePos.y()))

            self.dialog.change_text([mousePos.x(), mousePos.y()])
        super().mouseMoveEvent(event)