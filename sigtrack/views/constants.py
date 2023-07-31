from PySide6.QtWidgets import QMainWindow, QDockWidget

from PySide6.QtCore import Qt

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

LIGHT_THEME_STYLE = """
QMainWindow {
    background-color: #FFF;
}

DockWidget {
    background-color: #F0F0F0; /* Light gray background for dock widgets */
    border: 1px solid #BBB; /* Light gray border */
    font-size: 12px; /* Font size for dock widget content */
}
"""

DARK_THEME_STYLE = """
QMainWindow {
    background-color: #333;
    color: #FFF;
}

DockWidget {
    background-color: #222; /* Dark gray background for dock widgets */
    border: 1px solid #666; /* Dark gray border */
    font-size: 12px; /* Font size for dock widget content */
}
"""

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
FFMPEGPATH = 'C:\\FFMPEG\\bin\\ffmpeg.exe'
FFPROBEPATH = 'C:\\FFMPEG\\bin\\ffprobe.exe'

# Klv variables
UASLocalMetadataSet = b"\x06\x0e+4\x02\x0b\x01\x01\x0e\x01\x03\x01\x01\x00\x00\x00"
KlvHeaderKeyOther = b"\x06\x0e+4\x02\x01\x01\x01\x0e\x01\x01\x02\x01\x01\x00\x00"

#reverse geocoding service that transforms point to address
Reverse_geocoding_url = 'https://nominatim.openstreetmap.org/reverse.php?format=json&lat={}&lon={}'

FIELDS = ['fid', 'ID', 'Name', 'Date', 'Time', 'Lon', 'Lat', 'Altitude', 'North', 'Azimuth', 'Cam. Maker', 'Cam. Model', 'Title', 'Comment', 'Path', 'RelPath', 'Timestamp', 'Images']

VID_EXTs = ["ts", "mpeg4", "mp4", "avi", "mpg", "H264", "mov", "mpeg", "All Videos *.ts *.mpeg4 *.mp4 *.avi *.mpg *.H264 *.mov *.mpeg"]
