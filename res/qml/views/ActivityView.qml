import QtQuick 2.2
import QtQuick.Controls 1.0
import Views 1.0

ActivityView {
    Rectangle {
        id: panel2
        radius: 10
        width: viewArea.width
        height: viewArea.height
        color: "white"

        signal  processSelected(int row)
        signal  windowSelected(int row)

        TableView {
            id: processTable
            objectName: "processTable"
            x: 10
            y: 150
            width: parent.width / 2 - 40
            height: parent.height - 160

            horizontalScrollBarPolicy: Qt.ScrollBarAlwaysOff
            verticalScrollBarPolicy: Qt.ScrollBarAsNeeded

            model: processTableModel

            TableViewColumn {
                role: "process"
                title: "Process"
                width: processTable.width - 100
            }

            TableViewColumn {
                role: "time"
                title: "Time"
                width: 100
            }

            headerDelegate: Rectangle {
                height: textItem.implicitHeight * 1.2
                width: textItem.implicitWidth
                color: "white"

                Text {
                    id: textItem
                    anchors.fill: parent
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    text: styleData.value
                    elide: Text.ElideRight
                    renderType: Text.NativeRendering
                }
                Rectangle {
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 1
                    anchors.topMargin: 1
                    width: 1
                    color: "#ccc"
                }
            }

            itemDelegate: Rectangle {
                color: {
                    if (styleData.selected) {
                        "#ccc"
                    }
                    else {
                        "white"
                    }
                }

                Text {
                    text: styleData.value
                }
            }

            rowDelegate: Rectangle {
                color: {
                    "white"
                }
            }

            onRowCountChanged: {

            }

            onClicked: {
                processSelected(row)
            }
        }

        TableView {
            id: windowTable
            objectName: "windowTable"
            x: parent.width / 2 - 20
            y: 150
            width: parent.width / 2 + 10
            height: parent.height - 160

            horizontalScrollBarPolicy: Qt.ScrollBarAlwaysOff
            verticalScrollBarPolicy: Qt.ScrollBarAsNeeded

            model: windowTableModel

            TableViewColumn {
                role: "window"
                title: "Window"
                width: windowTable.width - 100
            }

            TableViewColumn {
                role: "time"
                title: "Time"
                width: 100
            }

            headerDelegate: Rectangle {
                height: textItem.implicitHeight * 1.2
                width: textItem.implicitWidth
                color: "white"

                Text {
                    id: textItem
                    anchors.fill: parent
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    text: styleData.value
                    elide: Text.ElideRight
                    renderType: Text.NativeRendering
                }
                Rectangle {
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 1
                    anchors.topMargin: 1
                    width: 1
                    color: "#ccc"
                }
            }

            itemDelegate: Rectangle {
                color: {
                    if (styleData.selected) {
                        "#ccc"
                    }
                    else {
                        "white"
                    }
                }

                Text {
                    text: styleData.value
                }
            }

            rowDelegate: Rectangle {
                color: {
                    "white"
                }
            }

            onRowCountChanged: {

            }

            onClicked: {
                windowSelected(row)
            }
        }
    }
}
