import QtQuick 2.12
import QtQuick.Controls 2.12
import Controls 1.0

TBaseCheckBox {
    id: baseCheckBox
    property string text
    CheckBox {
        text: baseCheckBox.text
        visible: baseCheckBox.pyVisible
        checked: baseCheckBox.pyChecked
        onClicked: baseCheckBox.checkedSlot(checked)
    }
}
