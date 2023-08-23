from PySide2.QtWidgets import QHBoxLayout, QGraphicsView, QLabel, QPushButton
from PySide2.QtCore import Qt

from sigtrack.models.video_models.marker.video_marker import VideoMarker

class UI_Marker(QHBoxLayout):
    """
        ui for each marker
    """
    def __init__(self):
        super().__init__()
        # indicator
        self.indicator = QGraphicsView()
        # lat
        self.lat = QLabel("0.0")
        # lon
        self.lon = QLabel("0.0")
        # close
        self.closeButton = QPushButton("X")
        self.setUpUI()
    
    def setUpUI(self):
        self.addWidget(self.indicator)
        self.addWidget(self.lat)
        self.addWidget(self.lon)
        self.addWidget(self.closeButton)
        
    def change_text(self, data: list) -> None:
        """
        Change the text when the button is clicked
        """
        self.lat.setText(f"lat: {str(data[0])}")
        self.lon.setText(f"lon: {str(data[1])}")