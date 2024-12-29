# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'markerpopup.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDockWidget, QListView, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_MarkerDockwidget(object):
    def setupUi(self, MarkerDockwidget):
        if not MarkerDockwidget.objectName():
            MarkerDockwidget.setObjectName(u"MarkerDockwidget")
        MarkerDockwidget.resize(400, 300)
        MarkerDockwidget.setFloating(True)
        MarkerDockwidget.setFeatures(QDockWidget.DockWidgetClosable|QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable)
        MarkerDockwidget.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.Markers = QWidget()
        self.Markers.setObjectName(u"Markers")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Markers.sizePolicy().hasHeightForWidth())
        self.Markers.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.Markers)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.listView = QListView(self.Markers)
        self.listView.setObjectName(u"listView")

        self.verticalLayout.addWidget(self.listView)

        self.addMarkerBtn = QPushButton(self.Markers)
        self.addMarkerBtn.setObjectName(u"addMarkerBtn")

        self.verticalLayout.addWidget(self.addMarkerBtn)

        MarkerDockwidget.setWidget(self.Markers)

        self.retranslateUi(MarkerDockwidget)

        QMetaObject.connectSlotsByName(MarkerDockwidget)
    # setupUi

    def retranslateUi(self, MarkerDockwidget):
        MarkerDockwidget.setWindowTitle(QCoreApplication.translate("MarkerDockwidget", u"Markers", None))
        self.addMarkerBtn.setText(QCoreApplication.translate("MarkerDockwidget", u"Add Marker", None))
    # retranslateUi

