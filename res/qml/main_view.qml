import QtQuick 2.2
import QtQuick.Controls 1.0
import Graphs 1.0
import Views 1.0

MainWindow {
    id: main
    objectName: "mainWindow"
    width: 640
    height: 480
    color: "grey"

    Rectangle {
        id: panel
        x: 100
        width: 500
        height: 600
        color: "white"

        PieGraph {
            id: pieGraph
            objectName: "pieGraph"
            width: 200
            height: 200
        }

        BarGraph {
            id: barGraph
            objectName: "barGraph"
            x: 200
            width: 400
            height: 200
        }
    }

    Rectangle {
        id: nav
        objectName: "nav"

        width: 80
        height: main.height
        color: "green"

        Image {
            x: 8
            y: 8
            width: 64
            height: 64
            source: "qrc:/img/icon.png"
        }

        Button {
            y: 80
            text: "test"
            onClicked: panel.visible = false
        }

        Button {
            y: 100
            text: "test2"
            onClicked: panel.visible = true
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            propagateComposedEvents: true

            onClicked: mouse.accepted = false;
            onPressed: mouse.accepted = false;
            onReleased: mouse.accepted = false;
            onDoubleClicked: mouse.accepted = false;
            onPositionChanged: mouse.accepted = false;
            onPressAndHold: mouse.accepted = false;

            onEntered: {
                nav.width = 200;
            }

            onExited: {
                nav.width = 80;
            }
        }
    }
 }
