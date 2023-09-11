# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'videodockwidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_VideoView(object):
    def setupUi(self, VideoView):
        if not VideoView.objectName():
            VideoView.setObjectName(u"VideoView")
        VideoView.resize(536, 425)
        VideoView.setFeatures(QDockWidget.DockWidgetClosable|QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContents.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, -1, 0, 0)
        self.playBtn = QPushButton(self.dockWidgetContents)
        self.playBtn.setObjectName(u"playBtn")
        icon = QIcon()
        iconThemeName = u"media-playback-pause"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.playBtn.setIcon(icon)

        self.horizontalLayout.addWidget(self.playBtn)

        self.stopBtn = QPushButton(self.dockWidgetContents)
        self.stopBtn.setObjectName(u"stopBtn")
        icon1 = QIcon()
        iconThemeName = u"media-playback-stop"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.stopBtn.setIcon(icon1)

        self.horizontalLayout.addWidget(self.stopBtn)

        self.volBtn = QPushButton(self.dockWidgetContents)
        self.volBtn.setObjectName(u"volBtn")
        icon2 = QIcon()
        iconThemeName = u"multimedia-volume-control"
        if QIcon.hasThemeIcon(iconThemeName):
            icon2 = QIcon.fromTheme(iconThemeName)
        else:
            icon2.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.volBtn.setIcon(icon2)

        self.horizontalLayout.addWidget(self.volBtn)

        self.volumeSlider = QSlider(self.dockWidgetContents)
        self.volumeSlider.setObjectName(u"volumeSlider")
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setSliderPosition(5)
        self.volumeSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.volumeSlider)

        self.fmvBtn = QPushButton(self.dockWidgetContents)
        self.fmvBtn.setObjectName(u"fmvBtn")

        self.horizontalLayout.addWidget(self.fmvBtn)

        self.vidMarkerBtn = QPushButton(self.dockWidgetContents)
        self.vidMarkerBtn.setObjectName(u"vidMarkerBtn")

        self.horizontalLayout.addWidget(self.vidMarkerBtn)

        self.multiplexBtn = QPushButton(self.dockWidgetContents)
        self.multiplexBtn.setObjectName(u"multiplexBtn")

        self.horizontalLayout.addWidget(self.multiplexBtn)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 10)
        self.timestampLabel = QLabel(self.dockWidgetContents)
        self.timestampLabel.setObjectName(u"timestampLabel")
        self.timestampLabel.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.timestampLabel)

        self.timeSlider = QSlider(self.dockWidgetContents)
        self.timeSlider.setObjectName(u"timeSlider")
        self.timeSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.timeSlider)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        VideoView.setWidget(self.dockWidgetContents)

        self.retranslateUi(VideoView)

        QMetaObject.connectSlotsByName(VideoView)
    # setupUi

    def retranslateUi(self, VideoView):
#if QT_CONFIG(statustip)
        VideoView.setStatusTip(QCoreApplication.translate("VideoView", u"Pause/Play", None))
#endif // QT_CONFIG(statustip)
        VideoView.setWindowTitle(QCoreApplication.translate("VideoView", u"VideoView", None))
#if QT_CONFIG(tooltip)
        self.playBtn.setToolTip(QCoreApplication.translate("VideoView", u"Pause/Play", None))
#endif // QT_CONFIG(tooltip)
        self.playBtn.setText("")
#if QT_CONFIG(shortcut)
        self.playBtn.setShortcut(QCoreApplication.translate("VideoView", u"Space", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.stopBtn.setToolTip(QCoreApplication.translate("VideoView", u"<html><head/><body><p>Stop</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.stopBtn.setStatusTip(QCoreApplication.translate("VideoView", u"Stop", None))
#endif // QT_CONFIG(statustip)
        self.stopBtn.setText("")
#if QT_CONFIG(shortcut)
        self.stopBtn.setShortcut(QCoreApplication.translate("VideoView", u"Esc", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.volBtn.setToolTip(QCoreApplication.translate("VideoView", u"Volume", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.volBtn.setStatusTip(QCoreApplication.translate("VideoView", u"Volume", None))
#endif // QT_CONFIG(statustip)
        self.volBtn.setText("")
#if QT_CONFIG(tooltip)
        self.fmvBtn.setToolTip(QCoreApplication.translate("VideoView", u"FMV", None))
#endif // QT_CONFIG(tooltip)
        self.fmvBtn.setText("")
#if QT_CONFIG(shortcut)
        self.fmvBtn.setShortcut(QCoreApplication.translate("VideoView", u"Ctrl+F", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.vidMarkerBtn.setToolTip(QCoreApplication.translate("VideoView", u"Video Marker", None))
#endif // QT_CONFIG(tooltip)
        self.vidMarkerBtn.setText("")
#if QT_CONFIG(shortcut)
        self.vidMarkerBtn.setShortcut(QCoreApplication.translate("VideoView", u"Ctrl+I", None))
#endif // QT_CONFIG(shortcut)
        self.multiplexBtn.setText("")
#if QT_CONFIG(shortcut)
        self.multiplexBtn.setShortcut(QCoreApplication.translate("VideoView", u"Ctrl+M", None))
#endif // QT_CONFIG(shortcut)
        self.timestampLabel.setText(QCoreApplication.translate("VideoView", u"'--:-- / --:--'", None))
    # retranslateUi

