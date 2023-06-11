from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
from DockWidgets.imageview.undo_redo_command import DeleteCommand

class WatermarkItem(QGraphicsPixmapItem):
    def __init__(self, pixmap):
        super().__init__(pixmap)

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedChange:
            self.setOpacity(1.0 if value else 0.5)
        return super().itemChange(change, value)

    def update_watermark_opacity(self, value):
        self.watermark_opacity = value
        if self.watermark_item:
            self.watermark_item.setOpacity(value / 100.0)

    def update_watermark_scale(self, value):
        self.watermark_scale = value / 100.0
        if self.watermark_item:
            self.watermark_item.setScale(self.watermark_scale)

    def update_watermark_rotation(self, value):
        self.watermark_rotation = value
        if self.watermark_item:
            self.watermark_item.setRotation(self.watermark_rotation)
