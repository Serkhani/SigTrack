from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex

class FlightModel(QAbstractListModel):
    FlightRole = Qt.UserRole + 1
    LatitudeRole = Qt.UserRole + 2
    LongitudeRole = Qt.UserRole + 3
    AltitudeRole = Qt.UserRole + 4
    OperatorRole = Qt.UserRole + 5
    TrackRole = Qt.UserRole + 6
    # URLRole = Qt.UserRole + 7

    def __init__(self, flights=None):
        super(FlightModel, self).__init__(flights)
        self._flights = flights or []

    def rowCount(self, parent=QModelIndex()):
        return len(self._flights)

    def data(self, index, role=Qt.DecorationRole):
        if 0 <= index.row() < self.rowCount():
            flight = self._flights[index.row()]
            if role == self.FlightRole:
                return flight.get("flight", "Unknown").strip()
            elif role == self.LatitudeRole:
                return flight.get("lat", 0.0)
            elif role == self.LongitudeRole:
                return flight.get("lon", 0.0)
            elif role == self.AltitudeRole:
                return flight.get("alt_baro", 0)
            elif role == self.OperatorRole:
                return flight.get("ownOp", "Unknown")
            elif role == self.TrackRole:
                return flight.get("track", 0.0)
            # elif role == self.URLRole:
            #     return flight.get("url", 0.0)
        return ""

    def roleNames(self):
        return {
            self.FlightRole: b"flight",
            self.LatitudeRole: b"lat",
            self.LongitudeRole: b"lon",
            self.AltitudeRole: b"alt",
            self.OperatorRole: b"ownOp",
            self.TrackRole: b"track",
            # self.URLRole: b"url",
        }

    def updateFlights(self, flights):
        self.beginResetModel()
        self._flights = flights
        self.endResetModel()
        # pass
