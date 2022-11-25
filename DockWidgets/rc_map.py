# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 5.15.2
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore

qt_resource_data = b"\
\x00\x00\x040\
i\
mport QtQuick 2.\
15\x0d\x0aimport QtPos\
itioning 5.15\x0d\x0ai\
mport QtLocation\
 5.15\x0d\x0a\x0d\x0aRectang\
le {\x0d\x0a    id: re\
ctangle\x0d\x0a    wid\
th: 640\x0d\x0a    hei\
ght: 480\x0d\x0a    Pl\
ugin {\x0d\x0a        \
id: osmPlugin\x0d\x0a \
       name: \x22os\
m\x22\x0d\x0a    }\x0d\x0a    P\
luginParameter {\
\x0d\x0a        name: \
\x22osm.mapping.pro\
vidersrepository\
.disabled\x22\x0d\x0a    \
    value: \x22true\
\x22\x0d\x0a    }\x0d\x0a    Pl\
uginParameter {\x0d\
\x0a        name: \x22\
osm.mapping.prov\
idersrepository.\
address\x22\x0d\x0a      \
  value: \x22http:/\
/maps-redirect.q\
t.io/osm/5.6/\x22\x0d\x0a\
    }\x0d\x0a    prope\
rty variant loca\
tionTC: QtPositi\
oning.coordinate\
(7.9465, 1.0232)\
\x0d\x0a    Map {\x0d\x0a   \
     id: map\x0d\x0a  \
      anchors.fi\
ll: parent\x0d\x0a    \
    plugin: osmP\
lugin\x0d\x0a        c\
enter: locationT\
C\x0d\x0a        zoomL\
evel: 10\x0d\x0a      \
  MapItemView {\x0d\
\x0a            mod\
el: markermodel\x0d\
\x0a            del\
egate: MapQuickI\
tem {\x0d\x0a         \
       coordinat\
e: model.positio\
n_marker\x0d\x0a      \
          anchor\
Point.x: image.w\
idth\x0d\x0a          \
      anchorPoin\
t.y: image.heigh\
t\x0d\x0a             \
   sourceItem: I\
mage {\x0d\x0a        \
            id: \
image\x0d\x0a         \
           sourc\
e: model.source_\
marker\x0d\x0a        \
        }\x0d\x0a     \
       }\x0d\x0a      \
  }\x0d\x0a    }\x0d\x0a}\x0d\x0a\
"

qt_resource_name = b"\
\x00\x03\
\x00\x00s\x80\
\x00m\
\x00a\x00p\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x84\xact&h\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
