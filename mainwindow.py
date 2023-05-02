# This Python file uses the following encoding: utf-8
import sys, os
from pprint import pprint
from time import sleep
from constants import _DOCK_OPTS, _DOCK_POSITIONS
from DockWidgets.imageview.ImageViewDockWidget import ImageViewDockWidget
from DockWidgets.videoview.VideoViewDockWidget import VideoViewDockWidget
from DockWidgets.mapview.MapViewDockWidget import MapWidget
from DockWidgets.dockWidget import DockWidget
import Editing.icon_resources
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QMessageBox, QDockWidget, QSplashScreen
from PySide2.QtCore import Qt, QThread
from PySide2.QtGui import QFont, QIcon, QPixmap, QTransform
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
        self.ui.actionImgFile.triggered.connect(self.importImgFileLocalAction)
        self.ui.actionImgFolder.triggered.connect(self.importImgFolderLocalAction)
        self.ui.actionImgNetwork.triggered.connect(self.importImgNetworkAction)
        self.ui.actionVidFile.triggered.connect(self.importVidFileLocalAction)
        self.ui.actionVidFolder.triggered.connect(self.importVidFolderLocalAction)
        self.ui.actionVidNetwork.triggered.connect(self.importVidNetworkAction)
        self.ui.actionSave.triggered.connect(self.saveAction)
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
        # videoFile = "C:\\Users\\LENOVO\\Desktop\\Tracking Vessel.ts"
        # print(videoFile)
        #create dockwidget
        dockWidget = DockWidget(self)
        
        if not filePath:
            label = QLabel()
            label.setText("No Video")
            label.setAlignment(Qt.AlignCenter)
            font = QFont()
            font.setPointSize(20)
            font.setBold(True)
            font.setItalic(True)
            label.setFont(font)
            dockWidget.setWidget(label)
        else:
            # creating the videoplayer
            videoPlayer = VideoViewDockWidget(filePath, self)
            dockWidget.setWidget(videoPlayer)

       
        dockWidget.setWindowTitle('VideoView')
        self.addDockWidget(_DOCK_POSITIONS[self.getDockIndex()], dockWidget)

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
        mapView = MapWidget(self)
        dockWidget.setWidget(mapView)
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
    
    def saveAction(self):
        #save file being edited
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        if self.imageViewer.imgPath:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", f'edit_{self.imageViewer.imgPath.split("/")[-1]}', "Images (*.png *.jpg *.xpm *.bmp)", options=options)
            if file_name:
                pixmap = self.imageViewer.grab()
                pixmap.save(file_name)

    def importVidFileLocalAction(self):
        self.inputFilesList = QFileDialog.getOpenFileNames(
        self, caption="Select image(s)",
        dir="C:\\Users\\LENOVO\\Desktop",#\\3months Vac\\Soko Aerial\\Building QGIS plugins with Python\\Images",
        filter="Video (*.mp4 *.ts *.mov)")
        if not self.findChild(MapWidget):
            self.mapAction()
        for vidfilePath in self.inputFilesList[0]:
            print(vidfilePath)
            self.videoAction(filePath=vidfilePath)
    
    def importVidFolderLocalAction(self): pass
    
    def importVidNetworkAction(self): pass
    
    def importImgNetworkAction(self):
        #import files from network
        pass
    
    def importImgFileLocalAction(self):
        #function used to gather selected images in a directory
        self.inputFilesList = QFileDialog.getOpenFileNames(
        self, caption="Select image(s)",
        dir="C:\\Users\\LENOVO\\Desktop",#\\3months Vac\\Soko Aerial\\Building QGIS plugins with Python\\Images",
        filter="Image (*.jpg)")
        if self.inputFilesList[0]:
            if not self.findChild(MapWidget):
                self.mapAction()

            for imgfilePath in self.inputFilesList[0]:
                self.importImage(imgfilePath)
                # with open(imgfilePath, 'rb') as src:
                #     img = Image(src)
                #     if img.has_exif:
                #         is_dms = img.get('gps_latitude')
                #         if is_dms:
                #             self.images_dict[imgfilePath] = self.getGPSInfo(img)
                #         else:
                #             self.images_dict[imgfilePath] = {
                #                 'lat': img.get('latitude'),
                #                 'long': img.get('longitude'),
                #             }
                #         self.images_dict[imgfilePath]['info'] = img
                #         self.imagePaths.append(imgfilePath)                
                #         self.map.addMarker(imgfilePath, self.images_dict[imgfilePath])
                #     else:
                #         msgBox = QMessageBox()
                #         msgBox.setText(f"No exif information present in {imgfilePath}")
                #         msgBox.exec_()

    def getGPSInfo(self, img: dict) -> dict:
       """return a dictionary with long, lat
       img: exif Image object. Contains all the image data
       """
       gpsInfo = {
           'gps_long': img.get('gps_longitude', None),
           'gps_lat': img.get('gps_latitude', None),
           'gps_lat_ref': img.get('gps_latitude_ref', None),
           'gps_long_ref': img.get('gps_longitude_ref', None)
           }
       long_ = self.dms2dd(gpsInfo['gps_long'], gpsInfo['gps_long_ref'])
       lat = self.dms2dd(gpsInfo['gps_lat'], gpsInfo['gps_lat_ref'])
       return  {'lat': lat, 'long': long_}

    def dms2dd(self, dms, ref: str):
       """converts dms to long and lat
       """
       sec = (dms[1] * 60.0 )+ float(dms[2])
       hrs = sec / 3600.0
       deg = float(dms[0]) + hrs
       if ref.upper() == 'W' or ref.upper() == 'S':
           deg *= -1
       return deg
    
    def importImgFolderLocalAction(self) -> None:
        """function used to gather all images from a specified directory
        """
        self.inputFolderPath = QFileDialog.getExistingDirectory(
        self, caption="Select input folder",
        #dir=os.path.expanduser("~")
        dir="C:\\Users\\LENOVO\\Desktop\\Image Support Type"
        )
        # print(self.inputFolderPath): C:/Users/USER/Desktop/Image Support Type
        # adds the markers to the mapView
        if self.inputFolderPath:#check if a path has been selected
            if not self.findChild(MapWidget):#check if a map view is not open
                self.mapAction()#add map view if not open
            imgFolderPath = os.path.normpath(self.inputFolderPath)
            # print(f"imgFolderPath: {imgFolderPath}"): C:\Users\USER\Desktop\Image Support Type
            for imgName in os.listdir(imgFolderPath): #taking each image from the folder
                self.importImage(imgFolderPath+os.sep+imgName) #importing each image
                
    def importImage(self, imgfilePath: str):
        """imports the specific image
        imgfilePath: absolute path to the image file
        """       
        with open(imgfilePath, 'rb') as src: #opening and reading each file
            img = Image(src)#extracting exif data
            if img.has_exif: #if exif data is present
                is_dms = img.get('gps_latitude')
                if is_dms:
                    self.images_dict[imgfilePath] = self.getGPSInfo(img)
                else:
                    self.images_dict[imgfilePath] = {
                        'lat': img.get('latitude'),
                        'long': img.get('longitude'),
                    }
                self.images_dict[imgfilePath]['info'] = img
                self.imagePaths.append(imgfilePath) #add image file path to the list of imported images              
                self.map.addMarker(imgfilePath, self.images_dict[imgfilePath])# add marker to the map
            else:
                msgBox = QMessageBox()
                msgBox.setText(f"No exif information present in {imgfilePath.split(os.sep)[-1]}")
                msgBox.exec_()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/sigtrack"))
    # threadcount = QThread.idealThreadCount()
    # use all available cores and parallel rendering
    # app.setMaxThreads(threadcount)

        # ======FOR SPLASH SCREEN======

    # Load the image for the splash screen
    pixmap = QPixmap(':/sigtrack')
    
    # Rotate and scale the image until it can't be seen
    angle = 100
    scale = 0.0

    # Create the splash screen and show it
    splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
    transform = QTransform().rotate(angle).scale(scale, scale)
    rotated = pixmap.transformed(transform, Qt.SmoothTransformation)
    splash.setPixmap(rotated)
    splash.show()
    
    while scale < 1.0:
        app.processEvents()
        angle -= 1
        scale += 0.01
        transform = QTransform().rotate(angle).scale(scale, scale)
        rotated = pixmap.transformed(transform, Qt.SmoothTransformation)
        splash.setPixmap(rotated)

    sleep(2)

        # ======SPLASH SCREEN ENDED======

    widget = MainWindow()
    widget.setWindowTitle("SigTrack")
    widget.show()
    
    # Close the splash screen and continue with the main application
    splash.close()
    sys.exit(app.exec_())


                    # self.images_dict[imgfilePath] = self.getGPSInfo(img)
