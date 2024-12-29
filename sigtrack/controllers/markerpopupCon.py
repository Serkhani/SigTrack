from PySide6.QtGui import QColor
from PySide6.QtWidgets import QDockWidget
from PySide6.QtCore import Qt

# from sigtrack.models.video_models.marker.marker_popup import MarkerPopUpModel
from sigtrack.models.video_models.marker.markerListModel import MarkerListModel
from sigtrack.views.videoview.ui_markerpopup import Ui_MarkerDockwidget
from sigtrack.controllers.removeBtnDelegate import RemoveButtonDelegate

class MarkerPopUpCon(QDockWidget):
    def __init__(self, videographicsview):
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)
        self.ui_marker = Ui_MarkerDockwidget()
        self.ui_marker.setupUi(self)
        self.videographicsview = videographicsview
        # self.marker_model = MarkerPopUpModel()
        self.removeButtonDelegate = RemoveButtonDelegate(self.ui_marker.listView, self.videographicsview)
        self.ui_marker.listView.setItemDelegateForColumn(0, self.removeButtonDelegate)
        self.marker_model = MarkerListModel()
        self.ui_marker.listView.setModel(self.marker_model)
        # self.ui_marker.addMarkerBtn.clicked.connect(self.marker_model.addMarker())
    
    def updatePopupWithMarkerData(self, marker_data):
        # Update the popup with data from the marker
        # You can access the marker data and update the UI elements here
        self.marker_model.setMarker(QColor('purple'), marker_data)

        