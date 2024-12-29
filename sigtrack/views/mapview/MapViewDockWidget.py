from PySide6.QtCore import QObject, QUrl, Signal, Slot
from PySide6.QtPositioning import QGeoCoordinate
from PySide6.QtQuickWidgets import QQuickWidget

from sigtrack.models.map_models.DroneModel import DroneModel
from sigtrack.models.map_models.FMVModel import FMVModel
from sigtrack.models.map_models.MarkerModel import MarkerModel
import sigtrack.resources.compiled.map_rc


class iceController(QObject):
    showImageSignal = Signal(str)

    def __init__(self):
        QObject.__init__(self)

    @Slot(str)
    def showImage(self, path):
        self.showImageSignal.emit(path)

    @Slot(str)
    def log(self, s):
        print(s)


class MapWidget(QQuickWidget):
    def __init__(self, mainWindow, parent=None):
        super(MapWidget, self).__init__(parent, resizeMode=QQuickWidget.SizeRootObjectToView)
        self.mainWindow = mainWindow
        self.markermodel = MarkerModel(self)
        self.dronemodel = DroneModel(self)
        self.fmvmodel = FMVModel(self)
        self.rootContext().setContextProperty("dronemodel", self.dronemodel)
        self.rootContext().setContextProperty("fmvmodel", self.fmvmodel)
        self.rootContext().setContextProperty("markermodel", self.markermodel)
        self.ice = iceController()
        self.rootContext().setContextProperty('PyConsole', self.ice)
        self.rootContext().setContextProperty('ice', self.ice)
        self.ice.showImageSignal.connect(self.showImage)
        self.setSource(QUrl('qrc://:/map'))
        # self.setSource(QUrl.fromLocalFile('sigtrack/views/mapview/map.qml'))
        self.mainWindow.map = self
        self.circleCenterMarker = None

    def focusInEvent(self, event):
        """
        set the map in focus as the current map
        """
        self.mainWindow.map = self
        QQuickWidget.focusInEvent(self, event)

    def showImage(self, imgPath):
        """
        call the imageAction.. This will add the image to an image viewer
        """
        self.mainWindow.imageAction(imgPath)

    def addMarker(self, imgPath, imgData: dict):
        """
        Adds a marker for any imported image
        """
        # print(imgPath, imgData)
        coord = QGeoCoordinate(imgData['lat'], imgData['long'])
        source = QUrl("qrc://:/marker")
        tooltip = "<b>sender: </b> @soldierName<br>"
        tooltip += f"<b>lat: </b> {coord.latitude()}<br>"
        tooltip += f"<b>long: </b> {coord.longitude()}<br>"
        # tooltip += f"<b>alt: </b> {imgData.get('alt', 'NA')}<br>"
        # exifData = imgData.get('info')
        # # print(exifData.list_all(), "yie")
        # info = exifData.list_all()
        # print(info)
        # for property in info:
        #     try:
        #         if property == 'flash':
        #             continue
        #         # if exifData.get(property, "Unable to read"):
        #         tooltip += f'<b>{property}:</b> {exifData.get(property, "Unable to read")}<br>'
        #     except:
        #         tooltip += f'<b>{property}:</b> Unable to read<br>'
        #     print(f"position: {coord}\n, source: {source}\n, imgPath: {imgPath}\n, imgTooltip: {tooltip}\n")
        self.markermodel.appendMarker(
            {"position": coord, "source": source, "imgPath": imgPath, "imgTooltip": tooltip})

    def updateDronePosition(self, droneData: dict):
        """
        drone is updated like a marker, wll change soon
        """
        droneCoord = QGeoCoordinate(
            float(droneData['Sensor Latitude']), float(droneData['Sensor Longitude']))

        heading = float(droneData['Platform Heading Angle'])
        # Update the data in the model
        self.dronemodel.updateData(droneCoord, heading)

        #     self.dronemodel["position"] = QGeoCoordinate(
        #         float(droneData['Sensor Latitude']), float(droneData['Sensor Longitude']))
        #     index = self.markermodel.index(0)
        #     self.markermodel.dataChanged.emit(
        #         index, index, [MarkerModel.PositionRole])
        fraCenLat = float(droneData['Frame Center Latitude'])
        fraCenLong = float(droneData['Frame Center Longitude'])
        corner1 = QGeoCoordinate(float(
            droneData['Offset Corner Latitude Point 1'])+fraCenLat, float(droneData['Frame Center Longitude'])+fraCenLong)
        corner2 = QGeoCoordinate(float(droneData['Offset Corner Latitude Point 2'])+fraCenLat, float(
            droneData['Offset Corner Longitude Point 2'])+fraCenLong)
        corner3 = QGeoCoordinate(float(droneData['Offset Corner Latitude Point 3'])+fraCenLat, float(
            droneData['Offset Corner Longitude Point 3'])+fraCenLong)
        corner4 = QGeoCoordinate(float(droneData['Offset Corner Latitude Point 4'])+fraCenLat, float(
            droneData['Offset Corner Longitude Point 4'])+fraCenLong)
        center = QGeoCoordinate(fraCenLat, fraCenLong)
        # self.polyline.addCoordinate(droneCoord)
        self.fmvmodel.updateData(
            polygon_points=[corner1, corner2, corner3, corner4],
            line_points=[
                [corner4, droneCoord],
                [corner3, droneCoord],
                [corner2, droneCoord],
                [corner1, droneCoord],
                [center, droneCoord]
            ]
        )
