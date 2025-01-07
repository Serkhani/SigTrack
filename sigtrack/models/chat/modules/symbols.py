import os
from PySide6.QtWidgets import (QWidget,QTabWidget,QVBoxLayout, QPushButton,QGridLayout,QScrollArea)
from PySide6.QtGui import QIcon,QPixmap
from PySide6.QtCore import QSize, Qt,Signal
import sigtrack.models.chat.nato_icons_rc
import sigtrack.models.chat.qt_icons_rc
from sigtrack.models.chat.modules.icons_path import icons_name

# import sigtrack.resources.icons.chat_icons.Nato_Icons
#basedir = os.path.dirname(__file__)


class SymbolManager(QWidget):
    #image_clicked = Signal(QPixmap)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Choose an Image")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.images_root = "sigtrack/models/chat/resources/Nato_Icons/"

        self.load_images()

    def load_images(self):
        subfolders = ["Friend_Air","Friend_Equipment", "Friend_Land",
                      "Friend_Subsurface","Hostile_Air","Hostile_Equipment",
                      "Hostile_Land", "Hostile_Subsurface","Neutral_Equipment",
                      "Neutral_Air", "Neutral_Land", "Neutral_Subsurface",
                      "Unknown_Air", "Unknown_Land", "Unknown_Equipment",
                      "Unknown_Subsurface"]

        # for folder in subfolders:
        for i in range(len(icons_name)):
            image_layout = QGridLayout()
            tab = QWidget()
            tab.setLayout(image_layout)

            #images_folder =f":Nato_Icons/"
            # images_folder =f"sigtrack/models/chat/resources/Nato_Icons/{folder}/"
            # images = [(f":resources/Nato_Icons/{folder}/{img}", img) for img in os.listdir(images_folder) if img.endswith(".png")]
            # # images = []
            # print(images)

            row = 0
            col = 0
            for img_path in icons_name[i]:
                btn = QPushButton()
                btn.setToolTip(img_path[1])
                btn.setIcon(QIcon(img_path[0]))
                btn.clicked.connect(self.image_clicked(img_path))
                # pixmap = QPixmap(img_path)
                # label = QLabel()
                # label.setPixmap(pixmap)
                # label.mousePressEvent = lambda event, img=img_path: self.image_clicked(img)
                image_layout.addWidget(btn, row, col)
                col += 1
                if col == 6:
                    col = 0
                    row += 1

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(tab)

            self.tab_widget.addTab(scroll_area, subfolders[i])

    def image_clicked(self, img_path):
        self.selected_image = img_path
        # self.accept()
        
    def dragEnterEvent(self, event):
        #if event.mimeData().hasFormat("application/x-icon"):
        if event.mimeData().hasFormat("image/png"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        pos = event.pos()  # In PySide6, use 'pos' instead of 'position'
        
        # Calculate the (x, y) point on the map widget
        widget_width = self.width()
        widget_height = self.height()

        # Map screen coordinates to Leaflet map coordinates
        # This simple approach assumes a consistent zoom level and center point.
        longitude = (pos.x() / widget_width) * 360 - 180
        latitude = 90 - (pos.y() / widget_height) * 180
        
        print(f"Dropped at screen point ({pos.x()}, {pos.y()})")
        print(f"Converted to geographical coordinates: latitude = {latitude}, longitude = {longitude}")

        event.acceptProposedAction()

# class SymbolManager(QWidget):
#     #image_clicked = Signal(QPixmap)

#     def _init_(self, parent=None):
#         super()._init_(parent)

#         self.setWindowTitle("Choose an Image")
#         self.layout = QVBoxLayout()
#         self.setLayout(self.layout)

#         self.tab_widget = QTabWidget()
#         self.layout.addWidget(self.tab_widget)

#         self.images_root = "Nato_Icons/"

#         self.load_images()

#     def load_images(self):
#         subfolders = [folder for folder in os.listdir(self.images_root) if
#                       os.path.isdir(os.path.join(self.images_root, folder))]

#         for folder in subfolders:
#             image_layout = QGridLayout()
#             tab = QWidget()
#             tab.setLayout(image_layout)

#             images_folder = os.path.join(self.images_root, folder)
#             images = [os.path.join(images_folder, img) for img in os.listdir(images_folder) if img.endswith(".png")]

#             row = 0
#             col = 0
#             for img_path in images:
#                 pixmap = QPixmap(img_path)
#                 label = QLabel()
#                 label.setPixmap(pixmap)
#                 label.mousePressEvent = lambda event, img=img_path: self.image_clicked(img)
#                 image_layout.addWidget(label, row, col)
#                 col += 1
#                 if col == 6:
#                     col = 0
#                     row += 1

#             scroll_area = QScrollArea()
#             scroll_area.setWidgetResizable(True)
#             scroll_area.setWidget(tab)

#             self.tab_widget.addTab(scroll_area, folder)

#     def image_clicked(self, img_path):
#         self.selected_image = img_path
#         self.accept()