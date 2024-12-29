from PySide6.QtWidgets import (QMainWindow, QDockWidget,
                               QToolButton, QToolBar,QScrollArea)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWebEngineWidgets import QWebEngineView
from meshtastic import serial_interface
from sigtrack.models.chat.item_model import ItemModel
from sigtrack.models.chat.peers import Peers
from sigtrack.models.chat.meshstatic_chat_interface import MeshtasticChatInterface
from sigtrack.models.chat.modules.symbols import SymbolManager
from sigtrack.models.chat.modules.weather import WeatherApp
import sigtrack.models.chat.qt_icons_rc
import os




class MapDisplay(QMainWindow):
    def __init__(self):
        super().__init__()
        #TODO: if anything.db in current dir remove it @serkhani
        interface = serial_interface.SerialInterface()
        self.node_ids = list(interface.nodes.keys())
        
        self.setWindowTitle("Map Application")
        self.setGeometry(100, 100, 1400, 600)
        self.setup_map(interface)
        self.setup_toolbar()
        self.symbol_button = QToolButton()
        #self.symbol_manager= SymbolManager()
        self.model = ItemModel()
        
        self.setup_map(interface)

        # Create a dock widget for stacking interfaces
        self.dock_widget = QDockWidget(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)
        self.dock_widget.hide()
        self.chat_interface = MeshtasticChatInterface(interface,self.model)
        self.peer_table = Peers(interface,self.model)
        self.symbol_manager = SymbolManager()
        
        
        
        
        
    def setup_toolbar(self):
        # Create a transparent vertical toolbar on the left side
        self.toolbar = QToolBar()
        self.toolbar.setOrientation(Qt.Vertical)
        self.toolbar.setMovable(True)
        #self.toolbar.setStyleSheet("background-color: red;")
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)

        # Chat button
        self.chat_button = QToolButton()
        self.chat_button.setIcon(QIcon(":/resources/qt_icons/message_icon.ico"))
        self.chat_button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.chat_button.setToolTip("Message")
        self.chat_button.clicked.connect(self.show_chat_interface)
        self.toolbar.addWidget(self.chat_button)

       
        # Symbol button
        self.symbol_button = self.create_tool_button(":/resources/qt_icons/box_icon.svg", "Symbols")
        self.symbol_button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.symbol_button.setToolTip("Symbols")
        self.symbol_button.clicked.connect(self.show_symbol_manager)
        self.toolbar.addWidget(self.symbol_button)

        # Peers button
        self.peers_button = self.create_tool_button(":/resources/qt_icons/people_icon.svg", "Peers")
        self.peers_button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.peers_button.setToolTip("Peers")
        self.peers_button.clicked.connect(self.show_peers)
        self.toolbar.addWidget(self.peers_button)

        # Weather button
        self.weather_button = self.create_tool_button(":/resources/qt_icons/weather_icon.svg", "Weather")
        self.weather_button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.weather_button.setToolTip("Weather")
        self.weather_button.clicked.connect(self.show_weather)
        self.toolbar.addWidget(self.weather_button)


        # Toggle dock button
        self.toggle_dock_button = QToolButton()
        self.toggle_dock_button.setIcon(QIcon(":/resources/qt_icons/toggle_icon.svg"))
        self.toggle_dock_button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.toggle_dock_button.setToolTip("Toggle Dock Widget")
        self.toggle_dock_button.clicked.connect(self.toggle_dock_widget)
        self.toolbar.addWidget(self.toggle_dock_button)


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

        print(f"{nodes_js_data} +IOIO")

        # HTML content of the map
        html_content = """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Leaflet Map with Satellite and Terrain Layers</title>
                <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
                <link rel="stylesheet" href="https://unpkg.com/leaflet-draw/dist/leaflet.draw.css" />
                <style>
                    #map {
                        height: 570px;
                    }
                </style>
                </head>
                <body>

                <div id="map"></div>

                <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
                <script src="https://unpkg.com/leaflet-draw/dist/leaflet.draw.js"></script>
                <script>
                var map = L.map('map').setView([5.590039, -0.156270], 13);

                // Satellite layer
                var satelliteLayer = L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
                    maxZoom: 20,
                    subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
                }).addTo(map);

                // Terrain layer
                var terrainLayer = L.tileLayer('https://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}', {
                maxZoom: 20,
                subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
                }).addTo(map);

                var satelliteOceanLayer = L.tileLayer('https://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', {
                    maxZoom: 20,
                    subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
                }).addTo(map);

                  // OSM layer
                var osmLayer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 20,
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                }).addTo(map); 

                // Feature group for drawn items
                var drawnItems = new L.FeatureGroup().addTo(map);
                
                // Feature group for nodes
                var nodes = new L.FeatureGroup().addTo(map);

                // Drawing tools
                var drawControl = new L.Control.Draw({
                    edit: {
                    featureGroup: drawnItems
                }
                });
                map.addControl(drawControl);

                // Layers control
                var baseLayers = {
                    "Satellite": satelliteLayer,
                    "Terrain": terrainLayer,
                    "Hybrid":satelliteOceanLayer,
                    "OSM": osmLayer 
                };
                
                
                var overlays = {
                    "Drawn Items": drawnItems,
                    "Nodes": nodes
                };

                L.control.layers(baseLayers, overlays).addTo(map);



                // Plotting nodes
                {nodes_js_data}

                </script>

                </body>
                </html>
                """

        html_contents = html_content.replace("{nodes_js_data}", nodes_js_data)
        self.web_view.setHtml(html_contents)

    
    def toggle_dock_widget(self):
        if self.dock_widget.isHidden():
            self.dock_widget.show()
        else:
            self.dock_widget.hide()

    def show_weather(self):
        self.weather_info = WeatherApp()
        self.dock_widget.setWidget(self.weather_info)


    
    def create_tool_button(self, icon_path, text):
        button = QToolButton()
        button.setIcon(QIcon(icon_path))
        button.setText(text)
        button.setIconSize(QSize(50, 50))
        button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        return button

    def show_chat_interface(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.chat_interface)
        self.dock_widget.setWidget(self.scroll_area)

    
    def show_symbol_manager(self):
        self.dock_widget.setWidget(self.symbol_manager)
        

    def show_peers(self):
        #self.peer_table = self.model
        self.dock_widget.setWidget(self.peer_table)
