import sys
import requests
from PySide6.QtCore import QUrl, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from model import FlightModel
from sigtrack.utils.airplane_api_wrapper import AirplanesApiWrapper
import map_rc
if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    # engine.load(QUrl('qrc://:/map'))

    # Initialize API wrapper and model
    api_wrapper = AirplanesApiWrapper()
    model = FlightModel()

    # Connect signals
    api_wrapper.dataFetched.connect(model.updateFlights)
    api_wrapper.errorOccurred.connect(lambda error: print(f"Error: {error}"))

    engine.rootContext().setContextProperty("flightModel", model)

    # Load QML
    # engine.load("tests\\map.qml")
    engine.load(QUrl('qrc://:/map'))
    if not engine.rootObjects():
        sys.exit(-1)

    # Timer to fetch data every second
    timer = QTimer()
    timer.timeout.connect(api_wrapper.fetch_flights)
    timer.start(1000)  # 1-second interval

    sys.exit(app.exec())