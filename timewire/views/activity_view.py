import PySide2.QtCore as QtCore
from PySide2.QtWidgets import QTableView

from timewire.core.database import get_process_data, get_window_data_by_process
from timewire.core.models.process_table_model import process_table_model_singleton
from timewire.core.models.window_table_model import window_table_model_singleton
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
        data = list(map(lambda x: [*x], get_process_data()))
        model.update_data(data)

    @QtCore.Slot(int)
    def processSelected(self, row: int):
        process_model = process_table_model_singleton()
        process = process_model.processes[row][0]
        print(process)
        window_data = get_window_data_by_process(process.id)

        window_model = window_table_model_singleton()
        window_model.update_data(window_data)


    @QtCore.Slot(int)
    def windowSelected(self, row: int):
        process_model = process_table_model_singleton()

        model = window_table_model_singleton()

        process = process_model.processes[row][0]

        print(process)

        data = get_window_data_by_process(process.id)

        model.setData(model.index(0, 0), row)
