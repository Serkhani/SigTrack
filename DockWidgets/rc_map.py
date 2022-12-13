# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 5.15.2
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore

qt_resource_data = b"\
\x00\x00\x06w\
i\
mport QtQuick 2.\
15\x0d\x0aimport QtQui\
ck.Controls 2.15\
\x0d\x0aimport QtPosit\
ioning 5.15\x0d\x0aimp\
ort QtLocation 5\
.15\x0d\x0aimport \x22app\
lication.js\x22 as \
App\x0d\x0a\x0d\x0aRectangle\
 {\x0d\x0a    id: rect\
angle\x0d\x0a    Plugi\
n {\x0d\x0a        id:\
 osmPlugin\x0d\x0a    \
    name: \x22osm\x22\x0d\
\x0a        PluginP\
arameter {\x0d\x0a    \
        name: \x22o\
sm.mapping.provi\
dersrepository.d\
isabled\x22\x0d\x0a      \
      value: \x22tr\
ue\x22\x0d\x0a        }\x0d\x0a\
        PluginPa\
rameter {\x0d\x0a     \
       name: \x22os\
m.mapping.provid\
ersrepository.ad\
dress\x22\x0d\x0a        \
    value: \x22http\
://maps-redirect\
.qt.io/osm/5.6/\x22\
\x0d\x0a        }\x0d\x0a   \
 }\x0d\x0a    property\
 variant locatio\
nTC: QtPositioni\
ng.coordinate(7.\
9465, 1.0232)\x0d\x0a \
   Map {\x0d\x0a      \
  id: map\x0d\x0a     \
   anchors.fill:\
 parent\x0d\x0a       \
 plugin: osmPlug\
in\x0d\x0a        cent\
er: locationTC\x0d\x0a\
        zoomLeve\
l: 6\x0d\x0a        Ma\
pItemView {\x0d\x0a   \
         model: \
markermodel\x0d\x0a   \
         delegat\
e: MapQuickItem \
{\x0d\x0a             \
   coordinate: m\
odel.position_ma\
rker\x0d\x0a          \
      anchorPoin\
t.x: image.width\
\x0d\x0a              \
  anchorPoint.y:\
 image.height\x0d\x0a \
               s\
ourceItem: Image\
 {\x0d\x0a            \
        id: imag\
e\x0d\x0a             \
       source: m\
odel.source_mark\
er\x0d\x0a            \
    }\x0d\x0a         \
       MouseArea\
 {\x0d\x0a            \
        id: mark\
erMouseArea\x0d\x0a   \
                \
 objectName: \x22bu\
ttonMouseArea\x22\x0d\x0a\
                \
    anchors.fill\
: parent\x0d\x0a      \
              ho\
verEnabled: true\
\x0d\x0a              \
      onClicked:\
 {\x0d\x0a            \
            App.\
showImage(model.\
imgPath)\x0d\x0a      \
              }\x0d\
\x0a               \
 }\x0d\x0a\x0d\x0a          \
      ToolTip {\x0d\
\x0a               \
     parent: ima\
ge\x0d\x0a            \
        visible:\
 markerMouseArea\
.containsMouse\x0d\x0a\
                \
    text: qsTr(m\
odel.tooltip)\x0d\x0a \
               }\
\x0d\x0a            }\x0d\
\x0a        }\x0d\x0a    \
}\x0d\x0a}\x0d\x0a\
\x00\x00\x00>\
f\
unction showImag\
e(imgPath) {\x0d\x0a  \
  ice.showImage(\
imgPath)\x0d\x0a}\x0d\x0a\
"

qt_resource_name = b"\
\x00\x03\
\x00\x00s\x80\
\x00m\
\x00a\x00p\
\x00\x0e\
\x04#\xfc\x13\
\x00a\
\x00p\x00p\x00l\x00i\x00c\x00a\x00t\x00i\x00o\x00n\x00.\x00j\x00s\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x84\xf0\xe8:\xf6\
\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x01\x00\x00\x06{\
\x00\x00\x01\x84\xbd\xc8K\xaf\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
