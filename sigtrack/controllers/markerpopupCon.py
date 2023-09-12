from PySide2.QtWidgets import QDockWidget
from PySide2.QtCore import Qt

from sigtrack.models.video_models.marker.marker_popup import MarkerPopUpModel
from sigtrack.views.videoview.ui_markerpopup import Ui_MarkerDockwidget

class MarkerPopUpCon(QDockWidget):
    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)
        self.ui_marker = Ui_MarkerDockwidget()
        self.marker_model = MarkerPopUpModel()
        self.ui_marker.setupUi(self)
        self.ui_marker.addMarkerBtn.clicked.connect(self.marker_model.addMarker())
        # self.hide()