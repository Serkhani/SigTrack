from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QMessageBox, QPushButton, QStyle, QSizePolicy, QGraphicsView, QGraphicsScene
from PySide2.QtCore import QUrl, QTimer, Qt, Slot
from PySide2.QtGui import QCloseEvent
from PySide2.QtMultimediaWidgets import QGraphicsVideoItem

from sigtrack.klv_data.element import UnknownElement
from sigtrack.klv_data.streamparser import StreamParser
from sigtrack.klv_data.FmvKlvReader import _time_to_seconds
from sigtrack.models.video_models.marker.marker_popup import MarkerPopUp
from sigtrack.models.video_models.muxing.full_motion_video_mux import Multiplexor
from sigtrack.models.video_models.graphicsview import VideoGraphicsView
# from sigtrack.models.video_models.custom_videographicsitem import VideoGraphicsItem

from pprint import pprint
import subprocess, sys, os

class VideoViewModel(QWidget):
    def __init__(self, filePath: str, mainWindow):
        super().__init__()
        self.metadata = None
        self.islocal = True
        self.isStreaming = not self.islocal
        self.pass_time = 250
        self.PrecisionTimeStamp = ""
        self.currentInfo = 0.0
        self.klv_folder = os.getcwd()
        self.filePath = filePath
        self.mainWindow = mainWindow
        # self.scene = QGraphicsScene()
        # self.videoGraphicsItem = QGraphicsVideoItem()
        # self.videoGraphicsItem = VideoGraphicsItem()
        # self.scene.addItem(self.videoGraphicsItem)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.error.connect(self.handleError)
        self.markerPopUp = MarkerPopUp()
        self.graphicsView = VideoGraphicsView()
        self.mediaPlayer.setVideoOutput(self.graphicsView.videoGraphicsItem)
        
    def showMultiplexor(self):
        self.multiplexor = Multiplexor()
        self.multiplexor.exec_()

    def fmv(self):
        if self.filePath:
            self.metadata = self.extract_metadata(self.filePath)
            self.setPosition(0)
            self.mediaPlayer.positionChanged.connect(self.on_position_changed)

    @Slot("QMediaPlayer::Error", str)
    def handleError(self, error_string):
        print(error_string, file=sys.stderr)
        self.show_status_message(error_string)

    # def play(self):
    #     if not self.filePath:
    #         return
    #     if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
    #         self.mediaPlayer.pause()
    #         self.playBtn.setIcon(
    #             self.style().standardIcon(QStyle.SP_MediaPlay))
    #     else:
    #         self.mediaPlayer.play()
    #         self.playBtn.setIcon(
    #             self.style().standardIcon(QStyle.SP_MediaPause))
    #         # self.timer.start()
    #     self.timeSlider.setRange(0, self.mediaPlayer.duration() / 1000)

    @Slot()
    def ensure_stopped(self):
        if self.mediaPlayer.state() != QMediaPlayer.StoppedState:
            self.mediaPlayer.stop()
        
    def show_status_message(self, message):
        msgBox = QMessageBox()
        msgBox.setText(message)
        msgBox.exec_()

    # def stop(self):
    #     if not self.filePath:
    #         return
    #     self.mediaPlayer.stop()
    #     self.playBtn.setIcon(
    #         self.style().standardIcon(QStyle.SP_MediaPlay))
        
    #     self.timeSlider.setValue(0)

    def setPosition(self, position):
        if not self.filePath:
            return
        self.mediaPlayer.setPosition(position * 1000)

    # def updateTime(self):
    #     if not self.filePath:
    #         return
    #     current_time = self.mediaPlayer.position() / 1000
    #     duration = self.mediaPlayer.duration() / 1000
    #     current_time_str = '{:02d}:{:02d}'.format(
    #         int(current_time // 60), int(current_time % 60))
    #     duration_str = '{:02d}:{:02d}'.format(
    #         int(duration // 60), int(duration % 60))
    #     self.timestampLabel.setText(current_time_str + ' / ' + duration_str)
    #     self.timeSlider.setValue(current_time)
    #     if current_time == duration:
    #         self.mediaPlayer.stop()
    #         self.playBtn.setIcon(
    #             self.style().standardIcon(QStyle.SP_MediaPlay))
    #         self.timeSlider.setValue(0)

    def extract_metadata(self, video_path):
        try:
            probe = subprocess.check_output(["ffmpeg", "-y", "-i", video_path, "-map", "0:d", "-c", "copy", "-copy_unknown", "-f", "data", "-"])
            print(probe)
        except subprocess.CalledProcessError as e:
            print("Error running FFmpeg to extract metadata: ", e)
            return None
        metadata = []
        for packet in StreamParser(probe):
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
        if self.mediaPlayer.state() == QMediaPlayer.PausedState:
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
        if currentInfo or duration:
            if self.islocal:
                while  True:
                    metadata = next(self.metadata)
                    mt = metadata[2][-1].split(' ')[-1]
                    precisiontime = _time_to_seconds(mt.split('+')[0]) 
                    if precisiontime >= currentInfo:
                        break
                #to create a dictionary 
                droneData = {
                    'Sensor Latitude': metadata[13][-1],
                	'Sensor Longitude': metadata[14][-1],
                    'Platform Heading Angle': metadata[5][-1],
                    'Frame Center Latitude': metadata[23][-1],
                    'Frame Center Longitude': metadata[24][-1],
                    'Frame Center Elevation': metadata[25][-1],
                    'Offset Corner Latitude Point 1': metadata[26][-1],
                    'Offset Corner Longitude Point 1': metadata[27][-1],
                    'Offset Corner Latitude Point 2': metadata[28][-1],
                    'Offset Corner Longitude Point 2': metadata[29][-1],
                    'Offset Corner Latitude Point 3': metadata[30][-1],
                    'Offset Corner Longitude Point 3': metadata[31][-1],
                    'Offset Corner Latitude Point 4': metadata[32][-1],
                    'Offset Corner Longitude Point 4': metadata[33][-1]
                    }
                self.mainWindow.map.updateDronePosition(droneData)
                if self.markerPopUp.isAddMarker and self.videoPlayerWidget.markerPos:
                    latPercentage  = (self.videoPlayerWidget.markerPos.x() / self.videoPlayerWidget.width())#*100
                    lonPercentage  = (self.videoPlayerWidget.markerPos.y()/ self.videoPlayerWidget.height())#*100
                    topLeftLat = float(metadata[23][-1]) - float(metadata[26][-1])
                    bottomRightLat = float(metadata[23][-1]) + float(metadata[32][-1])
                    topLeftLon = float(metadata[24][-1]) + float(metadata[27][-1])
                    bottomRightLon = float(metadata[24][-1]) + float(metadata[31][-1])
                    latdiff = bottomRightLat - topLeftLat
                    londiff = bottomRightLon - topLeftLon
                    latPercent = latdiff * latPercentage
                    lonPercent = londiff * lonPercentage
                    data = [topLeftLat+ latPercent, topLeftLon+lonPercent]
                    self.markerPopUp.change_text(data)
    
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