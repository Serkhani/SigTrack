# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsLineItem, QGraphicsPathItem, QGraphicsEllipseItem, QGraphicsRectItem, QUndoStack)
from PySide2.QtCore import (Qt, Signal, QLineF, QRectF, QPoint, QCoreApplication)
from PySide2.QtGui import (QPainterPath, QPainterPathStroker, QPixmap, QImage)


from DockWidgets.imageview.undo_redo_command import AddCommand#, DeleteCommand, MoveCommand
from DockWidgets.imageview.painter import Painter
from DockWidgets.imageview.textItem import TextItem
from Editing.EditingPanel import EditingPanel

class ImageViewDockWidget(QGraphicsView):
    afterLeftClick = Signal(float, float)
    afterLeftClickReleased = Signal(float, float)
    afterDoubleClick = Signal(float, float)
    keyPressed = Signal(int)

    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.setWindowTitle('ImageView')
        self.scene = QGraphicsScene()

        self.undoStack = QUndoStack()
        self.painter = Painter()
        self.pixmap = QPixmap()

#        setting up editing panel
        self.editingPanelWidget = EditingPanel(self)
#        self.editingPanel = EditingPanelDockWidget(self.editingPanelWidget)
        self.mainWindow.editingPanel.setWidget(self.editingPanelWidget)
        self.setScene(self.scene)
        self.imgPath = None

        self.panSelect = False
        self.zoomSelect = False
        self.drawRect = False
        self.drawCircle = False
        self.drawPolygon = False
        self.drawFreeHand = False
        self.addText = False
        self.drawLine = False
        self.rotate_value = 0
        self.zoom_data = []
        self.scene = QGraphicsScene()

        self.setScene(self.scene)
        self.setMouseTracking(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.NoDrag)
        #self.rect = self.scene.sceneRect()
        self.preview = None
        self.path = None
#        for drawing shapes
        self.begin, self.end = QPoint(), QPoint()

    def mousePressEvent(self, event):
        sc_pos = self.mapToScene(event.pos())
        if event.button() & Qt.LeftButton:
            self.begin = sc_pos
            if self.drawFreeHand:
                self.path = QPainterPath()
                self.path.moveTo(sc_pos)
                stroker = QPainterPathStroker()
                self.preview = QGraphicsPathItem(stroker.createStroke(self.path))
                self.preview.setPen(self.painter.pen)
                self.preview.setBrush(self.painter.brush)
                self.scene.addItem(self.preview)
            elif self.drawLine:
                self.preview = QGraphicsLineItem(QLineF(self.begin.x(),self.begin.y(),self.begin.x(),self.begin.y()))
                self.preview.setPen(self.painter.pen)
                self.scene.addItem(self.preview)
            elif self.drawRect:
                self.preview = QGraphicsRectItem(QRectF(self.begin, self.begin))
                self.preview.setBrush(self.painter.brush)
                self.preview.setPen(self.painter.pen)
                self.scene.addItem(self.preview)
            elif self.drawCircle:
                self.preview = QGraphicsEllipseItem(QRectF(self.begin, self.begin))
                self.preview.setBrush(self.painter.brush)
                self.preview.setPen(self.painter.pen)
                self.scene.addItem(self.preview)
        if self.panSelect:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
        if self.zoomSelect:
            self.setDragMode(QGraphicsView.RubberBandDrag)

        self.afterLeftClick.emit(sc_pos.x(), sc_pos.y())
        #self.rect = self.scene.sceneRect()
        QGraphicsView.mousePressEvent(self, event)

    def mouseDoubleClickEvent(self, event):
        sc_pos = self.mapToScene(event.pos())
        if self.zoomSelect or self.panSelect:
            self.zoom_data = []
            self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)
            #self.rect = self.sceneRect()
        self.afterDoubleClick.emit(sc_pos.x(), sc_pos.y())
        QGraphicsView.mouseDoubleClickEvent(self, event)

    def mouseMoveEvent(self, event):
        sc_pos = self.mapToScene(event.pos())
        if self.preview:
            if self.drawFreeHand and (self.preview.type()== QGraphicsPathItem().type()):
                self.scene.removeItem(self.preview)
                # Add a line to the path from the previous point to the current position
                self.path.lineTo(sc_pos)
                stroker = QPainterPathStroker()
                # Create a line item from the path and add it to the scene
                self.preview.setPath(stroker.createStroke(self.path))
                self.scene.addItem(self.preview)

            elif self.drawLine and (self.preview.type()== QGraphicsLineItem().type()):
                self.scene.removeItem(self.preview)
                self.end = sc_pos
                line = QLineF(self.begin.x(),self.begin.y(),self.end.x(),self.end.y())
                self.preview.setLine(line)
                self.scene.addItem(self.preview)

            elif (self.drawCircle or self.drawRect) and (self.preview.type()==QGraphicsEllipseItem().type() or self.preview.type()==QGraphicsRectItem().type()):
                self.scene.removeItem(self.preview)
                self.end = sc_pos
                rectf = QRectF(self.begin, self.end)
                self.preview.setRect(rectf)
                self.scene.addItem(self.preview)
        QGraphicsView.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        sc_pos = self.mapToScene(event.pos())
        self.end = sc_pos
        if self.preview:
            if (self.drawRect or self.drawCircle or self.drawLine or self.drawFreeHand) and self.preview.type()!=TextItem.itemType:
                self.scene.removeItem(self.preview)
                if self.drawLine and (self.preview.type()== QGraphicsLineItem().type()):
                    self.preview.setLine(QLineF(self.begin.x(), self.begin.y(), self.end.x(), self.end.y()))
                elif self.drawFreeHand and (self.preview.type()== QGraphicsPathItem().type()):
                    self.path.lineTo(self.end)
                    stroker = QPainterPathStroker()
                    self.preview.setPath(stroker.createStroke(self.path))
                else: self.preview.setRect(QRectF(self.begin, self.end))
                addCommand = AddCommand(self.preview, self.scene)
                self.undoStack.push(addCommand)
                self.begin, self.end = QPoint(), QPoint()
                self.preview = None
        elif self.zoomSelect:
            view_bb = self.sceneRect()
            selection_bb = self.scene.selectionArea().boundingRect().intersected(view_bb)
            self.scene.setSelectionArea(QPainterPath())
            if selection_bb.isValid() and (selection_bb != view_bb):
                self.zoom_data = selection_bb
                self.fitInView(self.zoom_data, Qt.KeepAspectRatio)
                #self.rect = self.zoom_data
