# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import (QDockWidget, QGraphicsView, QGraphicsScene, QVBoxLayout, QHBoxLayout, QWidget, QGraphicsTextItem, QGraphicsRectItem, QToolBar, QUndoStack, QSpinBox, QSlider,  QComboBox, QCheckBox, QLineEdit, QLabel, QSizePolicy, QPushButton, QFrame, QMenuBar, QMenu, QAction, QFileDialog, QColorDialog, QMessageBox)
from PySide2.QtCore import (Qt, QRectF, QRect, QSize, QCoreApplication)
from PySide2.QtGui import (QPainterPath, QPainter, QIcon, QPixmap, QImage, QFont, QKeySequence)
import Editing.icon_resources
from Editing.colorComboBox import ColorComboBox
import os.path

class EditingPanelDockWidget(QDockWidget):
    def __init__(self, widget):
        super().__init__()
        self.setWidget(widget)
        self.setWindowTitle("Editing Tools")


class EditingPanel(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.viewer = self.mainWindow.imageViewer
        self.editingToolbar = QToolBar("Edit",self)
        self.editingToolbar.setOrientation(Qt.Vertical)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setSizePolicy(sizePolicy)

        self.undoAction = self.viewer.undoStack.createUndoAction(self, self.tr("Undo"))
        self.undoAction.setIcon(QIcon(":/undo"))
        self.undoAction.setShortcuts(QKeySequence.Undo)
        self.redoAction = self.viewer.undoStack.createRedoAction(self, self.tr("Redo"))
        self.redoAction.setIcon(QIcon(":/redo"))
        self.redoAction.setShortcuts(QKeySequence.Redo)
        self.rectAction = QAction(QIcon(":/rect"),"rectangle")
        self.rectAction.triggered.connect(self.drawRect)
        self.circleAction = QAction(QIcon(":/circle"),"circle")
        self.circleAction.triggered.connect(self.drawCircle)
        self.freeHandAction = QAction(QIcon(":freeHand"),"freeHand")
        self.freeHandAction.triggered.connect(self.drawFreeHand)
        self.lineAction = QAction(QIcon(":/line"),"line")
        self.lineAction.triggered.connect(self.drawLine)
        self.polygonAction = QAction(QIcon(":/polygon"),"polygon")
        self.polygonAction.triggered.connect(self.drawPolygon)

        self.editingToolbar.addAction(self.undoAction)
        self.editingToolbar.addAction(self.redoAction)
        self.editingToolbar.addAction(self.rectAction)
        self.editingToolbar.addAction(self.circleAction)



        self.extent = QPushButton(self)
        self.extent.setIcon(QIcon(':extent'))
        self.extent.clicked.connect(self.extentbutton)

        self.zoom_in = QPushButton(self)
        self.zoom_in.setIcon(QIcon(':zoomIn'))
        self.zoom_in.clicked.connect(self.zoom_in_button)

        self.zoom_out = QPushButton(self)
        self.zoom_out.setIcon(QIcon(':zoomOut'))
        self.zoom_out.clicked.connect(self.zoom_out_button)

        self.zoom = QPushButton(self)
        self.zoom.setIcon(QIcon(':zoom_selected'))
        self.zoom.clicked.connect(self.zoombutton)

        self.pan = QPushButton(self)
        self.pan.setIcon(QIcon(':pan'))
        self.pan.clicked.connect(self.panbutton)

        self.strokeColorPicker = QPushButton(self)
        self.strokeColorPicker.setText('...')
        self.strokeColorPicker.clicked.connect(self.strokeColorPickerbutton)

        self.fillColorPicker = QPushButton(self)
        self.fillColorPicker.setText('...')
        self.fillColorPicker.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum))
        self.fillColorPicker.clicked.connect(self.fillColorPickerbutton)



        # # Add tips on buttons
        self.extent.setToolTip(self.tr('Extent photo'))
        self.zoom_out.setToolTip(self.tr('zoom out photo'))
        self.zoom_in.setToolTip(self.tr('zoom in photo'))
        self.zoom.setToolTip(self.tr('Select area to zoom'))
        self.pan.setToolTip(self.tr('Pan zoomed image'))
        self.fillColorPicker.setToolTip(self.tr('Custom Color'))
        self.strokeColorPicker.setToolTip(self.tr('Custom Color'))

        # Arrange layout
        VBlayout = QVBoxLayout(self)

        # Adding tools, view and properties row
        HBToolViewPropsLayout = QHBoxLayout()
        # tools
        VBToolsLayout = QVBoxLayout()
        VBToolsLayout.setAlignment(Qt.AlignTop)
        VBToolsLayout.addWidget(self.extent)
        VBToolsLayout.addWidget(self.zoom)
        VBToolsLayout.addWidget(self.zoom_in)
        VBToolsLayout.addWidget(self.zoom_out)
        VBToolsLayout.addWidget(self.pan)
        VBToolsLayout.addWidget(self.editingToolbar)
        HBToolViewPropsLayout.addLayout(VBToolsLayout)
        # view
