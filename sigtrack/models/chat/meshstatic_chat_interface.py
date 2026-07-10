from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QLineEdit, QPushButton, QRadioButton
from PySide2.QtGui import QIcon
from pubsub import pub
from sigtrack.models.chat.item_model import ItemModel
import sigtrack.models.chat.qt_icons_rc

class MeshtasticChatInterface(QWidget):
    def __init__(self, interface,model:ItemModel):
        super().__init__()
        self.interface = interface
        self.model =model

        # Main layout for the chat interface
        self.main_layout = QHBoxLayout(self)

        # Left layout for radio buttons
        self.left_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout)

        # Right layout for chat display and message input
        self.right_layout = QVBoxLayout()
        self.main_layout.addLayout(self.right_layout)

        # Create radio buttons
        self.create_radio_buttons()

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
        border-radius: 20px;                                
    }

''')


        self.right_layout.addWidget(self.chat_display)

        # Message input area
        input_layout = QHBoxLayout()
        self.message_input = QLineEdit()
        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input)
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        self.right_layout.addLayout(input_layout)

        # Subscribe to message reception events
        pub.subscribe(self.on_receive_message, "meshtastic.receive")


        # Broadcast icon button
        self.broadcast_icon = QRadioButton()
        self.broadcast_icon.setIcon(QIcon(":/resources/qt_icons/broadcast_line_icon.svg"))
        self.broadcast_icon.setToolTip("BroadCast")
        self.left_layout.addWidget(self.broadcast_icon)
        
        
        # Store the selected node ID
        self.selected_node_id = None

    def send_message(self):
        message = self.message_input.text()

        if self.broadcast_icon.isChecked():
            self.interface.sendText(message)
            self.chat_display.addItem(f"Broadcast message: {message}")
        elif self.selected_node_id:
            # Get the short name of the selected node
            short_name = self.find_short_name_by_node_id(self.selected_node_id)
            # Send the message to the selected node using its short name
            self.interface.sendText(message, destinationId=self.selected_node_id)
            self.chat_display.addItem(f"Direct message to {short_name}: {message}")
            self.model.add_sent_message(short_name,message)
        else:
            self.chat_display.addItem("No node selected. Cannot send message.")

        self.message_input.clear()

    def on_receive_message(self, packet):
        print("Received packet:", packet)  # Print the packet contents for debugging

        sender_id = packet.get('fromId')  # Get the sender's ID from the packet
        if sender_id:
            sender_name = self.find_short_name_by_node_id(sender_id)
        else:
            sender_name = 'Unknown'
        if packet['decoded']['text']:
            message_text = packet['decoded']['text']
            self.chat_display.addItem(f"{sender_name}: {message_text}")
            self.model.add_receive_message(sender_name,message_text)
        else:
            self.chat_display.addItem(f"Received packet with no text content: {packet}")



    def find_short_name_by_node_id(self, node_id):
        # Retrieve the short name of the node associated with the given node ID
        node_info = self.interface.nodes.get(node_id)
        if node_info:
            user_info = node_info.get("user", {})
            return user_info.get("shortName", "Unknown")
        return "Unknown"

    def create_radio_buttons(self):
        # Check if there are any nodes in the network
        self.node_ids = list(self.interface.nodes.keys())
        if not self.node_ids:
            print("No nodes found in the mesh network.")
        else:
            # Iterate through all available nodes
            for node_id in self.node_ids:
                if node_id in self.interface.nodes:
                    current_node = self.interface.nodes[node_id]

                    # Get short name of the radio associated with the node
                    user_info = current_node.get("user", {})
                    short_name = user_info.get("shortName", "Unknown")

                    # Create a QRadioButton for each node
                    radio_button = QRadioButton(short_name, parent=self)
                    radio_button.clicked.connect(self.handle_radio_button_clicked)

                    self.left_layout.addWidget(radio_button)

                else:
                    print(f"Node with ID '{node_id}' not found in the mesh network.")

    def handle_radio_button_clicked(self):
        # Get the text of the radio button that was clicked
        sender = self.sender()
        radio_button_text = sender.text()

        # Assuming the radio button text is the short name, find its corresponding node ID
        self.selected_node_id = self.find_node_id_by_short_name(radio_button_text)
        self.chat_display.clear()

    def find_node_id_by_short_name(self, short_name):
        for node_id, node_info in self.interface.nodes.items():
            user_info = node_info.get("user", {})
            if user_info.get("shortName") == short_name:
                return node_id
        return None
