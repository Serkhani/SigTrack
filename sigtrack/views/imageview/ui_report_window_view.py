# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'generate_pdf_popup.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_ReportWindow(object):
    def setupUi(self, ReportWindow):
        if not ReportWindow.objectName():
            ReportWindow.setObjectName(u"ReportWindow")
        ReportWindow.resize(511, 420)
        self.verticalLayout = QVBoxLayout(ReportWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.save_pdf_path_label = QLabel(ReportWindow)
        self.save_pdf_path_label.setObjectName(u"save_pdf_path_label")

        self.horizontalLayout.addWidget(self.save_pdf_path_label)

        self.save_pdf_button = QPushButton(ReportWindow)
        self.save_pdf_button.setObjectName(u"save_pdf_button")

        self.horizontalLayout.addWidget(self.save_pdf_button)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.author_label = QLabel(ReportWindow)
        self.author_label.setObjectName(u"author_label")

        self.horizontalLayout_2.addWidget(self.author_label)

        self.author_input = QLineEdit(ReportWindow)
        self.author_input.setObjectName(u"author_input")

        self.horizontalLayout_2.addWidget(self.author_input)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.title_label = QLabel(ReportWindow)
        self.title_label.setObjectName(u"title_label")

        self.horizontalLayout_3.addWidget(self.title_label)

        self.title_input = QLineEdit(ReportWindow)
        self.title_input.setObjectName(u"title_input")

        self.horizontalLayout_3.addWidget(self.title_input)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.content_label = QLabel(ReportWindow)
        self.content_label.setObjectName(u"content_label")

        self.horizontalLayout_4.addWidget(self.content_label)

        self.content_input = QTextEdit(ReportWindow)
        self.content_input.setObjectName(u"content_input")

        self.horizontalLayout_4.addWidget(self.content_input)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.save_button = QPushButton(ReportWindow)
        self.save_button.setObjectName(u"save_button")

        self.verticalLayout.addWidget(self.save_button)


        self.retranslateUi(ReportWindow)

        QMetaObject.connectSlotsByName(ReportWindow)
    # setupUi

    def retranslateUi(self, ReportWindow):
        ReportWindow.setWindowTitle(QCoreApplication.translate("ReportWindow", u"Form", None))
        self.save_pdf_path_label.setText(QCoreApplication.translate("ReportWindow", u"Path to Save PDF: ", None))
        self.save_pdf_button.setText(QCoreApplication.translate("ReportWindow", u"Select Path", None))
        self.author_label.setText(QCoreApplication.translate("ReportWindow", u"Author's Name: ", None))
        self.title_label.setText(QCoreApplication.translate("ReportWindow", u"Report Title:", None))
        self.content_label.setText(QCoreApplication.translate("ReportWindow", u"Report Content: ", None))
        self.save_button.setText(QCoreApplication.translate("ReportWindow", u"Save as PDF", None))
    # retranslateUi

