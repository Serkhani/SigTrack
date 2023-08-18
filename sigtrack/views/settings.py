import sys
import json

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QScrollArea,
    QWidget,
    QPushButton,
    QLineEdit,
)
from PySide6.QtGui import QPalette, QColor
from qt_material import list_themes, apply_stylesheet


class ThemeSelectWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        x, y = parent.width()//2.5 - parent.pos().x(), parent.pos().y() - 50
        self.setGeometry(x, y, 400, 400)
        self.setFixedSize(self.size())
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowSystemMenuHint
            | Qt.WindowTitleHint
            | Qt.WindowMinimizeButtonHint
            | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
        )
        self.settings = self.read_json()
        self.drag_position = None

        self.setStyleSheet("""
            /* Window theme */
            QMainWindow, QScrollArea {
                border: 1px solid black;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #F0F8FF;
            }

            /* Style for transparent buttons */
            QPushButton {
                border: none;
                text-align: left;
                padding: 2px;
                padding-left: 5px;
                border-radius: 5px;
                color: black; /* Text color */
            }
            
            QLineEdit {
                border: 1px solid gray;
                border-radius: 5px;
                padding: 0 8px;
                background: white;
                selection-background-color: #F0F8FF;
            }
        """)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.setPalette(QPalette(QColor("white")))

        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignTop)

        enter_theme = QLineEdit(self)
        enter_theme.setPlaceholderText(" Select colour theme ")
        layout.addWidget(enter_theme)

        # Themes
        scroll_area = QScrollArea(central_widget)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(scroll_area)

        scroll_content = QWidget()
        scroll_content.setPalette(QPalette(QColor("white")))
        scroll_area.setWidget(scroll_content)
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setAlignment(Qt.AlignTop)
        scroll_layout.setSpacing(1)

        self.original_theme = self.styleSheet()
        theme = self.settings["preferences"]["theme"]
        self.themes = list_themes()
        btns = [QPushButton(" ".join(theme[:-4].split("_")).title())
                for theme in self.themes]

        for btn in btns:
            btn.clicked.connect(self.change_theme)
            if btn.text() == theme:
                apply_stylesheet(
                    self, theme.lower().replace(" ", "_") + ".xml")
            scroll_layout.addWidget(btn)

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidgetResizable(True)

        # Reset button
        reset_btn = QPushButton("Reset", self)
        reset_btn.clicked.connect(self.reset_theme)
        reset_btn.setStyleSheet("""
                                background-color: blue;
                                border-radius: 5px; color: white;
                                padding: 5px; margin-top: 5px;
                                margin-bottom: 5px;
                                margin-left: 5px;
                                margin-right: 5px;
                                text-align: center;
                                font: bold 12px;
                                """)
        layout.addWidget(reset_btn)

    def change_theme(self, theme: str) -> bool:
        sender = self.sender()
        theme = sender.text().lower().replace(" ", "_") + ".xml"
        apply_stylesheet(self, theme)
        apply_stylesheet(self.parent, theme)
        self.settings["preferences"]["theme"] = " ".join(
            theme[:-4].split("_")).title()
        self.save_json()
        self.close()
        return True

    def reset_theme(self) -> bool:
        self.settings["preferences"]["theme"] = "Light Blue"
        self.save_json()
        self.setStyleSheet(self.original_theme)
        self.parent.setStyleSheet(self.original_theme)
        self.close()
        return True

    def read_json(self):
        try:
            with open("settings.json", "r") as f:
                return json.load(f)
        except FileNotFoundError as e:
            return e, False

    def save_json(self, ) -> bool:
        with open("settings.json", "w") as f:
            json.dump(self.settings, f, indent=4)
        return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ThemeSelectWindow()
    window.show()
    sys.exit(app.exec())
