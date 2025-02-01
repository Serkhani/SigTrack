from PySide6.QtWidgets import (QMainWindow, QDockWidget, QWidget, QVBoxLayout, QSizePolicy, QSpacerItem,
                               QToolButton, QToolBar,QScrollArea)
from PySide6.QtCore import Qt, QSize, Slot, QFile, QTextStream
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWebEngineWidgets import QWebEngineView
from sigtrack.models.chat.item_model import ItemModel
from sigtrack.models.chat.map_changer import MapChanger
from sigtrack.models.chat.peers import Peers
from sigtrack.models.chat.meshstatic_chat_interface import MeshtasticChatInterface
from sigtrack.models.chat.modules.symbols import SymbolManager
from sigtrack.models.chat.modules.weather import WeatherApp
import sigtrack.models.chat.qt_icons_rc
import sigtrack.models.chat.nato_icons_rc
import sigtrack.models.chat.maps_rc
import meshtastic.serial_interface
from pubsub import pub


# class Serial:
#     def __init__(self):
#         self.nodes = {
#                 '1': {},
#                 '2': {},
#                 '3': {},
#                 '4': {},
#                 '5': {},
#                 '6': {},
#                 '7': {},
#                 '8': {},
#                 '9': {},
#                 '10': {},
#             }
        
# interface = Serial()
interface = meshtastic.serial_interface.SerialInterface()


