from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QDockWidget

class MarkerPopUp(QDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFloating(True)

    
    def closeEvent(self, event: QCloseEvent) -> None:
        return super().closeEvent(event)