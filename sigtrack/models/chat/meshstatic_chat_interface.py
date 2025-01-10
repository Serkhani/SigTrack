from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QToolButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from pubsub import pub
from sigtrack.models.chat.item_model import ItemModel
import sigtrack.models.chat.qt_icons_rc

class MeshtasticChatInterface(QWidget):
    
    def __init__(self, interface,model:ItemModel):
        super().__init__()
        
        self.interface = interface
        self.model =model
        self.tool_buttons = []
        self.selected_node_id = None

        # Main layout for the chat interface
        self.main_layout = QHBoxLayout(self)

        # Left layout for radio buttons
        self.left_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_layout)

        # Right layout for chat display and message input
        self.right_layout = QVBoxLayout()
        self.main_layout.addLayout(self.right_layout)
        
        # Create the broadcast icon button
        self.create_broadcast_button()

        # Create radio buttons
        self.create_tool_buttons()

        # Chat display
        self.chat_display = QListWidget()
        self.chat_display.setStyleSheet('''
            QListWidget {
                        background-color: #f5f5f5; /*light gray*/
                        border: 3px solid #dcdcdc; /*light gray*/
                        border-radius: 3px;
                        padding: 10px;
                        
                    }
            QListWidget::item {
                background-color: #ffffff; /*white*/
                padding: 10px;
                margin: 2px;
                border-bottom: 1px solid #dcdcdc; /*light gray*/
                border-radius: 5px; 
                text-align: right;
                                                        
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
        self.send_button.setStyleSheet("color: black;")
        self.send_button.setStyleSheet("font-weight: bold;")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        self.right_layout.addLayout(input_layout)

        # Subscribe to message reception events
        pub.subscribe(self.on_receive_message, "meshtastic.receive")


    def create_broadcast_button(self):
        self.broadcast_icon = QToolButton()
        self.broadcast_icon.setIcon(QIcon("qt_icons/broadcast_black.svg"))
        self.broadcast_icon.setToolTip("Broadcast")
        self.broadcast_icon.setCheckable(True)
        self.broadcast_icon.setStyleSheet("""
            QToolButton {
                background-color: grey;
                border-radius: 8px;
                padding: 10px;
                color: black;
                font-weight: bold;
            }
            QToolButton:hover {
                background-color: white;
            }
        """)
        self.broadcast_icon.setFixedSize(60, 35)
        self.broadcast_icon.clicked.connect(self.handle_broadcast_clicked)
        self.left_layout.addWidget(self.broadcast_icon)


      

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
        # if packet['decoded']['text']:
        #     message_text = packet['decoded']['text']
        #     self.chat_display.addItem(f"{sender_name}: {message_text}")
        #     self.model.add_receive_message(sender_name,message_text)
        # else:
        #     self.chat_display.addItem(f"Received packet with no text content: {packet}")
        decoded_packet=packet.get('decoded',{})
        message_text=decoded_packet.get('text')
        
        if message_text:
            self.chat_display.addItem(f"{sender_name}:{message_text}")
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

    def create_tool_buttons(self):
        # Check if there are any nodes in the network
        self.node_ids = list(self.interface.nodes.keys())
        if not self.node_ids:
            print("No nodes found in the mesh network.")
        else:
            #self.tool_buttons = []
            # Iterate through all available nodes
            for node_id in self.node_ids:
                if node_id in self.interface.nodes:
                    current_node = self.interface.nodes[node_id]

                    # Get short name of the radio associated with the node
                    user_info = current_node.get("user", {})
                    short_name = user_info.get("shortName", "Unknown")

                    # Create a QTool Button for each node
                    tool_button = QToolButton()
                    tool_button.setCheckable(True)
                    tool_button.setText(short_name)
                    #tool_button.setToolButtonStyle(Qt.ToolButtonIconOnly)
                    tool_button.setToolButtonStyle(Qt.ToolButtonTextOnly)
                    tool_button.setStyleSheet("""
                        QToolButton {
                            background-color: grey;  /* Green background #4CAF50 */
                            border-radius: 8px;          /* Rounded corners */
                            padding:12px;               /* Padding around text */
                            color: black;                /* Text color */
                            font-weight: bold;           /* Bold text */
                        }
                        QToolButton:hover {
                            background-color:white ;   /* Darker green on hover #45a049*/
                        }
                    """)

                    tool_button.setFixedSize(60,35)
                    
                    tool_button.clicked.connect(self.handle_tool_button_clicked)
                    #tool_button.clicked.connect(lambda checked,  btn=tool_button: self.handle_tool_button_clicked(btn))


                    self.left_layout.addWidget(tool_button)
                    self.tool_buttons.append(tool_button)
                    

                else:
                    print(f"Node with ID '{node_id}' not found in the mesh network.")
                    
    def handle_broadcast_clicked(self):
        if self.broadcast_icon.isChecked():
            # Uncheck all other buttons
            for button in self.tool_buttons:
                button.setChecked(False)
                button.setStyleSheet("""
                    QToolButton {
                        background-color: grey;
                        border-radius: 8px;
                        padding: 12px;
                        color: black;
                        font-weight: bold;
                    }
                    QToolButton:hover {
                        background-color: white;
                    }
                """)
            
            # Set color effect for the broadcast button
            self.broadcast_icon.setStyleSheet("""
                QToolButton {
                    background-color: black;
                    border-radius: 8px;
                    padding: 10px;
                    color: white;
                    font-weight: bold;
                }
                QToolButton:hover {
                    background-color: black;
                }
            """)
            self.broadcast_icon.setIcon(QIcon("qt_icons/broadcast_white.svg"))
            self.selected_node_id = None
        else:
            # Reset broadcast button style when unchecked
            self.broadcast_icon.setStyleSheet("""
                QToolButton {
                    background-color: grey;
                    border-radius: 8px;
                    padding: 10px;
                    color: black;
                    font-weight: bold;
                }
                QToolButton:hover {
                    background-color: black;
                }
            """)
        
        self.chat_display.clear()


    
    def handle_tool_button_clicked(self):
        sender = self.sender()
        
        # Uncheck the broadcast button
        self.broadcast_icon.setChecked(False)
        self.broadcast_icon.setStyleSheet("""
            QToolButton {
                background-color: grey;
                border-radius: 8px;
                padding: 10px;
                color: black;
                font-weight: bold;
             }
             QToolButton:hover {
                 background-color: white;
             }
        """)
        self.broadcast_icon.setIcon(QIcon("qt_icons/broadcast_black.svg"))
        
        # Uncheck all other buttons
        for button in self.tool_buttons:
            if button != sender:
                button.setChecked(False)
                button.setStyleSheet("""
                    QToolButton {
                        background-color: grey;
                        border-radius: 8px;
                        padding: 12px;
                        color: black;
                        font-weight: bold;
                    }
                    QToolButton:hover {
                        background-color: white;
                    }
                """)

        # Handle the clicked button
        if sender.isChecked():
            # Set color effect for the checked button
            sender.setStyleSheet("""
                QToolButton {
                    background-color: black;  /* Black background for checked state */
                    border-radius: 8px;
                    padding: 12px;
                    color: white;
                    font-weight: bold;
                }
                QToolButton:hover {
                    background-color: black;
                }
            """)
            
            # radio_button_text = sender.text()
            # self.selected_node_id = self.find_node_id_by_short_name(radio_button_text)
            # self.chat_display.clear()
            self.selected_node_id = self.node_ids[self.tool_buttons.index(sender)]
        else:
            # If unchecked, clear selection
            # self.selected_node_id = None
            # self.chat_display.clear()
            
            sender.setStyleSheet("""
                QToolButton {
                    background-color: grey;
                    border-radius: 8px;
                    padding: 10px;
                    color: black;
                    font-weight: bold;
                }
                QToolButton:hover {
                    background-color: white;
                }
            """)
            self.selected_node_id = None
        
        self.chat_display.clear()
    
    
        
    # def handle_tool_button_clicked(self):
    #     # Get the text of the radio button that was clicked
    #     sender = self.sender()
    #     radio_button_text = sender.text()

    #     # Assuming the radio button text is the short name, find its corresponding node ID
    #     self.selected_node_id = self.find_node_id_by_short_name(radio_button_text)
    #     self.chat_display.clear()

    def find_node_id_by_short_name(self, short_name):
        for node_id, node_info in self.interface.nodes.items():
            user_info = node_info.get("user", {})
            if user_info.get("shortName") == short_name:
                return node_id
        return None


class Peers(QWidget):
    def __init__(self,interface,model:ItemModel):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.interface=interface
        self.model =model

        # Create the table widget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(6)  # Adjust the number of columns as needed
        self.table_widget.setHorizontalHeaderLabels(["Name", "Model", "Mac Address", "Last Heard", "SNR", "Battery Level"])

        # Populate the table with node information
        self.populate_table()

        # Add the table widget to the layout
        self.main_layout.addWidget(self.table_widget)

        # Set the layout for the widget
        self.setLayout(self.main_layout)

    def populate_table(self):
        if not self.interface.nodes:
            print("No nodes found in the mesh network.")
        else:
            # Iterate through each node
            for node_id, node_info in self.interface.nodes.items():
                # Extract node information
                user_info = node_info.get("user", {})
                short_name= node_info.get("shortname","")
                long_name = user_info.get("longName", "")
                modell = user_info.get("hwModel", "")
                mac_address = user_info.get("macaddr", "")
                last_heard = str(node_info.get("lastHeard", ""))
                snr = str(node_info.get("snr", ""))
                battery_level = str(node_info.get("deviceMetrics", {}).get("batteryLevel", ""))

                # Insert a new row in the table and set item data
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                self.table_widget.setItem(row_position, 0, QTableWidgetItem(long_name))
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(short_name))
                self.table_widget.setItem(row_position, 2, QTableWidgetItem(modell))
                self.table_widget.setItem(row_position, 3, QTableWidgetItem(mac_address))
                self.table_widget.setItem(row_position, 4, QTableWidgetItem(last_heard))
                self.table_widget.setItem(row_position, 5, QTableWidgetItem(snr))
                self.table_widget.setItem(row_position, 6, QTableWidgetItem(battery_level))

        #self.model.add_nodeInfo(str(node_id),str(short_name),str(long_name),str(modell))
                #print(f"node id",node_id)
                # print(short_name)
                # print(long_name)
                # print(node_id)
                # print(modell)
            self.model.add_nodeInfo(node_id,short_name,long_name,modell)

        # Remove row numbers
        self.table_widget.verticalHeader().setVisible(False)
        
        # Set style for the table widget
        self.table_widget.setStyleSheet(
            """
            QTableWidget {
                gridline-color: transparent;
                border: none;
                font-size: inherit;
                font-weight: inherit;
                gridline-color: black;     /* Set gridline color to black */
            }
                
            QHeaderView::section {
                background-color: gray;    /* Set header background color */
                color: black;              /* Set header text color */
                font-weight: bold;
           
            }
            """
        )
