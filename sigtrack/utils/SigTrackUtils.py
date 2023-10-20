  # -*- coding: utf-8 -*-
import os
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtWidgets import QMessageBox, QSpacerItem, QSizePolicy 
from sigtrack.utils.SigTrackFMVLog import log
from PySide2.QtCore import Qt

try:
    from pydevd import *
except ImportError:
    None


class SigTrackUtils(object):

    @staticmethod
    def GetIcon(icon):
        ''' Get Icon for Custom Informative Message '''
        if icon == "Question":
            i = QPixmap(":/question")
        elif icon == "Information":
            i = QPixmap(":/information")
        elif icon == "Warning":
            i = QPixmap(":/warning")
        else:
            i = QPixmap(":/critical")
        return i

    @staticmethod
    def CustomMessage(title, msg, informative="", icon="Critical"):
        ''' Custom Informative Message '''
        d = QMessageBox()
        d.setTextFormat(Qt.RichText)
        d.setWindowTitle(title)
        d.setWindowIcon(QIcon(QPixmap(":/mult_icon")))
        d.setText(msg)
        d.setInformativeText(informative)
        d.setIconPixmap(QgsUtils.GetIcon(icon))
        d.addButton(QMessageBox.Yes)
        d.addButton(QMessageBox.No)
        d.setDefaultButton(QMessageBox.No)
       
        # Trick resize QMessageBox
        horizontalSpacer = QSpacerItem(500, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout = d.layout()
        layout.addItem(horizontalSpacer, layout.rowCount(), 0, 1, layout.columnCount())
        
        ret = d.exec_()
        return ret

    # @staticmethod
    # def getLayerExtent(layer=None):
    #     ''' Get Layer extent '''
    #     return iface.mapCanvas().mapSettings().layerExtentToOutputExtent(layer, layer.extent())

    # @staticmethod
    # def selectLayerByName(layerName, group=None):
    #     ''' Select Layer by Name '''
    #     returnLayer = None
    #     try:
    #         if group is None:
    #             returnLayer = QgsProject.instance().mapLayersByName(layerName)[0]
    #             return returnLayer
    #         else:
    #             root = QgsProject.instance().layerTreeRoot()
    #             returnLayer = QgsProject.instance().mapLayersByName(layerName)
    #             g = root.findGroup(group)
    #             if g is not None:
    #                 for child in returnLayer:
    #                     layer = g.findLayer(child.id())
    #                     if layer is not None:
    #                         returnLayer = child
    #                         return returnLayer
    #     except IndexError:
    #         return returnLayer

    @staticmethod
    def createFolderByName(path, name):
        ''' Create Folder by Name '''
        directory = os.path.join(path, name)
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            None

    @staticmethod
    def showUserAndLogMessage(text="", level=1):#, duration=3, onlyLog=False):
        ''' Show user & log info/warning/error messages '''
        # if not onlyLog:
        #     iface.messageBar().popWidget()
        #     iface.messageBar().pushMessage(
        #         before, text, level=level, duration=duration)
        if level == 1:#QGis.Info:
            log.info(text)
        elif level == 2:#QGis.Warning:
            log.warning(text)
        elif level == 3:# QGis.Critical:
            log.error(text)
        return

    @staticmethod
    def removeFile(path):
        try:
            os.remove(path)
        except OSError:
            pass
