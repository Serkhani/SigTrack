from DockWidgets.mapview.models.MarkerModel import MarkerModel
from DockWidgets.mapview.models.DroneModel import DroneModel
from DockWidgets.mapview.models.FMVModel import FMVModel
from PySide2.QtQuickWidgets import QQuickWidget
from PySide2.QtPositioning import QGeoCoordinate
from PySide2.QtCore import QObject, Slot, Signal, QUrl
from exif import Image
import DockWidgets.mapview.rc_map


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
        super(MapWidget, self).__init__(
            parent, resizeMode=QQuickWidget.SizeRootObjectToView)
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
        # self.setSource(QUrl.fromLocalFile('Dockwidgets/mapview/map.qml'))
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
        coord = QGeoCoordinate(imgData['lat'], imgData['long'])
        source = QUrl(
            "http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_gray.png")
        tooltip = "<b>sender: </b> @soldierName<br>"
        exifData = imgData.get('info', Image)
        for property in exifData.get_all():
            try:
                if property == 'flash':
                    continue
                tooltip += f'<b>{property}:</b> {exifData[property]}<br>'
            except:
                tooltip += f'<b>{property}:</b> Unable to read<br>'

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

        #     # emit dataChanged signal for the updated marker
        #     self.circleCenterMarker["position"] = center
        #     index = self.markermodel.index(1)
        #     self.markermodel.dataChanged.emit(
        #         index, index, [MarkerModel.PositionRole])

        # else:
        #     self.addDrone(droneData)

    # def addDrone(self, droneData: dict):
    #     """
    #     drone is added like a marker, wll change soon
    #     """
    #     droneCoord = QGeoCoordinate(
    #         float(droneData['Sensor Latitude']), float(droneData['Sensor Longitude']))
    #     self.dronemodel.setProperty("coordinate", droneCoord)
    #     corner1 = QGeoCoordinate(float(droneData['Offset Corner Latitude Point 1']), float(
    #         droneData['Offset Corner Longitude Point 1']))
    #     corner2 = QGeoCoordinate(float(droneData['Offset Corner Latitude Point 2']), float(
    #         droneData['Offset Corner Longitude Point 2']))
    #     corner3 = QGeoCoordinate(float(droneData['Offset Corner Latitude Point 3']), float(
    #         droneData['Offset Corner Longitude Point 3']))
    #     corner4 = QGeoCoordinate(float(droneData['Offset Corner Latitude Point 4']), float(
    #         droneData['Offset Corner Longitude Point 4']))
    #     center = QGeoCoordinate(float(
    #         droneData['Frame Center Latitude']), float(droneData['Frame Center Longitude']))

        # # Add the new row to the model
        # self.dronemodel.beginInsertRows(QModelIndex(), 0, 0)
        # self.dronemodel.endInsertRows()
    #     # self.dronemodel = {"position": droneCoord, "source": droneUrl,
    #     #                     "imgPath": droneImgPath, "imgTooltip": tooltip}
    #     # self.markermodel.appendMarker(self.dronemodel)
    #     cornerCircleImgPath = 'qrc://:/ccircle'
    #     cornerCircleUrl = QUrl(cornerCircleImgPath)
    #     circleCenterImgPath = 'qrc://:/circlec'
    #     circleCenterUrl = QUrl(circleCenterImgPath)
    #     self.circleCenterMarker = {"position": center, "source": circleCenterUrl,
    #                                "imgPath": circleCenterImgPath, "imgTooltip": "Circle Center"}
    #     self.markermodel.appendMarker(self.circleCenterMarker)

    #     # self.fmvmodel.setData(self.fmvmodel.index(0),[corner1, corner2, corner3, corner4], self.fmvmodel.PolygonRole)#for polyon
    #     # self.fmvmodel.setData(self.fmvmodel.index(1),[], self.fmvmodel.DroneRole)#for drone
    #     # self.fmvmodel.setData(self.fmvmodel.index(2),[], self.fmvmodel.LineRole)#for line
    #     self.dronemodel.setData(self.dronemodel.index(0), droneCoord, DroneModel.PositionRole)
    #     self.dronemodel.setData(self.dronemodel.index(0), [], DroneModel.PathRole)
