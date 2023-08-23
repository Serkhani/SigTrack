from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QMessageBox, QPushButton, QStyle, QSizePolicy, QGraphicsView, QGraphicsScene
from PySide2.QtCore import QUrl, QTimer, Qt, Slot
from PySide2.QtGui import QCloseEvent
from PySide2.QtMultimediaWidgets import QGraphicsVideoItem

from sigtrack.klv_data.element import UnknownElement
from sigtrack.klv_data.streamparser import StreamParser
from sigtrack.klv_data.FmvKlvReader import _seconds_to_time, _seconds_to_time_frac, _time_to_seconds
from sigtrack.models.video_models.custom_videographicsitem import VideoGraphicsItem
from sigtrack.models.video_models.marker.marker_popup import MarkerPopUp
from sigtrack.models.video_models.muxing.full_motion_video_mux import Multiplexor

from pprint  import pprint
import platform, subprocess, os, sys

class UI_VideoView(QWidget):
    def __init__(self, filePath: str, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.filePath = filePath
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.error.connect(self.handleError)
        self.videoGraphicsItem = QGraphicsVideoItem()
        self.markerPopUp = MarkerPopUp()
        self.mediaPlayer.setVideoOutput(self.videoGraphicsItem)
        self.playBtn = QPushButton()
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.volBtn = QPushButton()
        self.volBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.volBtn.setDisabled(True)
        self.playBtn.clicked.connect(self.play)
        self.stopBtn = QPushButton()
        self.stopBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopBtn.clicked.connect(self.stop)
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(self.mediaPlayer.volume())
        self.volumeSlider.valueChanged.connect( self.mediaPlayer.setVolume)
        self.multiplexBtn = QPushButton()
        self.multiplexBtn.clicked.connect(self.showMultiplexor)
        self.timeSlider = QSlider(Qt.Horizontal)
        self.timeSlider.sliderMoved.connect(self.setPosition)
        self.timestampLabel = QLabel('--:-- / --:--')
        self.fmvBtn = QPushButton("FMV", self)
        self.fmvBtn.clicked.connect(self.fmv)
        self.metadata = None
        self.mediaPlayer.positionChanged.connect(self.updateTime)
        self.islocal = True
        self.isStreaming = not self.islocal
        self.pass_time = 250
        self.PrecisionTimeStamp = ""
        self.currentInfo = 0.0
        self.klv_folder = os.getcwd()
        self.initUI()


        if self.filePath:
            # media_content = QUrl.fromLocalFile(self.filePath)
            media_content = QUrl(self.filePath)
            self.mediaPlayer.setMedia(media_content)
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))


    def initUI(self):
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.playBtn)
        hbox1.addWidget(self.stopBtn)
        hbox1.addWidget(self.volBtn)
        hbox1.addWidget(self.volumeSlider)
        hbox1.addWidget(self.fmvBtn)
        hbox1.addWidget(self.multiplexBtn)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.timeSlider)
        hbox2.addWidget(self.timestampLabel)
        vbox = QVBoxLayout()
        graphicsview = QGraphicsView()
        scene=QGraphicsScene()
        graphicsview.setScene(scene)
        scene.addItem(self.videoGraphicsItem)
        vbox.addWidget(graphicsview,20)
        vbox.addLayout(hbox1,1)
        vbox.addLayout(hbox2,1)
        self.setLayout(vbox)
    
    
    def closeEvent(self, event: QCloseEvent) -> None:
        self.mediaPlayer.deleteLater()
        self.mediaPlayer = None
        self.markerPopUp.close()
        self.markerPopUp.deleteLater()
        self.markerPopUp = None
        return super().closeEvent(event)