#        else:
            #self.rect = self.scene.sceneRect()

        self.setDragMode(QGraphicsView.NoDrag)
        self.afterLeftClickReleased.emit(sc_pos.x(), sc_pos.y())
        QGraphicsView.mouseReleaseEvent(self, event)

    def resizeEvent(self, event):
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        #self.rect = self.scene.sceneRect()

    def wheelEvent(self, event):
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        if event.angleDelta().y() < 0:
            sceneRect = self.mapToScene(self.viewport().contentsRect()).boundingRect()
            if sceneRect.width()<=1200 or sceneRect.height() <= 720:
                self.scale(0.9,0.9)
        else:
            sceneRect = self.mapToScene(self.viewport().contentsRect()).boundingRect()
            if sceneRect.width()>=30 or sceneRect.height() >= 30:
                self.scale(1.1,1.1)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if self.mainWindow.isFullScreen():
                self.mainWindow.showMaximized()
                return

        if event.key() == Qt.Key_F11:
            if self.mainWindow.isFullScreen():
                self.mainWindow.showMaximized()
            else:
                self.mainWindow.showFullScreen()

        if event.key() == Qt.Key_Escape:
            self.mainWindow.close()
        #self.rect = self.scene.sceneRect()
        QGraphicsView.keyPressEvent(self, event)


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ImageViewer', message)


    def focusInEvent(self, event):
        self.mainWindow.imageViewer = self
#        self.editingPanel.show()
        self.mainWindow.editingPanel.setWidget(self.editingPanelWidget)
        self.mainWindow.editingPanel.show()

    def addTextItem(self):
        self.preview = TextItem(self)
        self.scene.addItem(self.preview)
        addCommand = AddCommand(self.preview, self.scene)
        self.undoStack.push(addCommand)

    def showImageOnView(self, imgPath):
        self.imgPath = imgPath
        #this function is called to show the image on the view
        if imgPath:
            if not self.mainWindow.dockCount:
                self.mainWindow.imageAction()
            img = QImage(imgPath)
            self.scene.clear()
            self.pixmap = QPixmap.fromImage(img)
            self.scene.addPixmap(self.pixmap)
            self.setSceneRect(QRectF(self.pixmap.rect()))
            self.resizeEvent([])
            self.showNormal()
