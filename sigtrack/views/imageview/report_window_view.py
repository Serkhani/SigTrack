from PySide6.QtWidgets import QDialog, QPushButton, QLabel, QLineEdit, QFormLayout, QVBoxLayout, QWidget, QTextEdit, QHBoxLayout, QSpacerItem
class ReportWindowView(QDialog):
    def __init__(self, parent=None):
        super(ReportWindowView, self).__init__(parent)
        self.setWindowTitle("Report Details")
        self.setGeometry(100, 100, 400, 300)
        # self.central_widget = QWidget()
        # self.setCentralWidget(self.central_widget)

        layout = QFormLayout()
        # self.verticalLayout = QVBoxLayout()
        # self.central_widget.setLayout(self.verticalLayout)

        self.save_pdf_path_label = QLabel("Path to Save PDF:")
        # self.save_pdf_text_input = QLineEdit()
        self.save_pdf_button = QPushButton("Select Path")
        save_pdf_layout = QHBoxLayout()
        save_pdf_layout.addWidget(self.save_pdf_path_label)
        save_pdf_layout.addStretch(1)
        # save_pdf_layout.addWidget(QSpacerItem(40, 20, 1, 1))
        # save_pdf_layout.addWidget(self.save_pdf_text_input)
        save_pdf_layout.addWidget(self.save_pdf_button)
        # layout.addRow("Path to Save PDF:", self.save_pdf_button)
        layout.addRow("", save_pdf_layout)

        # self.author_label = QLabel("Author's Name:")
        self.author_input = QLineEdit()
        layout.addRow("Author's Name:", self.author_input)

        # self.title_label = QLabel("Report Title:")
        self.title_input = QLineEdit()
        layout.addRow("Report Title:", self.title_input)
        

        # self.report_img = QLabel("ImagePath:")
        # self.get_save_path = QLineEdit()
        
        # self.content_label = QLabel("Report Content:")
        self.content_input = QTextEdit()
        layout.addRow("Report Content:", self.content_input)
        
        # self.report_path_button = QPushButton("Select Path")

        self.save_button = QPushButton("Save as PDF")
        layout.addRow("", self.save_button)
        self.setLayout(layout)

        # self.save_pdf_layout = QHBoxLayout()
        # self.save_pdf_layout.addWidget(self.save_pdf_path_label)
        # # self.save_pdf_layout.addWidget(self.save_pdf_text_input)
        # self.save_pdf_layout.addWidget(self.save_pdf_button)
        # self.verticalLayout.addLayout(self.save_pdf_layout)

        # self.save_pdf_layout = QHBoxLayout()
        # self.save_pdf_layout.addWidget(self.author_label)
        # self.save_pdf_layout.addWidget(self.author_input)
        # self.verticalLayout.addLayout(self.save_pdf_layout)

        # self.title_layout = QHBoxLayout()
        # self.title_layout.addWidget(self.title_label)
        # self.title_layout.addWidget(self.title_input)
        # self.verticalLayout.addLayout(self.title_layout)
        # # self.layout.addWidget(self.report_img)
        # # self.layout.addWidget(self.report_img_path)
        # # self.layout.addWidget(self.report_path_button)
        
        # self.content_layout = QHBoxLayout()
        # self.content_layout.addWidget(self.content_label)
        # self.content_layout.addWidget(self.content_input)
        # self.verticalLayout.addLayout(self.content_layout)

        # self.verticalLayout.addWidget(self.save_button)