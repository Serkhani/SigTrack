# This Python file uses the following encoding: utf-8
import sys, os
from constants import _DOCK_OPTS, _DOCK_POSITIONS
from DockWidgets.ImageViewDockWidget import ImageViewDockWidget
from DockWidgets.MapViewDockWidget import MapViewDockWidget
from DockWidgets.dockWidget import DockWidget
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
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
        self.mapView = MapViewDockWidget()
        self.imageViewer = ImageViewDockWidget(self)
#        various functions
    def videoAction(self):
        #add video dockwidget to central widget area
        #increment dockCount
        self.dockCount += 1
        #hide the label when there are views
        self.ui.label.hide()
        #create dockwidget
        dockWidget = DockWidget(self)
        dockWidget.setWidget(self.imageViewer)
        dockWidget.setWindowTitle('VideoView')
        self.addDockWidget(_DOCK_POSITIONS[self.getDockIndex()], dockWidget)

    def imageAction(self):
        #add image dockwidget to central widget area
        #increment dockCount
        self.dockCount += 1
        #hide the label when there are views
        self.ui.label.hide()
        #create dock widget
        dockWidget = DockWidget(self)
        dockWidget.setWidget(self.imageViewer)
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
        dockWidget.setWidget(self.mapView.webView)
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
        pass
    def importNetworkAction(self):
        #import files from network
        pass
    def importFileLocalAction(self):
        #function used to gather selected images in a directory
        self.inputFilesList = QFileDialog.getOpenFileNames(
        self, caption="Select image(s)",
        dir="C:\\Users\\LENOVO\\Desktop\\3months Vac\\Soko Aerial\\Building QGIS plugins with Python\\Images",
        filter="Image (*.jpg)")
        for imgfilePath in self.inputFilesList[0]:
            i = imgfilePath.split("/")[-1]
            with open(imgfilePath, 'rb') as src:
                img = Image(src)
                print(i)
                if img.has_exif:
                    self.imagePaths.append(imgfilePath)
                    self.images_dict[i] = self.getGPSInfo(img)
                    self.images_dict[i]['altitude'] = img.gps_altitude
                    self.images_dict[i]['timestamp'] = img.gps_timestamp
                    self.images_dict[i]['img_direction'] = img.gps_img_direction
                    self.images_dict[i]['datestamp'] = img.gps_datestamp
                    self.mapView.addMarker(i,self.images_dict[i])



    def importFolderLocalAction(self):
        #function used to gather all images from a specified directory
        self.inputFolderPath = QFileDialog.getExistingDirectory(
        self, caption="Select input folder",
        #dir=os.path.expanduser("~")
        dir="C:\\Users\\LENOVO\\Desktop\\3months Vac\\Soko Aerial\\Building QGIS plugins with Python\\Images"
        )
        if not self.findChild(MapViewDockWidget):
            self.mapAction()
        self.import_folder_path()

    def import_folder_path(self):
        # adds the markers to the mapView
        if self.inputFolderPath:
           imgPath = os.path.normpath(self.inputFolderPath)
           self.importImages(imgPath)
           if self.images_dict:
               for img, dict_ in self.images_dict.items():
                   print(img)
                   self.mapView.addMarker(imgPath+os.sep+img,dict_)

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
           print("west")
           deg = deg * -1
       if ref.upper() == 'S':
           print("south")
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
                       self.imagePaths.append(imgfilePath)
                       self.images_dict[i] = self.getGPSInfo(img)
                       self.images_dict[i]['altitude'] = img.gps_altitude
                       self.images_dict[i]['timestamp'] = img.gps_timestamp
                       self.images_dict[i]['img_direction'] = img.gps_img_direction
                       self.images_dict[i]['datestamp'] = img.gps_datestamp


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
