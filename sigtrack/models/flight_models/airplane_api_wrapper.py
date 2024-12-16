import sys
from PySide6.QtCore import QTimer, QUrl, Qt, QAbstractListModel, QModelIndex, QObject, Signal, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import json
from pprint import pprint

# API_URL = "https://api.airplanes.live/v2/point/5.658735/-0.184961/250"
API_URL = "https://api.airplanes.live/v2/point/39.742043/-104.991531/250"

class AirplanesApiWrapper(QObject):
    errorOccurred = Signal(str)
    dataFetched = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._network_manager = QNetworkAccessManager()

    def fetch_flights(self):
        request = QNetworkRequest(QUrl(API_URL))
        reply = self._network_manager.get(request)
        reply.finished.connect(lambda: self._handle_reply(reply))

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
            }
            for item in flights
        ]
        self.dataFetched.emit(formatted_data)