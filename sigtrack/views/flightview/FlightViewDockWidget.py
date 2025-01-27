from PySide6.QtCore import QObject, QUrl, Signal, Slot, QTimer, Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtPositioning import QGeoCoordinate
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QColor, QPalette

from sigtrack.models.flight_models.flightmodel import FlightModel
import sigtrack.resources.compiled.flight_rc
from sigtrack.utils.airplane_api_wrapper import AirplanesApiWrapper
from sigtrack.views.mapview.MapViewDockWidget import MapWidget


class IceController(QObject):
    update_url = Signal(list)

    def __init__(self):
        QObject.__init__(self)

    @Slot(str)
    def showImage(self, url):
        self.update_url.emit(url)

    @Slot(str)
    def log(self, s):
        print(s)


class FlightWidget(QQuickWidget):
    def __init__(self, mainWindow, parent=None):
        super(FlightWidget, self).__init__(parent, resizeMode=QQuickWidget.SizeRootObjectToView)
        self.mainWindow = mainWindow

        self.api_wrapper = AirplanesApiWrapper()
        self.model = FlightModel()
        self.api_wrapper.dataFetched.connect(self.model.updateFlights)
        self.api_wrapper.errorOccurred.connect(self.show_error_notification)  # Connect to error handler

        self.rootContext().setContextProperty("flightModel", self.model)
        self.ice = IceController()
        self.rootContext().setContextProperty('PyConsole', self.ice)
        self.rootContext().setContextProperty('ice', self.ice)
        self.ice.update_url.connect(self.api_wrapper._update_api_url)

        self.setSource(QUrl('qrc://:/flightmap'))

        # Timer to fetch data every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.api_wrapper.fetch_flights)
        self.timer.start(1000)  # 1-second interval

        # Notification setup
        self.notification = QLabel(self)
        self.notification.setStyleSheet(
            """
            QLabel {
                background-color: rgba(50, 50, 50, 200);
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            """
        )
        self.notification.setAlignment(Qt.AlignCenter)
        self.notification.hide()  # Initially hidden
        self.notification_timer = QTimer(self)
        self.notification_timer.timeout.connect(self.hide_notification)

    def closeEvent(self, event):
        self.timer.stop()
        self.api_wrapper.blockSignals(True)
        super().closeEvent(event)

    def show_error_notification(self, error_message):
        """
        Show a small notification at the bottom-left corner.
        """
        self.notification.setText(error_message)
        self.notification.adjustSize()  # Resize to fit text

        # Position the notification at the bottom-left corner
        self.notification.move(10, self.height() - self.notification.height() - 10)

        # Show the notification with a fade-in animation
        self.notification.show()
        self.fade_in_notification()

        # Automatically hide the notification after 3 seconds
        self.notification_timer.start(1500)

    def hide_notification(self):
        """
        Hide the notification with a fade-out animation.
        """
        self.fade_out_notification()
        self.notification_timer.stop()

    def fade_in_notification(self):
        """
        Fade-in animation for the notification.
        """
        animation = QPropertyAnimation(self.notification, b"windowOpacity", self)
        animation.setDuration(500)  # 0.5 seconds
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()

    def fade_out_notification(self):
        """
        Fade-out animation for the notification.
        """
        animation = QPropertyAnimation(self.notification, b"windowOpacity", self)
        animation.setDuration(500)  # 0.5 seconds
        animation.setStartValue(1)
        animation.setEndValue(0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.finished.connect(self.notification.hide)  # Hide after animation
        animation.start()