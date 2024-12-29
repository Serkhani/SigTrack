from PySide6.QtCore import QObject


class ItemController(QObject):
    def __init__(self, model, view):
        super(ItemController, self).__init__()
        self.model = model
        self.view = view