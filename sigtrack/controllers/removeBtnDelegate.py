from PySide2.QtCore import Qt, QSize, QRect, QModelIndex
from PySide2.QtGui import QMouseEvent, QPainter
from PySide2.QtWidgets import QItemDelegate, QStyleOptionButton, QApplication, QStyleOptionViewItem, QStyle

class RemoveButtonDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        if index.data(Qt.UserRole):        
            button = QStyleOptionButton()
            r = option.rect#getting the rect of the cell
            x = r.left() + r.width() - 30 #the X coordinate
            y = r.top();#the Y coordinate
            w = 30;#button width
            h = 30;#button height
            button.rect = QRect(x,y,w,h)
            button.text = "X"
            button.state = QStyle.State_Enabled
            QApplication.style().drawControl(QStyle.CE_PushButton, button, painter)
        super().paint(painter, option, index)

    def sizeHint(self, option, index):
        return QSize(70, 30)  # Adjust the size as needed

    def editorEvent(self, event, model, option, index):
        if not index.isValid():
            return False

        if event.type() == QMouseEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
            button_rect = option.rect
            if button_rect.contains(event.pos()):
                model.removeRow(index.row())
                return True

        return False