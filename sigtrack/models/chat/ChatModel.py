import socket
import threading
from PySide2.QtCore import Signal, QObject
class ChatClient(QObject):
    receivedSignal = Signal(str)

    def __init__(self, host_ip, host_port, radio_type="LoRa"):
        super().__init__()
        self.host_ip = host_ip
        self.host_port = host_port
        self.radio_type = radio_type
        self.encoder = "utf-8"
        self.bytesize = 1024
        # self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if radio_type == "LoRa":
            self.radio = LoRaRadio(host_ip, host_port)
        elif radio_type == "Silvus":
            self.radio = SilvusRadio(host_ip, host_port)
        # self.client.connect((self.host_ip, self.host_port))
        receive_thread = threading.Thread(target=self.radio.receive_messages)
        receive_thread.start()

    # def receive_messages(self):
    #     while True:
    #         message = self.client.recv(self.bytesize).decode()
    #         self.receivedSignal.emit(message)
    #         if message == "close":
    #             self.client.send("close".encode(self.encoder))
    #             break
    #         else:
    #             print(f"\nSERVER: {message}")
    #     self.client.close()

    def send_messages(self, message: str):
        # self.client.send(message.encode(self.encoder)[:1024])
        self.radio.send_messages(message)

class LoRaRadio(QObject):
    receivedSignal = Signal(str)

    def __init__(self, host_ip, host_port):
        super().__init__()
        """Add LoRa-specific initialization here"""
        self.host_ip = host_ip
        self.host_port = host_port

    def connect():
        """Add LoRa-specific connection logic here"""
        pass

    def receive_messages(self):
        """Add LoRa-specific message receiving logic here"""
        pass

    def send_messages(self, message: str):
        """Add LoRa-specific message sending logic here"""
        pass

class SilvusRadio(QObject):
    receivedSignal = Signal(str)

    def __init__(self, host_ip, host_port):
        super().__init__()
        """Add Silvus-specific initialization here"""
        self.host_ip = host_ip
        self.host_port = host_port

    def connect():
        """Add Silvus-specific connection logic here"""
        pass

    def receive_messages(self):
        """Add Silvus-specific message receiving logic here"""
        pass

    def send_messages(self, message: str):
        """Add Silvus-specific message sending logic here"""
        pass

class ItemModel(QObject):
    itemsChanged = Signal(list)

    def __init__(self):
        super(ItemModel, self).__init__()
        self._items = []

    def get_items(self):
        return self._items
    
    def add_item(self, item):
        self._items.append(item)
        self.itemsChanged.emit(self._items)
  