from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt
from PySide6.QtPositioning import QGeoCoordinate


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
        return 1

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

    def updateData(self, polygon_points: list[QGeoCoordinate], line_points: list[list[QGeoCoordinate, QGeoCoordinate]]):
        self._polygon_points = polygon_points
        self._line_points = line_points
        self.dataChanged.emit(self.index(0), self.index(
            self.rowCount() - 1), [FMVModel.PolygonRole, FMVModel.LineRole])
