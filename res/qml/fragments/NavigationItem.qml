import QtQuick 2.2
import QtQuick.Controls 1.0
import QtGraphicalEffects 1.0

Rectangle {
    property string source
    property string text
    property color defaultColor: "white"
    property color hoverColor: "black"
    property color textColor
    property var connectedView

    textColor: defaultColor
    id: item
    width: 80
    height: 64
    color: "transparent"

    Image {
        id: icon
        x: 16
        y: 8
        width: 48
        height: 48
        source: item.source
        sourceSize.width: parent.width
        sourceSize.height: parent.width
    }

    ColorOverlay {
        anchors.fill: icon
        source: icon
        color: item.textColor
        transform: rotation
        antialiasing: true
    }

    Text {
        id: itemText
        x: 64
        y: 14
        width: 184
        height: 36
        visible: false

        verticalAlignment: Text.AlignVCenter

        color: item.textColor
        text: item.text

        // Maximize font size
        font.pointSize: 18
        fontSizeMode: Text.Fit
    }

    function open() {
        itemText.visible = true;
        width = nav.openSize;
    }

    function close() {
        itemText.visible = false;
        width = nav.closedSize;
    }

    function hover() {
        textColor = hoverColor;
    }

    function noHover() {
        textColor = defaultColor;
    }

    function select() {
        nav.unselectAll();
        connectedView.visible = true;
    }

    function unselect() {
        connectedView.visible = false;
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true

        propagateComposedEvents: true

        onClicked: {
            select();
        }

        // Hover
        onEntered: {
            hover();
        }

        // Disable hover
        onExited: {
            noHover();
        }
    }
}
