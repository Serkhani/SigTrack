from PySide2 import QtCore 
from PySide2.QtPositioning import QGeoCoordinate

class DroneModel(QtCore.QAbstractListModel):
    IconRole, PositionRole, PathRole, HeadingRole = range(
        QtCore.Qt.UserRole, QtCore.Qt.UserRole + 4)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._drone_position = QGeoCoordinate()
        self._drone_path = []
        self._heading = 0

    def rowCount(self, parent=QtCore.QModelIndex()):
        return 1

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if 0 <= index.row() < self.rowCount():
            if role == DroneModel.PositionRole:
                return self._drone_position
            elif role == DroneModel.IconRole or role == QtCore.Qt.DecorationRole:
                return QtCore.QUrl('qrc://:/drone')
            elif role == DroneModel.PathRole:
                return self._drone_path
            elif role == DroneModel.HeadingRole:
                return self._heading
        return QtCore.QVariant()

    def roleNames(self):
        return {
            DroneModel.IconRole: b"droneIcon",
            DroneModel.PositionRole: b"dronePosition",
            DroneModel.PathRole: b"dronePath",
            DroneModel.HeadingRole: b"heading",
        }

    def updateData(self, drone_position: QGeoCoordinate, heading):
        """
        Updates the drone position as well as the path
        """
        self._drone_position = drone_position
        self._drone_path.append(drone_position)
        self._heading = heading
        self.dataChanged.emit(self.index(0), self.index(self.rowCount(
        ) - 1), [DroneModel.IconRole, DroneModel.PositionRole, DroneModel.PathRole, DroneModel.HeadingRole])

