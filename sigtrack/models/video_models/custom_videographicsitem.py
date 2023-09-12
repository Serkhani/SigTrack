from PySide2.QtMultimediaWidgets import QGraphicsVideoItem

class VideoGraphicsItem(QGraphicsVideoItem):
    def __init__(self):
        super().__init__()

        # player = new QMediaPlayer(this);

        # QGraphicsVideoItem *item = new QGraphicsVideoItem;
        # player->setVideoOutput(item);
        # graphicsView->scene()->addItem(item);
        # graphicsView->show();

        # player->setSource(QUrl("http://example.com/myclip4.ogv"));
        # player->play();
    def addMarker(self):
        pass

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
