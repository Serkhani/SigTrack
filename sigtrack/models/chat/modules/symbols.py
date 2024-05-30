import os
from PySide2.QtWidgets import (QWidget,QTabWidget,QVBoxLayout,QGridLayout,QScrollArea,QLabel)
from PySide2.QtGui import QIcon,QPixmap,QDrag,QImage
from PySide2.QtCore import QSize, Qt,Signal,QUrl,QBuffer,QByteArray,QIODevice,QMimeData
import sigtrack.models.chat.nato_icons_rc
import sigtrack.models.chat.qt_icons_rc
import base64
# import sigtrack.resources.icons.chat_icons.Nato_Icons
#basedir = os.path.dirname(__file__)

class DraggableImageLabel(QLabel):
    def __init__(self,pixmap,img_path:str,parent=None):
        super().__init__(parent)
        self.setPixmap(QPixmap(pixmap))
        self.img_path = img_path
        
        #self.setToolTip(os.path.basename(img_path))
        self.setAcceptDrops(True)  # Allow dropping onto this label

    def pixmap_to_base64(self, pixmap):
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.WriteOnly)
        pixmap.save(buffer, "PNG")
        buffer.close()
        base64_data = base64.b64encode(byte_array.data()).decode('utf-8')
        return base64_data
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Set the mime data to be dragged
            mime_data = QMimeData()
            # url= QUrl(f"qrc{self.img_path}")
            # mime_data.setUrls([url])
            # print("Mime Data URLs:", mime_data.urls())
            
            pixmap= QPixmap(self.img_path)
            base64_data = self.pixmap_to_base64(pixmap)
            mime_data.setText(base64_data)
            print('Base64 data:',base64_data)
            mime_data.setImageData(self.pixmap().toImage())
            
            # Create the drag object
            # drag = QDrag(self)
            # drag.setMimeData(mime_data)
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.setPixmap(self.pixmap())
            drag.exec_(Qt.CopyAction | Qt.MoveAction)
            
            # if self.img_path:
            #     # pixmap = QPixmap(self.img_path)
            #     # mime_data.setImageData(pixmap)  # Set image data for dragging
            #     drag = QDrag(self)
            #     drag.setMimeData(mime_data)
            
            #     drag.setPixmap(self.pixmap())
                
            #     drag.exec_(Qt.CopyAction | Qt.MoveAction)
                
                #super().mousePressEvent(event)



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
        subFolders = ["Friend_Air","Friend_Equipment", "Friend_Land",
                      "Friend_Subsurface","Hostile_Air","Hostile_Equipment",
                      "Hostile_Land", "Hostile_Subsurface","Neutral_Equipment",
                      "Neutral_Air", "Neutral_Land", "Neutral_Subsurface",
                      "Unknown_Air", "Unknown_Land", "Unknown_Equipment",
                      "Unknown_Subsurface"]

        for folder in subFolders:
            image_layout = QGridLayout()
            tab = QWidget()
            tab.setLayout(image_layout)

            #images_folder =f":Nato_Icons/"
            images_folder =f"sigtrack/models/chat/resources/Nato_Icons/{folder}/"
            images = [(f":/resources/Nato_Icons/{folder}/{img}", img) for img in os.listdir(images_folder) if img.endswith(".png")]
            # images = []
            print(images)

            row = 0
            col = 0
            for img_path in images:
                pixmap = QPixmap(img_path[0])
                label= DraggableImageLabel(pixmap,img_path[0])
                #btn = QPushButton()
                label.setToolTip(img_path[1])
                label.setPixmap(pixmap)
                
                image_layout.addWidget(label, row, col)
                col += 1
                if col == 6:
                    col = 0
                    row += 1

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(tab)

            self.tab_widget.addTab(scroll_area, folder)

    # def image_clicked(self, img_path):
    #     self.selected_image = img_path
    #     # self.accept()