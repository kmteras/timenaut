import QtQuick 2.2
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.12
import "qrc:/qml/fragments"


Rectangle {
    property int closedSize
    property int openSize

    id: nav
    objectName: "nav"

    width: closedSize
    height: main.height
    color: "#2C363F"

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
            nav.open();
        }

        onExited: {
            nav.close();
        }

        ColumnLayout {
            id: layout

            NavigationLogo {
                Layout.margins: 8
                id: logo
            }

            NavigationItem {
                id: dashboard
                connectedView: dashboardView
                text: "Dashboard"
                source: "qrc:/img/dashboard.svg"
            }

            NavigationItem {
                id: settings
                connectedView: settingsView
                text: "Settings"
                source: "qrc:/img/settings.svg"
            }
        }
    }

    function open() {
        nav.width = openSize;
        for (var i = 0; i < layout.children.length; i++) {
            layout.children[i].open();
        }
    }

    function close() {
        nav.width = closedSize;
        for (var i = 0; i < layout.children.length; i++) {
            layout.children[i].close();
        }
    }

    function unselectAll() {
        for (var i = 0; i < layout.children.length; i++) {
            if (layout.children[i].unselect != undefined) {
                layout.children[i].unselect()
            }
        }
    }
}
