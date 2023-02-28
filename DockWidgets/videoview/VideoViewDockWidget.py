# This Python file uses the following encoding: utf-8
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton, QStyle, QSizePolicy
from PySide2.QtCore import QUrl, QTimer, Qt
from PySide2.QtCore import QUrl
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout
# from DockWidgets.utils import getVideoLocationInfo
from klvdata.element import UnknownElement
from klvdata.streamparser import StreamParser
import platform
import subprocess
import os

import DockWidgets.videoview.rc_vid_icons


class VideoViewDockWidget(QWidget):
    def __init__(self, filePath: str, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.filePath = filePath
        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.error.connect(self.handleError)
        self.videoPlayerWidget = QVideoWidget()
        self.mediaPlayer.setVideoOutput(self.videoPlayerWidget)
        self.playBtn = QPushButton()
        self.playBtn.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPlay))
        self.volBtn = QPushButton()
        self.volBtn.setIcon(
            self.style().standardIcon(QStyle.SP_MediaVolume))
        self.volBtn.setDisabled(True)
        self.playBtn.clicked.connect(self.play)
        self.stopBtn = QPushButton()
        self.stopBtn.setIcon(
            self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopBtn.clicked.connect(self.stop)
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(self.mediaPlayer.volume())
        self.volumeSlider.valueChanged.connect( self.mediaPlayer.setVolume)
        self.timeSlider = QSlider(Qt.Horizontal)
        # self.timeSlider.setRange(0, 0)
        self.timeSlider.sliderMoved.connect(self.setPosition)
        self.timestampLabel = QLabel('--:-- / --:--')
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateTime)
        self.fmvBtn = QPushButton("FMV", self)
        self.fmvBtn.clicked.connect(self.fmv)
        self.initUI()


        if self.filePath:
            media_content = QMediaContent(QUrl.fromLocalFile(self.filePath))
            self.mediaPlayer.setMedia(media_content)
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))
            self.timestampLabel.setText('--:-- / --:--')

    # def setupMediaPlayer(self):
    #     self.mediaPlayer = QMediaPlayer(self)
    #     self.mediaPlayer.setVideoOutput(self.videoPlayerWidget)

    #     self.mediaPlayer.error.connect(self.handleError)

    #     self.mediaPlayer.stateChanged.connect(self.updateState)
    #     self.mediaPlayer.positionChanged.connect(self.updateTime)
    #     self.mediaPlayer.durationChanged.connect(self.updateTime)

    #     self.mediaPlayer.setVolume(self.volumeSlider.value())


    def initUI(self):
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.playBtn)
        hbox1.addWidget(self.stopBtn)
        hbox1.addWidget(self.volBtn)
        hbox1.addWidget(self.volumeSlider)
        hbox1.addWidget(self.fmvBtn)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.timeSlider)
        hbox2.addWidget(self.timestampLabel)
        vbox = QVBoxLayout()
        vbox.addWidget(self.videoPlayerWidget,20)
        vbox.addLayout(hbox1,1)
        vbox.addLayout(hbox2,1)
        self.setLayout(vbox)


    def fmv(self):
        # info = getVideoLocationInfo(self.filePath)
        # print(info)
        # run fmv mode
        self.f = subprocess.run(["ffmpeg", "-y", "-i", self.filePath, "-map",
                                "0:d", "-c", "copy", "-copy_unknown", "-f", "data", "output.bin"])
        i = self.filePath.split(os.sep)[-1]
        # load klv data
        try:
            with open('output.bin', 'rb') as f:
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

    def handleError(self, error):
        print('Error:', error)

    def play(self):
        if not self.filePath:
            return
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            self.mediaPlayer.play()
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
            self.timer.start()
        self.timeSlider.setRange(0, self.mediaPlayer.duration() / 1000)
        

    def stop(self):
        if not self.filePath:
            return
        self.mediaPlayer.stop()
        self.playBtn.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPlay))
        self.timer.stop()
        self.timeSlider.setValue(0)

    def setPosition(self, position):
        if not self.filePath:
            return
        self.mediaPlayer.setPosition(position * 1000)

    def updateTime(self):
        if not self.filePath:
            return
        current_time = self.mediaPlayer.position() / 1000
        duration = self.mediaPlayer.duration() / 1000
        print("duration: ", duration)
        current_time_str = '{:02d}:{:02d}'.format(
            int(current_time // 60), int(current_time % 60))
        duration_str = '{:02d}:{:02d}'.format(
            int(duration // 60), int(duration % 60))
        self.timestampLabel.setText(current_time_str + ' / ' + duration_str)
        self.timeSlider.setValue(current_time)

        if current_time == duration:
            self.mediaPlayer.stop()
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))
            self.timer.stop()
            self.timeSlider.setValue(0)