class MapDisplay(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.node_ids = list(interface.nodes.keys())
        # self.node_ids = []
        
        self.setWindowTitle("LoRa Chat Application")
        self.setGeometry(100, 100, 1500, 750)
        # self.setup_map(interface)
        self.setup_toolbar()
        #self.symbol_button = QToolButton()
        #self.symbol_manager= SymbolManager()
        self.model = ItemModel()
        self.font = QFont()
        self.setup_map(interface)

        # Create a dock widget for stacking interfaces
        self.messageDock_widget = QDockWidget(self)
        self.messageDock_widget.setMinimumSize(300,300)
        self.messageDock_widget.setMaximumSize(500,750)
        self.messageDock_widget.setWindowTitle("Messages")
        self.messageDock_widget.setStyleSheet("""
            QDockWidget::title {
                font-weight: bold;
                }
            """)
        #self.messageDock_widget.setFont(self.font(12))
        
        self.natoDock_widget = QDockWidget(self)
        self.natoDock_widget.setMinimumSize(300,300)
        self.natoDock_widget.setMaximumSize(500,750)
        self.natoDock_widget.setWindowTitle("Symbols")
        
        self.peersDock_widget = QDockWidget(self)
        self.peersDock_widget.setMinimumSize(350,150)
        self.peersDock_widget.setMaximumSize(500,400)
        self.peersDock_widget.setWindowTitle("Nodes Info")
        
        self.weatherDock_widget = QDockWidget(self)
        self.weatherDock_widget.setMinimumSize(350,150)
        self.weatherDock_widget.setMaximumSize(500,400)
        self.weatherDock_widget.setWindowTitle("Weather Info" )
        
        self.mapDock_widget = QDockWidget(self)
        self.mapDock_widget.setMinimumSize(350,150)
        self.mapDock_widget.setMaximumSize(500,400)
        self.mapDock_widget.setWindowTitle("Maps")
        
        self.addDockWidget(Qt.RightDockWidgetArea, self.messageDock_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.natoDock_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.peersDock_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.weatherDock_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.mapDock_widget)
        
       #self.dock_widget.hide()
        self.messageDock_widget.hide()
        self.natoDock_widget.hide()
        self.peersDock_widget.hide()
        self.weatherDock_widget.hide()
        self.mapDock_widget.hide()
        
        
        
        
    def setup_toolbar(self):
        # Create a transparent vertical toolbar on the left side
        self.toolbar = QToolBar()
        self.toolbar.setOrientation(Qt.Vertical)
        self.toolbar.setMovable(True)
        self.toolbar.setFixedWidth(50)
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)
        # self.toolbar.setStyleSheet("""
        #     QToolBar{
        #         background-color: none;
        #         border: none;
        #         padding:4px;
        #         spacing:10px;
        #         max-width: 10?00px; /* Limit button width */
                
                
        #     }                       
                                   
        # """)

        # Chat button
        self.chat_button = QToolButton()
        self.chat_button = self.create_tool_button(":/resources/qt_icons/message_black.svg", "Messages")
        self.chat_button.clicked.connect(self.show_chat_interface)
        #self.chat_button.clicked.connect(self.toggle_messageDock)
        self.toolbar.addWidget(self.chat_button)

       
        # Symbol button
        self.symbol_button = self.create_tool_button(":/resources/qt_icons/symbol_black.svg", "Symbols")
        self.symbol_button.clicked.connect(self.show_symbol_manager)
        self.toolbar.addWidget(self.symbol_button)
       
         

        # Peers button
        #self.peers_button = self.create_tool_button("qt_icons/people_icon.svg", "Peers")
        self.peers_button = self.create_tool_button(":/resources/qt_icons/peer_black.svg", "Peers")
        self.peers_button.clicked.connect(self.show_peers)
        self.toolbar.addWidget(self.peers_button)
        
        
        # self.toolbar.addWidget(self.peers_button)

        # Weather button
        self.weather_button = self.create_tool_button(":/resources/qt_icons/weather_black.svg", "Weather")
        self.weather_button.clicked.connect(self.show_weather)
        self.toolbar.addWidget(self.weather_button)

        #map button
        self.map_button = self.create_tool_button(":/resources/qt_icons/map_black.svg", "Maps")
        self.map_button.clicked.connect(self.change_maps)
        self.toolbar.addWidget(self.map_button)
        
        
        spacer_widget = QWidget()
        spacer_layout = QVBoxLayout(spacer_widget)
        spacer_layout.setContentsMargins(0, 0, 0, 0)  # Optional: to remove any margins
        spacer_layout.addItem(QSpacerItem(30, 300, QSizePolicy.Expanding, QSizePolicy.Minimum))        
        self.toolbar.addWidget(spacer_widget)
        
        #light theme button
        self.light_button = self.create_tool_button(":/resources/qt_icons/sun_black.svg", "Light")
        self.light_button.clicked.connect(self.change_dark)
        self.toolbar.addWidget(self.light_button)
        
        #dark theme button
        self.dark_button = self.create_tool_button(":/resources/qt_icons/moon.svg", "Dark")
        self.dark_button.clicked.connect(self.change_light)
        self.toolbar.addWidget(self.dark_button)

        # Toggle dock button
        # self.toggle_dock_button = QToolButton()
        # self.toggle_dock_button.setIcon(QIcon(os.path.join("qt_icons/toggle_icon.svg")))
        # self.toggle_dock_button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        # self.toggle_dock_button.setToolTip("Toggle Dock Widget")
        # #self.toggle_dock_button.clicked.connect(self.toggle_dock_widget)
        # self.toolbar.addWidget(self.toggle_dock_button)


    def setup_map(self,interface):
        nodes_data = {}
        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)

        if not self.node_ids:
            print("No nodes found in the mesh network.")
        else:
            for node_id in self.node_ids:
                if node_id in interface.nodes:
                    current_node = interface.nodes[node_id]
                    position_data = current_node.get("position", {})

                    latitude = position_data.get("latitude")
                    longitude = position_data.get("longitude")
                    user_info = current_node.get("user", {})
                    short_name = user_info.get("shortName")

                    if latitude is not None and longitude is not None:
                        print(
                            f"Node ID: {node_id}, Latitude: {latitude}, Longitude: {longitude}, Short Name: {short_name}")
                        nodes_data[node_id] = (latitude, longitude, short_name)
                    else:
                        print(f"No position information available for node with ID '{node_id}'")
                else:
                    print(f"Node with ID '{node_id}' not found in the mesh network.")

        nodes_js_data = ""
        for node_id, (latitude, longitude, short_name) in nodes_data.items():
            nodes_js_data += f"L.marker([{latitude}, {longitude}]).addTo(map).bindPopup('{short_name}');"

        #print(f"{nodes_js_data} +IOIO")

        # Read HTML content from file
        # with open('sigtrack/models/chat/resources/maps/lora_map.html', 'r') as file:
        # # with open(':/lora', 'r') as file:
        #     html_content = file.read()
        
        # # Replace placeholder with actual node data
        # html_contents = html_content.replace("{nodes_js_data}", nodes_js_data)
        # self.web_view.setHtml(html_contents)
        file = QFile(":/lora")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            html_content = stream.readAll()
            file.close()
            
            # Replace placeholder with actual node data
            html_contents = html_content.replace("{nodes_js_data}", nodes_js_data)
            self.web_view.setHtml(html_contents)
        else:
            print("Error: Could not open resource file ':lora'")
    
   
