from PySide2.QtWidgets import QGraphicsView, QGraphicsScene, QGridLayout
from PySide2.QtGui import QResizeEvent, QShowEvent, QColor
from PySide2.QtCore import Qt, QSizeF
 
from sigtrack.models.video_models.custom_videographicsitem import VideoGraphicsItem
from sigtrack.controllers.markerpopupCon import MarkerPopUpCon
from sigtrack.models.video_models.marker.video_marker import VideoMarker

class VideoGraphicsView(QGraphicsView):
    def __init__(self,vidModel):
        super().__init__()
        self.customScene = QGraphicsScene()
        self.setScene(self.customScene)
        self.vidModel = vidModel
        self.videoGraphicsItem = VideoGraphicsItem()
        self.customScene.addItem(self.videoGraphicsItem)
        self.markerPopUp = MarkerPopUpCon(self.videoGraphicsItem)
        self.markerPopUp.ui_marker.addMarkerBtn.clicked.connect(self.addMarker)

    def addMarker(self):
        # videoMarker = VideoMarker()
        # self.customScene.addItem(videoMarker.pixmapItem)
        # color = self.markerPopUp.marker_model.addMarker()
        if not self.vidModel.metadata:
            self.vidModel.fmv()
        self.markerPopUp.marker_model.setMarker(QColor('purple'), f"lat: ''\nlon: ''")
        self.videoGraphicsItem.addMarker()

    def updateData(self, metadata: dict):
        if self.markerPopUp.marker_model.getMarker():
            # latPercentage  = (self.videoPlayerWidget.markerPos.x() / self.videoPlayerWidget.width())#*100
            # lonPercentage  = (self.videoPlayerWidget.markerPos.y()/ self.videoPlayerWidget.height())#*100
            latPercentage = (self.videoGraphicsItem.videoMarker.x()/self.videoGraphicsItem.boundingRect().width())
            lonPercentage = (self.videoGraphicsItem.videoMarker.y()/self.videoGraphicsItem.boundingRect().height())
            topLeftLat = float(metadata[23][-1]) - float(metadata[26][-1])
            bottomRightLat = float(metadata[23][-1]) + float(metadata[32][-1])
            topLeftLon = float(metadata[24][-1]) + float(metadata[27][-1])
            bottomRightLon = float(metadata[24][-1]) + float(metadata[31][-1])
            latdiff = bottomRightLat - topLeftLat
            londiff = bottomRightLon - topLeftLon
            latPercent = latdiff * latPercentage
            lonPercent = londiff * lonPercentage
            data = [topLeftLat+ latPercent, topLeftLon+lonPercent]
            res = f"lat: {data[0]}\nlon: {data[1]}"


            self.markerPopUp.updatePopupWithMarkerData(res)
    


    def resizeEvent(self, event: QResizeEvent):
        self.customScene.setSceneRect(self.videoGraphicsItem.boundingRect())
        self.fitInView(self.customScene.sceneRect(), Qt.IgnoreAspectRatio)
        super().resizeEvent(event)