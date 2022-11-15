# This Python file uses the following encoding: utf-8
import folium
import io, base64
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget

class MapViewDockWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.coordinate = (7.9465, 1.0232)
        self.map= folium.Map(
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

    def addMarker(self, imgFilePath, dict_):
#        a function that adds image markers to map
        name = imgFilePath.split("\\")[-1].split(".")[0]
        folium.Marker(
        location=[dict_['lat'], dict_['long']],
        tooltip=(
        "<html>"
        "<div class='col1'><b>sender: </b>{sender}<br>"
        "<b>lat: </b>{lat}<br>"
        "<b>long: </b>{_long}<br>"
        "<b>time taken: </b>{tHr}:{tMn}<br>"
        "<b>date: </b>{date}<br>"
        "<b>altitude: </b>{alt}<br>"
        "<b>file: </b>{file}<br></div>"
#        "<div class='col2'>"
#        "<img src=\"file:///{source}\" width=\"250\" height=\"150\"></div>"
        "</html>"
        ).format(
        #source="/".join(imgFilePath.split("\\")),
        sender="ama", lat=dict_['lat'], _long=dict_['long'], tHr=int(dict_['timestamp'][0]),tMn=int(dict_['timestamp'][1]), date=dict_['datestamp'],alt=dict_['altitude'],file=name),
        icon=folium.Icon(color='green')).add_to(self.map)
        self.save()
