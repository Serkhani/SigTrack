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
    }
}
