import QtQuick 2.12
import QtQuick.Controls 2.12

ComboBox {
    id: comboBox
    x: 400
    y: 90
    width: 200
    textRole: "type"
    model: typeListModel
    delegate: ItemDelegate {
            Text {
                id: typeText
                font.bold: true
                text: type
                color: itemColor
                elide: Text.ElideRight
                verticalAlignment: Text.AlignVCenter
            }
            Text {
                    id: removeButton
                    text: "X"
                    visible: typeListModel.getRemovable(index)
                    anchors.left: typeText.right
                    leftPadding: 8
                    MouseArea {
                        anchors.fill: parent
                        onClicked: { TypeDeleted(index) }
                    }
            }
    }

    contentItem: Text {
        font.bold: true
        leftPadding: 8
        text: comboBox.displayText
        color: typeListModel.getColor(comboBox.currentIndex)
        verticalAlignment: Text.AlignVCenter
    }
}
