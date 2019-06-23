import QtQuick 2.2
import QtQuick.Controls 1.0

Rectangle {
    y: 8
    width: 100
    height: 64

    color: "transparent"

    Image {
        id: logo
        width: 64
        height: parent.height
        source: "qrc:/img/icon.png"
    }

    Text {
        id: textLogo
        width: 184
        height: parent.height
        visible: false

        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter

        color: "white"
        font.family: logoFont.name
        text: "timechart"

        // Maximize font size
        font.pointSize: 60
        fontSizeMode: Text.Fit
    }

    function open() {
        logo.visible = false;
        textLogo.visible = true;
    }

    function close() {
        logo.visible = true;
        textLogo.visible = false;
    }
}
