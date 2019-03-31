import QtQuick 2.12
import QtQuick.Controls 2.12

ComboBox {
    id: comboBox
    x: 400
    y: 90
    textRole: "type"
    model: typeListModel
    delegate: ItemDelegate {
        contentItem: Text {
            font.bold: true
            text: type
            color: itemColor
            elide: Text.ElideRight
            verticalAlignment: Text.AlignVCenter
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
