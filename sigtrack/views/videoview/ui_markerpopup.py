from PySide2.QtGui import QCloseEvent, QIcon
from PySide2.QtWidgets import QDockWidget, QVBoxLayout, QPushButton

from sigtrack.views.videoview.markers.ui_marker import UI_Marker
import sigtrack.resources.compiled.map_rc


class UI_MarkerPopUp(QDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFloating(True)
        self.setWindowTitle("Markers")
        self.setWindowIcon(QIcon('qrc://:marker'))
        self.markersLayout = QVBoxLayout()
        self.addMarkerButton = QPushButton("Add")
        self.setupUI()
    
    def setupUI(self) -> None:
        """
            set up the ui for the marker pop up dockwidget
        """
        layout = QVBoxLayout()
        layout.addLayout(self.markersLayout)
        layout.addWidget(self.addMarkerButton)
        self.setLayout(layout)

    def addMarker(self, marker:UI_Marker):
        """
            add marker entry to dockwidget
        """
        self.markersLayout.addLayout(marker)
    
    def closeEvent(self, event: QCloseEvent) -> None:
        """
            remove all markers
        """
        return super().closeEvent(event)