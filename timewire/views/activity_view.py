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
        self.selected_process_id: int = None
        self.selected_window_id: int = None

        self.process_info_visible = True

        self.process_path = None
        self.process_title = None

    def componentComplete(self):
        BaseView.componentComplete(self)

    def update(self):
        BaseView.update(self)
        process_model = process_table_model_singleton()
        data = list(map(lambda x: [*x], get_process_data()))
        process_model.update_data(data)

        if self.selected_process_id is not None:
            self.update_window_model()

    def update_window_model(self):
        window_data = get_window_data_by_process(self.selected_process_id)

        window_model = window_table_model_singleton()
        window_model.update_data(window_data)

    def get_process_info_visible(self):
        return self.process_info_visible

    def set_process_info_visible(self, visible: bool):
        self.process_info_visible = visible
        self.on_process_info_visible.emit()

    def get_process_path(self):
        return self.process_path

    def set_process_path(self, text: str):
        self.process_path = text
        self.on_process_path.emit()

    def get_process_title(self):
        return self.process_title

    def set_process_title(self, text: str):
        self.process_title = text
        self.on_process_title.emit()

    @QtCore.Slot(int)
    def processSelected(self, row: int):
        process_model = process_table_model_singleton()
        process = process_model.processes[row][0]

        self.set_process_path(process.path)
        self.set_process_title(process.get_process_title())

        self.set_process_info_visible(True)

        self.selected_process_id = process.id
        self.update_window_model()

    @QtCore.Slot(int)
    def windowSelected(self, row: int):
        if row == -1:
            self.selected_window_id = None
            return

        self.set_process_info_visible(False)

        window_model = window_table_model_singleton()
        window = window_model.windows[row][0]

        self.selected_window_id = window.id

    on_process_info_visible = QtCore.Signal()

    on_process_path = QtCore.Signal()
    on_process_title = QtCore.Signal()

    processInfoVisible = QtCore.Property(bool, get_process_info_visible, notify=on_process_info_visible)
    processPath = QtCore.Property(str, get_process_path, notify=on_process_path)
    processTitle = QtCore.Property(str, get_process_title, notify=on_process_title)
