# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QUrl
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout


class VideoViewDockWidget(QWidget):
    def __init__(self, filePath: str):
        super().__init__()
        self.filePath = filePath
        print(filePath)
        self.player = QMediaPlayer()
        self.videoPlayerWidget = QVideoWidget()
        self.player.setVideoOutput(self.videoPlayerWidget)
        self.playBtn = QPushButton("Play", self)
        self.playBtn.clicked.connect(self.play)
        self.stopBtn = QPushButton("Stop", self)
        self.stopBtn.clicked.connect(self.stop)
        layout = QVBoxLayout(self)
        controls = QHBoxLayout(self)
        controls.addWidget(self.playBtn)
        controls.addWidget(self.stopBtn)
        layout.addWidget(self.videoPlayerWidget)
        layout.addLayout(controls)


    def play(self):
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.filePath)))
        self.player.play()
    
    def stop(self):
        self.player.stop()