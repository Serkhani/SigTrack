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
        if reply.error() != QNetworkReply.NoError:
            self.errorOccurred.emit(reply.errorString())
            return

        # Read and decode the reply data
        data = json.loads(reply.readAll().data().decode())
        
        # Extract the list of flights
        flights = data.get("ac", [])
        
        # Format the data for the model
        formatted_data = [
            {
                "hex": item.get("hex", "Unknown"),
                "type": item.get("type", "Unknown"),
                "flight": item.get("flight", "Unknown").strip(),
                "registration": item.get("r", "Unknown"),
                "aircraft_type": item.get("t", "Unknown"),
                "description": item.get("desc", "Unknown"),
                "operator": item.get("ownOp", "Unknown"),
                "year": item.get("year", "Unknown"),
                "alt_baro": item.get("alt_baro", 0.0),
                "alt_geom": item.get("alt_geom", 0.0),
                "ground_speed": item.get("gs", 0.0),
                "track": item.get("track", 0.0),
                "baro_rate": item.get("baro_rate", 0.0),
                "geom_rate": item.get("geom_rate", 0.0),
                "squawk": item.get("squawk", "Unknown"),
                "emergency": item.get("emergency", "none"),
                "category": item.get("category", "Unknown"),
                "nav_qnh": item.get("nav_qnh", 0.0),
                "nav_altitude_mcp": item.get("nav_altitude_mcp", 0.0),
                "nav_heading": item.get("nav_heading", 0.0),
                "lat": item.get("lat", 0.0),
                "lon": item.get("lon", 0.0),
                "nic": item.get("nic", 0),
                "rc": item.get("rc", 0),
                "seen_pos": item.get("seen_pos", 0.0),
                "messages": item.get("messages", 0),
                "seen": item.get("seen", 0.0),
                "rssi": item.get("rssi", 0.0),
                "distance": item.get("dst", 0.0),
                "direction": item.get("dir", 0.0),
            }
            for item in flights
        ]
        
        # Emit the formatted data
        self.dataFetched.emit(formatted_data)
        
    def _update_api_url(self, props:list):
        
        self.api_url = f"https://api.airplanes.live/v2/point/{props[0] if props[0] else self.lat}/{props[1] if props[1] else self.lon}/{props[2] if props[2] else self.radius}"
        
        print(self.api_url)