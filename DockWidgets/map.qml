import QtQuick 2.15
import QtQuick.Controls 2.15
import QtPositioning 5.15
import QtLocation 5.15

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
            value: "http://maps-redirect.qt.io/osm/5.6/"
        }
    }
    property variant locationTC: QtPositioning.coordinate(7.9465, 1.0232)
    Map {
        id: map
        anchors.fill: parent
        plugin: osmPlugin
        center: locationTC
        zoomLevel: 6
        MapItemView {
            model: markermodel
            delegate: MapQuickItem {
                coordinate: model.position_marker
                anchorPoint.x: image.width
                anchorPoint.y: image.height
                sourceItem: Image {
                    id: image
                    source: model.source_marker
                }
                MouseArea {
                    id: markerMouseArea
                    anchors.fill: parent
                    hoverEnabled: true
                    onClicked: {

                    }
                }

                ToolTip {
                    parent: image
                    visible: markerMouseArea.containsMouse
                    text: qsTr(model.tooltip)
                }
            }
        }
    }
} //                ToolTip.visible: hovered//                ToolTip.text: qsTr("This tool tip is shown after hovering the button for a second.")
//                    }
//            MouseArea  {
//                id: markerMouseArea
//                property int pressX : -1
//                property int pressY : -1
//                property int jitterThreshold : 10
//                property int lastX: -1
//                property int lastY: -1
//                anchors.fill: parent
//                hoverEnabled : true
//                drag.target: modelmarker

//                onPressed : {
//                    map.pressX = mouse.x
//                    map.pressY = mouse.y
//                    map.currentMarker = -1
//                    for (var i = 0; i< map.markers.length; i++){
//                        if (marker == map.markers[i]){
//                            map.currentMarker = i
//                            break
//                        }
//                    }
//                    map.state = ""
//                }

//                onPressAndHold:{
//                    if (Math.abs(map.pressX - mouse.x ) < map.jitterThreshold
//                            && Math.abs(map.pressY - mouse.y ) < map.jitterThreshold) {
//                        lastX = map.toScreenPosition(marker.coordinate).x
//                        lastY = map.toScreenPosition(marker.coordinate).y
//                        map.markerPopup()
//                    }
//                }
//            }

//                    Text{
//                        id: number
//                        y: image.height/4
//                        color: "white"
//                        font.bold: true
//                        font.pixelSize: 14
//                        width:27
//                        horizontalAlignment: Text.AlignHCenter
//                        Component.onCompleted: {
//                            text = map.markerCounter
//                        }
//                    }

//        }

