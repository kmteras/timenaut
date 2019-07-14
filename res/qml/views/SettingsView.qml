import QtQuick 2.2
import QtQuick.Controls 2.0
import Graphs 1.0
import Views 1.0
import Controls 1.0
import "qrc:/qml/components"

SettingsView {
    Rectangle {
        id: panel2
        radius: 10
        width: viewArea.width
        height: viewArea.height
        color: "white"

        TCheckBox {
            id: autostartCheckbox
            objectName: "autostartCheckbox"
            x: 20
            y: 20
            text: "Run up system startup"
        }
    }
}
