from typing import List

import PySide2.QtCore as QtCore
from PySide2.QtCore import QAbstractListModel, QModelIndex, Qt
from PySide2.QtGui import QColor

from timechart.core.database import get_types

model = None


class TypeListModel(QAbstractListModel):
    def __init__(self):
        global model
        QAbstractListModel.__init__(self)
        if model is None:
            model = self

        self.types: List[List[str, QColor, bool]] = list(map(lambda x: [x[0], QColor(x[1]), x[2]], get_types()))

    def rowCount(self, index=QModelIndex()):
        return len(self.types)

    def data(self, index=QModelIndex(), role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self.types):
            return None

        if role == Qt.DisplayRole:
            return self.types[index.row()][0]
        elif role == Qt.DecorationRole:
            return self.types[index.row()][1]

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return False

        if index.isValid() and 0 <= index.row() < len(self.types):
            self.types[index.row()] = value
            self.dataChanged.emit(index, value)
            return True

        return False

    def insertRows(self, row: int, count: int = 1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        self.endInsertRows()
        return True

    def flags(self, index=QModelIndex()):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFrags(QAbstractListModel.flags(self, index) | Qt.ItemIsEditable)

    def roleNames(self):
        return {Qt.DisplayRole: b"type", Qt.DecorationRole: b"itemColor"}

    def update_data(self, data):
        # TODO: Reset ei not good, change in future
        self.beginResetModel()
        self.types = data
        self.endResetModel()

    @QtCore.Slot(int, result=QColor)
    def getColor(self, row: int) -> QColor:
        return self.types[row][1]

    @QtCore.Slot(int, result=bool)
    def getRemovable(self, row: int) -> bool:
        return self.types[row][2] == "true"

    def find(self, type_str: str) -> int:
        if type_str is None:
            return -1

        for index, type_el in enumerate(self.types):
            if type_el[0] == type_str:
                return index

        return -1


def type_list_model_singleton() -> TypeListModel:
    global model
    if model is None:
        model = TypeListModel()
    return model
