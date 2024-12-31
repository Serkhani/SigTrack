from PySide6.QtCore import QObject, QUrl, Signal, Slot, QTimer 
from PySide6.QtPositioning import QGeoCoordinate
from PySide6.QtQuickWidgets import QQuickWidget

from sigtrack.models.flight_models.flightmodel import FlightModel
import sigtrack.resources.compiled.flight_rc
from sigtrack.utils.airplane_api_wrapper import AirplanesApiWrapper
from sigtrack.views.mapview.MapViewDockWidget import MapWidget


class FlightWidget(QQuickWidget):
    def __init__(self, mainWindow, parent=None):
        super(FlightWidget, self).__init__(parent, resizeMode=QQuickWidget.SizeRootObjectToView)
        self.mainWindow = mainWindow

        self.api_wrapper = AirplanesApiWrapper()
        self.model = FlightModel()
        self.api_wrapper.dataFetched.connect(self.model.updateFlights)
        self.api_wrapper.errorOccurred.connect(lambda error: print(f"Error: {error}"))
        self.rootContext().setContextProperty("flightModel", self.model)

        self.setSource(QUrl('qrc://:/flightmap'))
        self.mainWindow.map = self
        
        # Timer to fetch data every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.api_wrapper.fetch_flights)
        self.timer.start(1000)  # 1-second interval
        
    def closeEvent(self, event):
        self.timer.stop()
        self.api_wrapper.blockSignals(True)
        super().closeEvent(event)
