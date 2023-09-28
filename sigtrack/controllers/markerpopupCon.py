import PySide2.QtGui
from PySide2.QtWidgets import QDockWidget
from PySide2.QtCore import Qt

# from sigtrack.models.video_models.marker.marker_popup import MarkerPopUpModel
from sigtrack.models.video_models.marker.markerListModel import MarkerListModel
from sigtrack.views.videoview.ui_markerpopup import Ui_MarkerDockwidget
from sigtrack.controllers.removeBtnDelegate import RemoveButtonDelegate

class MarkerPopUpCon(QDockWidget):
    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)
        self.ui_marker = Ui_MarkerDockwidget()
        self.ui_marker.setupUi(self)
        # self.marker_model = MarkerPopUpModel()
        self.removeButtonDelegate = RemoveButtonDelegate(self.ui_marker.listView)
        self.ui_marker.listView.setItemDelegateForColumn(0, self.removeButtonDelegate)
        self.marker_model = MarkerListModel()
        self.ui_marker.listView.setModel(self.marker_model)
        # self.ui_marker.addMarkerBtn.clicked.connect(self.marker_model.addMarker())
    

        