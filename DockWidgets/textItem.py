# This Python file uses the following encoding: utf-8
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGraphicsTextItem, QGraphicsItem


class TextItem(QGraphicsTextItem):
    def __init__(self, viewer):
        super().__init__()
        self.viewer = viewer
        self.setPlainText('text')
        self.setPos(self.viewer.scene.width()/2, self.viewer.scene.height()/2)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFont(self.viewer.painter.font)
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.setDefaultTextColor(self.viewer.painter.brush.color())

    def focusInEvent(self, event):
        self.viewer.preview = self
        self.setFont(self.viewer.painter.font)
