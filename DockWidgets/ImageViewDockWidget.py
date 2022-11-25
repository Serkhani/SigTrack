# This Python file uses the following encoding: utf-8

from PySide2.QtWidgets import QGraphicsScene, QGraphicsView
from PySide2.QtCore import Qt
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import QRectF

class ImageViewDockWidget(QGraphicsView):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.setWindowTitle('ImageView')
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

    def resizeEvent(self, event):
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def showImageOnView(self, imgPath):
        #this function is called to show the image on the view
        if imgPath:
            if not self.mainWindow.dockCount:
                self.mainWindow.imageAction()
            img = QImage(imgPath)
            self.scene.clear()
            pixmap = QPixmap.fromImage(img)
            self.scene.addPixmap(pixmap)
            self.setSceneRect(QRectF(pixmap.rect()))
            self.resizeEvent([])
            self.showNormal()
