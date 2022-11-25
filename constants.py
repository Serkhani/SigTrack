from PySide2.QtWidgets import QMainWindow, QDockWidget

from PySide2.QtCore import Qt

_DOCK_OPTS = QMainWindow.AnimatedDocks
_DOCK_OPTS |= QMainWindow.AllowNestedDocks
_DOCK_OPTS |= QMainWindow.AllowTabbedDocks

_DOCK_POSITIONS = (
    Qt.LeftDockWidgetArea,
    Qt.TopDockWidgetArea,
    Qt.RightDockWidgetArea,
    Qt.BottomDockWidgetArea
)

_DOCK_FEATURES = (
    QDockWidget.DockWidgetClosable,
    QDockWidget.DockWidgetMovable,
    QDockWidget.DockWidgetFloatable,
    QDockWidget.DockWidgetVerticalTitleBar
)

PHOTO_EXTENSIONS = {
        "jpeg": True,
        "jpg": True,
        "JPEG": True,
        "JPG": True
        }

DEPENDENCIES = {
        "exif": True,
        "PIL": True
        }

FIELDS = ['fid', 'ID', 'Name', 'Date', 'Time', 'Lon', 'Lat', 'Altitude', 'North', 'Azimuth', 'Cam. Maker', 'Cam. Model', 'Title', 'Comment', 'Path', 'RelPath', 'Timestamp', 'Images']
