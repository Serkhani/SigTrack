import os
from math import cos, tan, log, pi
from PySide2 import QtCore, QtQuickWidgets, QtPositioning
from PySide2.QtCore import QObject, Slot, Signal, QPointF
from PySide2.QtGui import QImage, QPixmap
from exif import Image
import DockWidgets.mapview.rc_map
# class MarkerModel(QtCore.QAbstractListModel):
#     # Define additional roles for the corner circles and circle center markers
#     PositionRole = QtCore.Qt.UserRole + 1
#     SourceRole = QtCore.Qt.UserRole + 2
#     TooltipRole = QtCore.Qt.UserRole + 3
#     CornerCircleRole = QtCore.Qt.UserRole + 4
#     CircleCenterRole = QtCore.Qt.UserRole + 5

#     def __init__(self, parent=None):
#         super(MarkerModel, self).__init__(parent)
#         self._markers = []
#         self._corner_circles = []
#         self._circle_center = None

#     def appendMarker(self, marker):
#         if 'corner_circle' in marker:
#             if marker['corner_circle'] == 'center':
#                 self._circle_center = marker
#             else:
#                 self._corner_circles.append(marker)
#         else:
#             self.beginInsertRows(QtCore.QModelIndex(), len(self._markers), len(self._markers))
#             self._markers.append(marker)
#             self.endInsertRows()

#     def rowCount(self, parent=QtCore.QModelIndex()):
#         return len(self._markers)

#     def data(self, index, role=QtCore.Qt.DisplayRole):
#         if not index.isValid() or index.row() >= len(self._markers):
#             return None
#         marker = self._markers[index.row()]
#         if role == MarkerModel.PositionRole:
#             return marker['position']
#         elif role == MarkerModel.SourceRole:
#             return marker['source']
#         elif role == MarkerModel.TooltipRole:
#             return marker['imgTooltip']
#         elif role == MarkerModel.CornerCircleRole:
#             return marker.get('corner_circle') == 'corner'
#         elif role == MarkerModel.CircleCenterRole:
#             return marker.get('corner_circle') == 'center'

class MarkerModel(QtCore.QAbstractListModel, QObject):
    PositionRole, SourceRole, TooltipRole, ImagePathRole = range(QtCore.Qt.UserRole, QtCore.Qt.UserRole + 4)

    def __init__(self, parent=None):
        super(MarkerModel, self).__init__(parent)
        self._markers = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._markers)

    def data(self, index, role=QtCore.Qt.DisplayRole):
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
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
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
        super(MapWidget, self).__init__(parent,resizeMode=QtQuickWidgets.QQuickWidget.SizeRootObjectToView)
        self.mainWindow = mainWindow
        self.model = MarkerModel(self)
        self.rootContext().setContextProperty("markermodel", self.model)
        self.ice = iceController()
        self.rootContext().setContextProperty('PyConsole', self.ice)
        self.rootContext().setContextProperty('ice', self.ice)
        self.ice.showImageSignal.connect(self.showImage)
        self.setSource(QtCore.QUrl('qrc://:/map'))
        self.mainWindow.map = self
        self.droneMarker = None
        self.circleCenterMarker = None
        self.corner1 = None
        self.corner2 = None
        self.corner3 = None
        self.corner4 = None        
        self.cornerCircleMarkers = []
#        qml_path = os.path.join(os.path.dirname(__file__), "map.qml")
#        self.setSource(QtCore.QUrl.fromLocalFile(qml_path))
    def focusInEvent(self, event):
        self.mainWindow.map = self
        QtQuickWidgets.QQuickWidget.focusInEvent(self, event)

    def showImage(self, imgPath):
