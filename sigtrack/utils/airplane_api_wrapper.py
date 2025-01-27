import sys
from PySide6.QtCore import QUrl, QObject, Signal
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import json

API_URL = "https://api.airplanes.live/v2/point/5.658735/-0.184961/250"
# API_URL = "https://api.airplanes.live/v2/point/39.742043/-104.991531/250"

class AirplanesApiWrapper(QObject):
    errorOccurred = Signal(str)
    dataFetched = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._network_manager = QNetworkAccessManager()
        self.api_url = API_URL
        self.lat, self.lon, self.radius = self.api_url.split('/')[-3:]
        

    def fetch_flights(self):
        request = QNetworkRequest(QUrl(self.api_url))
        reply = self._network_manager.get(request)
        reply.finished.connect(lambda: self._handle_reply(reply))
        reply.errorOccurred.connect(lambda error: self.errorOccurred.emit(error))

    def _handle_reply(self, reply):
        reply.deleteLater()
        if reply.error()!=QNetworkReply.NoError:
            self.errorOccurred.emit(reply.errorString())
            return

        data = json.loads(reply.readAll().data().decode())
        flights = data.get("ac", [])
        formatted_data = [
            {
                "flight": item.get("flight", "Unknown"),
                "lat": item.get("lat", 0.0),
                "lon": item.get("lon", 0.0),
                "alt_baro": item.get("alt_baro", 0.0),
                "track": item.get("track", 0.0),
                "ownOp": item.get("ownOp", "Unknown"),
                # "url": [lat, lon, radius]
            }
            for item in flights
        ]
        # print(formatted_data)
        self.dataFetched.emit(formatted_data)
        
    def _update_api_url(self, props:list):
        
        self.api_url = f"https://api.airplanes.live/v2/point/{props[0] if props[0] else self.lat}/{props[1] if props[1] else self.lon}/{props[2] if props[2] else self.radius}"
        
        print(self.api_url)