from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import (QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QWidget, QRadioButton, QComboBox)
import cv2
import threading
import socket
import pickle
import struct
import os


class StreamingObject(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(800, 600)

        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        # Your Video Label
        self.yourVideoLabel = QtWidgets.QLabel(self.dockWidgetContents)
        self.yourVideoLabel.setText("Your Video")
        self.yourVideoLabel.setObjectName("yourVideoLabel")
        self.yourVideoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.yourVideoLabel.setStyleSheet("font-size: 16px; background-color: lightgray;")
        self.horizontalLayout_3.addWidget(self.yourVideoLabel)

        # Vertical Line Separator
        self.line = QFrame(self.dockWidgetContents)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.horizontalLayout_3.addWidget(self.line)

        # Received Video Label
        self.receivedVideoLabel = QtWidgets.QLabel(self.dockWidgetContents)
        self.receivedVideoLabel.setText("Received Video")
        self.receivedVideoLabel.setObjectName("receivedVideoLabel")
        self.receivedVideoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.receivedVideoLabel.setStyleSheet("font-size: 16px; background-color: lightgray;")
        self.horizontalLayout_3.addWidget(self.receivedVideoLabel)

        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 2)

        # Layout for IP and USB devices
        self.bottomLayout = QVBoxLayout()

        # IP Address Layout
        self.ip_horizontal_layout = QHBoxLayout()
        self.ip_label = QLabel(self.dockWidgetContents)
        self.ip_label.setText("IP Address:")
        self.ip_label.setStyleSheet("font-size: 14px;")
        self.ip_horizontal_layout.addWidget(self.ip_label)
        self.ip_textbox = QLineEdit(self.dockWidgetContents)
        self.ip_textbox.setFixedWidth(200)  # Fixed width for IP address
        self.ip_horizontal_layout.addWidget(self.ip_textbox)
        self.bottomLayout.addLayout(self.ip_horizontal_layout)

        # Radio Button Layout
        self.radio_layout = QHBoxLayout()
        self.usb_radio = QRadioButton("USB", self.dockWidgetContents)
        self.network_radio = QRadioButton("Network", self.dockWidgetContents)
        self.usb_radio.setStyleSheet("font-size: 14px;")
        self.network_radio.setStyleSheet("font-size: 14px;")
        self.radio_layout.addWidget(self.usb_radio)
        self.radio_layout.addWidget(self.network_radio)
        self.bottomLayout.addLayout(self.radio_layout)

        # USB Device Selector
        self.usbDeviceLabel = QLabel("USB Devices:")
        self.usbDeviceComboBox = QComboBox()
        self.populate_usb_devices()  # Always populate the list
        self.usbDeviceComboBox.setEnabled(True)  # Always enabled to show even if no devices are found.

        usbLayout = QVBoxLayout()
        usbLayout.addWidget(self.usbDeviceLabel)
        usbLayout.addWidget(self.usbDeviceComboBox)
        self.bottomLayout.addLayout(usbLayout)

        # Button Layout
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.start_button = QPushButton(self.dockWidgetContents)
        self.start_button.setObjectName("start_button")
        self.start_button.setStyleSheet("font-size: 14px;")
        self.start_button.clicked.connect(self.start_stream)
        self.horizontalLayout_2.addWidget(self.start_button)
        self.stop_button = QPushButton(self.dockWidgetContents)
        self.stop_button.setObjectName("stop_button")
        self.stop_button.setStyleSheet("font-size: 14px;")
        self.stop_button.clicked.connect(self.stop_stream)
        self.horizontalLayout_2.addWidget(self.stop_button)

        # Additional buttons
        self.share_button = QPushButton(self.dockWidgetContents)
        self.share_button.setObjectName("share_button")
        self.share_button.setText("Share Stream")
        self.share_button.clicked.connect(self.share_stream)
        self.horizontalLayout_2.addWidget(self.share_button)

        self.receive_button = QPushButton(self.dockWidgetContents)
        self.receive_button.setObjectName("receive_button")
        self.receive_button.setText("Receive Stream")
        self.receive_button.clicked.connect(self.receive_stream)
        self.horizontalLayout_2.addWidget(self.receive_button)

        self.capture_button = QPushButton(self.dockWidgetContents)
        self.capture_button.setObjectName("capture_button")
        self.capture_button.setText("Capture Picture")
        self.capture_button.clicked.connect(self.capture_image)
        self.horizontalLayout_2.addWidget(self.capture_button)

        self.record_button = QPushButton(self.dockWidgetContents)
        self.record_button.setObjectName("record_button")
        self.record_button.setText("Record")
        self.record_button.clicked.connect(self.toggle_recording)
        self.horizontalLayout_2.addWidget(self.record_button)

        self.bottomLayout.addLayout(self.horizontalLayout_2)

        self.gridLayout.addLayout(self.bottomLayout, 1, 0, 1, 2)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        DockWidget.setWidget(self.dockWidgetContents)
        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

        # Variables for video capture and network streaming
        self.capture = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.is_sharing = False
        self.server_thread = None
        self.frame_counter = 0
        self.is_recording = False
        self.out = None

        # Connect the radio button changes to enable/disable USB device dropdown
        self.usb_radio.toggled.connect(self.toggle_usb_dropdown)
        self.network_radio.toggled.connect(self.toggle_usb_dropdown)

    def retranslateUi(self, DockWidget):
        _translate = QtCore.QCoreApplication.translate
        DockWidget.setWindowTitle(_translate("DockWidget", "Stream Controller"))
        self.start_button.setText(_translate("DockWidget", "Start Stream"))
        self.stop_button.setText(_translate("DockWidget", "Stop Stream"))

    def populate_usb_devices(self):
        """Populates the USB device dropdown with available devices."""
        self.usbDeviceComboBox.clear()
        devices_found = False
        for device_index in range(5):  # Assuming up to 5 devices
            capture = cv2.VideoCapture(device_index)
            if capture.isOpened():
                devices_found = True
                self.usbDeviceComboBox.addItem(f"Device {device_index}")
                capture.release()

        if not devices_found:
            self.usbDeviceComboBox.addItem("No devices found")

    def toggle_usb_dropdown(self):
        """Enable or disable the USB dropdown based on the selected option."""
        self.usbDeviceComboBox.setEnabled(self.usb_radio.isChecked())

    def start_stream(self):
        # Reset existing capture
        if self.capture is not None:
            self.capture.release()
            self.capture = None

        # Check if USB or Network option is selected
        if self.usb_radio.isChecked():
            selected_device = self.usbDeviceComboBox.currentText()
            if selected_device != "No devices found":
                # Parse the selected device index
                device_index = int(selected_device.split()[1])
                self.capture = cv2.VideoCapture(device_index)  # Open USB Camera
            else:
                print("Error: No USB device selected.")
                return
        elif self.network_radio.isChecked():
            ip_address = self.ip_textbox.text()
            if ip_address:
                # Form the appropriate network stream URL
                stream_url = f"http://{ip_address}/video"  # Adjust URL format as needed
                self.capture = cv2.VideoCapture(stream_url)
            else:
                print("Error: No IP address provided.")
                return
        else:
            print("Error: No source selected.")
            return

        # Check if the video capture has successfully opened the stream
        if not self.capture or not self.capture.isOpened():
            print("Error: Could not open video stream.")
            self.capture = None  # Set to None explicitly to prevent further issues
            return

        # Start the timer to update frames every 30 ms
        self.timer.start(30)

    def stop_stream(self):
        if self.capture:
            self.capture.release()
            self.capture = None
        if self.is_recording:
            self.toggle_recording()  # Stop recording if active
        self.timer.stop()
        self.yourVideoLabel.clear()

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.resize(frame, (self.yourVideoLabel.width(), self.yourVideoLabel.height()))
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qt_image = QtGui.QImage(rgb_frame.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qt_image)
            self.yourVideoLabel.setPixmap(pixmap)
            if self.is_recording:
                self.out.write(frame)

    def capture_image(self):
        if self.capture and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                os.makedirs("captures", exist_ok=True)
                filename = f"captures/capture_{self.frame_counter}.png"
                cv2.imwrite(filename, frame)
                print(f"Image saved: {filename}")
                self.frame_counter += 1

    def toggle_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.record_button.setText("Record")
            self.out.release()
        else:
            if self.capture and self.capture.isOpened():
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                os.makedirs("recordings", exist_ok=True)
                filename = f"recordings/recording_{self.frame_counter}.avi"
                self.out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
                self.record_button.setText("Stop Recording")
                self.is_recording = True

    def share_stream(self):
        if not self.capture or not self.capture.isOpened():
            print("Start stream before sharing.")
            return
        self.is_sharing = True
        ip = self.ip_textbox.text()
        port = 9999
        threading.Thread(target=self._share_stream_thread, args=(ip, port)).start()

    def _share_stream_thread(self, ip, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((ip, port))
        server_socket.listen(1)
        conn, addr = server_socket.accept()
        print(f"Connected to {addr}")
        while self.is_sharing and self.capture and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                data = pickle.dumps(frame)
                conn.sendall(struct.pack("L", len(data)) + data)
        conn.close()

    def receive_stream(self):
        ip = self.ip_textbox.text()
        port = 9999
        threading.Thread(target=self._receive_stream_thread, args=(ip, port)).start()

    def _receive_stream_thread(self, ip, port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))
        data = b""
        payload_size = struct.calcsize("L")
        while True:
            while len(data) < payload_size:
                data += client_socket.recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_socket.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_image = QtGui.QImage(frame.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(qt_image)
            self.receivedVideoLabel.setPixmap(pixmap)
