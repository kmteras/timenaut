import PySide2.QtCore as QtCore
from PySide2.QtQuick import QQuickItem


class TCheckBox(QQuickItem):
    def __init__(self):
        QQuickItem.__init__(self)
        self._visible: bool = True
        self._checked: bool = False
        self.on_checked = lambda x: None

    def set_visible(self, value: bool):
        self._visible = value
        self.visible_changed.emit()

    def get_visible(self):
        return self._visible

    @QtCore.Slot(bool)
    def checkedSlot(self, value: bool):
        self._checked = value
        self.on_checked(value)

    def set_checked(self, value: bool):
        self._checked = value
        self.checked_changed.emit()

    def get_checked(self):
        return self._checked

    visible = property(get_visible, set_visible)
    checked = property(get_checked, set_checked)

    visible_changed = QtCore.Signal()
    checked_changed = QtCore.Signal()
    pyVisible = QtCore.Property(bool, get_visible, notify=visible_changed)
    pyChecked = QtCore.Property(bool, get_checked, notify=checked_changed)
