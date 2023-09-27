from PySide2.QtCore import (Qt, QAbstractListModel, QModelIndex)
from PySide2.QtGui import QColor
from datetime import datetime

class MarkerListModel(QAbstractListModel):
    def __init__(self):
        super().__init__()
        self.markers = []

    def rowCount(self, parent=QModelIndex()):
        return len(self.markers)

    def data(self, index, role):
        if not index.isValid() or not (0 <= index.row() < len(self.markers)):
            return None

        marker = self.markers[index.row()]

        if role == Qt.DisplayRole:
            return marker['text']
        elif role == Qt.DecorationRole:
            return marker['color']

    def removeRow(self, row, parent=QModelIndex()):
        if 0 <= row < len(self.markers):
            self.beginRemoveRows(parent, row, row)
            del self.markers[row]
            self.endRemoveRows()

    def addMarker(self):
        # color = Qt.black
        colorName = QColor().colorNames()[len(self.markers)]
        print(colorName)
        color = QColor(colorName)
        # text= f"lat: {1.1}\nlong: {2.2}"
        text = datetime.now().time()
        self.beginInsertRows(QModelIndex(), len(self.markers), len(self.markers))
        self.markers.append({'color': color, 'text': text})
        self.endInsertRows()
