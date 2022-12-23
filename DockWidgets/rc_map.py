# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 5.15.2
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore

qt_resource_data = b"\
\x00\x00\x08\xce\
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
   property int \
zoomLevel: 6\x0d\x0a  \
  Map {\x0d\x0a       \
 id: map\x0d\x0a      \
  anchors.fill: \
parent\x0d\x0a        \
plugin: osmPlugi\
n\x0d\x0a        cente\
r: locationTC\x0d\x0a \
       zoomLevel\
: 6\x0d\x0a        Col\
umn {\x0d\x0a         \
   anchors.right\
: parent.right\x0d\x0a\
            righ\
tPadding: 5\x0d\x0a   \
         topPadd\
ing: 5\x0d\x0a        \
    spacing: 5\x0d\x0a\
            Butt\
on {\x0d\x0a          \
      text: '+'\x0d\
\x0a               \
 onClicked: {\x0d\x0a \
                \
   map.zoomLevel\
 += 1\x0d\x0a         \
       }\x0d\x0a      \
          width:\
 50\x0d\x0a           \
     height: 30\x0d\
\x0a            }\x0d\x0a\
            Butt\
on {\x0d\x0a          \
      text: '-'\x0d\
\x0a               \
 onClicked: {\x0d\x0a \
                \
   map.zoomLevel\
 -= 1\x0d\x0a         \
       }\x0d\x0a      \
          width:\
 50\x0d\x0a           \
     height: 30\x0d\
\x0a            }\x0d\x0a\
        }\x0d\x0a\x0d\x0a   \
     MapItemView\
 {\x0d\x0a            \
model: markermod\
el\x0d\x0a            \
delegate: MapQui\
ckItem {\x0d\x0a      \
          coordi\
nate: model.posi\
tion_marker\x0d\x0a   \
             anc\
horPoint.x: imag\
e.width\x0d\x0a       \
         anchorP\
oint.y: image.he\
ight\x0d\x0a          \
      sourceItem\
: Image {\x0d\x0a     \
               i\
d: image\x0d\x0a      \
              so\
urce: model.sour\
ce_marker\x0d\x0a     \
           }\x0d\x0a  \
              Mo\
useArea {\x0d\x0a     \
               i\
d: markerMouseAr\
ea\x0d\x0a            \
        objectNa\
me: \x22buttonMouse\
Area\x22\x0d\x0a         \
           ancho\
rs.fill: parent\x0d\
\x0a               \
     hoverEnable\
d: true\x0d\x0a       \
             onC\
licked: {\x0d\x0a     \
                \
   App.showImage\
(model.imgPath)\x0d\
\x0a               \
     }\x0d\x0a        \
        }\x0d\x0a\x0d\x0a   \
             Too\
lTip {\x0d\x0a        \
            pare\
nt: image\x0d\x0a     \
               v\
isible: markerMo\
useArea.contains\
Mouse\x0d\x0a         \
           text:\
 qsTr(model.tool\
tip)\x0d\x0a          \
      }\x0d\x0a       \
     }\x0d\x0a        \
}\x0d\x0a    }\x0d\x0a}\x0d\x0a\
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
\x00\x00\x01\x85A\x01'\xbb\
\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x01\x00\x00\x08\xd2\
\x00\x00\x01\x84\xbd\xc8K\xaf\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
