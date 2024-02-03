import socket
import threading
from PySide2.QtCore import Signal, QObject

class ChatClient(QObject):
    receivedSignal = Signal(str)
    def __init__(self, host_ip, host_port):
        super().__init__()
        self.host_ip = host_ip
        self.host_port = host_port
        self.encoder = "utf-8"
        self.bytesize = 1024
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client.bind((self.host_ip, self.host_port))
        # self.client.listen(5)
        self.client.connect((self.host_ip, self.host_port))


        # create two threads for sending and receiving
        receive_thread = threading.Thread(target=self.receive_messages)
        # send_thread = threading.Thread(target=self.send_messages)

        # start the threads
        receive_thread.start()
        # send_thread.start()

        # wait for both threads to finish
        # receive_thread.join()
        # send_thread.join()

        # accept incoming connections
        print("Client running...\n")

    # function to handle receiving messages
    def receive_messages(self):
        while True:
            message = self.client.recv(self.bytesize).decode()
            self.receivedSignal.emit(message)

            if message == "close":
                self.client.send("close".encode(self.encoder))
                print("\nMessage closed")
                break
            else:
                print(f"\nSERVER: {message}")
        self.client.close()


    # function to handle sending messages
    def send_messages(self, message: str):
        # self.client, client_address = self.client.accept()
        # message = input(f"{self.client.getsockname()}: ")
        # self.client.send(message.encode(self.encoder))
        # while True:
            # self.client.send("You are connected...\n".encode())
            # message = input(f"{self.client.getsockname()}: ")
            # message = input("SERVER: ")
        self.client.send(message.encode(self.encoder)[:1024])
            # if message == "close":
            #     break
            # self.client.close

        # self.client.close()


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



  