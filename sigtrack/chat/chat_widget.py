# -*- coding: utf-8 -*-
# Author: Jude Boachie
# (with ai-generated code)

"""
NOTE
1. I created this as a widget so that it can be embedded somewhere else
in the software (probably in a dock widget)

In a production environment, it is recommended to use a backend service
to securely handle sensitive information like API keys.

The desktop application should communicate with this backend service,
which will perform operations like authentication and database interactions with Firebase.

This ensures that sensitive credentials are not exposed to the end user,
adding an extra layer of security.

TODO
Will be discussing and building this next.
GitGuardian is going to be so pissed when I commit this code :D

- Jude
"""


import sys
import time
import uuid
import requests # type:ignore
import threading
import sigtrack.chat.firebase_config as firebase_config

from firebase_admin import firestore  # type:ignore
from sigtrack.chat.type_definitions import Message, Session

from PySide6.QtCore import Signal, QObject, Qt, QTimer
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QLineEdit,
    QTabWidget,
    QScrollArea,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QApplication,
    QStackedLayout,
)


class MessagePoller(QObject):
    new_message = Signal(dict)  # Signal to notify when new messages are fetched

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.running = False
        self.last_timestamp = None

    def start_polling(self):
        """Start the polling thread."""
        self.running = True
        self.poll_thread = threading.Thread(target=self.poll_messages)
        self.poll_thread.start()

    def stop_polling(self):
        """Stop the polling thread."""
        self.running = False
        if self.poll_thread.is_alive():
            self.poll_thread.join()

    def poll_messages(self):
        """Poll Firestore for new messages in a separate thread."""
        while self.running:
            query = self.db.collection("messages").order_by("timestamp")

            # Fetch messages after the last timestamp
            if self.last_timestamp:
                query = query.start_after({"timestamp": self.last_timestamp})

            messages = query.stream()
            for message in messages:
                data = message.to_dict()
                self.last_timestamp = data["timestamp"]
                self.new_message.emit(data)

            time.sleep(0.25)  # Poll every 0.25 seconds


