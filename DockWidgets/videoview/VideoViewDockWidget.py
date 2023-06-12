# This Python file uses the following encoding: utf-8
import PySide2.QtGui
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton, QStyle, QSizePolicy, QGraphicsView, QGraphicsScene
from PySide2.QtCore import QUrl, QTimer, Qt
# from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PySide2.QtGui import QCloseEvent
# from DockWidgets.utils import getVideoLocationInfo
from klv_data.element import UnknownElement
from klv_data.streamparser import StreamParser
import platform
import subprocess
import os

import DockWidgets.videoview.rc_vid_icons
from klv_data.FmvKlvReader import _seconds_to_time, _seconds_to_time_frac, _time_to_seconds
from pprint  import pprint
from DockWidgets.videoview.custom_videographicsitem import VideoWidget
from DockWidgets.videoview.latlon_dialog import MarkerPopUp


class VideoViewDockWidget(QWidget):
    def __init__(self, filePath: str, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.filePath = filePath
        self.markerPopUp = MarkerPopUp()
        self.addMarkerButton = QPushButton()
        self.addMarkerButton.clicked.connect(self.show_popup)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.error.connect(self.handleError)
        self.videoPlayerWidget = VideoWidget(self.markerPopUp)
        self.mediaPlayer.setVideoOutput(self.videoPlayerWidget)
        self.playBtn = QPushButton()
        self.playBtn.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPlay))
        self.volBtn = QPushButton()
        self.volBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
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
        # self.timeSlider.sliderPressed.connect(pprint)
        # self.timeSlider.sliderReleased.connect(pprint)
        # self.timeSlider.valueChanged.connect(self.setPosition)
        # self.timeSlider.sliderReleased.connect(self.setPosition)
        # self.timeSlider.mousePressEvent = self.slider_pressed
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
        self.playerState = QMediaPlayer.PlayingState
        self.klv_folder = os.getcwd()
        self.initUI()


        if self.filePath:
            media_content = QMediaContent(QUrl.fromLocalFile(self.filePath))
            self.mediaPlayer.setMedia(media_content)
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))
            # self.timestampLabel.setText('--:-- / --:--')

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
        hbox1.addWidget(self.addMarkerButton)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.timeSlider)
        hbox2.addWidget(self.timestampLabel)
        vbox = QVBoxLayout()
        # view = QGraphicsView()
        # scene = QGraphicsScene()
        # scene.addItem(self.videoPlayerWidget)
        # view.setScene(self.videoPlayerWidget)
        # vbox.addWidget(view, 20)
        vbox.addWidget(self.videoPlayerWidget,20)
        vbox.addLayout(hbox1,1)
        vbox.addLayout(hbox2,1)
        self.setLayout(vbox)
    
    # def slider_pressed(self, event):
    #     "To handle the time slider track click event"
    #     # Calculate the position of the click on the track
    #     position = self.timeSlider.minimum() + ((self.timeSlider.maximum() - self.timeSlider.minimum()) * event.pos().x()) // self.timeSlider.width()
    #     # Set the value of the slider to that position
    #     print(position)
    #     # self.timeSlider.setValue(position)    
    #     self.setPosition(position*0.01*self.mediaPlayer.duration())

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
        #         
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
            # self.timer.start()
        self.timeSlider.setRange(0, self.mediaPlayer.duration() / 1000)
        

    def stop(self):
        if not self.filePath:
            return
        self.mediaPlayer.stop()
        self.playBtn.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPlay))
        
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
            
            self.timeSlider.setValue(0)
    def show_popup(self):
        self.fmv()
        self.markerPopUp.show()

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
        # print(f"currentInfo: {currentInfo}")
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
                # print(f"nextTimeInfo: {nextTimeInfo}")
                while  True:
                    metadata = next(self.metadata)
                    print(f"metadata[2][-1].split(' ')[-1]: {metadata[2][-1]}")
                    pprint(metadata)
                    mt = metadata[2][-1].split(' ')[-1]
                    precisiontime = _time_to_seconds(mt.split('+')[0]) 
                    if precisiontime >= currentInfo:
                        break
                #use this: (23, ('Frame Center Latitude', '5.499739123275376')),
                # (24, ('Frame Center Longitude', '-0.002616830171376705')),
                # (25, ('Frame Center Elevation', '-0.2716105897612806')),
                # (26, ('Offset Corner Latitude Point 1', '-0.033804589983825184')),
                # (27, ('Offset Corner Longitude Point 1', '-0.02761543626209296')),
                # (28, ('Offset Corner Latitude Point 2', '-0.0629146702475051')),
                # (29, ('Offset Corner Longitude Point 2', '-0.043397320474868')),
                # (30, ('Offset Corner Latitude Point 3', '0.04748298593096713')),
                # (31, ('Offset Corner Longitude Point 3', '0.007132175664540552')),
                # (32, ('Offset Corner Latitude Point 4', '0.04887462996307261')),
                # (33, ('Offset Corner Longitude Point 4', '0.009961241492965484')),
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
                
                # Offset_Corner_Latitude_Point_3 = metadata[30][-1]
                # Offset_Corner_Longitude_Point_3 = metadata[30][-1]
                # frameCenterAlt = data[15][-1]
                #drone motion and stuff
                # self.mainWindow.map.updateDronePosition(Offset_Corner_Latitude_Point_3, Offset_Corner_Longitude_Point_3)
                self.mainWindow.map.updateDronePosition(droneData)
                if self.markerPopUp.isAddMarker and self.videoPlayerWidget.markerPos:
                    latPercentage  = (self.videoPlayerWidget.markerPos.x() / self.videoPlayerWidget.width())#*100
                    lonPercentage  = (self.videoPlayerWidget.markerPos.y()/ self.videoPlayerWidget.height())#*100
                    topLeftLat = float(metadata[23][-1]) - float(metadata[26][-1])
                    bottomRightLat = float(metadata[23][-1]) + float(metadata[32][-1])
                    topLeftLon = float(metadata[24][-1]) + float(metadata[27][-1])
                    bottomRightLon = float(metadata[24][-1]) + float(metadata[31][-1])
                    # latdiff = float(metadata[26][-1]) - float(metadata[30][-1]);print(f"lat1: {metadata[26][-1]}"); print(f"latdiff:{latdiff}")
                    # londiff = float(metadata[27][-1]) - float(metadata[31][-1]);print(f"lon1: {metadata[27][-1]}"); print(f"londiff:{londiff}")
                    latdiff = bottomRightLat - topLeftLat
                    londiff = bottomRightLon - topLeftLon
                    latPercent = latdiff * latPercentage
                    lonPercent = londiff * lonPercentage
                    # data = [float(metadata[27][-1])+ latPercent, float(metadata[27][-1])+lonPercent]
                    data = [topLeftLat+ latPercent, topLeftLon+lonPercent]
                    self.markerPopUp.change_text(data)
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
    
    def closeEvent(self, event: QCloseEvent) -> None:
        # print("close")
        # self.mediaPlayer.stop()
        self.mediaPlayer.deleteLater()
        self.mediaPlayer = None
        self.videoPlayerWidget.close()
        self.videoPlayerWidget.deleteLater()
        self.videoPlayerWidget = None
        self.markerPopUp.close()
        self.markerPopUp.deleteLater()
        self.markerPopUp = None
        # self.markerPopUp.destroy()
        return super().closeEvent(event)