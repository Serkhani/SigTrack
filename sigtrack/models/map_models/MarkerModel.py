# from PySide2 import QtCore

from PySide6 import QtCore


class MarkerModel(QtCore.QAbstractListModel):
    PositionRole, SourceRole, TooltipRole, ImagePathRole = range(
        QtCore.Qt.UserRole, QtCore.Qt.UserRole + 4)

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
        self.beginInsertRows(QtCore.QModelIndex(),
                             self.rowCount(), self.rowCount())
        self._markers.append(marker)
        self.endInsertRows()
