from PySide2.QtCore import (QCoreApplication)
from PySide2 import QtWidgets

class AddCommand(QtWidgets.QUndoCommand):
    def __init__(self, item, scene ):
        super(AddCommand, self).__init__()
        self.item = item
        self.scene = scene

    def undo(self):
        self.scene.removeItem(self.item)
        self.scene.update()

    def redo(self):
        self.scene.addItem(self.item)
        self.scene.clearSelection()
        self.scene.update()

    def tr(self, message):
        return QCoreApplication.translate('SigTrack', message)


class DeleteCommand(QtWidgets.QUndoCommand):
    def __init__(self, scene):
        super(DeleteCommand, self).__init__()
        self.scene = scene
        self.selectedItems = self.scene.selectedItems()

    def undo(self):
        for i in self.selectedItems:
            self.scene.addItem(i)
        self.scene.update()

    def redo(self):
        for i in self.selectedItems:
            self.scene.removeItem(i)
    
    def tr(self, message):
        return QCoreApplication.translate('SigTrack', message)


class MoveCommand(QtWidgets.QUndoCommand):
    def __init__(self, item, oldPos):
        super(MoveCommand, self).__init__()
        self.item = item
        self.oldPos = oldPos
        self.newPos = self.item.pos()

    def undo(self):
        self.item.setPos(self.oldPos)
        self.item.scene().update()
        
    def redo(self):
        self.item.setPos(self.newPos)
    
    def tr(self, message):
        return QCoreApplication.translate('SigTrack', message)