#     def get_file_path(relative_path):
#         """ Get the correct file path for PyInstaller compatibility """
#         if getattr(sys, 'frozen', False):  # Running as EXE
#             base_path = sys._MEIPASS
#         else:
#             base_path = os.path.abspath(os.path.dirname(__file__))
        
#         return os.path.join(base_path, relative_path)

# html_file_path = get_file_path("sigtrack/models/chat/resources/maps/lora_map.html")
    def show_weather(self):
        self.scroll_area3 = QScrollArea()
        self.scroll_area3.setWidgetResizable(True)
        self.weather_info = WeatherApp()
        self.scroll_area3.setWidget(self.weather_info)
        self.weatherDock_widget.setWidget(self.scroll_area3)
        if self.weatherDock_widget.isHidden():
            self.weatherDock_widget.show()
        else:
            self.weatherDock_widget.hide()


    
    def create_tool_button(self, icon_path, text):
        button = QToolButton()
        button.setIcon(QIcon(icon_path))
        button.setText(text)
        button.setToolTip(text)
        button.setIconSize(QSize(100, 100))
        button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        #button.setToolButtonStyle(Qt.AlignCenter)
    
        return button

    def show_chat_interface(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.chat_interface = MeshtasticChatInterface(interface,self.model)
        self.scroll_area.setWidget(self.chat_interface)
        self.messageDock_widget.setWidget(self.scroll_area)
        
        if self.messageDock_widget.isHidden():
            self.messageDock_widget.show()
        else:
            self.messageDock_widget.hide()
            
    def change_light(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #212529;
            }                
            """)
        self.toolbar.setFixedWidth(50)
        #self.toolbar.setStyleSheet("background-color: #212529;") #dark
        # self.toolbar.setStyleSheet("""
        #       QToolBar{
        #         background-color: none;
        #         border: none;
        #         padding:4px;
        #         spacing:10px;
        #         max-width: 100px; /* Limit button width */
                
                
        #     }         
        #     """)
        self.chat_button.setIcon(QIcon(":/resources/qt_icons/message_white.svg"))
        self.symbol_button.setIcon(QIcon(":/resources/qt_icons/symbol_white.svg"))
        self.peers_button.setIcon(QIcon(":/resources/qt_icons/peer_white.svg"))
        self.weather_button.setIcon(QIcon(":/resources/qt_icons/weather_white.svg"))
        self.map_button.setIcon(QIcon(":/resources/qt_icons/map_white.svg"))
        self.light_button.setIcon(QIcon(":/resources/qt_icons/sun_white.svg"))
        self.dark_button.setIcon(QIcon(":/resources/qt_icons/moon_white.svg"))
        #self.messageDock_widget.setStyleSheet("background-color: #212529;")
        self.messageDock_widget.setStyleSheet("""
            QWidget{
                background-color: #212529;
                }
            QDockWidget::title {
                
                color: white; /* White text color */
                padding: 5px; /* Padding in title bar */
            }
                
            
             """)
        self.chat_interface.chat_display.setStyleSheet("""
            QListWidget{
                color:white;
            }                                            
                                                       
            QListWidget::item {
                background-color:#212529; /*white*/
                color: white;
                border-bottom: 1px solid #dcdcdc; /*light gray*/
                text-align: center;
                padding: 10px;
                
            QLineEdit {
                background-color: #ffffff;  /* White background */
                color: white;  
                 }
                                                       
         """)
        
        
        self.natoDock_widget.setStyleSheet("background-color: #212529;")
        self.peersDock_widget.setStyleSheet("background-color: #212529;")
        self.peer_table.table_widget.setStyleSheet("""
            QTableWidget { 
                background-color: #212529;  /* Set table background color */
                color: white;              /* Set text color to white */
                gridline-color: white;     /* Set gridline color to white */
            }
            QHeaderView::section {
                background-color: gray;    /* Set header background color */
                color: white;              /* Set header text color */
            }
        """
            
        )
        self.symbol_manager.tab_widget.setStyleSheet("""
            QTabWidget{
                background-color:  #212529;
                padding: 5px;
            }
             QTabBar::tab {
                background: #212529;
                
                padding: 10px;
                margin: 3px;
                color: white;
            }
            
            QTabBar::tab:selected {
                background-color: gray;
                color: white;
            }
            
            """)
        
        self.weather_info.setStyleSheet("background-color: #212529;")
        self.weatherDock_widget.setStyleSheet("background-color: #212529;")
        self.mapDock_widget.setStyleSheet("background-color: #212529;")
       
        self.switch_map.setStyleSheet("""
            QWidget {
                background-color: #212529;
            }
            QRadioButton {
                color: white;
            }
        """)
        
        
        
    def change_dark(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #D3D3D3;
            }                
                           """)
        
        self.toolbar.setFixedWidth(50)
        #self.toolbar.setStyleSheet("background-color: #D3D3D3;") #grey
        # self.toolbar.setStyleSheet("""
        #      QToolBar{
        #         background-color: none;
        #         border: none;
        #         padding:4px;
        #         spacing:10px;
        #         max-width: 100px; /* Limit button width */
                
                
        #     }         
        #     """)
        
        self.chat_button.setIcon(QIcon(":/resources/qt_icons/message_black.svg"))
        self.symbol_button.setIcon(QIcon(":/resources/qt_icons/symbol_black.svg"))
        self.peers_button.setIcon(QIcon(":/resources/qt_icons/peer_black.svg"))
        self.weather_button.setIcon(QIcon(":/resources/qt_icons/weather_black.svg"))
        self.map_button.setIcon(QIcon(":/resources/qt_icons/map_black.svg"))
        self.light_button.setIcon(QIcon(":/resources/qt_icons/sun_black.svg"))
        self.dark_button.setIcon(QIcon(":/resources/qt_icons/moon.svg"))
        self.messageDock_widget.setStyleSheet("background-color: #D3D3D3;")
        
        # self.chat_interface.chat_display.setStyleSheet("""
        #     QListWidget{
        #         color:black;
        #     }                                            
                                                       
        #     QListWidget::item {
        #         background-color:#212529; /*white*/
        #         color: white;
        #         border-bottom: 1px solid white; 
        #         text-align: center;
        #         padding: 10px;
                                                       
        #  """)
        
        self.chat_interface.chat_display.setStyleSheet('''
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
                                      
                                                               
                    
            QListWidget::item:last {
                border-bottom: none;
                border-radius: 20px;                                
            }
            
            QLineEdit {
                background-color: #ffffff;  /* White background */
                color: #000000;  /* Black text */
                
            }

                ''')
        
        
        
        self.natoDock_widget.setStyleSheet("background-color: #D3D3D3;")
        self.peersDock_widget.setStyleSheet("background-color: #D3D3D3;")
        self.peer_table.table_widget.setStyleSheet("""
            QTableWidget { 
                background-color: #D3D3D3;  /* Set table background color */
                color: black;              /* Set text color to black */
                gridline-color: black;     /* Set gridline color to black */
            }
            QHeaderView::section {
                background-color: gray;    /* Set header background color */
                color: black;              /* Set header text color */
            }
        """     
        )
        
        self.symbol_manager.tab_widget.setStyleSheet("""
            QTabWidget{
                background-color:  #D3D3D3;
                padding: 5px;
            }
             QTabBar::tab {
                background: #D3D3D3;
           
                padding: 10px;
                margin: 3px;
                color: black;
            }
            
            QTabBar::tab:selected {
                background-color: white;
                color: black;
            }
            
            """)
        
        
        self.weatherDock_widget.setStyleSheet("background-color: #D3D3D3;")
        #self.mapDock_widget.setStyleSheet("background-color: #212529;")
       
        self.switch_map.setStyleSheet("""
            QWidget {
                background-color: #212529;
            }
            QRadioButton {
                color: white;
            }
        """)
        
        #self.weatherDock_widget.setStyleSheet("background-color: #D3D3D3;")
        self.mapDock_widget.setStyleSheet("background-color: #D3D3D3;")
        
        
        self.switch_map.setStyleSheet("""
            QWidget {
                background-color: #D3D3D3;
            }
            QRadioButton {
                color: black;
            }
        """)
        
        

    
    def show_symbol_manager(self):
        self.symbol_manager = SymbolManager()
        self.natoDock_widget.setWidget(self.symbol_manager)
        if self.natoDock_widget.isHidden():
            self.natoDock_widget.show()
        else:
            self.natoDock_widget.hide()
        

    def show_peers(self):
        self.scroll_area2 = QScrollArea()
        self.scroll_area2.setWidgetResizable(True)
        self.peer_table = Peers(interface,self.model)
        
        self.scroll_area2.setWidget(self.peer_table)
        self.peersDock_widget.setWidget(self.scroll_area2)
        # self.peersDock_widget.setWidget(self.peer_table)
        if self.peersDock_widget.isHidden():
            self.peersDock_widget.show()
        else:
            self.peersDock_widget.hide()
            
    @Slot()
    def change_maps(self):
        self.switch_map = MapChanger()
        self.switch_map.map_changed.connect(self.update_map)  # Connect signal to slot
        #self.setCentralWidget(self.switch_map)
        self.mapDock_widget.setWidget(self.switch_map)
        if self.mapDock_widget.isHidden():
            self.mapDock_widget.show()
        else:
            self.mapDock_widget.hide()
            
    @Slot()
    def update_map(self, map_type):
        if map_type == 'mapbox':
            self.load_mapbox_map(interface)
        elif map_type == 'leaflet':
            self.load_leaflet_map(interface)
        elif map_type == 'google':
            self.load_google_map(interface)    
            
    @Slot()
    def load_mapbox_map(self, interface):
        nodes_data = {}

        if not self.node_ids:
            print("No nodes found in the mesh network.")
        else:
            for node_id in self.node_ids:
                if node_id in interface.nodes:
                    current_node = interface.nodes[node_id]
                    position_data = current_node.get("position", {})

                    latitude = position_data.get("latitude")
                    longitude = position_data.get("longitude")

                    user_info = current_node.get("user", {})
                    short_name = user_info.get("shortName")

                    if latitude is not None and longitude is not None:
                        print(
                            f"Node ID: {node_id}, Latitude: {latitude}, Longitude: {longitude}, Short Name: {short_name}")
                        nodes_data[node_id] = (latitude, longitude, short_name)
                    else:
                        print(f"No position information available for node with ID '{node_id}'")
                else:
                    print(f"Node with ID '{node_id}' not found in the mesh network.")

        nodes_js_data = ""
        for node_id, (latitude, longitude, short_name) in nodes_data.items():
            nodes_js_data += f"new mapboxgl.Marker().setLngLat([{longitude}, {latitude}]).addTo(map).setPopup(new mapboxgl.Popup().setText('{short_name}'));"

        # # Read HTML content from file
        # with open('sigtrack/models/chat/resources/maps/mapbox.html', 'r') as file:
        #     html_content = file.read()

        # # Replace placeholder with actual node data
        # html_content = html_content.replace("{nodes_js_data}", nodes_js_data)

        # self.web_view.setHtml(html_content)
        file = QFile(":/mapbox")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            html_content = stream.readAll()
            file.close()
            
            # Replace placeholder with actual node data
            html_contents = html_content.replace("{nodes_js_data}", nodes_js_data)
            self.web_view.setHtml(html_contents)
        else:
            print("Error: Could not open resource file ':lora'")
        
    @Slot()
    def load_google_map(self, interface):
        nodes_data = {}
        
        if not self.node_ids:
            print("No nodes found in the mesh network.")
        else:
            for node_id in self.node_ids:
                if node_id in interface.nodes:
                    current_node = interface.nodes[node_id]
                    position_data = current_node.get("position", {})

                    latitude = position_data.get("latitude")
                    longitude = position_data.get("longitude")
                    user_info = current_node.get("user", {})
                    short_name = user_info.get("shortName")

                    if latitude is not None and longitude is not None:
                        print(
                            f"Node ID: {node_id}, Latitude: {latitude}, Longitude: {longitude}, Short Name: {short_name}")
                        nodes_data[node_id] = (latitude, longitude, short_name)
                    else:
                        print(f"No position information available for node with ID '{node_id}'")
                else:
                    print(f"Node with ID '{node_id}' not found in the mesh network.")

        nodes_js_data = ""
        for node_id, (latitude, longitude, short_name) in nodes_data.items():
            nodes_js_data +=f"new google.maps.Marker({{position: {{lat: {latitude}, lng: {longitude}}}, map: map, title: '{short_name}'}});\n"
            
        # with open('sigtrack/models/chat/resources/maps/google_map.html', 'r') as file:
        #     html_content = file.read()
        #     self.web_view.setHtml(html_content)
        file = QFile(":/google")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            html_content = stream.readAll()
            file.close()
            
            # Replace placeholder with actual node data
            html_contents = html_content.replace("{nodes_js_data}", nodes_js_data)
            self.web_view.setHtml(html_contents)
        else:
            print("Error: Could not open resource file ':lora'")
            
    @Slot()
    def load_leaflet_map(self, interface):
        nodes_data = {}

        if not self.node_ids:
            print("No nodes found in the mesh network.")
        else:
            for node_id in self.node_ids:
                if node_id in interface.nodes:
                    current_node = interface.nodes[node_id]
                    position_data = current_node.get("position", {})

                    latitude = position_data.get("latitude")
                    longitude = position_data.get("longitude")
                    user_info = current_node.get("user", {})
                    short_name = user_info.get("shortName")

                    if latitude is not None and longitude is not None:
                        print(
                            f"Node ID: {node_id}, Latitude: {latitude}, Longitude: {longitude}, Short Name: {short_name}")
                        nodes_data[node_id] = (latitude, longitude, short_name)
                    else:
                        print(f"No position information available for node with ID '{node_id}'")
                else:
                    print(f"Node with ID '{node_id}' not found in the mesh network.")

        nodes_js_data = ""
        for node_id, (latitude, longitude, short_name) in nodes_data.items():
            nodes_js_data += f"L.marker([{latitude}, {longitude}]).addTo(map).bindPopup('{short_name}');"

        # # Read HTML content from file
        # with open('sigtrack/models/chat/resources/maps/lora_map.html', 'r') as file:
        #     html_content = file.read()

        # # Replace placeholder with actual node data
        # html_content = html_content.replace("{nodes_js_data}", nodes_js_data)

        # self.web_view.setHtml(html_content)
        file = QFile(":/lora")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            html_content = stream.readAll()
            file.close()
            
            # Replace placeholder with actual node data
            html_contents = html_content.replace("{nodes_js_data}", nodes_js_data)
            self.web_view.setHtml(html_contents)
        else:
            print("Error: Could not open resource file ':lora'")

    


