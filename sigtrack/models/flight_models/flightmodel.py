from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex

class FlightModel(QAbstractListModel):
    HexRole = Qt.UserRole + 1
    TypeRole = Qt.UserRole + 2
    FlightRole = Qt.UserRole + 3
    RegistrationRole = Qt.UserRole + 4
    AircraftTypeRole = Qt.UserRole + 5
    DescriptionRole = Qt.UserRole + 6
    OperatorRole = Qt.UserRole + 7
    YearRole = Qt.UserRole + 8
    AltBaroRole = Qt.UserRole + 9
    AltGeomRole = Qt.UserRole + 10
    GroundSpeedRole = Qt.UserRole + 11
    TrackRole = Qt.UserRole + 12
    BaroRateRole = Qt.UserRole + 13
    GeomRateRole = Qt.UserRole + 14
    SquawkRole = Qt.UserRole + 15
    EmergencyRole = Qt.UserRole + 16
    CategoryRole = Qt.UserRole + 17
    NavQNHRole = Qt.UserRole + 18
    NavAltitudeMCPRole = Qt.UserRole + 19
    NavHeadingRole = Qt.UserRole + 20
    LatitudeRole = Qt.UserRole + 21
    LongitudeRole = Qt.UserRole + 22
    NicRole = Qt.UserRole + 23
    RcRole = Qt.UserRole + 24
    SeenPosRole = Qt.UserRole + 25
    MessagesRole = Qt.UserRole + 26
    SeenRole = Qt.UserRole + 27
    RssiRole = Qt.UserRole + 28
    DistanceRole = Qt.UserRole + 29
    DirectionRole = Qt.UserRole + 30
    RowCountRole = Qt.UserRole + 31


    def __init__(self, flights=None):
        super(FlightModel, self).__init__()
        self._flights = flights or []

    def rowCount(self, parent=QModelIndex()):
        return len(self._flights)

    def data(self, index, role=Qt.DisplayRole):
        if 0 <= index.row() < self.rowCount():
            flight = self._flights[index.row()]
            if role == self.HexRole:
                return flight.get("hex", "Unknown")
            elif role == self.TypeRole:
                return flight.get("type", "Unknown")
            elif role == self.FlightRole:
                return flight.get("flight", "Unknown").strip()
            elif role == self.RegistrationRole:
                return flight.get("registration", "Unknown")
            elif role == self.AircraftTypeRole:
                return flight.get("aircraft_type", "Unknown")
            elif role == self.DescriptionRole:
                return flight.get("description", "Unknown")
            elif role == self.OperatorRole:
                return flight.get("operator", "Unknown")
            elif role == self.YearRole:
                return flight.get("year", "Unknown")
            elif role == self.AltBaroRole:
                return flight.get("alt_baro", 0.0)
            elif role == self.AltGeomRole:
                return flight.get("alt_geom", 0.0)
            elif role == self.GroundSpeedRole:
                return flight.get("ground_speed", 0.0)
            elif role == self.TrackRole:
                return flight.get("track", 0.0)
            elif role == self.BaroRateRole:
                return flight.get("baro_rate", 0.0)
            elif role == self.GeomRateRole:
                return flight.get("geom_rate", 0.0)
            elif role == self.SquawkRole:
                return flight.get("squawk", "Unknown")
            elif role == self.EmergencyRole:
                return flight.get("emergency", "none")
            elif role == self.CategoryRole:
                return flight.get("category", "Unknown")
            elif role == self.NavQNHRole:
                return flight.get("nav_qnh", 0.0)
            elif role == self.NavAltitudeMCPRole:
                return flight.get("nav_altitude_mcp", 0.0)
            elif role == self.NavHeadingRole:
                return flight.get("nav_heading", 0.0)
            elif role == self.LatitudeRole:
                return flight.get("lat", 0.0)
            elif role == self.LongitudeRole:
                return flight.get("lon", 0.0)
            elif role == self.NicRole:
                return flight.get("nic", 0)
            elif role == self.RcRole:
                return flight.get("rc", 0)
            elif role == self.SeenPosRole:
                return flight.get("seen_pos", 0.0)
            elif role == self.MessagesRole:
                return flight.get("messages", 0)
            elif role == self.SeenRole:
                return flight.get("seen", 0.0)
            elif role == self.RssiRole:
                return flight.get("rssi", 0.0)
            elif role == self.DistanceRole:
                return flight.get("distance", 0.0)
            elif role == self.DirectionRole:
                return flight.get("direction", 0.0)
            elif role == self.RowCountRole:
                return self.rowCount()
        return None

    def roleNames(self):
        return {
            self.HexRole: b"hex",
            self.TypeRole: b"type",
            self.FlightRole: b"flight",
            self.RegistrationRole: b"registration",
            self.AircraftTypeRole: b"aircraft_type",
            self.DescriptionRole: b"description",
            self.OperatorRole: b"operator",
            self.YearRole: b"year",
            self.AltBaroRole: b"alt_baro",
            self.AltGeomRole: b"alt_geom",
            self.GroundSpeedRole: b"ground_speed",
            self.TrackRole: b"track",
            self.BaroRateRole: b"baro_rate",
            self.GeomRateRole: b"geom_rate",
            self.SquawkRole: b"squawk",
            self.EmergencyRole: b"emergency",
            self.CategoryRole: b"category",
            self.NavQNHRole: b"nav_qnh",
            self.NavAltitudeMCPRole: b"nav_altitude_mcp",
            self.NavHeadingRole: b"nav_heading",
            self.LatitudeRole: b"lat",
            self.LongitudeRole: b"lon",
            self.NicRole: b"nic",
            self.RcRole: b"rc",
            self.SeenPosRole: b"seen_pos",
            self.MessagesRole: b"messages",
            self.SeenRole: b"seen",
            self.RssiRole: b"rssi",
            self.DistanceRole: b"distance",
            self.DirectionRole: b"direction",
            self.RowCountRole: b"rowCount",
        }

    def updateFlights(self, flights):
        self.beginResetModel()
        self._flights = flights
        self.endResetModel()
    #     self._flights = flights
    #     # self.dataChanged.emit(self.index(index), self.index(index))
    #     self.dataChanged.emit(self.index(0), self.index(self.rowCount() - 1), [
    #          self.HexRole ,
    # self.TypeRole ,
    # self.FlightRole ,
    # self.RegistrationRole ,
    # self.AircraftTypeRole ,
    # self.DescriptionRole ,
    # self.OperatorRole ,
    # self.YearRole ,
    # self.AltBaroRole ,
    # self.AltGeomRole ,
    # self.GroundSpeedRole ,
    # self.TrackRole ,
    # self.BaroRateRole ,
    # self.GeomRateRole ,
    # self.SquawkRole ,
    # self.EmergencyRole ,
    # self.CategoryRole ,
    # self.NavQNHRole ,
    # self.NavAltitudeMCPRole ,
    # self.NavHeadingRole ,
    # self.LatitudeRole ,
    # self.LongitudeRole ,
    # self.NicRole ,
    # self.RcRole ,
    # self.SeenPosRole ,
    # self.MessagesRole ,
    # self.SeenRole ,
    # self.RssiRole ,
    # self.DistanceRole ,
    # self.DirectionRole ,
    #     ])