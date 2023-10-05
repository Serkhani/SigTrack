from PySide2.QtCore import (Qt, QAbstractListModel, QModelIndex)
from PySide2.QtGui import QColor
from datetime import datetime

# class MarkerListModel(QAbstractListModel):
#     def __init__(self):
#         super().__init__()
#         self.markers = []

#     def rowCount(self, parent=QModelIndex()):
#         return len(self.markers)

#     def data(self, index, role):
#         if not index.isValid() or not (0 <= index.row() < len(self.markers)):
#             return None

#         marker = self.markers[index.row()]

#         if role == Qt.DisplayRole:
#             return marker['text']
#         elif role == Qt.DecorationRole:
#             return marker['color']
#         elif role == Qt.UserRole:
#             return "Custom Button"

#     def removeRow(self, row, parent=QModelIndex()):
#         if 0 <= row < len(self.markers):
#             self.beginRemoveRows(parent, row, row)
#             del self.markers[row]
#             self.endRemoveRows()

#     def addMarker(self)-> QColor:
#         # color = Qt.black
#         colorName = QColor().colorNames()[9+len(self.markers)]
#         print(colorName)
#         color = QColor(colorName)
#         # text= f"lat: {1.1}\nlong: {2.2}"
#         # text = datetime.now().time()
#         text =f"lat: ''\nlon: ''"
#         self.beginInsertRows(QModelIndex(), len(self.markers), len(self.markers))
#         self.markers.append({'color': color, 'text': text})
#         self.endInsertRows()
#         return color
    
    
# from PyQt5.QtCore import Qt, QModelIndex, QAbstractListModel
# from PyQt5.QtGui import QColor

class MarkerListModel(QAbstractListModel):
    def __init__(self):
        super().__init__()
        self.marker = None  # Initialize with no marker

    def rowCount(self, parent=QModelIndex()):
        return 1 if self.marker else 0

    def data(self, index, role):
        if not index.isValid() or not self.marker:
            return None

        if role == Qt.DisplayRole:
            return self.marker['text']
        elif role == Qt.DecorationRole:
            return self.marker['color']
        elif role == Qt.UserRole:
            return "Custom Button"
    def getMarker(self):
        return self.marker

    def setMarker(self, color: QColor, text: str):
        if self.marker:
            # If a marker already exists, update it
            self.marker['color'] = color
            self.marker['text'] = text
            self.dataChanged.emit(self.index(0, 0), self.index(0, 0))
        else:
            # If no marker exists, create one
            self.beginInsertRows(QModelIndex(), 0, 0)
            self.marker = {'color': color, 'text': text}
            self.endInsertRows()

    def removeMarker(self):
        if self.marker:
            self.beginRemoveRows(QModelIndex(), 0, 0)
            self.marker = None
            self.endRemoveRows()
