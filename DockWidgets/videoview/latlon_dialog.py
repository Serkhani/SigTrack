from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget#, QMessageBox
from PySide2.QtCore import Qt
from PySide2.QtPositioning import QGeoCoordinate

class MarkerPopUp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("LatLon")
        
        self.isAddMarker = False

        # Create the layout
        layout = QVBoxLayout()
        horizontal = QHBoxLayout()

        # Create the widgets
        self.lat = QLabel("0.0")
        self.lon = QLabel("0.0")
        self.markerButton = QPushButton("Add")
        self.markerButton.clicked.connect(self.changeAddMarker)

        # Add the widgets to the layout
        horizontal.addWidget(self.lat)
        horizontal.addWidget(self.lon)
        layout.addLayout(horizontal)
        layout.addWidget(self.markerButton)

        # Set the layout for the dialog
        self.setLayout(layout)

    def changeAddMarker(self):
        self.isAddMarker = not self.isAddMarker
        
        print(self.isAddMarker)

    def change_text(self, data: list) -> None:
        # print(f"moouse.x(): {data.x()} mouse.y: {data.y()}")
        # print(f"moouse.x(): {data.latitude()} mouse.y: {data.longitude()}")
        # print(f"moouse.x(): {type(data.latitude())} mouse.y: {data.longitude()}")
        # Change the text when the button is clicked
        self.lat.setText(f"lat: {str(data[0])}")
        self.lon.setText(f"lon: {str(data[1])}")
