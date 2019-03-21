import PySide2.QtCore as QtCore
from PySide2.QtWidgets import QTableView

from timewire.core.database import get_process_data
from timewire.core.models.process_table_model import process_table_model_singleton
from timewire.views.base_view import BaseView


class ActivityView(BaseView):
    def __init__(self):
        BaseView.__init__(self)
        self.process_table: QTableView = None
        self.window_table: QTableView = None

    def componentComplete(self):
        BaseView.componentComplete(self)
        # self.process_table: QTableView = QTableView(self.findChild(QObject, "processTable"))
        # print(self.process_table)
        # self.window_table: QTableView = self.findChild(QQuickItem, "windowTable")

    def update(self):
        BaseView.update(self)
        model = process_table_model_singleton()
        process_data = list(
            map(lambda process_tuple: [process_tuple[0].get_process_title(), process_tuple[1]], get_process_data()))
        model.update_data(process_data)
        print(process_data)


    @QtCore.Slot(int)
    def processSelected(self, row: int):
        print(row)
        model = process_table_model_singleton()
        model.setData(model.index(0, 0), row)
