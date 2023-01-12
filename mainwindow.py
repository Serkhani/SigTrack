# This Python file uses the following encoding: utf-8
import sys, os
from constants import _DOCK_OPTS, _DOCK_POSITIONS
from DockWidgets.ImageViewDockWidget import ImageViewDockWidget
from DockWidgets.VideoViewDockWidget import VideoViewDockWidget
from DockWidgets.MapViewDockWidget import MapWidget
from DockWidgets.dockWidget import DockWidget
import Editing.icon_resources
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QMessageBox, QDockWidget
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont, QIcon
# Important:
# You need to run the following command to generate the ui_form.py file
#     PySide2-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py

from ui_form import Ui_MainWindow
from exif import Image
from constants import PHOTO_EXTENSIONS#, DEPENDENCIES

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setDockOptions(_DOCK_OPTS)# defines docking behaviour
#        variable initializations
        self.dockCount = 0
        self.inputFolderPath, self.inputFilesList = None, None
        self.images_dict = {}
        self.imagePaths = []
#        setting up function callbacks for menu actions
        self.ui.actionFile_s.triggered.connect(self.importFileLocalAction)
        self.ui.actionFolder.triggered.connect(self.importFolderLocalAction)
        self.ui.actionNetwork.triggered.connect(self.importNetworkAction)
        self.ui.actionSave.triggered.connect(self.saveAction)
        self.ui.actionSave_As.triggered.connect(self.saveAsAction)
        self.ui.actionUndo.triggered.connect(self.undoAction)
        self.ui.actionRedo.triggered.connect(self.redoAction)
        self.ui.actionZoom_In.triggered.connect(self.zoomInAction)
        self.ui.actionZoom_Out.triggered.connect(self.zoomOutAction)
        self.ui.actionZoom_Selection.triggered.connect(self.zoomSelectionAction)
        self.ui.actionPan.triggered.connect(self.panAction)
        self.ui.actionMap.triggered.connect(self.mapAction)
        self.ui.actionImage.triggered.connect(self.imageAction)
        self.ui.actionVideo.triggered.connect(self.videoAction)
        self.setCentralWidget(self.ui.label)
#        custom dockwidgetviews initializations
        self.map = MapWidget(self)
        self.editingPanel = QDockWidget()
        self.addDockWidget(Qt.LeftDockWidgetArea, self.editingPanel)
        self.editingPanel.setFloating(True)
        self.editingPanel.hide()
        self.imageViewer = ImageViewDockWidget(self)
#        various functions
    def videoAction(self, filePath=""):
        #add video dockwidget to central widget area
        #increment dockCount
        self.dockCount += 1
        #hide the label when there are views
        self.ui.label.hide()
        videoFile = "C:\\Users\\LENOVO\\Desktop\\Tracking Vessel.ts"
        print(videoFile)
        # creating the videoplayer
        videoPlayer = VideoViewDockWidget(videoFile)
        #create dockwidget
        dockWidget = DockWidget(self)
        
        # if not filePath:
        #     label = QLabel()
        #     label.setText("No Video")
        #     label.setAlignment(Qt.AlignCenter)
        #     font = QFont()
        #     font.setPointSize(20)
        #     font.setBold(True)
        #     font.setItalic(True)
        #     label.setFont(font)
        #     dockWidget.setWidget(label)
        # else:
        dockWidget.setWidget(videoPlayer)
        dockWidget.setWindowTitle('VideoView')
        self.addDockWidget(_DOCK_POSITIONS[self.getDockIndex()], dockWidget)
        videoPlayer.play()

    def imageAction(self, imgPath=""):
        #add image dockwidget to central widget area
        #increment dockCount
        self.dockCount += 1
        #hide the label when there are views
        self.ui.label.hide()
        #creating the imageviewer
        imageViewer = ImageViewDockWidget(self)
        #create dock widget
        dockWidget = DockWidget(self)
        if not imgPath:
            label = QLabel()
            label.setText("No Image")
            label.setAlignment(Qt.AlignCenter)
            font = QFont()
            font.setPointSize(20)
            font.setBold(True)
            font.setItalic(True)
            label.setFont(font)
            dockWidget.setWidget(label)
        else:
            imageViewer.showImageOnView(imgPath)
            dockWidget.setWidget(imageViewer)
        dockWidget.setWindowTitle('ImageView')
        self.addDockWidget(_DOCK_POSITIONS[self.getDockIndex()], dockWidget)

    def mapAction(self):
        #add map dockwidget to central widget area
        #increment dockCount
        self.dockCount += 1
        #hide the label when there are views
        self.ui.label.hide()
        #create dock widget
        dockWidget = DockWidget(self)
        dockWidget.setWindowTitle('MapView')
        #creating map widget
