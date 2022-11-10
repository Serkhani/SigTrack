# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QGraphicsScene, QGraphicsView

class ImageViewDockWidget(QGraphicsView):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.scene = QGraphicsScene()
        self.setScene(self.scene)


    def uploadImage(self):
#        self.scene.
        pass
