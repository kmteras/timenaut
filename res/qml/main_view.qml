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

    FontLoader {
        id: logoFont
        source: "qrc:/font/Slabo13px-Regular.ttf"
    }

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
        color: "#2C363F"

        Image {
            id: logo
            x: 8
            y: 8
            width: 64
            height: 64
            source: "qrc:/img/icon.png"
        }

        Text {
            id: logoName
            x: 8
            y: 8
            visible: false

            color: "white"

            font {
                family: logoFont.name
                pixelSize: 40
            }

            text: "timewire"
        }

        Button {
            y: 80
            text: "Home"
            onClicked: panel.visible = true
        }

        Button {
            y: 160
            text: "Overview"
            onClicked: panel.visible = false
        }

        Button {
            y: 120
            text: "Settings"
            onClicked: panel.visible = false
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
                logo.visible = false;
                logoName.visible = true;
                nav.width = 200;
            }

            onExited: {
                logo.visible = true;
                logoName.visible = false;
                nav.width = 80;
            }
        }
    }
 }
