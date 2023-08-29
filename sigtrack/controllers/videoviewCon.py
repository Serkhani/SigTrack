from PySide2.QtMultimedia import QMediaPlayer
from PySide2.QtWidgets import QWidget, QSlider, QLabel, QMessageBox, QPushButton, QStyle
from PySide2.QtCore import QUrl, Qt, Slot
from PySide2.QtGui import QCloseEvent
from PySide2.QtMultimediaWidgets import QGraphicsVideoItem

from sigtrack.klv_data.element import UnknownElement
from sigtrack.klv_data.streamparser import StreamParser
from sigtrack.klv_data.FmvKlvReader import _seconds_to_time_frac, _time_to_seconds
from sigtrack.models.video_models.videoviewModel import VideoViewModel
from sigtrack.views.videoview.ui_videoview import UI_VideoView

import subprocess, os

class VideoViewCon(QWidget):
    def __init__(self, filePath: str, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.filePath = filePath

        self.model = VideoViewModel(filePath, mainWindow)
        self.ui_video = UI_VideoView(filePath, mainWindow)


        
        self.ui_video.playBtn.clicked.connect(self.play)
        self.ui_video.stopBtn.clicked.connect(self.stop)
        self.ui_video.volumeSlider.valueChanged.connect( self.model.mediaPlayer.setVolume)
        self.ui_video.multiplexBtn.clicked.connect(self.model.showMultiplexor)
        self.ui_video.timeSlider.sliderMoved.connect(self.setPosition)
        self.ui_video.fmvBtn.clicked.connect(self.model.fmv)
        self.ui_video.volumeSlider.setValue(self.model.mediaPlayer.volume())
        self.ui_video.volumeSlider.valueChanged.connect(self.model.mediaPlayer.setVolume)
        self.model.mediaPlayer.setVideoOutput(self.ui_video.videoGraphicsItem)
        self.model.mediaPlayer.positionChanged.connect(self.updateTime)
        if self.filePath:
            media_content = QUrl(self.filePath)
            self.model.mediaPlayer.setMedia(media_content)
            self.ui_video.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))
            
        # self.model.mediaPlayer.error.connect(self.handleError)
        # self.playBtn.clicked.connect(self.play)
        # self.stopBtn.clicked.connect(self.stop)
        # self.multiplexBtn.clicked.connect(self.showMultiplexor)
        # self.timeSlider.sliderMoved.connect(self.setPosition)
        # self.fmvBtn.clicked.connect(self.fmv)
        # self.model.mediaPlayer.positionChanged.connect(self.updateTime)


    def fmv(self):
        if self.filePath:
            self.metadata = self.extract_metadata(self.filePath)
            self.setPosition(0)
            self.model.mediaPlayer.positionChanged.connect(self.on_position_changed)

    def play(self):
        if not self.filePath:
            return
        if self.model.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.model.mediaPlayer.pause()
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            self.model.mediaPlayer.play()
            self.ui_video.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        self.ui_video.timeSlider.setRange(0, self.model.mediaPlayer.duration() / 1000)

    @Slot()
    def ensure_stopped(self):
        if self.model.mediaPlayer.state() != QMediaPlayer.StoppedState:
            self.model.mediaPlayer.stop()
        
    def show_status_message(self, message):
        msgBox = QMessageBox()
        msgBox.setText(message)
        msgBox.exec_()

    def stop(self):
        if not self.filePath:
            return
        self.model.mediaPlayer.stop()
        self.ui_video.playBtn.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPlay))
        
        self.ui_video.timeSlider.setValue(0)

    def setPosition(self, position):
        if not self.filePath:
            return
        self.model.mediaPlayer.setPosition(position * 1000)

    def updateTime(self):
        if not self.filePath:
            return
        current_time = self.model.mediaPlayer.position() / 1000
        duration = self.model.mediaPlayer.duration() / 1000
        current_time_str = '{:02d}:{:02d}'.format(
            int(current_time // 60), int(current_time % 60))
        duration_str = '{:02d}:{:02d}'.format(
            int(duration // 60), int(duration % 60))
        self.ui_video.timestampLabel.setText(current_time_str + ' / ' + duration_str)
        self.ui_video.timeSlider.setValue(current_time)
        if current_time == duration:
            self.model.mediaPlayer.stop()
            self.ui_video.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))
            self.ui_video.timeSlider.setValue(0)

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
        # print(f"progress_in_seconds: {progress_in_seconds}")
        if self.model.mediaPlayer.state() == QMediaPlayer.PausedState:
            self.updateDurationInfo(progress_in_seconds, True)
        else:
            self.updateDurationInfo(progress_in_seconds)


    def updateDurationInfo(self, currentInfo, isPrecise=False):
        """Update labels duration Info and CallBack Metadata
        @type currentInfo: String
        @param currentInfo: Current time value
        """
        duration = self.model.mediaPlayer.duration()
        self.currentInfo = currentInfo
        if currentInfo or duration:
            currentTimeInfo = _seconds_to_time_frac(currentInfo)
            if self.model.islocal:
                while True:
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
                # if self.markerPopUp.isAddMarker and self.videoPlayerWidget.markerPos:
                #     latPercentage  = (self.videoPlayerWidget.markerPos.x() / self.videoPlayerWidget.width())#*100
                #     lonPercentage  = (self.videoPlayerWidget.markerPos.y()/ self.videoPlayerWidget.height())#*100
                #     topLeftLat = float(metadata[23][-1]) - float(metadata[26][-1])
                #     bottomRightLat = float(metadata[23][-1]) + float(metadata[32][-1])
                #     topLeftLon = float(metadata[24][-1]) + float(metadata[27][-1])
                #     bottomRightLon = float(metadata[24][-1]) + float(metadata[31][-1])
                #     latdiff = bottomRightLat - topLeftLat
                #     londiff = bottomRightLon - topLeftLon
                #     latPercent = latdiff * latPercentage
                #     lonPercent = londiff * lonPercentage
                #     data = [topLeftLat+ latPercent, topLeftLon+lonPercent]
                #     self.markerPopUp.change_text(data)
            else:
                self.get_metadata_from_buffer(currentTimeInfo)
        else:
            tStr = ""
    
    
    def closeEvent(self, event: QCloseEvent) -> None:
        self.model.mediaPlayer.deleteLater()
        self.model.mediaPlayer = None
        self.model.markerPopUp.close()
        self.model.markerPopUp.deleteLater()
        self.model.markerPopUp = None
        return super().closeEvent(event)