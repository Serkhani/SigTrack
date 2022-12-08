# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import QDockWidget
from PySide2.QtCore import Qt

class DockWidget(QDockWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.setFocusPolicy(Qt.StrongFocus)

    def closeEvent(self, event):
        self.mainWindow.dockCount -= 1
#        self.mainWindow.imageViewer.editingPanel.hide()
        self.mainWindow.editingPanel.hide()
        if self.mainWindow.dockCount == 0:
            self.mainWindow.ui.label.show()

        QDockWidget.closeEvent(self, event)

