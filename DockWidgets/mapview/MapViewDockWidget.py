from math import cos, tan, log, pi
from PySide2 import QtQuickWidgets, QtPositioning, QtCore, QtLocation
from PySide2.QtCore import QObject, Slot, Signal, QPointF, QAbstractListModel, QModelIndex, Qt, QUrl
from PySide2.QtGui import QIcon
from exif import Image
import DockWidgets.mapview.rc_map


# class DroneModel(QAbstractListModel):
#     IconRole, PositionRole, PathRole = range(Qt.UserRole, Qt.UserRole + 3)

#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self._drone_position = QtPositioning.QGeoCoordinate()
#         self._drone_path = []

#     def rowCount(self, parent=QModelIndex()):
#         return 1

#     def data(self, index, role=Qt.DisplayRole):
#         if 0 <= index.row() < self.rowCount():
#             if role == DroneModel.PositionRole:
#                 return self._drone_position
#             elif role == DroneModel.IconRole or role == Qt.DecorationRole:
#                 return QUrl('qrc://:/drone')
#             elif role == DroneModel.PathRole:
#                 return self._drone_path
#         return QtCore.QVariant()


#     def roleNames(self):
#         return {
#             DroneModel.IconRole: b"droneIcon",
#             DroneModel.PositionRole: b"dronePosition",
#             DroneModel.PathRole: b"dronePath",
#         }
    
#     def updateData(self, drone_position: QtPositioning.QGeoCoordinate):
#         """
#         Updates the drone position as well as the path
#         """
#         # self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
#         # print(f"self.dronepath: {self._drone_path}")
#         self._drone_position = drone_position
#         self._drone_path.append(drone_position)
#         # print(f"self.dronepath: {self._drone_path}")
#         # print(f"dronePosition: {drone_position}\ndronepath: {self._drone_path}")
#         self.dataChanged.emit(self.index(0), self.index(self.rowCount() - 1), [DroneModel.IconRole, DroneModel.PositionRole, DroneModel.PathRole])
#         # self.endInsertRows()

class DroneModel(QAbstractListModel):
    IconRole, PositionRole, PathRole, PolylineRole = range(
        Qt.UserRole, Qt.UserRole + 4)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._drone_position = QtPositioning.QGeoCoordinate()
        self._drone_path = []
        self._drone_polyline = QtPositioning.QGeoPath()
        # self._drone_polyline.setColor(Qt.red)
        self._drone_polyline.setWidth(3)

    def rowCount(self, parent=QModelIndex()):
        return 1

    def data(self, index, role=Qt.DisplayRole):
        if 0 <= index.row() < self.rowCount():
            if role == DroneModel.PositionRole:
                return self._drone_position
            elif role == DroneModel.IconRole or role == Qt.DecorationRole:
                return QUrl('qrc://:/drone')
            elif role == DroneModel.PathRole:
                return self._drone_path
            elif role == DroneModel.PolylineRole:
                return self._drone_polyline
        return QtCore.QVariant()

    def roleNames(self):
        return {
            DroneModel.IconRole: b"droneIcon",
            DroneModel.PositionRole: b"dronePosition",
            DroneModel.PathRole: b"dronePath",
            DroneModel.PolylineRole: b"dronePolyline",
        }

    def setData(self, index, value, role):
        if not index.isValid() or index.row() != 0 or role not in [DroneModel.IconRole, DroneModel.PositionRole, DroneModel.PathRole, DroneModel.PolylineRole]:
            return False

        if role == DroneModel.IconRole:
            return False
        elif role == DroneModel.PositionRole:
            self._drone_position = value
        elif role == DroneModel.PathRole:
            self._drone_path = value
            self._updatePolyline()
        elif role == DroneModel.PolylineRole:
            return False
        else:
            return False

        self.dataChanged.emit(index, index, [role])
        return True

    def _updatePolyline(self):
        # self._drone_polyline.clear()
        self._drone_polyline.addCoordinate(self._drone_position)
        for coord in self._drone_path:
            self._drone_polyline.addCoordinate(coord)
        self.dataChanged.emit(self.index(0), self.index(
            self.rowCount() - 1), [DroneModel.PolylineRole])

    def updateData(self, drone_position, drone_path):
        # self._drone_position = QtPositioning.QGeoCoordinate(
        #     drone_position[0], drone_position[1])
        # self._drone_path = [QtPositioning.QGeoCoordinate(
        #     lat, lon) for lat, lon in drone_path]
        self._drone_position = drone_position
        self._drone_path.append(drone_path)
        self._updatePolyline()
        self.dataChanged.emit(self.index(0), self.index(self.rowCount(
        ) - 1), [DroneModel.PositionRole, DroneModel.PathRole, DroneModel.PolylineRole])


class FMVModel(QAbstractListModel):
    PolygonRole, LineRole = range(Qt.UserRole, Qt.UserRole + 2)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._line_points = []
        self._polygon_points = []

    def roleNames(self):
        return {
            FMVModel.PolygonRole: b"polygonPoints",
            FMVModel.LineRole: b"linePoints"
        }

    def rowCount(self, parent=QModelIndex()):
        return 5


    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        if role == Qt.DisplayRole:
            if row == 0:
                return "Polygon"
            elif row == 1:
                return "Line"
        if role == Qt.DecorationRole:
            return None
        elif role == FMVModel.PolygonRole:
            return self._polygon_points
        elif role == FMVModel.LineRole:
            return self._line_points

    def setData(self, index, value, role):
        if not index.isValid() or index.row() != 0 or role != FMVModel.PolygonRole:
            return False

        if role == FMVModel.PolygonRole:
            self._polygon_points = value
        elif role == FMVModel.LineRole:
            self._line_points = value
        else:
            return False
        self.dataChanged.emit(index, index, [role])
        return True
    
    def updateData(self, polygon_points: list[QtPositioning.QGeoCoordinate], line_points: list[list[QtPositioning.QGeoCoordinate]]):
        self._polygon_points = polygon_points
        self._line_points = line_points
        self.dataChanged.emit(self.index(0), self.index(self.rowCount() - 1), [FMVModel.PolygonRole, FMVModel.LineRole])


