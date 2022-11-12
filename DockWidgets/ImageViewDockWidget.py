# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QGraphicsScene, QGraphicsView
from PySide6.QtCore import Qt

class ImageViewDockWidget(QGraphicsView):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.setWindowTitle('ImageView')
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

    def resizeEvent(self, event):
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def uploadImage(self):
#        self.scene.
        pass
