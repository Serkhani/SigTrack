# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'form.ui'
##
# Created by: Qt User Interface Compiler version 6.5.1
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
                           QCursor, QFont, QFontDatabase, QGradient,
                           QIcon, QImage, QKeySequence, QLinearGradient,
                           QPainter, QPalette, QPixmap, QRadialGradient,
                           QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenu,
                               QMenuBar, QSizePolicy, QToolBar, QVBoxLayout,
                               QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(502, 320)
        MainWindow.setDocumentMode(True)
        self.actionO = QAction(MainWindow)
        self.actionO.setObjectName(u"actionO")
        self.actionReopen = QAction(MainWindow)
        self.actionReopen.setObjectName(u"actionReopen")
        self.actionNetwork = QAction(MainWindow)
        self.actionNetwork.setObjectName(u"actionNetwork")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        self.actionUndo = QAction(MainWindow)
        self.actionUndo.setObjectName(u"actionUndo")
        self.actionRedo = QAction(MainWindow)
        self.actionRedo.setObjectName(u"actionRedo")
        self.actionZoom_In = QAction(MainWindow)
        self.actionZoom_In.setObjectName(u"actionZoom_In")
        self.actionZoom_Out = QAction(MainWindow)
        self.actionZoom_Out.setObjectName(u"actionZoom_Out")
        self.actionZoom_Selection = QAction(MainWindow)
        self.actionZoom_Selection.setObjectName(u"actionZoom_Selection")
        self.actionPan = QAction(MainWindow)
        self.actionPan.setObjectName(u"actionPan")
        self.actionMap = QAction(MainWindow)
        self.actionMap.setObjectName(u"actionMap")
        self.actionImage = QAction(MainWindow)
        self.actionImage.setObjectName(u"actionImage")
        self.actionVideo = QAction(MainWindow)
        self.actionVideo.setObjectName(u"actionVideo")
        self.actionFile_s = QAction(MainWindow)
        self.actionFile_s.setObjectName(u"actionFile_s")
        self.actionFolder = QAction(MainWindow)
        self.actionFolder.setObjectName(u"actionFolder")
        self.actionImgNetwork = QAction(MainWindow)
        self.actionImgNetwork.setObjectName(u"actionImgNetwork")
        self.actionVidFile = QAction(MainWindow)
        self.actionVidFile.setObjectName(u"actionVidFile")
        self.actionVidFolder = QAction(MainWindow)
        self.actionVidFolder.setObjectName(u"actionVidFolder")
        self.actionFile_s_3 = QAction(MainWindow)
        self.actionFile_s_3.setObjectName(u"actionFile_s_3")
        self.actionVidNetwork = QAction(MainWindow)
        self.actionVidNetwork.setObjectName(u"actionVidNetwork")
        self.actionImgFile = QAction(MainWindow)
        self.actionImgFile.setObjectName(u"actionImgFile")
        self.actionImgFolder = QAction(MainWindow)
        self.actionImgFolder.setObjectName(u"actionImgFolder")
        self.actionSwitch_Theme = QAction(MainWindow)
        self.actionSwitch_Theme.setObjectName(u"actionSwitch_Theme")
        self.actionSwitch_Theme.setCheckable(True)
        self.actionLight_Teal = QAction(MainWindow)
        self.actionLight_Teal.setObjectName(u"actionLight_Teal")
        self.actionDark_Teal = QAction(MainWindow)
        self.actionDark_Teal.setObjectName(u"actionDark_Teal")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 502, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuImport = QMenu(self.menuFile)
        self.menuImport.setObjectName(u"menuImport")
        self.menuVideo = QMenu(self.menuImport)
        self.menuVideo.setObjectName(u"menuVideo")
        self.menuVidLocal = QMenu(self.menuVideo)
        self.menuVidLocal.setObjectName(u"menuVidLocal")
        self.menuImage = QMenu(self.menuImport)
        self.menuImage.setObjectName(u"menuImage")
        self.menuImgLocal = QMenu(self.menuImage)
        self.menuImgLocal.setObjectName(u"menuImgLocal")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuZoom = QMenu(self.menuEdit)
        self.menuZoom.setObjectName(u"menuZoom")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        self.menuSwitch_theme = QMenu(self.menuSettings)
        self.menuSwitch_theme.setObjectName(u"menuSwitch_theme")
        MainWindow.setMenuBar(self.menubar)
        self.editingToolbar = QToolBar(MainWindow)
        self.editingToolbar.setObjectName(u"editingToolbar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.editingToolbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menuFile.addAction(self.menuImport.menuAction())
        self.menuFile.addAction(self.actionSave)
        self.menuImport.addAction(self.menuVideo.menuAction())
        self.menuImport.addAction(self.menuImage.menuAction())
        self.menuVideo.addAction(self.menuVidLocal.menuAction())
        self.menuVideo.addAction(self.actionVidNetwork)
        self.menuVidLocal.addAction(self.actionVidFile)
        self.menuVidLocal.addAction(self.actionVidFolder)
        self.menuImage.addAction(self.menuImgLocal.menuAction())
        self.menuImage.addAction(self.actionImgNetwork)
        self.menuImgLocal.addAction(self.actionImgFile)
        self.menuImgLocal.addAction(self.actionImgFolder)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addAction(self.menuZoom.menuAction())
        self.menuEdit.addAction(self.actionPan)
        self.menuZoom.addAction(self.actionZoom_In)
        self.menuZoom.addAction(self.actionZoom_Out)
        self.menuZoom.addAction(self.actionZoom_Selection)
        self.menuView.addAction(self.actionMap)
        self.menuView.addAction(self.actionImage)
        self.menuView.addAction(self.actionVideo)
        self.menuSettings.addAction(self.menuSwitch_theme.menuAction())
        self.menuSwitch_theme.addAction(self.actionLight_Teal)
        self.menuSwitch_theme.addAction(self.actionDark_Teal)
        self.editingToolbar.addSeparator()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"MainWindow", None))
        self.actionO.setText(
            QCoreApplication.translate("MainWindow", u"O", None))
        self.actionReopen.setText(
            QCoreApplication.translate("MainWindow", u"Reopen", None))
        self.actionNetwork.setText(
            QCoreApplication.translate("MainWindow", u"Network", None))
