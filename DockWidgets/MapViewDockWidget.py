# This Python file uses the following encoding: utf-8
import folium
import io
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget

class MapViewDockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.coordinate = (7.9465, 1.0232)
        self.map= folium.Map(
#                tiles='Stamen Terrain',
                tiles= 'openstreetmap',
                zoom_start=6,
                location=self.coordinate
        )
        self.webView = QWebEngineView()#creating the widget to be able to view the map
        self.save()

    def save(self):
        # save map data to data object
        self.data = io.BytesIO()
        self.map.save(self.data, close_file=False)
        self.webView.setHtml(self.data.getvalue().decode())

    def addMarker(self, lat, long_, name):
#        a function that adds image markers to map
        folium.Marker(
        location=[lat, long_],
        popup=name,
        icon=folium.Icon(color='green')).add_to(self.map)
        self.save()
