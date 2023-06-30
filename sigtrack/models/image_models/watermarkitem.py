from PySide6.QtCore import (
    Qt,
    QSizeF,
)
from PySide6.QtGui import (
    QPixmap,
    QTransform,
)
from PySide6.QtWidgets import (
    QGraphicsPixmapItem,
    QGraphicsItem,
    QGraphicsScene,
    QApplication,
)

import math

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(filename)s %(lineno)s %(levelname)s\t| %(message)s',
)


class WatermarkItem(QGraphicsPixmapItem):
    def __init__(self, scene: QGraphicsScene):
        super().__init__()

        self.scene = scene

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)

        self.setAcceptHoverEvents(True)
        self.setTransformOriginPoint(self.boundingRect().center())
        self.setTransformationMode(Qt.SmoothTransformation)

        self.scale_factor = 1.0

        self.current_cursor = Qt.ArrowCursor
        self.resize_mode = False
        self.rotation_mode = False

        self.start_pos = None
        self.start_scale = None
        self.original_rotation = 0.0
        self.original_position = self.pos()

    def hoverEnterEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)
        return super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.resize_mode = False
        self.rotation_mode = False
        self.setCursor(Qt.ArrowCursor)
        return super().hoverLeaveEvent(event)

    def hoverMoveEvent(self, event):
        hover_x = event.pos().x()
        hover_y = event.pos().y()
        if hover_x > self.boundingRect().width() - 30 and hover_y > self.boundingRect().height() - 30:
            self.resize_mode = True
            self.setCursor(Qt.SizeFDiagCursor)
        elif hover_x > self.boundingRect().width() - 30 and hover_y < 30:
            self.rotation_mode = True
        elif self.rotation_mode:
            pass
        else:
            self.resize_mode = False
            self.setCursor(Qt.ArrowCursor)
        return super().hoverMoveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.scenePos()
            self.start_width = self.boundingRect().width()
            self.start_scale = self.scale_factor
        if self.resize_mode:
            self.setFlag(QGraphicsItem.ItemIsMovable, False)
            self.setCursor(Qt.SizeFDiagCursor)
        elif self.rotation_mode:
            self.setFlag(QGraphicsItem.ItemIsMovable, False)
            self.setCursor(Qt.ClosedHandCursor)
            self.original_rotation = self.rotation()
            self.original_position = self.pos()
        else:
            self.setFlag(QGraphicsItem.ItemIsMovable, True)
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.resize_mode:
            self.setFlag(QGraphicsItem.ItemIsMovable, True)
            self.resize_mode = False
        self.original_position = self.pos()
        return super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.resize_mode:
            delta = event.scenePos() - self.start_pos
            width = self.start_width + delta.x()
            scale = width / self.boundingRect().width()
            self.scale_factor = self.start_scale * scale
            self.setScale(self.scale_factor)
        if self.rotation_mode:
            delta = event.scenePos() - self.start_pos
            rotation = self.original_rotation + delta.y()
            value = (rotation/self.scale_factor) % 360
            self.update_watermark_rotation(value)
        return super().mouseMoveEvent(event)

    def load_watermark_image(self, watermark_image_path):
        self.reset()
        watermark_image = QPixmap(watermark_image_path)
        self.setPixmap(watermark_image)

    def update_watermark_opacity(self, value):
        self.setOpacity(value / 100.0)

    def update_watermark_scale(self, value):
        self.setScale(value/100.0)

    def update_watermark_rotation(self, value):
        self.setTransformOriginPoint(self.boundingRect().center())
        self.setRotation(value)

    def itemChange(self, change, value):
        return super().itemChange(change, value)

    def reset(self):
        self.setPos(0.0, 0.0)
        self.setScale(1.0)
        self.setRotation(0.0)
        self.setOpacity(1.0)
