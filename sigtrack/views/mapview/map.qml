import QtQuick
import QtQuick.Controls.Basic
import QtPositioning
import QtLocation
import Qt.labs.animation
import "../../views/mapview/application.js" as App

Rectangle {
    id: rectangle
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
        id: map
        anchors.fill: parent
        plugin: osmPlugin
        center: QtPositioning.coordinate(5.658735, -0.184961)

        width: parent.width
        height: parent.height
        tilt: tiltHandler.persistentTranslation.y / -5
        property bool pinchAdjustingZoom: false
        BoundaryRule on zoomLevel {
            id: br
            minimum: map.minimumZoomLevel
            maximum: map.maximumZoomLevel
        }
        onZoomLevelChanged: {
            br.returnToBounds();
            if (!pinchAdjustingZoom) resetPinchMinMax()
        }

        function resetPinchMinMax() {
            pinch.persistentScale = 1
            pinch.scaleAxis.minimum = Math.pow(2, parent.minimumZoomLevel - map.zoomLevel + 1)
            pinch.scaleAxis.maximum = Math.pow(2, parent.maximumZoomLevel - map.zoomLevel - 1)
        }

        PinchHandler {
            id: pinch
            target: null
            property real rawBearing: 0
            property geoCoordinate startCentroid
            onActiveChanged: if (active) {
                flickAnimation.stop()
                pinch.startCentroid = map.toCoordinate(pinch.centroid.position, false)
            } else {
                flickAnimation.restart(centroid.velocity)
                map.resetPinchMinMax()
            }
            onScaleChanged: (delta) => {
                map.pinchAdjustingZoom = true
                map.zoomLevel += Math.log2(delta)
                map.alignCoordinateToPoint(pinch.startCentroid, pinch.centroid.position)
                map.pinchAdjustingZoom = false
            }
            onRotationChanged: (delta) => {
                pinch.rawBearing -= delta
                // snap to 0° if we're close enough
                map.bearing = (Math.abs(pinch.rawBearing) < 5) ? 0 : pinch.rawBearing
                map.alignCoordinateToPoint(pinch.startCentroid, pinch.centroid.position)
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
            onWheel: (event) => {
                const loc = map.toCoordinate(wheel.point.position)
                switch (event.modifiers) {
                    case Qt.NoModifier:
                        map.zoomLevel += event.angleDelta.y / 120
                        break
                    case Qt.ShiftModifier:
                        map.bearing += event.angleDelta.y / 15
                        break
                    case Qt.ControlModifier:
                        map.tilt += event.angleDelta.y / 15
                        break
                }
                map.alignCoordinateToPoint(loc, wheel.point.position)
            }
        }
        DragHandler {
            id: drag
            signal flickStarted // for autotests only
            signal flickEnded
            target: null
            onTranslationChanged: (delta) => map.pan(-delta.x, -delta.y)
            onActiveChanged: if (active) {
                flickAnimation.stop()
            } else {
                flickAnimation.restart(centroid.velocity)
            }
        }

        property vector3d animDest
        onAnimDestChanged: if (flickAnimation.running) {
            const delta = Qt.vector2d(animDest.x - flickAnimation.animDestLast.x, animDest.y - flickAnimation.animDestLast.y)
            map.pan(-delta.x, -delta.y)
            flickAnimation.animDestLast = animDest
        }

        Vector3dAnimation on animDest {
            id: flickAnimation
            property vector3d animDestLast
            from: Qt.vector3d(0, 0, 0)
            duration: 500
            easing.type: Easing.OutQuad
            onStarted: drag.flickStarted()
            onStopped: drag.flickEnded()

            function restart(vel) {
                stop()
                map.animDest = Qt.vector3d(0, 0, 0)
                animDestLast = Qt.vector3d(0, 0, 0)
                to = Qt.vector3d(vel.x / duration * 100, vel.y / duration * 100, 0)
                start()
            }
        }

        DragHandler {
            id: tiltHandler
            minimumPointCount: 2
            maximumPointCount: 2
            target: null
            xAxis.enabled: false
            grabPermissions: PointerHandler.TakeOverForbidden
            onActiveChanged: if (active) flickAnimation.stop()
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
}

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