# This Python file uses the following encoding: utf-8
import sys, os
from constants import _DOCK_OPTS, _DOCK_POSITIONS
from DockWidgets.ImageViewDockWidget import ImageViewDockWidget
from DockWidgets.dockWidget import DockWidget
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QRectF

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.dockCount = 0
        self.setDockOptions(_DOCK_OPTS)# defines docking behaviour
#       setting up function callbacks for menu actions
        self.ui.actionlocal.triggered.connect(self.importLocalAction)
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

        self.imageViewer = ImageViewDockWidget(self)

    def videoAction(self):
#        add video dockwidget to central widget area

#        increment dockCount
        self.dockCount += 1
#        hide the label when there are views
        self.ui.label.hide()

    def imageAction(self):
#        add image dockwidget to central widget area

#        increment dockCount
        self.dockCount += 1
#        hide the label when there are views
        self.ui.label.hide()
        dockWidget = DockWidget(self)
        imageViewer = self.imageViewer
        dockWidget.setWidget(imageViewer)
        index = self.getDockIndex()
        self.addDockWidget(_DOCK_POSITIONS[index], dockWidget)

    def mapAction(self):
#        add map dockwidget to central widget area

#        increment dockCount
        self.dockCount += 1
#        hide the label when there are views
        self.ui.label.hide()

    def getDockIndex(self):
#        returns the index which will be used to specify the docking position of the view
        if self.dockCount == 1:
            return 0
        elif self.dockCount%2 == 0:
            return 3
        else: return 1


    def panAction(self):
#        pan the view
        pass
    def zoomSelectionAction(self):
#        fit selected area into view
        pass
    def zoomOutAction(self):
#        zoom out of frame
        pass
    def zoomInAction(self):
#        zoom into frame
        pass
    def redoAction(self):
#        redo an edited action
        pass

    def undoAction(self):
#        undo an edited action
        pass

    def saveAsAction(self):
#        create a file with current image state
        pass
    def saveAction(self):
#        save file being edited
        pass
    def importNetworkAction(self):
#        import files from network
        pass

    def importLocalAction(self):
#        this function imports files from the local disk
        self.inputFile = os.path.normpath(QFileDialog.getOpenFileName(
        self, caption="Select image",
        #directory=os.path.expanduser("~")
        dir="C:\\Users\\LENOVO\\Desktop\\3months Vac\\Soko Aerial\\Building QGIS plugins with Python\\Images"
        )[0])
        if self.inputFile:
            if not self.dockCount:
                self.imageAction()
            print(self.inputFile)
            img = QImage(self.inputFile)
            self.imageViewer.scene.clear()
            pixmap = QPixmap.fromImage(img)
            self.imageViewer.scene.addPixmap(pixmap)
            self.imageViewer.setSceneRect(QRectF(pixmap.rect()))
            self.imageViewer.resizeEvent([])
            self.imageViewer.showNormal()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
