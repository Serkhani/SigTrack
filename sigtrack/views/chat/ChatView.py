from PySide6.QtWidgets import (
    QApplication, QMainWindow, QListWidget, QTextEdit, QLineEdit, QPushButton,
    QHBoxLayout, QVBoxLayout, QWidget, QDockWidget, QToolBar, QStackedWidget, QComboBox,
    QLabel, QSizePolicy, QToolButton, QMdiArea, QRadioButton
)

from PySide6.QtCore import Qt, QSize, Slot
from PySide6.QtGui import QIcon

from sigtrack.models.chat.ChatModel import ChatClient

class ItemView(QWidget):
    def __init__(self, model):
        super(ItemView, self).__init__()
        self.model = model

    # Main layout for the chat interface
        self.main_layout = QHBoxLayout(self)
        self.setStyleSheet("background-color: #bcbec2; border: 100px;")
        

        # Sidebar divided into two parts
        self.sidebar_layout = QHBoxLayout()
        self.toolbar = QToolBar()
        self.stacked_widget = QStackedWidget()

        # Set up the toolbar with buttons
        self.setup_toolbar()

        # stack widgets linked to push buttons
        self.setup_stacked_widget()

        # Add the toolbar and the stacked widget to the sidebar layout
        self.sidebar_layout.addWidget(self.toolbar)
        self.sidebar_layout.addWidget(self.stacked_widget)

        
        #top layout
        self.top_layout = QHBoxLayout()

        self.connectBtn= QRadioButton("Disconnected",self)
        #self.connectBtn.setDisabled()
        self.connectBtn.setIconSize(QSize(24,24))

        self.topLabel =QLabel("Chatting With :")
        # self.topLabel.setFixedHeight(1)
        # self.topLabel.setFixedWidth(1)
        #frame1.
        

        self.searchBtn = QToolButton()
        self.searchBtn.setIcon(QIcon('sigtrack/resources/icons/chat_icons/search.svg'))
        self.searchBtn.setIconSize(QSize(24,24))
        self.searchBtn.setStyleSheet("border: none;")
        #self.searchBtn.setToolButtonStyle(Qt.AlignLeft )
        self.searchBtn.setStyleSheet("padding: 0px;")

        self.sideBtn = QToolButton()
        self.sideBtn.setIcon(QIcon('sigtrack/resources/icons/chat_icons/sidebar.svg'))
        self.sideBtn.setIconSize(QSize(24,24))
        self.sideBtn.setStyleSheet("border: none;")
        #self.sideBtn.setToolButtonStyle(Qt.AlignLeft )
        self.sideBtn.setStyleSheet("padding: 0px;")
        
        self.moreBtn = QToolButton()
        self.moreBtn.setIcon(QIcon('sigtrack/resources/icons/chat_icons/more-horizontal.svg'))
        self.moreBtn.setIconSize(QSize(24,24))
        self.moreBtn.setStyleSheet("border: none;")
        #self.moreBtn.setToolButtonStyle(Qt.AlignLeft )
        self.moreBtn.setStyleSheet("padding: 0px;")

        self.top_layout.addWidget(self.connectBtn)
        self.top_layout.addWidget(self.topLabel)
        self.top_layout.addWidget(self.searchBtn)
        self.top_layout.addWidget(self.sideBtn)
        self.top_layout.addWidget(self.moreBtn)

        
        # Chat display
        self.chat_display = QListWidget()
        self.chat_display.setStyleSheet('''
    QListWidget {
        background-color: #f5f5f5;
        border: 3px solid #dcdcdc;
        border-radius: 3px;
        padding: 10px;
        
    }
    QListWidget::item {
        background-color: #ffffff;
        border-bottom: 1px solid #dcdcdc;
        text-align: center;
        padding: 10px;
    QListWidget::item {
        text-align: right;
    } 
        
    }
    QListWidget::item:last {
        border-bottom: none;
    }

''')
        

        # Message input area
        self.message_input = QLineEdit()
        #self.message_input.setStyleSheet("background-color: #bcbec2; border: none;")
        #self.message_input.setFixedHeight(50)
        
        
        self.emoji_button=QToolButton()
        self.emoji_button = QToolButton()
        self.emoji_button.setIcon(QIcon('sigtrack/resources/icons/chat_icons/smile.svg'))
        self.emoji_button.setStyleSheet("background-color: #bcbec2; border: none;")
        self.emoji_button.setIconSize(QSize(24,24))
        

        self.send_button = QToolButton()
        self.send_button.setIcon(QIcon('sigtrack/resources/icons/chat_icons/send.svg'))
        self.send_button.setStyleSheet("background-color: #bcbec2; border: none;")
        self.send_button.setIconSize(QSize(24,24))
        self.send_button.clicked.connect(self.add_item)
        
        self.upload_button = QToolButton()
        self.upload_button.setIcon(QIcon('sigtrack/resources/icons/chat_icons/paperclip.svg'))
        self.upload_button.setStyleSheet("background-color: #bcbec2; border: none;")
        self.upload_button.setIconSize(QSize(24,24))
        

        # Layout for the message input area
        self.input_layout = QHBoxLayout()
        self.input_layout.addWidget(self.emoji_button)
        self.input_layout.addWidget(self.message_input)
        self.input_layout.addWidget(self.send_button)
        self.input_layout.addWidget(self.upload_button)
        #QWidget.setStyleSheet("background-color:#6c6c6c;")
        

        # Layout for the chat area
        self.chat_layout = QVBoxLayout()
        self.chat_layout.addLayout(self.top_layout)
        self.chat_layout.addWidget(self.chat_display)
        self.chat_layout.addLayout(self.input_layout)

        # Add sidebar and chat layouts to the main layout
        self.main_layout.addLayout(self.sidebar_layout, 1)  # Sidebar takes up 1 part of the space
        self.main_layout.addLayout(self.chat_layout, 3)  # Chat area takes up 3 parts of the space
        self.chat_client = ChatClient("127.0.0.1", 8000)

        self.chat_client.receivedSignal.connect(self.received_message)
        self.model.itemsChanged.connect(self.update_view)
    
    # def send_message(self):
    #     message = self.message_input.text()
    #     self.chat_display.addItem("You: " + message)
    #     self.chat_client.send_messages(message)
    #     self.message_input.clear()
    
    @Slot(str)
    def received_message(self, message):
        self.chat_display.addItem("Other: " + message)
    
    def setup_toolbar(self):
        # Set the style sheet for the toolbar to have a background color of #808080
        self.toolbar.setStyleSheet("QToolBar { background-color:#808080;}")
        self.toolbar.setOrientation(Qt.Vertical)
        self.toolbar.setFixedWidth(53)
        
        icon_size = QSize(100, 100)

        # Create buttons and add them to the toolbar
        button1 = QToolButton()
        button1.setIcon(QIcon("sigtrack/resources/icons/chat_icons/align-justify.svg"))
        button1.setToolButtonStyle(Qt.ToolButtonIconOnly)
        button1.setStyleSheet("background-color:#808080; padding: 9px;")
        button1.setIconSize(icon_size)
        
        
        button2 = self.create_tool_button("sigtrack/resources/icons/chat_icons/settings.svg","Settings")
        button3 = self.create_tool_button("sigtrack/resources/icons/chat_icons/chat.svg","Chats")
        button4 = self.create_tool_button("sigtrack/resources/icons/chat_icons/video-stream.svg","Video Streaming")
        
        # button5 = QToolButton()
        # button5.setIcon(QIcon("qt sigtrack/resources/icons/chat_icons/settings.ico"))
        # button5.setText("Settings")
        # button5.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
                
        
        self.toolbar.addWidget(button1)
        self.toolbar.addWidget(button2)
        self.toolbar.addWidget(button3)
        self.toolbar.addWidget(button4)
        #button1.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        button2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        button3.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))  
        button4.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))  
        #button5.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))

    #connect button1 to toggle the visibility of button names
        button1.clicked.connect(self.toggle_button_names)

    def create_tool_button(self, icon_path, text):
        button = QToolButton()
        button.setIcon(QIcon(icon_path))
        button.setText(text)
        button.setIconSize(QSize(50,50))
        button.setStyleSheet("background-color:#808080; padding: 9px;")
        button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        return button

    def toggle_button_names(self):
        #Toggle between showing and hiding the text of buttons
        for button in self.toolbar.children():
            if isinstance(button, QToolBar) and button.toolButtonStyle() == Qt.ToolButtonIconOnly:
                self.toolbar.setFixedWidth(100)
                button.setIconSize(QSize(50,50))
                button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

            elif isinstance(button, QToolButton):
                self.toolbar.setFixedWidth(50)
                button.setToolButtonStyle(Qt.ToolButtonIconOnly)

    def setup_stacked_widget(self):
        # Create different content widgets for the stack
        # widget1 = QWidget()
        # widget1.setStyleSheet("background-color: #0d0a03;")
        # widget1_layout = QVBoxLayout()
        # widget1_layout.addWidget(QLineEdit())
        # widget1.setLayout(widget1_layout)

        widget2 = QWidget()
        widget2.setStyleSheet("background-color: #bcbec2; opacity: 0.5;")
        widget2_layout = QVBoxLayout()
        widget2_layout.addWidget(QLabel("IP Adress"))
        widget2_layout.addWidget(QComboBox())
        widget2_layout.addWidget(QPushButton())
        widget2.setLayout(widget2_layout)
        
        widget3 = QWidget()
        widget3.setStyleSheet("background-color: #bcbec2;")
        widget3_layout = QVBoxLayout()
        widget3_layout.addWidget(QPushButton())
        widget3.setLayout(widget3_layout)
        
        widget4 = QWidget()
        widget4.setStyleSheet("background-color: #bcbec2;")
        widget4_layout = QVBoxLayout()
        widget4_layout.addWidget(QPushButton())
        widget4.setLayout(widget4_layout)
        
        widget5 = QWidget()
        widget5.setStyleSheet("background-color: #bcbec5;")
        widget5_layout = QVBoxLayout()
        widget5_layout.addWidget(QPushButton("Me"))
        widget5.setLayout(widget5_layout)
        
        # Add the widgets to the stacked widget
        #self.stacked_widget.addWidget(widget1)
        self.stacked_widget.addWidget(widget2)
        self.stacked_widget.addWidget(widget3)
        self.stacked_widget.addWidget(widget4)
        self.stacked_widget.addWidget(widget5)

    @Slot()
    def add_item(self):
        message = self.message_input.text()
        if message:
            self.chat_display.addItem("You: " + message)
            self.chat_client.send_messages(message)
            self.message_input.clear()
    
    @Slot(list)
    def update_view(self, items):
        self.chat_display.clear()
        self.chat_display.addItems(items)
