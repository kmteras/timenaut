from typing import List

import PySide2.QtCore as QtCore
from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide2.QtGui import QColor

from timechart.core.models.process import Process
from timechart.util.util import get_formatted_time

table = None


class ProcessTableModel(QAbstractTableModel):
    def __init__(self):
        global table
        QAbstractTableModel.__init__(self)
        if table is None:
            table = self

        self.processes: List[List[Process, int]] = []

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
            time = self.processes[index.row()][self.timeRole]
            return get_formatted_time(time)

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

    @QtCore.Slot(int, result=QColor)
    def getColor(self, row: int) -> QColor:
        if row < len(self.processes):
            return QColor(self.processes[row][0].type_color)
        else:
            return QColor("black")


def process_table_model_singleton() -> ProcessTableModel:
    global table
    if table is None:
        table = ProcessTableModel()
    return table
