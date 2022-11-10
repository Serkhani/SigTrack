# This Python file uses the following encoding: utf-8
import sys
from constants import _DOCK_OPTS

from PySide6.QtWidgets import QApplication, QMainWindow

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

    def videoAction(self):
#        add video dockwidget to central widget area
        pass
    def imageAction(self):
#        add image dockwidget to central widget area
        pass
    def mapAction(self):
#        add map dockwidget to central widget area
        pass
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
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
