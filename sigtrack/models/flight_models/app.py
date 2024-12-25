import sys
import requests
from PySide6.QtCore import QUrl, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from sigtrack.models.flight_models.flightmodel import FlightModel
from sigtrack.utils.airplane_api_wrapper import AirplanesApiWrapper
import map_rc
if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    # engine.load(QUrl('qrc://:/map'))

    # Initialize API wrapper and model

    # Load QML
    # engine.load("tests\\map.qml")
    