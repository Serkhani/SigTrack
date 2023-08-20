# This Python file uses the following encoding: utf-8
from sigtrack.models.image_models.colorComboBox import ColorComboBox
import logging

from PySide2.QtWidgets import (
    QDockWidget,
    QGraphicsView,
    QVBoxLayout,
    QButtonGroup,
    QMessageBox,
    QHBoxLayout,
    QCheckBox,
    QSpinBox,
    QComboBox,
    QWidget,
    QLabel,
    QSlider,
    QToolBar,
    QPushButton,
    QColorDialog,
    QAction,
    QSizePolicy
)

from PySide2.QtCore import (
    Qt,
    QRectF,
    QCoreApplication
)

from PySide2.QtGui import (
    QIcon,
    QPixmap,
    QImage,
    QFont,
    QKeySequence
)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(filename)s [%(levelname)s] %(message)s',
)

# import sigtrack.views.editing.icon_resources


class EditingPanelDockWidget(QDockWidget):
    def __init__(self, widget):
        super().__init__()
        self.setWidget(widget)
        self.setWindowTitle("Editing Tools")


class EditingPanel(QWidget):
    def __init__(self, viewer):
        super().__init__()
        self.viewer = viewer
        self.editingToolbar = QToolBar("Edit", self)
        self.editingToolbar.setOrientation(Qt.Vertical)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setSizePolicy(sizePolicy)

        self.undoAction = self.viewer.undoStack.createUndoAction(
            self, self.tr("Undo"))
        self.undoAction.setIcon(QIcon(":/undo"))
        self.undoAction.setShortcuts(QKeySequence.Undo)
        self.redoAction = self.viewer.undoStack.createRedoAction(
            self, self.tr("Redo"))
        self.redoAction.setIcon(QIcon(":/redo"))
        self.redoAction.setShortcuts(QKeySequence.Redo)
        self.rectAction = QAction(QIcon(":/rect"), "rectangle")
        self.rectAction.triggered.connect(self.drawRect)
        self.circleAction = QAction(QIcon(":/circle"), "circle")
        self.circleAction.triggered.connect(self.drawCircle)
        self.freeHandAction = QAction(QIcon(":freehand"), "freeHand")
        self.freeHandAction.triggered.connect(self.drawFreeHand)
        self.lineAction = QAction(QIcon(":/line"), "line")
        self.lineAction.triggered.connect(self.drawLine)
        self.polygonAction = QAction(QIcon(":/polygon"), "polygon")
        self.polygonAction.triggered.connect(self.drawPolygon)
        self.textAction = QAction(QIcon(":/addText"), "Text")
        self.textAction.triggered.connect(self.addTextbutton)
        self.watermarkAction = QAction(QIcon(":/watermark"), "Watermark")
        self.watermarkAction.triggered.connect(self.watermarkbutton)

        self.editingToolbar.addAction(self.undoAction)
        self.editingToolbar.addAction(self.redoAction)
        self.editingToolbar.addAction(self.rectAction)
        self.editingToolbar.addAction(self.circleAction)
        self.editingToolbar.addAction(self.lineAction)
        self.editingToolbar.addAction(self.freeHandAction)
        self.editingToolbar.addAction(self.textAction)
        self.editingToolbar.addAction(self.watermarkAction)

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
        self.zoom.setIcon(QIcon(':zoomSelected'))
        self.zoom.clicked.connect(self.zoombutton)

        self.pan = QPushButton(self)
        self.pan.setIcon(QIcon(':pan'))
        self.pan.clicked.connect(self.panbutton)

        self.strokeColorPicker = QPushButton(self)
        self.strokeColorPicker.setText('...')
        self.strokeColorPicker.clicked.connect(self.strokeColorPickerbutton)

        self.fillColorPicker = QPushButton(self)
        self.fillColorPicker.setText('...')
        self.fillColorPicker.setSizePolicy(QSizePolicy(
            QSizePolicy.Minimum, QSizePolicy.Minimum))
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
        self.strokeWidthSpinBox.setRange(1, 10)
        self.strokeWidthSpinBox.setSingleStep(1)
        self.strokeWidthSpinBox.valueChanged.connect(
            self.strokeWidthSpinBoxValueChanged)
        StrokeWidthLayout.addWidget(self.strokeWidthSpinBox)
        VBToolPropertiesLayout.addLayout(StrokeWidthLayout)
        # Color
        StrokeColorLayout = QHBoxLayout()
        self.strokeColorLabel = QLabel(self)
        self.strokeColorLabel.setText(self.tr('Color'))
        StrokeColorLayout.addWidget(self.strokeColorLabel)
        self.strokeColorComboBox = ColorComboBox()
        self.strokeColorComboBox.currentIndexChanged.connect(
            self.strokeColorComboBoxValueChanged)
        StrokeColorLayout.addWidget(self.strokeColorComboBox)
        StrokeColorLayout.addWidget(self.strokeColorPicker)
        VBToolPropertiesLayout.addLayout(StrokeColorLayout)
        # Style
        StrokeStyleLayout = QHBoxLayout()
        self.strokeStyleLabel = QLabel(self)
        self.strokeStyleLabel.setText(self.tr('Style'))
        StrokeStyleLayout.addWidget(self.strokeStyleLabel)
        self.strokeStyleComboBox = QComboBox()
        self.strokeStyleComboBox.currentIndexChanged.connect(
            self.strokeStyleComboBoxValueChanged)
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
        self.opacitySlider.setSizePolicy(
            QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.opacitySlider.setMinimum(0)
        self.opacitySlider.setMaximum(255)
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
        self.fillColorComboBox.currentIndexChanged.connect(
            self.fillColorComboBoxValueChanged)
        FillColorLayout.addWidget(self.fillColorComboBox)
        FillColorLayout.addWidget(self.fillColorPicker)
        VBToolPropertiesLayout.addLayout(FillColorLayout)

        # Style
        FillStyleLayout = QHBoxLayout()
        self.fillStyleLabel = QLabel(self)
        self.fillStyleLabel.setText(self.tr('Style'))
        FillStyleLayout.addWidget(self.fillStyleLabel)
        self.fillStyleComboBox = QComboBox()
        self.fillStyleComboBox.currentIndexChanged.connect(
            self.fillStyleComboBoxValueChanged)
        FillStyleLayout.addWidget(self.fillStyleComboBox)
        VBToolPropertiesLayout.addLayout(FillStyleLayout)

        self.fillCheckBoxClicked()
        self.strokeCheckBoxClicked()

        HBToolViewPropsLayout.addWidget(VBToolPropertiesWidget)
        VBlayout.addLayout(HBToolViewPropsLayout)

#        self.setLayout(VBlayout)

#        Font
        self.fontLabel = QLabel(self)
        self.fontLabel.setText(self.tr('Font'))
        self.fontLabel.setVisible(False)
        VBToolPropertiesLayout.addWidget(self.fontLabel)

        # Bold
        self.fontBoldCheckBox = QCheckBox("Bold", self)
        self.fontBoldCheckBox.stateChanged.connect(
            self.fontBoldCheckBoxClicked)
        self.fontBoldCheckBox.setVisible(False)
        VBToolPropertiesLayout.addWidget(self.fontBoldCheckBox)

        # PointSize slider
        pointSizeLayout = QHBoxLayout(self)
        # label
        self.pointSizeLabel = QLabel(self)
        self.pointSizeLabel.setText(self.tr('Point Size'))
        self.pointSizeLabel.setVisible(False)
        pointSizeLayout.addWidget(self.pointSizeLabel)
        # Slider
        self.pointSizeSlider = QSlider(Qt.Horizontal)
        self.pointSizeSlider.setSizePolicy(
            QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.pointSizeSlider.setMinimum(0)
        self.pointSizeSlider.setMaximum(100)
        self.pointSizeSlider.setValue(50)
        self.pointSizeSlider.setTickInterval(25)
        self.pointSizeSlider.setVisible(False)
        self.pointSizeSlider.valueChanged.connect(
            self.pointSizeSliderValueChanged)
        pointSizeLayout.addWidget(self.pointSizeSlider)
        # pointSizeValue
        self.pointSizeValue = QLabel(self)
        self.pointSizeValue.setText(self.tr(str(self.pointSizeSlider.value())))
        pointSizeLayout.addWidget(self.pointSizeValue)
        self.pointSizeValue.setVisible(False)
        VBToolPropertiesLayout.addLayout(pointSizeLayout)

#        Alignment
        alignmentLayout = QHBoxLayout(self)
        # label
        self.alignmentLabel = QLabel(self)
        self.alignmentLabel.setText(self.tr('Alignment'))
        self.alignmentLabel.setVisible(False)
        VBToolPropertiesLayout.addWidget(self.alignmentLabel)
        buttonGroup = QButtonGroup()

        self.alignLeft = QPushButton(self)
        self.alignLeft.setIcon(QIcon(':alignLeft'))
        self.alignLeft.clicked.connect(self.alignLeftButton)
        self.alignLeft.setToolTip(self.tr('Align Left'))
        self.alignLeft.setVisible(False)
        buttonGroup.addButton(self.alignLeft)
        alignmentLayout.addWidget(self.alignLeft)

        self.alignRight = QPushButton(self)
        self.alignRight.setIcon(QIcon(':alignRight'))
        self.alignRight.clicked.connect(self.alignRightButton)
        self.alignRight.setToolTip(self.tr('Align Right'))
        self.alignRight.setVisible(False)
        buttonGroup.addButton(self.alignRight)
        alignmentLayout.addWidget(self.alignRight)

        self.alignJustify = QPushButton(self)
        self.alignJustify.setIcon(QIcon(':alignJustify'))
        self.alignJustify.clicked.connect(self.alignJustifyButton)
        self.alignJustify.setToolTip(self.tr('Justify'))
        self.alignJustify.setVisible(False)
        buttonGroup.addButton(self.alignJustify)
        alignmentLayout.addWidget(self.alignJustify)

        self.alignCenter = QPushButton(self)
        self.alignCenter.setIcon(QIcon(':alignCenter'))
        self.alignCenter.clicked.connect(self.alignCenterButton)
        self.alignCenter.setToolTip(self.tr('Align Center'))
        buttonGroup.addButton(self.alignCenter)
        alignmentLayout.addWidget(self.alignCenter)
        self.alignCenter.setVisible(False)
        VBToolPropertiesLayout.addLayout(alignmentLayout)

    def alignLeftButton(self):
        self.viewer.preview.updateGeometry(Qt.AlignLeft)

    def alignRightButton(self):
        self.viewer.preview.updateGeometry(Qt.AlignRight)

    def alignJustifyButton(self):
        self.viewer.preview.updateGeometry(Qt.AlignJustify)

    def alignCenterButton(self):
        self.viewer.preview.updateGeometry(Qt.AlignHCenter)

    def fontBoldCheckBoxClicked(self):
        self.viewer.painter.setFontBold(self.fontBoldCheckBox.isChecked())

    def pointSizeSliderValueChanged(self):
        self.viewer.painter.setFontPointSize(self.pointSizeSlider.value())
        self.pointSizeValue.setText(self.tr(str(self.pointSizeSlider.value())))

    def strokeColorPickerbutton(self):
        # color picker
        self.strokeColorDialog = QColorDialog()
        self.strokeColorDialog.setCurrentColor(self.viewer.painter.pen.color())
        if self.strokeColorDialog.exec_():
            self.viewer.painter.setStrokeColor(
                self.strokeColorDialog.currentColor().name())
            self.strokeColorComboBox.setEditText(self.tr('Custom'))

    def strokeWidthSpinBoxValueChanged(self):
        self.viewer.painter.setStrokeWidth(self.strokeWidthSpinBox.value())

    def strokeColorComboBoxValueChanged(self):
        # set pen color
        self.viewer.painter.setStrokeColor(
            self.strokeColorComboBox.currentData())

    def strokeStyleComboBoxValueChanged(self):
        # set pen style
        self.viewer.painter.setStrokeStyle(
            self.strokeStyleComboBox.currentData())

    def strokeCheckBoxClicked(self):
        isChecked = self.strokeCheckBox.isChecked()
        self.strokeWidthLabel.setVisible(isChecked)
        self.strokeWidthSpinBox.setVisible(isChecked)
        self.strokeColorPicker.setVisible(isChecked)
        self.strokeStyleLabel.setVisible(False)
        self.strokeStyleComboBox.setVisible(False)
        self.strokeColorLabel.setVisible(isChecked)
        self.strokeColorComboBox.setVisible(isChecked)
        if isChecked:
            self.strokeColorComboBoxValueChanged()
            self.strokeWidthSpinBoxValueChanged()
#           self.strokeStyleComboBoxValueChanged()
        else:
            self.viewer.painter.setStrokeDefault()

    def fillColorPickerbutton(self):
        # color picker
        self.fillColorDialog = QColorDialog()
        self.fillColorDialog.setCurrentColor(self.viewer.painter.brush.color())
        if self.fillColorDialog.exec_():
            self.viewer.painter.setFillColor(
                self.fillColorDialog.currentColor().name())
            self.fillColorComboBox.setEditText(self.tr('Custom'))
            self.opacitySliderValueChanged()

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
        self.fillStyleLabel.setVisible(False)
        self.fillColorPicker.setVisible(isChecked)
        self.fillStyleComboBox.setVisible(False)
        self.fillColorLabel.setVisible(isChecked)
        self.fillColorComboBox.setVisible(isChecked)
#        change painting style here: stroke or fill
        if isChecked:
            self.fillColorComboBoxValueChanged()
            self.opacitySliderValueChanged()
            # self.fillStyleComboBoxValueChanged()
        else:
            self.viewer.painter.setFillDefault()

    def opacitySliderValueChanged(self):
        color = self.fillColorComboBox.currentData()
        value = self.opacitySlider.value()
        color.setAlpha(value)
        self.viewer.painter.setFillColor(color)
        self.OpacityValue.setText(str(value))

        if self.viewer.watermark:
            self.viewer.watermark_item.update_watermark_opacity(value)

    def showMessage(self, title, msg, button, icon):
        msgBox = QMessageBox()
        if icon == 'Warning':
            msgBox.setIcon(QMessageBox.Warning)
        if icon == 'Info':
            msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.Ok)
        font = QFont()
        font.setPointSize(9)
        msgBox.setFont(font)
        msgBox.setWindowFlags(Qt.CustomizeWindowHint |
                              Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        buttonY = msgBox.button(QMessageBox.Ok)
        buttonY.setText(button)
        buttonY.setFont(font)
        msgBox.exec_()

    def updateForText(self, condition):
        #        self.alignCenter.setVisible(condition)
        #        self.alignLeft.setVisible(condition)
        #        self.alignRight.setVisible(condition)
        #        self.alignJustify.setVisible(condition)
        self.pointSizeValue.setVisible(condition)
        #self.alignmentLabel.setVisible(condition)
        self.pointSizeSlider.setVisible(condition)
        self.pointSizeLabel.setVisible(condition)
        self.fontBoldCheckBox.setVisible(condition)
        self.fontLabel.setVisible(condition)
        self.fillCheckBox.setCheckState(Qt.Unchecked)

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
        self.viewer.addText = False
        self.viewer.watermark = False
        self.viewer.drawRect = False
        self.viewer.zoomSelect = True
        self.viewer.drawCircle = False
        self.viewer.drawPolygon = False
        self.viewer.drawFreeHand = False
        self.viewer.drawLine = False
        self.viewer.setCursor(Qt.CrossCursor)
        self.viewer.setDragMode(QGraphicsView.RubberBandDrag)
        self.updateForText(self.viewer.addText)

    def drawCircle(self):
        self.viewer.panSelect = False
        self.viewer.addText = False
        self.viewer.watermark = False
        self.viewer.drawRect = False
        self.viewer.zoomSelect = False
        self.viewer.drawCircle = True
        self.viewer.drawPolygon = False
        self.viewer.drawFreeHand = False
        self.viewer.drawLine = False
        self.viewer.setCursor(Qt.CrossCursor)
        self.viewer.setDragMode(QGraphicsView.NoDrag)
        self.updateForText(self.viewer.addText)

    def drawLine(self):
        self.viewer.panSelect = False
        self.viewer.drawRect = False
        self.viewer.watermark = False
        self.viewer.addText = False
        self.viewer.zoomSelect = False
        self.viewer.drawCircle = False
        self.viewer.drawPolygon = False
        self.viewer.drawFreeHand = False
        self.viewer.drawLine = True
        self.viewer.setCursor(Qt.CrossCursor)
        self.viewer.setDragMode(QGraphicsView.NoDrag)
        self.updateForText(self.viewer.addText)

    def drawFreeHand(self):
        self.viewer.panSelect = False
        self.viewer.drawRect = False
        self.viewer.zoomSelect = False
        self.viewer.drawCircle = False
        self.viewer.watermark = False
        self.viewer.addText = False
        self.viewer.drawPolygon = False
        self.viewer.drawFreeHand = True
        self.viewer.drawLine = False
        self.viewer.setCursor(Qt.CrossCursor)
        self.viewer.setDragMode(QGraphicsView.NoDrag)
        self.updateForText(self.viewer.addText)

    def drawPolygon(self):
        self.viewer.panSelect = False
        self.viewer.drawRect = False
        self.viewer.watermark = False
        self.viewer.zoomSelect = False
        self.viewer.addText = False
        self.viewer.drawCircle = False
        self.viewer.drawPolygon = True
        self.viewer.drawFreeHand = False
        self.viewer.drawLine = False
        self.viewer.setCursor(Qt.CrossCursor)
        self.viewer.setDragMode(QGraphicsView.NoDrag)
        self.updateForText(self.viewer.addText)

    def drawRect(self):
        self.viewer.panSelect = False
        self.viewer.watermark = False
        self.viewer.drawCircle = False
        self.viewer.zoomSelect = False
        self.viewer.addText = False
        self.viewer.drawRect = True
        self.viewer.drawPolygon = False
        self.viewer.drawFreeHand = False
        self.viewer.drawLine = False
        self.viewer.setCursor(Qt.CrossCursor)
        self.viewer.setDragMode(QGraphicsView.NoDrag)
        self.updateForText(self.viewer.addText)

    def zoom_out_button(self):
        self.viewer.panSelect = False
        self.viewer.drawRect = False
        self.viewer.watermark = False
        self.viewer.zoomSelect = False
        self.viewer.addText = False
        self.viewer.drawCircle = False
        self.viewer.drawPolygon = False
        self.viewer.drawFreeHand = False
        self.viewer.drawLine = False
        self.viewer.setCursor(Qt.ArrowCursor)
        sceneRect = self.viewer.mapToScene(
            self.viewer.viewport().contentsRect()).boundingRect()
        if sceneRect.width() >= 1200 or sceneRect.height() >= 720:
            return
        else:
            self.viewer.scale(0.9, 0.9)
        # x, y, w, h = self.viewer.rect.getRect()
        # if w>=1200 or h >=720:
        #     self.extentbutton()
        #     return
        # rect = QRectF(x-10,y-10,w+20,h+20)
        # self.viewer.fitInView(rect, Qt.KeepAspectRatio)
        # self.viewer.rect = rect
        self.updateForText(self.viewer.addText)

    def zoom_in_button(self):
        self.viewer.panSelect = False
        self.viewer.drawRect = False
        self.viewer.addText = False
        self.viewer.watermark = False
        self.viewer.zoomSelect = False
        self.viewer.drawCircle = False
        self.viewer.drawPolygon = False
        self.viewer.drawFreeHand = False
        self.viewer.drawLine = False
        self.viewer.setCursor(Qt.ArrowCursor)
        sceneRect = self.viewer.mapToScene(
            self.viewer.viewport().contentsRect()).boundingRect()
        if sceneRect.width() >= 30 or sceneRect.height() >= 30:
            self.viewer.scale(1.1, 1.1)
        else:
            return
        # x, y, w, h = self.viewer.rect.getRect()
        # if (w-20 >= 30) or (h-20 >= 30):
        #     rect = QRectF(x+10,y+10,w-20,h-20)
        #     self.viewer.fitInView(rect, Qt.KeepAspectRatio)
        #     self.viewer.rect = rect
        # else: return
        self.updateForText(self.viewer.addText)

    def extentbutton(self):
        self.viewer.zoom_data = []
        self.viewer.fitInView(self.viewer.sceneRect(), Qt.KeepAspectRatio)
        self.viewer.rect = self.viewer.sceneRect()
        self.viewer.drawRect = False
        self.viewer.watermark = False
        self.viewer.panSelect = False
        self.viewer.drawCircle = False
        self.viewer.addText = False
        self.viewer.zoomSelect = False
        self.viewer.drawPolygon = False
        self.viewer.drawFreeHand = False
        self.viewer.drawLine = False
        self.viewer.setCursor(Qt.ArrowCursor)
        self.viewer.setDragMode(QGraphicsView.NoDrag)
        self.updateForText(self.viewer.addText)

    def addTextbutton(self):
        self.viewer.drawRect = False
        self.viewer.panSelect = False
        self.viewer.watermark = False
        self.viewer.drawCircle = False
        self.viewer.addText = True
        self.viewer.zoomSelect = False
        self.viewer.drawPolygon = False
        self.viewer.drawFreeHand = False
        self.viewer.drawLine = False
        self.viewer.setCursor(Qt.ArrowCursor)
#        self.fillCheckBox.setCheckState(Qt.Checked)
        self.viewer.addTextItem()
        self.updateForText(self.viewer.addText)

    def watermarkbutton(self):
        self.viewer.drawRect = False
        self.viewer.panSelect = False
        self.viewer.watermark = False
        self.viewer.drawCircle = False
        self.viewer.addText = False
        self.viewer.zoomSelect = False
        self.viewer.drawPolygon = False
        self.viewer.drawFreeHand = False
        self.viewer.drawLine = False
        self.viewer.setCursor(Qt.ArrowCursor)
        self.viewer.addWatermark()
        self.updateForText(self.viewer.addText)

    def panbutton(self):
        self.viewer.panSelect = True
        self.viewer.drawRect = False
        self.viewer.zoomSelect = False
        self.viewer.watermark = False
        self.viewer.addText = False
        self.viewer.drawPolygon = False
        self.viewer.drawFreeHand = False
        self.viewer.drawLine = False
        self.viewer.setCursor(Qt.OpenHandCursor)
        self.viewer.setDragMode(QGraphicsView.ScrollHandDrag)
        self.updateForText(self.viewer.addText)

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
