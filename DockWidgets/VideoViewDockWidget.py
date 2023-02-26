# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QUrl
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout
# from DockWidgets.utils import getVideoLocationInfo
from klvdata.element import UnknownElement
from klvdata.streamparser import StreamParser
import platform, subprocess, os

class VideoViewDockWidget(QWidget):
    def __init__(self, filePath: str, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.filePath = filePath
        print(filePath)
        self.player = QMediaPlayer()
        self.videoPlayerWidget = QVideoWidget()
        self.player.setVideoOutput(self.videoPlayerWidget)
        self.playBtn = QPushButton("Play", self)
        self.playBtn.clicked.connect(self.play)
        self.stopBtn = QPushButton("Stop", self)
        self.stopBtn.clicked.connect(self.stop)
        self.fmvBtn = QPushButton("FMV", self)
        self.fmvBtn.clicked.connect(self.fmv)
        layout = QVBoxLayout(self)
        controls = QHBoxLayout(self)
        controls.addWidget(self.playBtn)
        controls.addWidget(self.stopBtn)
        controls.addWidget(self.fmvBtn)
        layout.addWidget(self.videoPlayerWidget)
        layout.addLayout(controls)
        if self.filePath:
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.filePath)))
            self.play()


    def fmv(self):
        # info = getVideoLocationInfo(self.filePath)
        # print(info)
        # run fmv mode
        self.f = subprocess.run(["ffmpeg", "-y", "-i",self.filePath, "-map", "0:d", "-c", "copy", "-copy_unknown", "-f", "data", "output.bin"])
        i = self.filePath.split(os.sep)[-1]
        # load klv data
        try:
            with open('output.bin','rb') as f:
                frameCenterLat, frameCenterLong = None, None
                try:
                    for index, packet in enumerate(StreamParser(f)):
                        data = packet.MetadataList()
                        frameCenterLat = data[13][-1]
                        frameCenterLong = data[14][-1]
                        frameCenterAlt = data[15][-1]
                        print(frameCenterLat)
                        print(frameCenterLong)
                        print(frameCenterAlt)
                        # self.mainWindow.mapAction()
                except ValueError as e:
                    print("value Error")
                self.mainWindow.map.addDrone(frameCenterLat, frameCenterLong)
        except:
            self.showMessage(f"some geo info missing from {i}")
            
        # load video


    def play(self):
        if self.player.state() == QMediaPlayer.PausedState:
            self.player.play()
            self.playBtn.setText("Pause")
        else: 
            self.player.pause()
            self.playBtn.setText("Play")

    
    def stop(self):
        self.player.stop()
