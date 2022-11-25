# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import QDockWidget


class DockWidget(QDockWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow

    def closeEvent(self, event):
        self.mainWindow.dockCount -= 1
        if self.mainWindow.dockCount == 0:
            self.mainWindow.ui.label.show()