# if QT_CONFIG(shortcut)
        self.actionNetwork.setShortcut(
            QCoreApplication.translate("MainWindow", u"Ctrl+Shift+N", None))
# endif // QT_CONFIG(shortcut)
        self.actionSave.setText(
            QCoreApplication.translate("MainWindow", u"Save", None))
# if QT_CONFIG(statustip)
        self.actionSave.setStatusTip(QCoreApplication.translate(
            "MainWindow", u"Save edited file", None))
# endif // QT_CONFIG(statustip)
# if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(
            QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
# endif // QT_CONFIG(shortcut)
        self.actionSave_As.setText(
            QCoreApplication.translate("MainWindow", u"Save As", None))
# if QT_CONFIG(statustip)
        self.actionSave_As.setStatusTip(QCoreApplication.translate(
            "MainWindow", u"Save current file state", None))
# endif // QT_CONFIG(statustip)
# if QT_CONFIG(shortcut)
        self.actionSave_As.setShortcut(
            QCoreApplication.translate("MainWindow", u"Ctrl+F12", None))
# endif // QT_CONFIG(shortcut)
        self.actionUndo.setText(
            QCoreApplication.translate("MainWindow", u"Undo", None))
# if QT_CONFIG(whatsthis)
        self.actionUndo.setWhatsThis(QCoreApplication.translate(
            "MainWindow", u"undo previous action", None))
# endif // QT_CONFIG(whatsthis)
# if QT_CONFIG(shortcut)
        self.actionUndo.setShortcut(
            QCoreApplication.translate("MainWindow", u"Ctrl+Z", None))
# endif // QT_CONFIG(shortcut)
        self.actionRedo.setText(
            QCoreApplication.translate("MainWindow", u"Redo", None))
# if QT_CONFIG(shortcut)
        self.actionRedo.setShortcut(
            QCoreApplication.translate("MainWindow", u"Ctrl+Y", None))
# endif // QT_CONFIG(shortcut)
        self.actionZoom_In.setText(
            QCoreApplication.translate("MainWindow", u"Zoom In", None))
# if QT_CONFIG(shortcut)
        self.actionZoom_In.setShortcut(
            QCoreApplication.translate("MainWindow", u"+", None))
# endif // QT_CONFIG(shortcut)
        self.actionZoom_Out.setText(
            QCoreApplication.translate("MainWindow", u"Zoom Out", None))
# if QT_CONFIG(shortcut)
        self.actionZoom_Out.setShortcut(
            QCoreApplication.translate("MainWindow", u"-", None))
# endif // QT_CONFIG(shortcut)
        self.actionZoom_Selection.setText(
            QCoreApplication.translate("MainWindow", u"Zoom Selection", None))
        self.actionPan.setText(
            QCoreApplication.translate("MainWindow", u"Pan", None))
# if QT_CONFIG(shortcut)
        self.actionPan.setShortcut(
            QCoreApplication.translate("MainWindow", u"Shift+P", None))
# endif // QT_CONFIG(shortcut)
        self.actionMap.setText(
            QCoreApplication.translate("MainWindow", u"Map", None))