#        dockWidget.setWidget(self.mapView.webView)
        dockWidget.setWidget(self.map)
        self.addDockWidget(_DOCK_POSITIONS[self.getDockIndex()], dockWidget)

    def getDockIndex(self):
        #returns the index which will be used to specify the docking position of the view
        if self.dockCount == 1:
            return 0
        elif self.dockCount%2 == 0:
            return 3
        else: return 1


    def panAction(self):
        #pan the view
        pass

    def zoomSelectionAction(self):
        #fit selected area into view
        pass

    def zoomOutAction(self):
        #zoom out of frame
        pass

    def zoomInAction(self):
        #zoom into frame
        pass

    def redoAction(self):
        #redo an edited action
        pass

    def undoAction(self):
        #undo an edited action
        pass

    def saveAsAction(self):
        #create a file with current image state
        pass
    def saveAction(self):
        #save file being edited
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        if self.imageViewer.imgPath:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", f'edit_{self.imageViewer.imgPath.split("/")[-1]}', "Images (*.png *.jpg *.xpm *.bmp)", options=options)
            if file_name:
                pixmap = self.imageViewer.grab()
                pixmap.save(file_name)

    def importNetworkAction(self):
        #import files from network
        pass
    def importFileLocalAction(self):
        #function used to gather selected images in a directory
        self.inputFilesList = QFileDialog.getOpenFileNames(
        self, caption="Select image(s)",
        dir="C:\\Users\\LENOVO\\Desktop\\3months Vac\\Soko Aerial\\Building QGIS plugins with Python\\Images",
        filter="Image (*.jpg)")
        if not self.findChild(MapWidget):
            self.mapAction()
        for imgfilePath in self.inputFilesList[0]:
            i = imgfilePath.split("/")[-1]
#            self.imageAction(imgfilePath)
            with open(imgfilePath, 'rb') as src:
                img = Image(src)
                if img.has_exif:
                    try:
                        assert img.make == 'DJI', AssertionError
                    except AssertionError:
#                        if file is from NIKON
                        self.errorHandling(img, i, imgfilePath)
                    except:
#                        if file is neither DJI nor NIKON
                        self.errorHandling(img, i, imgfilePath)
                    else:
#                        if file is DJI
                        try:
                            self.images_dict[i] = self.getGPSInfo(img)
                            self.images_dict[i]['altitude'] = img.gps_altitude
                            self.images_dict[i]['dji'] = True
                            self.images_dict[i]['timestamp'] = img.datetime.split(' ')[1]
#                            self.images_dict[i]['img_direction'] = img.gps_img_direction
#                            print(self.images_dict[i]['img_direction'])
                            self.images_dict[i]['datestamp'] = img.datetime.split(' ')[0]
                        except:
                            msgBox = QMessageBox()
                            msgBox.setText("some geo info missing from {}".format(i))
                            msgBox.exec()
                        else:
                            self.imagePaths.append(imgfilePath)
                            self.map.addMarker(imgfilePath,self.images_dict[i])





    def errorHandling(self, img, i, imgfilePath):
        try:
            self.images_dict[i] = self.getGPSInfo(img)
            self.images_dict[i]['altitude'] = img.gps_altitude
            self.images_dict[i]['dji'] = False
            self.images_dict[i]['timestamp'] = img.gps_timestamp
