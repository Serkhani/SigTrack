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
import os

class UI_VideoView(QWidget):
    def __init__(self, filePath: str, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.filePath = filePath
        self.videoGraphicsItem = QGraphicsVideoItem()
        self.markerPopUp = MarkerPopUp()
        self.playBtn = QPushButton()
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.volBtn = QPushButton()
        self.volBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.volBtn.setDisabled(True)
        self.stopBtn = QPushButton()
        self.stopBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.multiplexBtn = QPushButton()
        self.timeSlider = QSlider(Qt.Horizontal)
        self.timestampLabel = QLabel('--:-- / --:--')
        self.fmvBtn = QPushButton("FMV", self)
        
        self.initUI()

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