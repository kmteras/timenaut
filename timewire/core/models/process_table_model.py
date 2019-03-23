from typing import List

from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt

from timewire.core.models.process import Process

table = None


class ProcessTableModel(QAbstractTableModel):
    def __init__(self):
        global table
        QAbstractTableModel.__init__(self)
        if table is None:
            table = self

        self.processes: List[List[Process, int]] = [["process", "time"], ["process", "time"]]

        self.processRole = Qt.DisplayRole
        self.timeRole = Qt.DisplayRole + 1

    def rowCount(self, index=QModelIndex()):
        return len(self.processes)

    def columnCount(self, index=QModelIndex()):
        return len(self.processes[0])

    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return None

        if section == 0:
            return "Process"
        elif section == 1:
            return "Time"

        return None

    def data(self, index=QModelIndex(), role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self.processes):
            return None

        # index.column() usually 0 (WHY?) but for getting data with it, fit it
        if index.column() != 0:
            role = index.column()

        if role == self.processRole:
            return self.processes[index.row()][self.processRole].get_process_title()
        elif role == self.timeRole:
            return self.processes[index.row()][self.timeRole]

        return None

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return False

        if index.isValid() and 0 <= index.row() < len(self.processes):
            self.processes[index.row()][index.column()] = value
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
        return {self.processRole: b"process", self.timeRole: b"time"}

    def update_data(self, data):
        # TODO: Reset ei not good, change in future
        self.beginResetModel()
        self.processes = data
        self.endResetModel()


def process_table_model_singleton() -> ProcessTableModel:
    global table
    if table is None:
        table = ProcessTableModel()
    return table
