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

        api_wrapper = AirplanesApiWrapper()
        model = FlightModel()
        api_wrapper.dataFetched.connect(model.updateFlights)
        api_wrapper.errorOccurred.connect(lambda error: print(f"Error: {error}"))
        self.rootContext().setContextProperty("flightModel", model)

        self.setSource(QUrl('qrc://:/flightmap'))
        self.mainWindow.map = self
        
        # Timer to fetch data every second
        timer = QTimer()
        timer.timeout.connect(api_wrapper.fetch_flights)
        timer.start(1000)  # 1-second interval