#                     self.images_dict[imgfilePath]['altitude'] = img.get('gps_altitude', None)
#                     self.images_dict[imgfilePath]['dji'] = True
#                     self.images_dict[imgfilePath]['timestamp'] = img.get('datetime', '').split(' ')[1]
# #                            self.images_dict[i]['img_direction'] = img.gps_img_direction
# #                            print(self.images_dict[i]['img_direction'])
#                     self.images_dict[imgfilePath]['datestamp'] = img.get('datetime', '').split(' ')[0]
#                 else:
#                     self.imagePaths.append(imgfilePath)
#                     self.map.addMarker(imgfilePath,self.images_dict[imgfilePath])

#         for imgfilePath in self.inputFilesList[0]:
#             i = imgfilePath.split("/")[-1]
# #            self.imageAction(imgfilePath)
#             with open(imgfilePath, 'rb') as src:
#                 img = Image(src)
#                 if img.has_exif:
#                     try:
#                         assert img.make == 'DJI', AssertionError
#                     except AssertionError:
# #                        if file is from NIKON
#                         self.errorHandling(img, i, imgfilePath)
#                     except:
# #                        if file is neither DJI nor NIKON
#                         self.errorHandling(img, i, imgfilePath)
#                     else:
# #                        if file is DJI
#                         try:
#                             self.images_dict[i] = self.getGPSInfo(img)
#                             self.images_dict[i]['altitude'] = img.get('gps_altitude', None)
#                             self.images_dict[i]['dji'] = True
#                             self.images_dict[i]['timestamp'] = img.get('datetime', '').split(' ')[1]
# #                            self.images_dict[i]['img_direction'] = img.gps_img_direction
# #                            print(self.images_dict[i]['img_direction'])
#                             self.images_dict[i]['datestamp'] = img.get('datetime', '').split(' ')[0]
#                         except:
#                             msgBox = QMessageBox()
#                             msgBox.setText("some geo info missing from {}".format(i))
#                             msgBox.exec()
#                         else:
#                             self.imagePaths.append(imgfilePath)
#                             self.map.addMarker(imgfilePath,self.images_dict[i])


