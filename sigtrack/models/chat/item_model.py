from PySide6.QtCore import QObject, Signal
import sqlite3, time

class ItemModel(QObject):
    itemsChanged = Signal(list)

    def __init__(self):
        super(ItemModel, self).__init__()
        #self._items = []
        self.connection = sqlite3.connect('loraChat2.db')
        
        self.cursor =  self.connection.cursor()

        print("Opened database successfully")

        # Enable foreign key support
        self.cursor.execute("PRAGMA foreign_keys = ON")

        # Creating the 'nodes' Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS nodes (
                    node_id TEXT PRIMARY KEY,
                    short_name TEXT,
                    long_name TEXT,
                    modell TEXT
        );''')

        # Creating the 'sent_messages' Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sent_messages (
                    node_id INTEGER PRIMARY KEY,
                    short_name TEXT,
                    message_content TEXT,
                    sent_at DATE,
                    is_broadcast TEXT,
                    FOREIGN KEY (short_name) REFERENCES nodes(short_name)
        );''')

        # Creating the 'received_messages' Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS received_messages (
                    node_id INTEGER PRIMARY KEY,
                    short_name TEXT,
                    message_content TEXT,
                    received_at DATE,
                    is_broadcast TEXT,
                    FOREIGN KEY (short_name) REFERENCES nodes(short_name)
        )''')

        print("Tables created successfully")

    def add_nodeInfo(self,node_id:str,short_name:str,long_name:str,modell:str):
        self.cursor.execute("INSERT into nodes (node_id, short_name,long_name,modell) VALUES (?,?,?,?)", (node_id,short_name,long_name, modell))
        self.connection.commit()
        # cursor  = self.cursor.execute("SELECT node_id, short_name, long_name, modell from nodes")
        # print(cursor)

    # def add_message(self, short_name, message):
    #     timestamp = int(time.time())  # Current timestamp
    #     self.c.execute("INSERT INTO messages (sender, message, timestamp) VALUES (?, ?, ?)", (sender, message, timestamp))
    #     self.conn.commit()

    def add_sent_message(self, sender:str, message:str):
        timestamp = int(time.time())  # Current timestamp
        self.cursor.execute("INSERT INTO sent_messages (node_id, message_content, sent_at) VALUES (?, ?, ?)", (sender, message, timestamp))
        self.conn.commit()

    def add_receive_message(self, receiver:str, message:str):
        timestamp = int(time.time())  # Current timestamp
        self.cursor.execute("INSERT INTO received_messages (node_id, message_content, received_at) VALUES (?, ?, ?)", (receiver, message, timestamp))
        self.conn.commit()

    # def delete_messages(self, task: str) -> None:
    #     self.cursor.execute("delete from loraChat where title = ?", (task,))
    #     self.connection.commit()

    # def get_message(self) -> list[str]:
    #     tasks: list[str] = []
    #     for row in self.cursor.execute("select title from tasks"):
    #         tasks.append(row[0])
    #     return tasks



    # def get_items(self):
    #     return self._items

    # def add_item(self, item):
    #     self._items.append(item)
    #     self.itemsChanged.emit(self._items)
    