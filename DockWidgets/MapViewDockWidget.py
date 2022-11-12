# This Python file uses the following encoding: utf-8
import folium
import io
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget

class MapViewDockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.coordinate = (7.9465, 1.0232)
        self.m = folium.Map(
#                tiles='Stamen Terrain',
                tiles= 'openstreetmap',
                zoom_start=6,
                location=self.coordinate
        )

        # save map data to data object
        self.data = io.BytesIO()
        self.m.save(self.data, close_file=False)

        self.webView = QWebEngineView()
        self.webView.setHtml(self.data.getvalue().decode())
#        layout.addWidget(webView)
