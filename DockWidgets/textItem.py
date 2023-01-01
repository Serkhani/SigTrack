# This Python file uses the following encoding: utf-8
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGraphicsTextItem, QGraphicsItem
from PySide2.QtGui import QTextBlockFormat, QTextCursor
from DockWidgets.undo_redo_command import DeleteCommand

class TextItem(QGraphicsTextItem):
    itemType = QGraphicsTextItem().type()
    def __init__(self, viewer):
        super().__init__()
        self.viewer = viewer
        self.setPlainText('text')
        self.setPos(self.viewer.scene.width()/2, self.viewer.scene.height()/2)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFont(self.viewer.painter.font)
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.setDefaultTextColor(self.viewer.painter.brush.color())
        self.alignment = Qt.AlignLeft
#        self.setTextAlignment(Qt.AlignCenter)

    def type(self):
        return TextItem.itemType

    def updateGeometry(self, alignment):
        prevTopRight = self.boundingRect().topRight()
        self.setTextWidth(-1)
        self.setTextWidth(self.boundingRect().width())
        self.setTextAlignment(alignment)
        topRight = self.boundingRect().topRight()
        if self.alignment==Qt.AlignRight:
            self.setPos(self.pos()+(prevTopRight- topRight))

    def setTextAlignment(self, alignment):
        self.alignment = alignment
        format = QTextBlockFormat()
        format.setAlignment(self.alignment)
        cursor = QTextCursor()
        cursor.select(QTextCursor.Document)
        cursor.mergeBlockFormat(format)
        cursor.clearSelection()
        self.setTextCursor(cursor)

    def focusInEvent(self, event):
        self.viewer.preview = self
        self.setDefaultTextColor(self.viewer.painter.brush.color())
        self.setFont(self.viewer.painter.font)

#    def keyPressEvent(self, event):
#        if event.key() == Qt.Key_Delete:
#            self.viewer.scene.removeItem(self)
#            deleteCommand = DeleteCommand(self.viewer.scene)
#            self.viewer.undoStack.push(deleteCommand)
#        QGraphicsTextItem.keyPressEvent(self, event)

