# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'markerpopup.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MarkerDockwidget(object):
    def setupUi(self, MarkerDockwidget):
        if not MarkerDockwidget.objectName():
            MarkerDockwidget.setObjectName(u"MarkerDockwidget")
        MarkerDockwidget.resize(400, 300)
        MarkerDockwidget.setAllowedAreas(Qt.NoDockWidgetArea)
        self.Markers = QWidget()
        self.Markers.setObjectName(u"Markers")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Markers.sizePolicy().hasHeightForWidth())
        self.Markers.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.Markers)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.Markers)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.pushButton = QPushButton(self.Markers)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        MarkerDockwidget.setWidget(self.Markers)

        self.retranslateUi(MarkerDockwidget)

        QMetaObject.connectSlotsByName(MarkerDockwidget)
    # setupUi

    def retranslateUi(self, MarkerDockwidget):
        MarkerDockwidget.setWindowTitle(QCoreApplication.translate("MarkerDockwidget", u"Markers", None))
        self.label.setText(QCoreApplication.translate("MarkerDockwidget", u"No Markers", None))
        self.pushButton.setText(QCoreApplication.translate("MarkerDockwidget", u"Add Marker", None))
    # retranslateUi

