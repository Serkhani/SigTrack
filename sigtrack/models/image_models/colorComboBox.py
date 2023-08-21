from PySide2.QtWidgets import QComboBox
from PySide2.QtGui import QColor
from PySide2.QtCore import Qt


class ColorComboBox(QComboBox):
    def __init__(self):
        QComboBox.__init__(self)
        for index, colorName in enumerate(QColor.colorNames()):
            color = QColor(colorName)
            self.addItem(colorName, color)
            idx = self.model().index(index, 0)
            self.model().setData(idx, color, Qt.DecorationRole)
            if index == 20:
                break