class FirebaseAuth:
    """Handles Firebase Authentication using REST API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.user = None
        self.id_token: str | None = None

    def sign_up(self, email: str, password: str, display_name: str) -> bool:
        """Sign up a new user with Firebase."""
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.api_key}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True,
            "displayName": display_name,
        }
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            response_data = response.json()
            session_data = {
                "displayName": response_data.get("displayName", ""),
                "email": response_data.get("email", ""),
                "expiresIn": int(response_data.get("expiresIn", 0)),
                "idToken": response_data.get("idToken", ""),
                "kind": response_data.get("kind", ""),
                "localId": response_data.get("localId", ""),
                "refreshToken": response_data.get("refreshToken", ""),
                "registered": response_data.get("registered", None),  # Default to None if missing
            }
            self.session = Session(**session_data)
            self.id_token = self.session.idToken
            return True
        else:
            print("Sign-up failed:", response.json().get("error", {}).get("message", "Unknown error"))
            return False

    def login(self, email: str, password: str) -> bool:
        """Authenticate user with Firebase."""
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}"
        payload = {"email": email, "password": password, "returnSecureToken": True}
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            self.session = Session(**(response.json()))
            self.id_token = self.session.idToken
            return True
        else:
            print("Login failed:", response.json().get("error", {}).get("message", "Unknown error"))
            return False


class LoginWidget(QWidget):
    """Login and Sign-Up screen for Firebase authentication."""

    authenticated = Signal(str)  # Emits user email after successful authentication

    def __init__(self, auth_manager: FirebaseAuth):
        super().__init__()
        self.auth_manager = auth_manager

        tab_widget = QTabWidget(self)
        tab_widget.setStyleSheet("""
            QTabWidget::tab-bar {
                alignment: center;
            }
        """)
        layout = QVBoxLayout(self)
        layout.addWidget(tab_widget)

        self.login_tab = self.create_login_tab()
        self.sign_up_tab = self.create_sign_up_tab()

        tab_widget.addTab(self.login_tab, "Login")
        tab_widget.addTab(self.sign_up_tab, "Sign Up")

    def create_login_tab(self):
        """Create the login tab."""
        login_tab = QWidget()
        layout = QVBoxLayout(login_tab)

        self.email_input_login = QLineEdit(self)
        self.email_input_login.setPlaceholderText("Enter email")
        layout.addWidget(self.email_input_login)

        self.password_input_login = QLineEdit(self)
        self.password_input_login.setPlaceholderText("Enter password")
        self.password_input_login.setEchoMode(QLineEdit.Password)  # type:ignore
        layout.addWidget(self.password_input_login)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.login_status_label = QLabel("")
        layout.addWidget(self.login_status_label)

        return login_tab

    def create_sign_up_tab(self):
        """Create the sign-up tab."""
        sign_up_tab = QWidget()
        layout = QVBoxLayout(sign_up_tab)

        self.email_input_signup = QLineEdit(self)
        self.email_input_signup.setPlaceholderText("Enter email")
        layout.addWidget(self.email_input_signup)

        self.password_input_signup = QLineEdit(self)
        self.password_input_signup.setPlaceholderText("Enter password")
        self.password_input_signup.setEchoMode(QLineEdit.Password)  # type:ignore
        layout.addWidget(self.password_input_signup)

        self.callsign_input_signup = QLineEdit(self)
        self.callsign_input_signup.setPlaceholderText("Enter callsign")
        layout.addWidget(self.callsign_input_signup)

        self.sign_up_button = QPushButton("Sign Up")
        self.sign_up_button.clicked.connect(self.sign_up)
        layout.addWidget(self.sign_up_button)

        self.sign_up_status_label = QLabel("")
        layout.addWidget(self.sign_up_status_label)

        return sign_up_tab

    def login(self):
        """Attempt to authenticate the user."""
        email = self.email_input_login.text().strip()
        password = self.password_input_login.text().strip()
        if self.auth_manager.login(email, password):
            self.authenticated.emit(email)
        else:
            self.login_status_label.setText("Invalid credentials. Please try again.")

    def sign_up(self):
        """Attempt to register a new user."""
        email = self.email_input_signup.text().strip()
        password = self.password_input_signup.text().strip()
        callsign = self.callsign_input_signup.text().strip()

        if not callsign:
            self.sign_up_status_label.setText("Please provide a callsign for sign-up.")
            return

        if self.auth_manager.sign_up(email, password, callsign):
            self.sign_up_status_label.setText("Sign-up successful! You can now log in.")
        else:
            self.sign_up_status_label.setText("Sign-up failed. Please try again.")

class ChatInterface(QWidget):
    def __init__(self, db, user_email: str):
        super().__init__()
        self.setWindowTitle(f"Chat - Logged in as {user_email}")
        self.db = db
        self.user_email = user_email

        main_layout = QVBoxLayout(self)

        # Scrollable area for messages
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: 0px solid;
                border-radius: 6px;
            }
        """)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_content = QWidget(self)
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_content)
        self.scroll_area_layout.setAlignment(Qt.AlignTop)  # type:ignore
        self.scroll_area.setWidget(self.scroll_area_content)
        main_layout.addWidget(self.scroll_area)

        # Message input area
        input_layout = QHBoxLayout()
        self.message_input = QLineEdit(self)
        self.message_input.setPlaceholderText("Type a message...")
        input_layout.addWidget(self.message_input)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        main_layout.addLayout(input_layout)

        # Poll messages
        self.poller = MessagePoller(self.db)
        self.poller.new_message.connect(self.display_message_from_data)
        self.poller.start_polling()
        self.destroyed.connect(self.poller.stop_polling)

    def display_message_from_data(self, data: dict):
        """Render a new message as a custom widget."""
        message_widget = self.create_message_widget(data)
        self.scroll_area_layout.addWidget(message_widget)
        QTimer.singleShot(0, lambda: self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum()))
        # self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    def create_message_widget(self, data: dict) -> QWidget:
        """Create a custom widget for a message."""
        display_name = data.get("displayName", data.get('senderID'))
        content = data.get("text", "")

        timestamp = data.get("timestamp")
        timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S") if timestamp else "Unknown time"

        # Create a container widget for the message
        message_widget = QWidget(self)
        layout = QVBoxLayout(message_widget)

        # Display name and timestamp
        header_label = QLabel(f"<small><b>{display_name}</b></small>", self)
        layout.addWidget(header_label)

        # Message content
        content_label = QLabel(content, self)
        content_label.setWordWrap(True)
        layout.addWidget(content_label)

        time_label = QLabel(f"<small>{timestamp_str}</small>", self)
        layout.addWidget(time_label, alignment=Qt.AlignRight) # type:ignore

        # Style the message widget
        message_widget.setStyleSheet("""
            QWidget {
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 0px;
                background-color: #f9f9f9;
            }

            QLabel {
                border: 0px solid;
            }
        """)
        header_label.setStyleSheet("""
            QLabel {
                color: #666;
            }
        """)
        time_label.setStyleSheet("""
            QLabel {
                color: #666;
            }
        """)
        # layout.setContentsMargins(5, 5, 5, 5)

        return message_widget

    def send_message(self) -> None:
        """Send a message to Firestore."""
        message_content = self.message_input.text().strip()
        if message_content:
            message_data: Message = Message(
                containsImage=False,
                containsText=True,
                senderID=firebase_auth.session.displayName,
                messageID=str(uuid.uuid4()),
                text=message_content,
                video=None,
                image=None,
                timestamp=firestore.SERVER_TIMESTAMP
            )
            self.db.collection("messages").add(message_data.__dict__)
            self.message_input.clear()

class ChatWidget(QWidget):
    """Main application with login and chat widgets."""

    def __init__(self, firebase_auth: FirebaseAuth, db):
        super().__init__()
        self.setWindowTitle("Chat Widget")

        self.firebase_auth = firebase_auth
        self.db = db

        # Apply custom styles
        self.setStyleSheet("""
            QWidget {
                font-family: 'Inter', sans-serif;
                font-size: 14px;
            }
            QLineEdit, QPushButton {
                font-size: 14px;
            }
            QPushButton {
                background-color: #0078D4;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
            QPushButton:pressed {
                background-color: #003A6B;
            }
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            QLabel {
                color: #333;
            }
        """)

        self.baseLayout = QStackedLayout(self)
        self.login_widget = LoginWidget(self.firebase_auth)
        self.login_widget.authenticated.connect(self.show_chat_interface)
        self.baseLayout.addWidget(self.login_widget)

    def show_chat_interface(self, user_email: str):
        """Switch to the chat widget after successful login."""
        chat_interface = ChatInterface(self.db, user_email)
        self.baseLayout.addWidget(chat_interface)
        self.baseLayout.setCurrentWidget(chat_interface)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    firebase_auth = FirebaseAuth(firebase_config.firebase_config['apiKey'])
    window = ChatWidget(firebase_auth, firebase_config.db)
    window.resize(400, 500)
    window.show()
    sys.exit(app.exec())