# if QT_CONFIG(shortcut)
        self.actionMap.setShortcut(
            QCoreApplication.translate("MainWindow", u"F1", None))
# endif // QT_CONFIG(shortcut)
        self.actionImage.setText(
            QCoreApplication.translate("MainWindow", u"Image", None))
# if QT_CONFIG(shortcut)
        self.actionImage.setShortcut(
            QCoreApplication.translate("MainWindow", u"F2", None))
# endif // QT_CONFIG(shortcut)
        self.actionVideo.setText(
            QCoreApplication.translate("MainWindow", u"Video", None))
# if QT_CONFIG(shortcut)
        self.actionVideo.setShortcut(
            QCoreApplication.translate("MainWindow", u"F3", None))
# endif // QT_CONFIG(shortcut)
        self.actionFile_s.setText(
            QCoreApplication.translate("MainWindow", u"File(s)", None))
# if QT_CONFIG(shortcut)
        self.actionFile_s.setShortcut(QCoreApplication.translate(
            "MainWindow", u"Ctrl+Shift+F", None))
# endif // QT_CONFIG(shortcut)
        self.actionFolder.setText(
            QCoreApplication.translate("MainWindow", u"Folder", None))
# if QT_CONFIG(shortcut)
        self.actionFolder.setShortcut(QCoreApplication.translate(
            "MainWindow", u"Ctrl+Shift+L", None))
# endif // QT_CONFIG(shortcut)
        self.actionImgNetwork.setText(
            QCoreApplication.translate("MainWindow", u"Network", None))
        self.actionVidFile.setText(
            QCoreApplication.translate("MainWindow", u"File(s)", None))
# if QT_CONFIG(shortcut)
        self.actionVidFile.setShortcut(
            QCoreApplication.translate("MainWindow", u"Ctrl+Shift+F", None))
# endif // QT_CONFIG(shortcut)
        self.actionVidFolder.setText(
            QCoreApplication.translate("MainWindow", u"Folder", None))
# if QT_CONFIG(shortcut)
        self.actionVidFolder.setShortcut(
            QCoreApplication.translate("MainWindow", u"Ctrl+Shift+L", None))
# endif // QT_CONFIG(shortcut)
        self.actionFile_s_3.setText(
            QCoreApplication.translate("MainWindow", u"File(s)", None))
        self.actionVidNetwork.setText(
            QCoreApplication.translate("MainWindow", u"Network", None))
        self.actionImgFile.setText(
            QCoreApplication.translate("MainWindow", u"File(s)", None))
# if QT_CONFIG(shortcut)
        self.actionImgFile.setShortcut(
            QCoreApplication.translate("MainWindow", u"Ctrl+Alt+F", None))
# endif // QT_CONFIG(shortcut)
        self.actionImgFolder.setText(
            QCoreApplication.translate("MainWindow", u"Folder", None))
# if QT_CONFIG(shortcut)
        self.actionImgFolder.setShortcut(QCoreApplication.translate(
            "MainWindow", u"Ctrl+Alt+\u00d8", None))
# endif // QT_CONFIG(shortcut)
        self.actionSwitch_Theme.setText(QCoreApplication.translate(
            "MainWindow", u"Switch to dark theme", None))
        self.actionLight_Teal.setText(
            QCoreApplication.translate("MainWindow", u"Light Teal", None))
        self.actionDark_Teal.setText(
            QCoreApplication.translate("MainWindow", u"Dark Teal", None))
        self.label.setText(QCoreApplication.translate(
            "MainWindow", u"Add a View", None))
        self.menuFile.setTitle(
            QCoreApplication.translate("MainWindow", u"File", None))
        self.menuImport.setTitle(
            QCoreApplication.translate("MainWindow", u"Import", None))
        self.menuVideo.setTitle(
            QCoreApplication.translate("MainWindow", u"Video", None))
        self.menuVidLocal.setTitle(
            QCoreApplication.translate("MainWindow", u"Local", None))
        self.menuImage.setTitle(
            QCoreApplication.translate("MainWindow", u"Image", None))
        self.menuImgLocal.setTitle(
            QCoreApplication.translate("MainWindow", u"Local", None))
        self.menuEdit.setTitle(
            QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuZoom.setTitle(
            QCoreApplication.translate("MainWindow", u"Zoom", None))
        self.menuView.setTitle(
            QCoreApplication.translate("MainWindow", u"View", None))
        self.menuSettings.setTitle(
            QCoreApplication.translate("MainWindow", u"Settings", None))
        self.menuSwitch_theme.setTitle(
            QCoreApplication.translate("MainWindow", u"Switch theme", None))
        self.editingToolbar.setWindowTitle(
            QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi
