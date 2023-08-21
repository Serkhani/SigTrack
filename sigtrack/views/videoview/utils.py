import json
from PySide2.QtWidgets import QMessageBox
from PySide2.QtNetwork import QNetworkAccessManager,QNetworkRequest
from PySide2.QtCore import QUrl, QEventLoop
from sigtrack.klv_data.element import UnknownElement
from sigtrack.klv_data.streamparser import StreamParser
import platform, subprocess, os

from constants import FFMPEGPATH, FFPROBEPATH, Reverse_geocoding_url


def showMessage(message):
        msgBox = QMessageBox()
        msgBox.setText(message)
        msgBox.exec()
        
def spawn(cmds, t="ffmpeg"):
    """ Subprocess and Shell Commands in Python """
    if t == "ffmpeg":
        cmds.insert(0, FFMPEGPATH)
    else:
        cmds.insert(0, FFPROBEPATH)

    cmds.insert(3, "-preset")
    cmds.insert(4, "ultrafast")
    isWindows = platform.system() == "Windows"
    return subprocess.Popen(
        cmds,
        shell=isWindows,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=0,
        close_fds=(not isWindows),
    )

def getVideoLocationInfo(videoPath, islocal=False, klv_folder=None, klv_index=0):
    """ Get basic location info about the video """
    location = []
    try:
        if islocal:
            dataFile = os.path.join(klv_folder, "0.0.klv")
            f = open(dataFile, "rb")
            stdout_data = f.read()
        else:
            p = spawn(
                [
                    "-i",
                    videoPath,
                    "-ss",
                    "00:00:00",
                    "-to",
                    "00:00:01",
                    "-map",
                    "0:d:" + str(klv_index),
                    "-f",
                    "data",
                    "-",
                ]
            )

            stdout_data, _ = p.communicate()
            # qgsu.showUserAndLogMessage("Video Loc info raw result", stdout_data, onlyLog=True)
        if stdout_data == b"":
            # qgsu.showUserAndLogMessage("Error interpreting klv data, metadata cannot be read.", "the parser did not recognize KLV data", level=QGis.Warning)
            return
        for packet in StreamParser(stdout_data):
            if isinstance(packet, UnknownElement):
                showMessage( "Error interpreting klv data, metadata cannot be read.\nThe parser did not recognize KLV data")
                continue
            packet.MetadataList()
            centerLat = packet.FrameCenterLatitude
            centerLon = packet.FrameCenterLongitude
            # Target maybe unavailable because of horizontal view
            if centerLat is None and centerLon is None:
                centerLat = packet.SensorLatitude
                centerLon = packet.SensorLongitude
            loc = "-"

            if Reverse_geocoding_url != "":
                try:
                    url = QUrl(
                        Reverse_geocoding_url.format(str(centerLat), str(centerLon))
                    )
                    request = QNetworkRequest(url)
                    reply = QNetworkAccessManager.instance().get(request)
                    loop = QEventLoop()
                    reply.finished.connect(loop.quit)
                    loop.exec_()
                    reply.finished.disconnect(loop.quit)
                    loop = None
                    result = reply.readAll()
                    data = json.loads(result.data())

                    if "village" in data["address"] and "state" in data["address"]:
                        loc = (
                            data["address"]["village"] + ", " + data["address"]["state"]
                        )
                    elif "town" in data["address"] and "state" in data["address"]:
                        loc = data["address"]["town"] + ", " + data["address"]["state"]
                    else:
                        loc = data["display_name"]

                except Exception:
                    showMessage("getVideoLocationInfo: failed to get address from reverse geocoding service.")

            location = [centerLat, centerLon, loc]

            showMessage(
                "Got Location: lon: "
                + str(centerLon)
                + " lat: "
                + str(centerLat)
                + " location: "
                + str(loc),
            )
            break
        else:
            showMessage(
                "This video doesn't have Metadata ! : "
            )
            

    except Exception as e:
        showMessage(
            "Video info callback failed! : \n"+str(e)
        )

    return location