#            self.images_dict[i]['img_direction'] = img.gps_img_direction
            self.images_dict[i]['datestamp'] = img.gps_datestamp
        except:
            msgBox = QMessageBox()
            msgBox.setText("some geo info missing from {}".format(i))
            msgBox.exec()
        else:
            self.imagePaths.append(imgfilePath)
            self.map.addMarker(imgfilePath,self.images_dict[i])


    def importFolderLocalAction(self):
        #function used to gather all images from a specified directory
        self.inputFolderPath = QFileDialog.getExistingDirectory(
        self, caption="Select input folder",
        #dir=os.path.expanduser("~")
        dir="C:\\Users\\LENOVO\\Desktop\\3months Vac\\Soko Aerial\\Building QGIS plugins with Python\\Images"
        )
        if not self.findChild(MapWidget):
            self.mapAction()
        self.import_folder_path()

    def import_folder_path(self):
        # adds the markers to the mapView
        if self.inputFolderPath:
           imgPath = os.path.normpath(self.inputFolderPath)
           self.importImages(imgPath)
           if self.images_dict:
               for img, dict_ in self.images_dict.items():
#                   print("dict:", dict_)
#                   print(img)
                   self.map.addMarker(imgPath+os.sep+img,dict_)

    def getGPSInfo(self, img):
       #return a dictionary with long, lat, ..... ie: NOT YET... orientation, date_time
       gpsInfo = {
           'gps_long': img.gps_longitude,
           'gps_lat': img.gps_latitude,
           'gps_lat_ref': img.gps_latitude_ref,
           'gps_long_ref': img.gps_longitude_ref
           }
       long_ = self.dms2dd(gpsInfo['gps_long'], gpsInfo['gps_long_ref'])
       lat = self.dms2dd(gpsInfo['gps_lat'], gpsInfo['gps_lat_ref'])
       return  {'lat': lat, 'long': long_}

    def dms2dd(self, dms, ref):
       # conversion function to convert dms to long and lat
       sec = (dms[1] * 60.0 )+ float(dms[2])
       hrs = sec / 3600.0
       deg = float(dms[0]) + hrs
       if ref.upper() == 'W':
#           print("west")
           deg = deg * -1
       if ref.upper() == 'S':
#           print("south")
           deg = deg * -1
       return deg

    def importImages(self, path):
       # function that imports the images in the directory
       for i in os.listdir(path):
           imgfilePath = path+os.sep+i
           if i.split(".")[-1] in PHOTO_EXTENSIONS:
               with open(imgfilePath, 'rb') as src:
                   img = Image(src)
                   if img.has_exif:
                       try:
                           assert img.make == 'DJI', AssertionError
                       except AssertionError:
#                           print('assert')
   #                        if file is from NIKON
                           self.errorHandling(img, i, imgfilePath)
                       except:
   #                        if file is neither DJI nor NIKON
                           self.errorHandling(img, i, imgfilePath)
                       else:
   #                        if file is DJI
                           try:
                               self.images_dict[i] = self.getGPSInfo(img)
                               self.images_dict[i]['altitude'] = img.gps_altitude
                               self.images_dict[i]['dji'] = True
                               self.images_dict[i]['timestamp'] = img.datetime.split(' ')[1]
   #                            self.images_dict[i]['img_direction'] = img.gps_img_direction
   #                            print(self.images_dict[i]['img_direction'])
                               self.images_dict[i]['datestamp'] = img.datetime.split(' ')[0]
                           except:
                               msgBox = QMessageBox()
                               msgBox.setText("some geo info missing from {}".format(i))
                               msgBox.exec()
                           else:
                               self.imagePaths.append(imgfilePath)
                               self.map.addMarker(imgfilePath,self.images_dict[i])




if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/sigtrack"))
    widget = MainWindow()
    widget.setWindowTitle("SigTrack")
    widget.show()
    sys.exit(app.exec_())
