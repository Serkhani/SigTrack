import QtQuick 2.15
import QtQuick.Controls 2.15
import QtPositioning 5.15
import QtLocation 5.15
import "application.js" as App

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
    property int zoomLevel: 6
        Map {
            id: map
            anchors.fill: parent
            plugin: osmPlugin
            center: locationTC
            zoomLevel: 6
            Column {
                anchors.right: parent.right
                rightPadding: 5
                topPadding: 5
                spacing: 5
                Button {
                    contentItem: Text {
                        text: '+'
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        font.pointSize: 24
                        color: "white"
                    }
                    onClicked: {
                        map.zoomLevel += 1
                    }
                    width: 50
                    height: 30
                    background: Rectangle {
                        color: "#8572a8"
                    }
                }
                Button {
                    contentItem: Text {
                        text: '-'
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        font.pointSize: 24
                        color: "white"
                    }
                    onClicked: {
                        map.zoomLevel -= 1
                    }
                    width: 50
                    height: 30
                    background: Rectangle {
                        color: "#8572a8"
                    }
                }
            }

            MapItemGroup {

                MapItemView {
                    model: markermodel
                    delegate: MapQuickItem {
                        coordinate: model.position_marker
                        anchorPoint.x: image.width/2
                        anchorPoint.y: image.height/2
                        sourceItem: Image {
                            id: image
                            source: model.source_marker
                        }
                        MouseArea {
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
                        }
                    }
                }


                MapItemView {
                    model: dronemodel
                    delegate: MapPolyline {
                        line.width: 3
                        line.color: 'blue'
                        path: model.dronePath
                    }
                }
                MapItemView {
                    model: dronemodel
                    delegate: MapQuickItem {
                        coordinate: model.dronePosition
                        anchorPoint.x: droneImg.width/2
                        anchorPoint.y: droneImg.height/2
                        sourceItem: Image {
                            id: droneImg
                            source: model.droneIcon
                        }
                    }
                }
            }
        }
    }
