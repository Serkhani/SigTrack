import os
import DockWidgets.rc_map

from PySide2 import QtCore, QtQuickWidgets, QtPositioning
from PySide2.QtQml import QJSValue
from PySide2.QtCore import QObject, Slot, Signal

class MarkerModel(QtCore.QAbstractListModel):
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
        qml_path = os.path.join(os.path.dirname(__file__), "map.qml")
        self.setSource(QtCore.QUrl.fromLocalFile(qml_path))

    def showImage(self, imgPath):
        print(imgPath)
        self.mainWindow.imageViewer.showImageOnView(imgPath)
        self.mainWindow.imageAction()

    def addMarker(self, imgPath, imgData):
        print("add marker: ",imgPath)
        coord = QtPositioning.QGeoCoordinate(imgData['lat'], imgData['long'])
        source = QtCore.QUrl("http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_gray.png")
        tooltip ="<b>sender: <\b> ama<br><b>lat: <\b> {lat}<br><b>long: <\b> {long_}<br><b>altitude: <\b> {alt}<br><b>time taken: <\b> {ttHr}:{ttMn}:{ttS}<br><b>date: <\b> {date}<br><b>file: <\b> {file}<br>".format(lat=imgData['lat'], long_=imgData['long'], alt=imgData['altitude'], ttHr=int(imgData['timestamp'][0]), ttMn=int(imgData['timestamp'][1]), ttS=int(imgData['timestamp'][2]),date=imgData['datestamp'], file=imgPath.split('/')[-1])
        self.model.appendMarker({"position": coord , "source": source, "imgPath": imgPath, "imgTooltip": tooltip})


