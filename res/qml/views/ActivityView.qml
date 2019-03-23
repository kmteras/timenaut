import QtQuick 2.2
import QtQuick.Controls 1.0
import Views 1.0

ActivityView {
    id: activityView

    Rectangle {

        Rectangle {
            visible: activityView.processInfoVisible

            Text {
                x: 10
                y: 10
                text: "Path:"
            }

            Text {
                x: 10
                y: 30
                text: activityView.processPath
            }

            Text {
                x: 10
                y: 70
                text: "Process:"
            }

            Text {
                x: 10
                y: 90
                text: activityView.processTitle
            }
        }

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

                delegate: Rectangle {
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
                        color: "red"
                        horizontalAlignment: Text.AlignRight
                        verticalAlignment: Text.AlignRight
                    }
                }
            }

            TableViewColumn {
                role: "time"
                title: "Time"
                width: 100

                delegate: Rectangle {
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
                        horizontalAlignment: Text.AlignRight
                        verticalAlignment: Text.AlignRight
                    }
                }
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

            rowDelegate: Rectangle {
                color: {
                    "white"
                }
            }

            onRowCountChanged: {

            }

            onClicked: {
                windowTable.selection.clear()
                processSelected(row)
                windowSelected(-1)
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
