# This Python file uses the following encoding: utf-8
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton, QStyle, QSizePolicy
from PySide2.QtCore import QUrl, QTimer, Qt
from PySide2.QtCore import QUrl
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout
# from DockWidgets.utils import getVideoLocationInfo
from klv_data.element import UnknownElement
from klv_data.streamparser import StreamParser
import platform
import subprocess
import os

import DockWidgets.videoview.rc_vid_icons
from klv_data.FmvKlvReader import _seconds_to_time, _seconds_to_time_frac


class VideoViewDockWidget(QWidget):
    def __init__(self, filePath: str, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.filePath = filePath
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
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
        self.metadata = None
        # self.mediaPlayer.positionChanged.connect(self.on_position_changed)
        self.islocal = True
        self.isStreaming = not self.islocal
        self.pass_time = 250
        self.PrecisionTimeStamp = ""
        self.currentInfo = 0.0
        self.playerState = QMediaPlayer.PlayingState
        self.klv_folder = os.getcwd()
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
        # self.f = subprocess.run(["ffmpeg", "-y", "-i", self.filePath, "-map",
        #                         "0:d", "-c", "copy", "-copy_unknown", "-f", "data", "output.bin"])
        # i = self.filePath.split(os.sep)[-1]
        # # load klv data
        # try:
        #     with open('output.bin', 'rb') as f:
        #         frameCenterLat, frameCenterLong = None, None
        #         try:
        #             for index, packet in enumerate(StreamParser(f)):
        #                 data = packet.MetadataList()
        #                 frameCenterLat = data[13][-1]
        #                 frameCenterLong = data[14][-1]
        #                 frameCenterAlt = data[15][-1]
        #                 print(frameCenterLat)
        #                 print(frameCenterLong)
        #                 print(frameCenterAlt)
        #                 # self.mainWindow.mapAction()
        #         except ValueError as e:
        #             print("value Error")
        #         self.mainWindow.map.addDrone(frameCenterLat, frameCenterLong)
        # except:
        #     self.showMessage(f"some geo info missing from {i}")
        if self.filePath:
            self.metadata = self.extract_metadata(self.filePath)
            self.setPosition(0)
            self.mediaPlayer.positionChanged.connect(self.on_position_changed)
        # # load video

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

    def extract_metadata(self, video_path):
        try:
            probe = subprocess.check_output(["ffmpeg", "-y", "-i", video_path, "-map", "0:d", "-c", "copy", "-copy_unknown", "-f", "data", "-"])
            print(probe)
        except subprocess.CalledProcessError as e:
            print("Error running FFmpeg to extract metadata: ", e)
            return None
        metadata = []
        for packet in StreamParser(probe):
            # try:
            if isinstance(packet, UnknownElement):
                print("Error interpreting klv data, metadata cannot be read: The parser did not recognize KLV data")
                continue
            data = packet.MetadataList()
            self.data = data
            metadata.append(data)
        data = (i for i in metadata)
        return data

    
    def on_position_changed(self, progress):
        """Current Video position change
        @type progress: qint64
        @param progress: Slide video duration current value
        """
        progress_in_seconds = progress / 1000
        if self.playerState == QMediaPlayer.PausedState:
            self.updateDurationInfo(progress_in_seconds, True)
        else:
            self.updateDurationInfo(progress_in_seconds)


    def updateDurationInfo(self, currentInfo, isPrecise=False):
        """Update labels duration Info and CallBack Metadata
        @type currentInfo: String
        @param currentInfo: Current time value
        """
        duration = self.mediaPlayer.duration()
        self.currentInfo = currentInfo
        print(f"currentInfo: {currentInfo}")
        if currentInfo or duration:
            totalTime = _seconds_to_time(duration)
            currentTime = _seconds_to_time(currentInfo)
            tStr = currentTime + " / " + totalTime
            currentTimeInfo = _seconds_to_time_frac(currentInfo)
            if self.isStreaming:
                self.get_metadata_from_buffer()
            elif self.islocal:
                nextTime = currentInfo + self.pass_time / 1000
                nextTimeInfo = _seconds_to_time_frac(nextTime)
                print(f"nextTimeInfo: {nextTimeInfo}")
                metadata = next(self.metadata)
                print(metadata)
                # self.callMetadataSync(currentTimeInfo, nextTimeInfo)
            else:
                self.get_metadata_from_buffer(currentTimeInfo)
        else:
            tStr = ""
        # if self.PrecisionTimeStamp != "":
        #     self.lb_prec_ts.setText(self.PrecisionTimeStamp)
    
    def get_metadata_from_buffer(self, currentTime=None):
        """Metadata CallBack
        @type currentTime: String
        @param currentTime: Current video timestamp
        """
        try:
            if not self.islocal:
                stdout_data = self.meta_reader.get(currentTime)    
            else:
                stdout_data = b"\x15"       
            if stdout_data == "NOT_READY":
                print("Buffer value read but is not ready, increase buffer size.")
                return
            elif stdout_data == "BUFFERING":
                if self.mediaPlayer.notifyInterval() <= 1000:
                    print("QgsFmvPlayer: Metadata Buffering...")
                    oldState = self.playerState
                    self.mediaPlayer.pause()    
                    QTimer.singleShot(2000, lambda: self.resumePlay(oldState))
                    return
            elif stdout_data is None:
                return
            elif stdout_data == b"" or len(stdout_data) == 0:
                return
            self.packetStreamParser(stdout_data)
        except Exception as inst:
            print("Metadata Buffer Failed! : " + str(inst))
    
    def packetStreamParser(self, stdout_data):
        """Common packet process
        @type stdout_data: String
        @param stdout_data: Binary data
        """
        for packet in StreamParser(stdout_data):
            if isinstance(packet, UnknownElement):
                print("Error interpreting klv data, metadata cannot be read: The parser did not recognize KLV data")
                continue
            data = packet.MetadataList()
            self.data = data