#        HBToolViewPropsLayout.addWidget(self.viewer)
        # properties
        VBToolPropertiesWidget = QWidget()
        VBToolPropertiesLayout = QVBoxLayout()
        VBToolPropertiesWidget.setLayout(VBToolPropertiesLayout)
        VBToolPropertiesLayout.setAlignment(Qt.AlignTop)
        PropertiesLabel = QLabel(self)
        PropertiesLabel.setText(self.tr('Properties'))
        PropertiesLabel.setAlignment(Qt.AlignCenter)
        VBToolPropertiesLayout.addWidget(PropertiesLabel)
        # Stroke
        self.strokeCheckBox = QCheckBox("Stroke", self)
        self.strokeCheckBox.stateChanged.connect(self.strokeCheckBoxClicked)
        VBToolPropertiesLayout.addWidget(self.strokeCheckBox)
        # Width
        StrokeWidthLayout = QHBoxLayout()
        self.strokeWidthLabel = QLabel(self)
        self.strokeWidthLabel.setText(self.tr('Width'))
        StrokeWidthLayout.addWidget(self.strokeWidthLabel)
        self.strokeWidthSpinBox = QSpinBox()
        self.strokeWidthSpinBox.setRange(1,10)
        self.strokeWidthSpinBox.setSingleStep(1)
        self.strokeWidthSpinBox.valueChanged.connect(self.strokeWidthSpinBoxValueChanged)
        StrokeWidthLayout.addWidget(self.strokeWidthSpinBox)
        VBToolPropertiesLayout.addLayout(StrokeWidthLayout)
        # Color
        StrokeColorLayout = QHBoxLayout()
        self.strokeColorLabel = QLabel(self)
        self.strokeColorLabel.setText(self.tr('Color'))
        StrokeColorLayout.addWidget(self.strokeColorLabel)
        self.strokeColorComboBox = ColorComboBox()
        self.strokeColorComboBox.currentIndexChanged.connect(self.strokeColorComboBoxValueChanged)
        StrokeColorLayout.addWidget(self.strokeColorComboBox)
        StrokeColorLayout.addWidget(self.strokeColorPicker)
        VBToolPropertiesLayout.addLayout(StrokeColorLayout)
        # Style
        StrokeStyleLayout = QHBoxLayout()
        self.strokeStyleLabel = QLabel(self)
        self.strokeStyleLabel.setText(self.tr('Style'))
        StrokeStyleLayout.addWidget(self.strokeStyleLabel)
        self.strokeStyleComboBox = QComboBox()
        self.strokeStyleComboBox.currentIndexChanged.connect(self.strokeStyleComboBoxValueChanged)
        StrokeStyleLayout.addWidget(self.strokeStyleComboBox)
        VBToolPropertiesLayout.addLayout(StrokeStyleLayout)

        # Fill
        self.fillCheckBox = QCheckBox("Fill", self)
        self.fillCheckBox.stateChanged.connect(self.fillCheckBoxClicked)
        VBToolPropertiesLayout.addWidget(self.fillCheckBox)

        # Opacity slider
        OpacityLayout = QHBoxLayout(self)
        # label
        self.opacityLabel = QLabel(self)
        self.opacityLabel.setText(self.tr('Opacity'))
        OpacityLayout.addWidget(self.opacityLabel)
        # Slider
        self.opacitySlider = QSlider(Qt.Horizontal)
        self.opacitySlider.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed))
        self.opacitySlider.setMinimum(0)
        self.opacitySlider.setMaximum(100)
        self.opacitySlider.setValue(100)
        self.opacitySlider.setTickInterval(25)
        self.opacitySlider.valueChanged.connect(self.opacitySliderValueChanged)
        OpacityLayout.addWidget(self.opacitySlider)
        # OpacityValue
        self.OpacityValue = QLabel(self)
        self.OpacityValue.setText(self.tr(str(self.opacitySlider.value())))
        OpacityLayout.addWidget(self.OpacityValue)
        VBToolPropertiesLayout.addLayout(OpacityLayout)

        # Color
        FillColorLayout = QHBoxLayout()
        self.fillColorLabel = QLabel(self)
        self.fillColorLabel.setText(self.tr('Color'))
        FillColorLayout.addWidget(self.fillColorLabel)
        self.fillColorComboBox = ColorComboBox()
        self.fillColorComboBox.currentIndexChanged.connect(self.fillColorComboBoxValueChanged)
        FillColorLayout.addWidget(self.fillColorComboBox)
        FillColorLayout.addWidget(self.fillColorPicker)
        VBToolPropertiesLayout.addLayout(FillColorLayout)

        # Style
        FillStyleLayout = QHBoxLayout()
        self.fillStyleLabel = QLabel(self)
        self.fillStyleLabel.setText(self.tr('Style'))
        FillStyleLayout.addWidget(self.fillStyleLabel)
        self.fillStyleComboBox = QComboBox()
        self.fillStyleComboBox.currentIndexChanged.connect(self.fillStyleComboBoxValueChanged)
        FillStyleLayout.addWidget(self.fillStyleComboBox)
        VBToolPropertiesLayout.addLayout(FillStyleLayout)

        self.fillCheckBoxClicked()
        self.strokeCheckBoxClicked()

        HBToolViewPropsLayout.addWidget(VBToolPropertiesWidget)
        VBlayout.addLayout(HBToolViewPropsLayout)

        self.setLayout(VBlayout)

    def strokeColorPickerbutton(self):
        # color picker
        pass

    def strokeWidthSpinBoxValueChanged(self):
        self.viewer.painter.setStrokeWidth(self.strokeWidthSpinBox.value())


    def strokeColorComboBoxValueChanged(self):
        # set pen color
        self.viewer.painter.setStrokeColor(self.strokeColorComboBox.currentData())

    def strokeStyleComboBoxValueChanged(self):
        # set pen style
        self.viewer.painter.setStrokeStyle(self.strokeStyleComboBox.currentData())

    def strokeCheckBoxClicked(self):
        isChecked = self.strokeCheckBox.isChecked()
        self.strokeWidthLabel.setVisible(isChecked)
        self.strokeWidthSpinBox.setVisible(isChecked)
        self.strokeColorPicker.setVisible(isChecked)
        self.strokeStyleLabel.setVisible(isChecked)
        self.strokeStyleComboBox.setVisible(isChecked)
        self.strokeColorLabel.setVisible(isChecked)
        self.strokeColorComboBox.setVisible(isChecked)

    def fillColorPickerbutton(self):
        # color picker
        pass

    def fillStyleComboBoxValueChanged(self):
        # set brush style
        self.viewer.painter.setFillStyle(self.fillStyleComboBox.currentData())

    def fillColorComboBoxValueChanged(self):
        # set brush color
        color = self.fillColorComboBox.currentData()
        color.setAlpha(self.opacitySlider.value())
        self.viewer.painter.setFillColor(color)

    def fillCheckBoxClicked(self):
        isChecked = self.fillCheckBox.isChecked()
        self.opacityLabel.setVisible(isChecked)
        self.opacitySlider.setVisible(isChecked)
        self.OpacityValue.setVisible(isChecked)
        self.fillStyleLabel.setVisible(isChecked)
        self.fillColorPicker.setVisible(isChecked)
        self.fillStyleComboBox.setVisible(isChecked)
        self.fillColorLabel.setVisible(isChecked)
        self.fillColorComboBox.setVisible(isChecked)

    def opacitySliderValueChanged(self):
        color = self.fillColorComboBox.currentData()
        value = self.opacitySlider.value()
        color.setAlpha(value)
        self.viewer.painter.setFillColor(color)
        self.OpacityValue.setText(str(value))

    def showMessage(self, title, msg, button, icon):
        msgBox = QMessageBox()
        if icon=='Warning':
            msgBox.setIcon(QMessageBox.Warning)
        if icon=='Info':
            msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.Ok)
        font = QFont()
        font.setPointSize(9)
        msgBox.setFont(font)
        msgBox.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        buttonY = msgBox.button(QMessageBox.Ok)
        buttonY.setText(button)
        buttonY.setFont(font)
        msgBox.exec_()

    def updateWindow(self):
        self.viewer.scene.clear()
        self.drawSelf.getImage = QImage(self.viewer.imgPath)

        pixmap = QPixmap.fromImage(self.drawSelf.getImage)
        self.viewer.scene.addPixmap(pixmap)
        self.viewer.setSceneRect(QRectF(pixmap.rect()))
        self.drawSelf.layerActive.selectByIds([self.drawSelf.featureIndex])
        self.viewer.resizeEvent([])
        self.extentbutton()

    def zoom_to_selectbutton(self):
        self.drawSelf.iface.actionZoomToSelected().trigger()

    def zoombutton(self):
        self.viewer.panSelect = False
        self.viewer.drawRect = False
        self.viewer.zoomSelect = True
        self.viewer.drawCircle = False
        self.drawPolygon = False
        self.drawFreeHand = False
        self.drawLine = False
        self.viewer.setCursor(Qt.CrossCursor)
        self.viewer.setDragMode(QGraphicsView.RubberBandDrag)

    def drawCircle(self):
        self.viewer.panSelect = False
        self.viewer.drawRect = False
        self.viewer.zoomSelect = False
        self.viewer.drawCircle = True
        self.drawPolygon = False
        self.drawFreeHand = False
        self.drawLine = False
        self.viewer.setCursor(Qt.CrossCursor)
        self.viewer.setDragMode(QGraphicsView.RubberBandDrag)

    def drawLine(self):
        self.viewer.panSelect = False
        self.viewer.drawRect = False
        self.viewer.zoomSelect = True
        self.viewer.drawCircle = False
        self.drawPolygon = False
        self.drawFreeHand = False
        self.drawLine = True
        self.viewer.setCursor(Qt.CrossCursor)
        self.viewer.setDragMode(QGraphicsView.NoDrag)


    def drawFreeHand(self):
        self.viewer.panSelect = False
        self.viewer.drawRect = False
        self.viewer.zoomSelect = True
        self.viewer.drawCircle = False
        self.drawPolygon = False
        self.drawFreeHand = True
        self.drawLine = False
        self.viewer.setCursor(Qt.CrossCursor)
        self.viewer.setDragMode(QGraphicsView.NoDrag)



    def drawPolygon(self):
        self.viewer.panSelect = False
        self.viewer.drawRect = False
        self.viewer.zoomSelect = True
        self.viewer.drawCircle = False
        self.drawPolygon = True
        self.drawFreeHand = False
        self.drawLine = False
        self.viewer.setCursor(Qt.CrossCursor)
        self.viewer.setDragMode(QGraphicsView.NoDrag)



    def drawRect(self):
        self.viewer.panSelect = False
        self.viewer.drawCircle = False
        self.viewer.zoomSelect = False
        self.viewer.drawRect = True
        self.drawPolygon = False
        self.drawFreeHand = False
        self.drawLine = False
        self.viewer.setCursor(Qt.CrossCursor)
        self.viewer.setDragMode(QGraphicsView.RubberBandDrag)

    def zoom_out_button(self):
        self.viewer.panSelect = False
        self.viewer.drawRect = False
        self.viewer.zoomSelect = False
        self.viewer.drawCircle = False
        self.drawPolygon = False
        self.drawFreeHand = False
        self.drawLine = False
        self.viewer.setCursor(Qt.ArrowCursor)
        sceneRect = self.viewer.mapToScene(self.viewer.viewport().contentsRect()).boundingRect()
        if sceneRect.width()>=1200 or sceneRect.height() >= 720:
            return
        else:
            self.viewer.scale(0.9,0.9)
        # x, y, w, h = self.viewer.rect.getRect()
        # if w>=1200 or h >=720:
        #     self.extentbutton()
        #     return
        # rect = QRectF(x-10,y-10,w+20,h+20)
        # self.viewer.fitInView(rect, Qt.KeepAspectRatio)
        # self.viewer.rect = rect

    def zoom_in_button(self):
        self.viewer.panSelect = False
        self.viewer.drawRect = False
        self.viewer.zoomSelect = False
        self.viewer.drawCircle = False
        self.drawPolygon = False
        self.drawFreeHand = False
        self.drawLine = False
        self.viewer.setCursor(Qt.ArrowCursor)
        sceneRect = self.viewer.mapToScene(self.viewer.viewport().contentsRect()).boundingRect()
        if sceneRect.width()>=30 or sceneRect.height() >= 30:
            self.viewer.scale(1.1,1.1)
        else: return
        # x, y, w, h = self.viewer.rect.getRect()
        # if (w-20 >= 30) or (h-20 >= 30):
        #     rect = QRectF(x+10,y+10,w-20,h-20)
        #     self.viewer.fitInView(rect, Qt.KeepAspectRatio)
        #     self.viewer.rect = rect
        # else: return

    def extentbutton(self):
        self.viewer.zoom_data = []
        self.viewer.fitInView(self.viewer.sceneRect(), Qt.KeepAspectRatio)
        self.viewer.rect = self.viewer.sceneRect()
        self.viewer.drawRect = False
        self.viewer.panSelect = False
        self.viewer.drawCircle = False
        self.viewer.zoomSelect = False
        self.drawPolygon = False
        self.drawFreeHand = False
        self.drawLine = False
        self.viewer.setCursor(Qt.ArrowCursor)
        self.viewer.setDragMode(QGraphicsView.NoDrag)

    def addText(self, pos, text):
        imgText = self.viewer.scene.addText(text)
        imgText.setPos(pos[0], pos[1])

        # imgText = QGraphicsTextItem()
        # imgText.setPos(pos[0], pos[1])
        # imgText.setPlainText(text);

        # self.scene.addItem(imgText)

    def panbutton(self):
        self.viewer.panSelect = True
        self.viewer.drawRect = False
        self.viewer.zoomSelect = False
        self.drawPolygon = False
        self.drawFreeHand = False
        self.drawLine = False
        self.viewer.setCursor(Qt.OpenHandCursor)
        self.viewer.setDragMode(QGraphicsView.ScrollHandDrag)

    def closeEvent(self, event):
        self.viewer.undoStack.clear()
        QWidget.closeEvent(self, event)

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
        return QCoreApplication.translate('ViewWindow', message)

