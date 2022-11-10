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
