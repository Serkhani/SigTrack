from PySide2.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from sigtrack.models.chat.item_model import ItemModel
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
            }
            """
        )
