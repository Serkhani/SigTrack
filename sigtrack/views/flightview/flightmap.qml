import QtQuick
import QtQuick.Controls
import QtLocation
import QtPositioning
import Qt.labs.animation
import "../../views/flightview/js_file.js" as App

Rectangle {
    // visible: true
    // width: 1024
    // height: 768
    // title: "Flight Tracker"
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
    Component.onCompleted: map.resetPinchMinMax()

    Map {
        anchors.fill: parent
        id: map
        plugin: osmPlugin
        center: QtPositioning.coordinate(5.658735, -0.184961)
        zoomLevel: 2
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
            enabled: !radiusSelector.enabled
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

        // Circle to show the selected radius
        Rectangle {
            id: radiusCircle
            visible: false
            width: radius * 2
            height: radius * 2
            radius: 0
            border.color: "red"
            border.width: 2
            color: "transparent"
            x: map.center.x - radius
            y: map.center.y - radius
        }

        // MouseArea to handle radius selection
        MouseArea {
            id: radiusSelector
            anchors.fill: parent
            enabled: false
            property real startX: 0
            property real startY: 0
            property real endX: 0
            property real endY: 0
            property real radius: 0 // Radius in nautical miles
            property var centerCoordinate: map.center

            onPressed: (mouse) => {
                startX = mouse.x
                startY = mouse.y
                radiusCircle.visible = true
                radiusCircle.x = mouse.x - radiusCircle.radius
                radiusCircle.y = mouse.y - radiusCircle.radius
            }

            onPositionChanged: (mouse) => {
                endX = mouse.x
                endY = mouse.y

                // Convert pixel distance to nautical miles
                const startCoord = map.toCoordinate(Qt.point(startX, startY))
                const endCoord = map.toCoordinate(Qt.point(endX, endY))
                const distanceMeters = startCoord.distanceTo(endCoord)
                const distanceNauticalMiles = distanceMeters / 1852 // Convert meters to nautical miles
                radius = Math.min(distanceNauticalMiles, 250) // Limit radius to 250 nautical miles

                // Calculate the radius in pixels
                const radiusPixels = metersToPixels(distanceMeters, startCoord.latitude, map.zoomLevel)
                radiusCircle.radius = radiusPixels
                radiusCircle.x = startX - radiusCircle.radius
                radiusCircle.y = startY - radiusCircle.radius
            }

            onReleased: (mouse) => {
                // Calculate the center coordinate and radius
                centerCoordinate = map.toCoordinate(Qt.point(startX, startY))
                radius = Math.min(radius, 250) // Ensure radius does not exceed 250 nautical miles

                // Update the text fields
                latTextField.text = centerCoordinate.latitude.toFixed(6)
                lonTextField.text = centerCoordinate.longitude.toFixed(6)
                radiusTextField.text = radius.toFixed(2)
                
                App.update_url([latTextField.text, lonTextField.text, radiusTextField.text])

                // Hide the circle
                radiusCircle.visible = false
                radiusSelector.enabled = false
            }

            // Function to convert meters to pixels based on latitude and zoom level
            function metersToPixels(meters, latitude, zoomLevel) {
                // Earth's circumference in meters
                const earthCircumference = 40075000
                // Calculate the scale in meters per pixel
                const scale = (earthCircumference * Math.cos(latitude * Math.PI / 180)) / Math.pow(2, zoomLevel + 8)
                // Convert meters to pixels
                return meters / scale
            }
        }

        MapItemView {
            model: flightModel
            anchors.fill: parent
            delegate: MapQuickItem {
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
                            [
                                Rotation {
                                    id: rotation
                                    origin.x: droneImg.width/2
                                    origin.y: droneImg.height/2
                                    angle: model.track
                                }
                            ]
                            source:  'qrc:/drone'
                        }
                    }
}
    }

    Column {
        anchors {
            top: parent.top
            right: parent.right
            margins: 10
        }
        spacing: 10

        TextField {
            id: latTextField
            placeholderText: "Lat"
        }

        TextField {
            id: lonTextField
            placeholderText: "Lon"
        }

        TextField {
            id: radiusTextField
            placeholderText: "Radius"
        }

        Button {
            text: "Submit"
            onClicked: {
                App.update_url([latTextField.text, lonTextField.text, radiusTextField.text])
            }
        }

        // Button to enable radius selection
        Button {
            text: "Select Radius"
            enabled: !radiusSelector.enabled
            onClicked: {
                radiusSelector.enabled = true
            }
        }
    }
    ComboBox {
        id: mapTypeComboBox
        function setMapType(index) {
            map.activeMapType = map.supportedMapTypes[index]
        }
        model: map.supportedMapTypes.map(type => type.name)
        currentIndex: 0
        onCurrentIndexChanged: setMapType(currentIndex)
    }

    Column {
        anchors.top: mapTypeComboBox.bottom
        anchors.left: parent.left
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
            }
            onClicked: {
                map.zoomLevel += 1
            }
            width: 50
            height: 30
            background: Rectangle {
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
}