#        self.mainWindow.imageViewer.showImageOnView(imgPath)
        self.mainWindow.imageAction(imgPath)

    def addMarker(self, imgPath, imgData: dict):
        # coord = QtPositioning.QGeoCoordinate(imgData['lat'], imgData['long'])
        coord = QtPositioning.QGeoCoordinate(imgData['lat'], imgData['long'])
        source = QtCore.QUrl("http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_gray.png")
        tooltip ="<b>sender: </b> @soldierName<br>"
        exifData = imgData.get('info', Image)
        for property in exifData.get_all():
            print(f'property: {property}')
            try:
                tooltip += f'<b>{property}:</b> {exifData[property]}<br>'
            except: 
                tooltip += f'<b>{property}:</b> Unable to read<br>'

        self.model.appendMarker({"position": coord , "source": source, "imgPath": imgPath, "imgTooltip": tooltip})

    def updateDronePosition(self, droneData: dict):
        if self.droneMarker is not None:
            # update the position of the existing drone marker
            self.droneMarker["position"] = QtPositioning.QGeoCoordinate(float(droneData['Sensor Latitude']), float(droneData['Sensor Longitude']))
            # emit dataChanged signal for the updated marker
            index = self.model.index(0)
            # index = self.model.index(self.model.rowCount() - 1)
            self.model.dataChanged.emit(index, index, [MarkerModel.PositionRole])

            corner1 = QtPositioning.QGeoCoordinate(float(droneData['Offset Corner Latitude Point 1']), float(droneData['Offset Corner Longitude Point 1']))
            corner2 = QtPositioning.QGeoCoordinate(float(droneData['Offset Corner Latitude Point 2']), float(droneData['Offset Corner Longitude Point 2']))
            corner3 = QtPositioning.QGeoCoordinate(float(droneData['Offset Corner Latitude Point 3']), float(droneData['Offset Corner Longitude Point 3']))
            corner4 = QtPositioning.QGeoCoordinate(float(droneData['Offset Corner Latitude Point 4']), float(droneData['Offset Corner Longitude Point 4']))
            # Compute center coordinate of the drone
            center = QtPositioning.QGeoCoordinate(float(droneData['Frame Center Latitude']), float(droneData['Frame Center Longitude']))
            # self.corner1["position"] = corner1
            # # emit dataChanged signal for the updated marker
            # index = self.model.index(1)
            # # index = self.model.index(self.model.rowCount() - 1)
            # self.model.dataChanged.emit(index, index, [MarkerModel.PositionRole])

            # self.corner2["position"] = corner2# emit dataChanged signal for the updated marker
            # index = self.model.index(2)
            # # index = self.model.index(self.model.rowCount() - 1)
            # self.model.dataChanged.emit(index, index, [MarkerModel.PositionRole])

            # self.corner3["position"] = corner3# emit dataChanged signal for the updated marker
            # index = self.model.index(3)
            # # index = self.model.index(self.model.rowCount() - 1)
            # self.model.dataChanged.emit(index, index, [MarkerModel.PositionRole])

            # self.corner4["position"] = corner4 # emit dataChanged signal for the updated marker
            # index = self.model.index(4)
            # # index = self.model.index(self.model.rowCount() - 1)
            # self.model.dataChanged.emit(index, index, [MarkerModel.PositionRole])
   
            self.circleCenterMarker["position"] = center# emit dataChanged signal for the updated marker
            index = self.model.index(1)
            # index = self.model.index(self.model.rowCount() - 1)
            self.model.dataChanged.emit(index, index, [MarkerModel.PositionRole])

        else:
            # add drone marker with initial position
            self.addDrone(droneData)

    # def updateDronePosition(self, droneData: dict):
    #     # update drone position
    #     droneCoord = QtPositioning.QGeoCoordinate(float(droneData['Sensor Latitude']), float(droneData['Sensor Longitude']))
    #     if self.droneMarker:
    #         # update the position of the existing drone marker
    #         self.droneMarker["position"] = droneCoord
    #         # emit dataChanged signal for the updated marker
    #         index = self.model.index(0)
    #         self.model.dataChanged.emit(index, index, [MarkerModel.PositionRole])
    #     else:
    #         # add drone marker with initial position
    #         self.addDrone(droneData)

    #     # update corner circle position
    #     corner1 = QtPositioning.QGeoCoordinate(float(droneData['Offset Corner Latitude Point 1']), float(droneData['Offset Corner Longitude Point 1']))
    #     corner2 = QtPositioning.QGeoCoordinate(float(droneData['Offset Corner Latitude Point 2']), float(droneData['Offset Corner Longitude Point 2']))
    #     corner3 = QtPositioning.QGeoCoordinate(float(droneData['Offset Corner Latitude Point 3']), float(droneData['Offset Corner Longitude Point 3']))
    #     corner4 = QtPositioning.QGeoCoordinate(float(droneData['Offset Corner Latitude Point 4']), float(droneData['Offset Corner Longitude Point 4']))

    #     cornerCircleMarkers = [corner1, corner2, corner3, corner4]
    #     for circleCorner, i in  self.cornerCircleMarkers, range(1,5):
    #         # update the position of the existing corner circle marker
    #         circleCorner["position"] = cornerCircleMarkers[i-1]
    #         # emit dataChanged signal for the updated marker
    #         index = self.model.index(i)
    #         self.model.dataChanged.emit(index, index, [MarkerModel.PositionRole])
    #     # update circle center position
    #     circleCenterCoord = QtPositioning.QGeoCoordinate(float(droneData['Frame Center Latitude']), float(droneData['Frame Center Longitude']))
    #     if self.circleCenterMarker is not None:
    #         # update the position of the existing circle center marker
    #         self.circleCenterMarker["position"] = circleCenterCoord
    #         # emit dataChanged signal for the updated marker
    #         index = self.model.index(self.model.rowCount() - 1)
    #         self.model.dataChanged.emit(index, index, [MarkerModel.PositionRole])
        



    # def addDrone(self, droneData: dict):
    #     coord = QtPositioning.QGeoCoordinate(float(droneData['Sensor Latitude']), float(droneData['Sensor Longitude']))
    #     droneImgPath = 'qrc://:/drone'
    #     cornerCircleImgPath = 'qrc://:/ccircle'
    #     circleCenterImgPath = 'qrc://:/circlec'
    #     tooltip = "data"
    #     droneUrl = QtCore.QUrl(droneImgPath)
    #     cornerCircleUrl = QtCore.QUrl(cornerCircleImgPath)
    #     circleCenterUrl = QtCore.QUrl(circleCenterImgPath)
    #     self.droneMarker = {"position": coord , "source": droneUrl, "imgPath": droneImgPath, "imgTooltip": tooltip}
    #     self.model.appendMarker(self.droneMarker)

    def addDrone(self, droneData: dict):
        # Extract corner coordinates of the drone
        corner1 = QtPositioning.QGeoCoordinate(float(droneData['Offset Corner Latitude Point 1']), float(droneData['Offset Corner Longitude Point 1']))
        corner2 = QtPositioning.QGeoCoordinate(float(droneData['Offset Corner Latitude Point 2']), float(droneData['Offset Corner Longitude Point 2']))
        corner3 = QtPositioning.QGeoCoordinate(float(droneData['Offset Corner Latitude Point 3']), float(droneData['Offset Corner Longitude Point 3']))
        corner4 = QtPositioning.QGeoCoordinate(float(droneData['Offset Corner Latitude Point 4']), float(droneData['Offset Corner Longitude Point 4']))
        # Compute center coordinate of the drone
        center = QtPositioning.QGeoCoordinate(float(droneData['Frame Center Latitude']), float(droneData['Frame Center Longitude']))
        
        droneCoord = QtPositioning.QGeoCoordinate(float(droneData['Sensor Latitude']), float(droneData['Sensor Longitude']))
        droneImgPath = 'qrc://:/drone'
        tooltip = "drone"
        droneUrl = QtCore.QUrl(droneImgPath)

        # Add drone marker
        self.droneMarker = {"position": droneCoord , "source": droneUrl, "imgPath": droneImgPath, "imgTooltip": tooltip}
        self.model.appendMarker(self.droneMarker)

        # Add corner circle marker
        cornerCircleImgPath = 'qrc://:/ccircle'
        cornerCircleUrl = QtCore.QUrl(cornerCircleImgPath)
        # self.corner1 = {"position": corner1, "source": cornerCircleUrl, "imgPath": cornerCircleImgPath, "imgTooltip": "Corner Circle"}
        # self.model.appendMarker(self.corner1)
        # self.corner2 = {"position": corner2, "source": cornerCircleUrl, "imgPath": cornerCircleImgPath, "imgTooltip": "Corner Circle"}
        # self.model.appendMarker(self.corner2)
        # self.corner3 = {"position": corner3, "source": cornerCircleUrl, "imgPath": cornerCircleImgPath, "imgTooltip": "Corner Circle"}
        # self.model.appendMarker(self.corner3)
        # self.corner4 = {"position": corner4, "source": cornerCircleUrl, "imgPath": cornerCircleImgPath, "imgTooltip": "Corner Circle"}
        # self.model.appendMarker(self.corner4)
        # Add circle center marker
        circleCenterImgPath = 'qrc://:/circlec'
        circleCenterUrl = QtCore.QUrl(circleCenterImgPath)
        self.circleCenterMarker = {"position": center, "source": circleCenterUrl, "imgPath": circleCenterImgPath, "imgTooltip": "Circle Center"}
        self.model.appendMarker(self.circleCenterMarker)



    def map_geocoordinate(self, lat_, long_):
        x = (long_ +180) / 360 *self.width()
        y = (1 - log(tan(lat_ * pi/180) + 1 /cos(lat_*pi/180))/pi)/2 *self.height()
        return QPointF(x, y)