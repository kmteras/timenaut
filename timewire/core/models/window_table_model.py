from typing import List

from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt

from timewire.core.models.window import Window

table = None


class WindowTableModel(QAbstractTableModel):
    def __init__(self):
        global table
        QAbstractTableModel.__init__(self)
        if table is None:
            table = self

        self.windows: List[List[Window, int]] = []

        self.windowRole = Qt.DisplayRole
        self.timeRole = Qt.DisplayRole + 1

    def rowCount(self, index=QModelIndex()):
        return len(self.windows)

    def columnCount(self, index=QModelIndex()):
        return len(self.windows[0])

    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return None

        if section == 0:
            return "Window"
        elif section == 1:
            return "Time"

        return None

    def data(self, index=QModelIndex(), role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self.windows):
            return None

        # index.column() usually 0 (WHY?) but for getting data with it, fit it
        if index.column() != 0:
            role = index.column()

        if role == self.windowRole:
            return self.windows[index.row()][self.windowRole].title
        elif role == self.timeRole:
            return self.windows[index.row()][self.timeRole]

        return None

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return False

        if index.isValid() and 0 <= index.row() < len(self.windows):
            self.windows[index.row()][index.column()] = value
            self.dataChanged.emit(index, value)
            return True

        return False

    def insertRows(self, row: int, count: int = 1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        self.endInsertRows()
        return True

    def insertColumns(self, column: int, count: int = 1, index=QModelIndex):
        self.beginInsertColumns(QModelIndex, column, column + count - 1)
        self.endInsertColumns()
        return True

    def flags(self, index=QModelIndex()):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFrags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)

    def roleNames(self):
        return {self.windowRole: b"window", self.timeRole: b"time"}

    def update_data(self, data):
        # TODO: Reset ei not good, change in future
        self.beginResetModel()
        self.windows = data
        self.endResetModel()


def window_table_model_singleton() -> WindowTableModel:
    global table
    if table is None:
        table = WindowTableModel()
    return table
