from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget, QDockWidget #, QMessageBox
from PySide2.QtCore import Qt
from PySide2.QtPositioning import QGeoCoordinate

class MarkerPopUp(QDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.parent = parent
        # x, y = parent.width()//2.5 - parent.pos().x(), parent.pos().y() - 50
        # self.setGeometry(x, y, 400, 400)
        # self.setFixedSize(self.size())
        # self.setWindowFlags(
        #     Qt.FramelessWindowHint
        #     | Qt.WindowSystemMenuHint
        #     | Qt.WindowTitleHint
        #     | Qt.WindowMinimizeButtonHint
        #     | Qt.WindowCloseButtonHint
        #     | Qt.WindowStaysOnTopHint
        # )
        
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

    
