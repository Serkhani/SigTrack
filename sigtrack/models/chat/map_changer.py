from PySide6.QtWidgets import QWidget, QRadioButton,QVBoxLayout
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
import sigtrack.models.chat.qt_icons_rc

class MapChanger(QWidget):
    map_changed = Signal(str)  # Signal to notify when the map is changed

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Map")
        self.setGeometry(100, 100, 800, 600)

        # Create buttons
        self.mapbox_icon = QRadioButton("MapBox")
        self.mapbox_icon.setIcon(QIcon(":/qt_icons/map_icon.ico"))
        self.mapbox_icon.setToolTip("Mapbox")

        self.leaflet_icon = QRadioButton("Leaflet Map")
        self.leaflet_icon.setIcon(QIcon(":/qt_icons/map_icon.ico"))
        self.leaflet_icon.setToolTip("Leaflet Map")

        self.google_icon = QRadioButton("Google Map")
        self.google_icon.setIcon(QIcon(":/qt_icons/map_icon.ico"))
        self.google_icon.setToolTip("Google Map")

       

        # Connect radio buttons to the slot
        self.mapbox_icon.toggled.connect(lambda: self.map_changed.emit('mapbox') if self.mapbox_icon.isChecked() else None)
        self.leaflet_icon.toggled.connect(lambda: self.map_changed.emit('leaflet') if self.leaflet_icon.isChecked() else None)
        self.google_icon.toggled.connect(lambda: self.map_changed.emit('google') if self.google_icon.isChecked() else None)
       
        # Layout for buttons
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.mapbox_icon)
        button_layout.addWidget(self.leaflet_icon)
        button_layout.addWidget(self.google_icon)
     
        # Main layout
        self.layout = QVBoxLayout()
        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)
