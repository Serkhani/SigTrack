// import QtQuick
// import QtQuick.Controls
// import QtPositioning
// import QtLocation
// import QtQuick.Controls.Basic 2.15
// import QtQuick 2.15
// import QtQuick.Controls.Basic
import QtQuick
import QtQuick.Controls.Basic
import QtPositioning
import QtLocation
import "../../views/mapview/application.js" as App

Rectangle {
    id: rectangle
//     Plugin {
//     id: herePlugin
// // GiUN_4L8BA4g7VP8H7JvyA
// // 0UkfUkOWcuKOJl44gpyjsqtnpZQO-jCCSr53pUzAwIdISJLNd7iTetC_MmA0rrZVPplxfXdi73KF8CnuYNcqZA
//     name: "here"
//     parameters: [
//         PluginParameter {
//             name: "here.app_id"
//             value: "pImRQYN55MDCWPrhMlMz"
//         },
//         PluginParameter {
//             name: "here.token"
//             value: "ll4wz9OgFeLy08ElhzVfZ3QDk1V35LqMJnD5I9CimRE"
//         }
//     ]
// }
//   Plugin {
//         id: mapbox
//         name: "mapbox"
//         PluginParameter {
//             name: "mapbox.access_token"
//             value: "pk.eyJ1Ijoic2Vya2hhbmkiLCJhIjoiY201ZDluYnM0MmppNTJrczJ6M3Z2a2ZqOSJ9.TUP4GZ15D462LkUy5PUcWQ"
//         }

//     }
    Plugin {
        id: osmPlugin
        name: "osm"
        // name: "esri"
        // name: "mapboxgl"
        // preferred: ["esri", "osm"]
        // PluginParameter {
        //     name: "osm.mapping.providersrepository.disabled"
        //     value: "false"
        // }
        // PluginParameter {
        //     name: "osm.mapping.providersrepository.address"
        //     // value: "http://maps-redirect.qt.io/osm/5.8/"
        //     // value: "https://tile.thunderforest.com/cycle/"
        //     // value: "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/8/136/74"
        // }
        // PluginParameter { name: "osm.useragent"; value: "My great Qt OSM application" }
        // PluginParameter { name: "osm.mapping.host"; value: "http://osm.tile.server.address/" }
        // PluginParameter { name: "osm.mapping.copyright"; value: "Soko Aerial Robotics" }
        // PluginParameter { name: "osm.routing.host"; value: "http://osrm.server.address/viaroute" }
        // PluginParameter { name: "osm.geocoding.host"; value: "http://geocoding.server.address" }
        // PluginParameter { name: "osm.places.host"; value: "http://geocoding.server.address" }

        PluginParameter {
            name: "osm.mapping.providersrepository.disabled"
            value: "true"
        }
        PluginParameter {
            name: "osm.mapping.providersrepository.address"
            value: "http://maps-redirect.qt.io/osm/5.8/"
        }
    }
    property variant locationTC: QtPositioning.coordinate(7.9465, 1.0232)
    property int zoomLevel: 6

    property bool mousePressed: false
    property point lastMousePos
    Map {
        id: map
        anchors.fill: parent
        plugin: osmPlugin
        // plugin: herePlugin
        // plugin: mapbox
        center: locationTC
        zoomLevel: 6
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
    // WheelHandler {
    //     id: wheel
    //     // workaround for QTBUG-87646 / QTBUG-112394 / QTBUG-112432:
    //     // Magic Mouse pretends to be a trackpad but doesn't work with PinchHandler
    //     // and we don't yet distinguish mice and trackpads on Wayland either
    //     // acceptedDevices: Qt.platform.pluginName === "cocoa" || Qt.platform.pluginName === "wayland"
    //     // ? PointerDevice.Mouse | PointerDevice.TouchPad
    //     // : PointerDevice.Mouse
    //     rotationScale: 1/120
    //     acceptedDevices: PointerDevice.Mouse | PointerDevice.TouchPad
    //     property: "zoomLevel"

    // }
    WheelHandler {
    id: wheel
    acceptedDevices: PointerDevice.Mouse | PointerDevice.TouchPad
    rotationScale: 1/120
    property: "zoomLevel"

    // onWheel: {
        // // Calculate new zoom level
        // let newZoomLevel = map.zoomLevel + wheel.angleDelta.y / 120;

        // // Clamp zoom level within allowed range
        // newZoomLevel = Math.max(map.minimumZoomLevel, Math.min(map.maximumZoomLevel, newZoomLevel));

//         // Get the geographical coordinate at the mouse position
//         let pointerCoord = map.toCoordinate(wheel.position, false)

//         // Update the map's center to the pointer location
//         map.center = pointerCoord

//         // Update the map's zoom level
//         // map.zoomLevel = newZoomLevel;
//     }
}

    DragHandler {
        id: drag
        target: null
        onTranslationChanged: (delta) => map.pan(-delta.x, -delta.y)
    }
    Shortcut {
        enabled: map.zoomLevel < map.maximumZoomLevel
        sequence: StandardKey.ZoomIn
        onActivated: map.zoomLevel = Math.round(map.zoomLevel + 1)
    }
    Shortcut {
        enabled: map.zoomLevel > map.minimumZoomLevel
        sequence: StandardKey.ZoomOut
        onActivated: map.zoomLevel = Math.round(map.zoomLevel - 1)
    }
    Column {
        anchors.right: parent.right
        rightPadding: 5
        topPadding: 5
        spacing: 5
        Button {
            id: zoomInBtn
            text: qsTr("+")
            contentItem: Text {
                text: zoomInBtn.text
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                opacity: enabled ? 1.0 : 0.3
                color: zoomInBtn.down ? "#17a81a" : "#21be2b"
                elide: Text.ElideRight
                font.pointSize: 24
                // color: "white"
            }
            onClicked: {
                map.zoomLevel += 1
            }
            width: 50
            height: 30
            background: Rectangle {
                // color: "#8572a8"
                implicitWidth: 100
                implicitHeight: 40
                opacity: enabled ? 1 : 0.3
                border.color: zoomInBtn.down ? "#17a81a" : "#21be2b"
                border.width: 1
                radius: 2

            }
        }
        Button {
            
            id: zoomOutBtn
            text: qsTr("-")
            contentItem: Text {
                text: zoomOutBtn.text
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                opacity: enabled ? 1.0 : 0.3
                color: zoomOutBtn.down ? "#17a81a" : "#21be2b"
                elide: Text.ElideRight
                font.pointSize: 24
                // color: "white"
            }
            onClicked: {
                map.zoomLevel -= 1
            }
            width: 50
            height: 30
            background: Rectangle {
            implicitWidth: 100
            implicitHeight: 40
            opacity: enabled ? 1 : 0.3
            border.color: zoomOutBtn.down ? "#17a81a" : "#21be2b"
            border.width: 1
            radius: 2
        }

        }
    }
    // group of items that will show on the map
    MapItemGroup {
        // marker added to the map
        MapItemView {
            model: markermodel
            delegate: MapQuickItem {
                coordinate: model.position_marker
                anchorPoint.x: image.width/2
                anchorPoint.y: image.height
                sourceItem: Image {
                    id: image
                    source: model.source_marker
                }
                MouseArea {
                    propagateComposedEvents: true
                    id: markerMouseArea
                    objectName: "buttonMouseArea"
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: {
                        App.showImage(model.imgPath)
                    }
                }

                ToolTip {
                    parent: image
                    visible: markerMouseArea.containsMouse
                    text: qsTr(model.tooltip)
                    width: contentWidth + 16
                    height: contentHeight + 16

                }
            }
        }
        //                 MapItemView {
        //     model: markermodel
        //     delegate: MapQuickItem {
        //         coordinate: model.position_marker
        //         anchorPoint.x: image.width/2
        //         anchorPoint.y: image.height

        //         sourceItem: Item {
        //             id: tooltipContainer

        //             // Tooltip MouseArea
        //             MouseArea { propagateComposedEvents: true
        //                 id: markerMouseArea
        //                 objectName: "buttonMouseArea"
        //                 anchors.fill: parent
        //                 hoverEnabled: true
        //                 onClicked: {
        //                     App.showImage(model.imgPath)
        //                 }
        //             }

        //             // Tooltip Rectangle
        //             Rectangle {
        //                 id: tooltip
        //                 width: Math.min(contentWidth + 16, image.width * 0.5) // Limit width to 50% of the image width
        //                 height: Math.min(contentHeight + 16, image.height * 0.5) // Limit height to 50% of the image height
        //                 color: "lightyellow"
        //                 border.color: "black"
        //                 border.width: 1
        //                 radius: 4

        //                 // Tooltip Text
        //                 Text {
        //                     anchors.centerIn: parent
        //                     text: qsTr(model.tooltip)
        //                     font.pixelSize: 14
        //                     wrapMode: Text.Wrap
        //                 }

        //                 // Position the tooltip within the parent image
        //                 x: markerMouseArea.containsMouse ? -width - 8 : image.width + 8
        //                 y: markerMouseArea.containsMouse ? -height - 8 : image.height + 8

        //                 // Hide the tooltip when not hovered
        //                 visible: markerMouseArea.containsMouse
        //             }
        //         }
        //     }
        // }

        // path traversed by the drone
        MapItemView {
            model: dronemodel
            delegate: MapPolyline {
                line.width: 3
                line.color: "blue"
                path: model.dronePath
            }
        }

        // polygon that shows where the drone is viewing
        MapItemView {
            model: fmvmodel
            delegate: MapPolygon {
                color: "#4c98e073"
                border.color: "blue"
                border.width: 2
                path: model.polygonPoints
            }
        }
        // next four lines for the drone"s view
        MapItemView {
            model: fmvmodel
            delegate: MapPolyline {
                line.width: 1
                line.color: "blue"
                path: model.linePoints[0]
            }
        }

        MapItemView {
            model: fmvmodel
            delegate: MapPolyline {
                line.width: 2
                line.color: "blue"
                path: model.linePoints[1]
            }
        }

        MapItemView {
            model: fmvmodel
            delegate: MapPolyline {
                line.width: 2
                line.color: "blue"
                path: model.linePoints[2]
            }
        }

        MapItemView {
            model: fmvmodel
            delegate: MapPolyline {
                line.width: 2
                line.color: "blue"
                path: model.linePoints[3]
            }
        }
        // frame center line
        MapItemView {
            model: fmvmodel
            delegate: MapPolyline {
                id: framecenterline
                line.width: 3
                // line.color: "blue"
                line.color: "red"
                path: model.linePoints[4]
                MouseArea {
                    propagateComposedEvents: true
                    id: frame_center_line_mousearea
                    objectName: "buttonMouseArea"
                    anchors.fill: parent
                    hoverEnabled: true
                }

                ToolTip {
                    parent: framecenterline
                    visible: frame_center_line_mousearea.containsMouse
                    text: qsTr("Frame Center")
                }
            }
        }

        // drone marker
        MapItemView {
            model: dronemodel
            anchors.fill: parent
            delegate: MapQuickItem {
                coordinate: model.dronePosition
                anchorPoint.x: droneImg.width/2
                anchorPoint.y: droneImg.height/2
                sourceItem: Image {
                    id: droneImg
                    width: 70
                    height: 70
                    transform: Rotation {
                        origin.x: droneImg.width/2
                        origin.y: droneImg.height/2
                        angle: model.heading
                    }
                    source: model.droneIcon
                }
            }
        }
    }
    // MouseArea {
    //     propagateComposedEvents: true
    //     anchors.fill: parent
    //     onPressed: {
    //         mousePressed = true
    //         lastMousePos = Qt.point(mouse.x, mouse.y)
    //         event.accepted = true
    //     }
    //     onReleased: {
    //         mousePressed = false
    //         event.accepted = true
    //     }
    //     onPositionChanged: {
    //         if (mousePressed)
    //         {
    //             var dx = mouse.x - lastMousePos.x
    //             var dy = mouse.y - lastMousePos.y
    //             map.center = QtPositioning.coordinate(map.center.latitude - dy / map.pixelSize,
    //             map.center.longitude - dx / map.pixelSize)
    //             lastMousePos = Qt.point(mouse.x, mouse.y)
    //             event.accepted = true

    //         }
    //     }
    // }

    // Touch events (for touch devices)
    // onTouchPressed: {
    //     mousePressed = true
    //     lastMousePos = Qt.point(touchPoints[0].x, touchPoints[0].y)
    //     event.accepted = true
    // }
    // onTouchReleased: {
    //     mousePressed = false
    //     event.accepted = true
    // }
    // onTouchUpdated: {
    //     if (mousePressed && touchPoints.length === 1)
    //     {
    //         var dx = touchPoints[0].x - lastMousePos.x
    //         var dy = touchPoints[0].y - lastMousePos.y
    //         map.center = QtPositioning.coordinate(map.center.latitude - dy / map.pixelCoordinateAt(0, 0).latitudePerPixel,
    //         map.center.longitude - dx / map.pixelCoordinateAt(0, 0).longitudePerPixel)
    //         lastMousePos = Qt.point(touchPoints[0].x, touchPoints[0].y)
    //         event.accepted = true
    //     }
    // }
}
//   Map {
//         id: mapOverlay
//         anchors.fill: parent
//         plugin: Plugin { name: "itemsoverlay" }
//         // gesture.enabled: false
//         center: map.center
//         color: 'transparent' // Necessary to make this map transparent
//         minimumFieldOfView: map.minimumFieldOfView
//         maximumFieldOfView: map.maximumFieldOfView
//         minimumTilt: map.minimumTilt
//         maximumTilt: map.maximumTilt
//         minimumZoomLevel: map.minimumZoomLevel
//         maximumZoomLevel: map.maximumZoomLevel
//         zoomLevel: map.zoomLevel
//         tilt: map.tilt;
//         bearing: map.bearing
//         fieldOfView: map.fieldOfView
//         z: map.z + 1

//         MapCircle {
//             id: circle
//             center: QtPositioning.coordinate(44, 10)
//             radius: 200000
//             border.width: 5

//             MouseArea {
//                 anchors.fill: parent
//                 drag.target: parent
//             }
//         }

//         // The code below enables SSAA
//         layer.enabled: true
//         layer.smooth: true
//         property int w : mapOverlay.width
//         property int h : mapOverlay.height
//         property int pr: Screen.devicePixelRatio
//         layer.textureSize: Qt.size(w  * 2 * pr, h * 2 * pr)
//     }

ComboBox {
    id: mapTypeComboBox
    function setMapType(index)
    {
        map.activeMapType = map.supportedMapTypes[index]
    }
    model: map.supportedMapTypes.map(type => type.name)
    currentIndex: 0
    onCurrentIndexChanged: setMapType(currentIndex)
}
}