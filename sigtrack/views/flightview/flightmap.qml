import QtQuick 2.15
import QtQuick.Controls 2.15
import QtLocation 
import QtPositioning 

ApplicationWindow {
    visible: true
    width: 1024
    height: 768
    title: "Flight Tracker"
    Plugin {
            id: osmPlugin
            name: "osm"

            PluginParameter {
                name: "osm.mapping.providersrepository.disabled"
                value: "true"
            }
            PluginParameter {
                name: "osm.mapping.providersrepository.address"
                value: "http://maps-redirect.qt.io/osm/5.8/"
            }
        }
    Map {
        anchors.fill: parent
        id: map
        plugin: osmPlugin
        center: QtPositioning.coordinate(5.658735, -0.184961)
        // zoomLevel: 2
        property geoCoordinate startCentroid

        PinchHandler {
            id: pinch
            target: null
            onActiveChanged: if (active) {
                map.startCentroid = map.toCoordinate(pinch.centroid.position, false)
            }
            onScaleChanged: (delta) => {
                map.zoomLevel += Math.log2(delta)
                map.alignCoordinateToPoint(map.startCentroid, pinch.centroid.position)
            }
            onRotationChanged: (delta) => {
                map.bearing -= delta
                map.alignCoordinateToPoint(map.startCentroid, pinch.centroid.position)
            }
            grabPermissions: PointerHandler.TakeOverForbidden
        }
        WheelHandler {
            id: wheel
            // workaround for QTBUG-87646 / QTBUG-112394 / QTBUG-112432:
            // Magic Mouse pretends to be a trackpad but doesn't work with PinchHandler
            // and we don't yet distinguish mice and trackpads on Wayland either
            acceptedDevices: Qt.platform.pluginName === "cocoa" || Qt.platform.pluginName === "wayland"
                             ? PointerDevice.Mouse | PointerDevice.TouchPad
                             : PointerDevice.Mouse
            rotationScale: 1/120
            property: "zoomLevel"
        }
        DragHandler {
            id: drag
            target: null
            onTranslationChanged: (delta) => map.pan(-delta.x, -delta.y)
        }
         MapItemView {
       
            model: flightModel
            anchors.fill: parent
           delegate:
            MapQuickItem {
                coordinate: QtPositioning.coordinate(model.lat, model.lon)
                
                anchorPoint.x: droneImg.width/2
                anchorPoint.y: droneImg.height/2
                // transform: Rotation {
                //     origin.x: droneImg.width/2
                //     origin.y: droneImg.height/2
                //     angle: model.track
                // }
                 MouseArea{
            anchors.fill: parent
            onClicked: {
                console.log(model.flight)
                console.log(model.lat)
                console.log(model.lon)
                console.log(model.alt)
                console.log(model.ownOp)
                console.log(model.track)
            }
        }
                sourceItem: Image {
                    
                    id: droneImg
                    property alias rotationAngle: rotation.angle

                    width: 70
                    height: 70
                    transform: 
                    [Rotation {
                        id: rotation
                        origin.x: droneImg.width/2
                        origin.y: droneImg.height/2
                        angle: model.track

                    }]
                    source:  'qrc:/drone'
                }
            }
    
function updatePositionAndRotation(angleDeg)
{
    image.rotationAngle = angleDeg
}

    }
}
    }