class MarkerModel(QAbstractListModel):
    PositionRole, SourceRole, TooltipRole, ImagePathRole = range(
        Qt.UserRole, Qt.UserRole + 4)

    def __init__(self, parent=None):
        super(MarkerModel, self).__init__(parent)
        self._markers = []

    def rowCount(self, parent=QModelIndex()):
        return len(self._markers)

    def data(self, index, role=Qt.DisplayRole):
        if 0 <= index.row() < self.rowCount():
            if role == MarkerModel.PositionRole:
                return self._markers[index.row()]["position"]
            elif role == MarkerModel.SourceRole:
                return self._markers[index.row()]["source"]
            elif role == MarkerModel.TooltipRole:
                return self._markers[index.row()]["imgTooltip"]
            elif role == MarkerModel.ImagePathRole:
                return self._markers[index.row()]["imgPath"]
        return QtCore.QVariant()

    def roleNames(self):
        return {MarkerModel.PositionRole: b"position_marker", MarkerModel.SourceRole: b"source_marker", MarkerModel.TooltipRole: b"tooltip", MarkerModel.ImagePathRole: b"imgPath"}

    def appendMarker(self, marker):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._markers.append(marker)
        self.endInsertRows()


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


class MapWidget(QtQuickWidgets.QQuickWidget):
    def __init__(self, mainWindow, parent=None):
        super(MapWidget, self).__init__(parent, resizeMode=QtQuickWidgets.QQuickWidget.SizeRootObjectToView)
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
        self.polyline = QtPositioning.QGeoPath()

        

        self.circleCenterMarker = None

    def focusInEvent(self, event):
        """
        set the map in focus as the current map
        """
        self.mainWindow.map = self
        QtQuickWidgets.QQuickWidget.focusInEvent(self, event)

    def showImage(self, imgPath):
        """
        call the imageAction.. This will add the image to an image viewer
        """
        self.mainWindow.imageAction(imgPath)

    def addMarker(self, imgPath, imgData: dict):
        """
        Adds a marker for any imported image
        """
        coord = QtPositioning.QGeoCoordinate(imgData['lat'], imgData['long'])
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
        # if self.dronemodel._drone_position.isValid():
        droneCoord = QtPositioning.QGeoCoordinate(float(droneData['Sensor Latitude']), float(droneData['Sensor Longitude']))
        # Check if the model already exists, otherwise create a new one
        # if not hasattr(self, 'dronemodel'):
        #     self.dronemodel = DroneModel()

        # Update the data in the model
        self.dronemodel.updateData(droneCoord, droneCoord)
        # print("hi")


        #     self.dronemodel["position"] = QtPositioning.QGeoCoordinate(
        #         float(droneData['Sensor Latitude']), float(droneData['Sensor Longitude']))
        #     index = self.markermodel.index(0)
        #     self.markermodel.dataChanged.emit(
        #         index, index, [MarkerModel.PositionRole])

        corner1 = QtPositioning.QGeoCoordinate(float(droneData['Offset Corner Latitude Point 1']), float(
            droneData['Offset Corner Longitude Point 1']))
        corner2 = QtPositioning.QGeoCoordinate(float(droneData['Offset Corner Latitude Point 2']), float(
            droneData['Offset Corner Longitude Point 2']))
        corner3 = QtPositioning.QGeoCoordinate(float(droneData['Offset Corner Latitude Point 3']), float(
            droneData['Offset Corner Longitude Point 3']))
        corner4 = QtPositioning.QGeoCoordinate(float(droneData['Offset Corner Latitude Point 4']), float(
            droneData['Offset Corner Longitude Point 4']))
        center = QtPositioning.QGeoCoordinate(float(
            droneData['Frame Center Latitude']), float(droneData['Frame Center Longitude']))
        self.polyline.addCoordinate(droneCoord)
        self.fmvmodel.updateData(
            polygon_points= [corner1, corner2, corner3, corner4],
            line_points=[
                [corner4, droneCoord],
                [corner3, droneCoord],
                [corner2, droneCoord],
                [corner1, droneCoord],
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
    #     droneCoord = QtPositioning.QGeoCoordinate(
    #         float(droneData['Sensor Latitude']), float(droneData['Sensor Longitude']))
    #     self.dronemodel.setProperty("coordinate", droneCoord)
    #     corner1 = QtPositioning.QGeoCoordinate(float(droneData['Offset Corner Latitude Point 1']), float(
    #         droneData['Offset Corner Longitude Point 1']))
    #     corner2 = QtPositioning.QGeoCoordinate(float(droneData['Offset Corner Latitude Point 2']), float(
    #         droneData['Offset Corner Longitude Point 2']))
    #     corner3 = QtPositioning.QGeoCoordinate(float(droneData['Offset Corner Latitude Point 3']), float(
    #         droneData['Offset Corner Longitude Point 3']))
    #     corner4 = QtPositioning.QGeoCoordinate(float(droneData['Offset Corner Latitude Point 4']), float(
    #         droneData['Offset Corner Longitude Point 4']))
    #     center = QtPositioning.QGeoCoordinate(float(
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
