import PySide2.QtCore as QtCore
from PySide2.QtWidgets import QTableView

import timechart.core.database as database
from timechart.core.database import get_process_data, get_window_data_by_process, get_types
from timechart.core.models.process import Process
from timechart.core.models.process_table_model import process_table_model_singleton
from timechart.core.models.type_list_model import type_list_model_singleton
from timechart.core.models.window import Window
from timechart.core.models.window_table_model import window_table_model_singleton
from timechart.util.util import get_formatted_time
from timechart.views.base_view import BaseView


class ActivityView(BaseView):
    def __init__(self):
        BaseView.__init__(self)
        self.process_table: QTableView = None
        self.window_table: QTableView = None
        self.selected_process: Process = None
        self.selected_window: Window = None

        self.selected_process_row = None
        self.selected_window_row = None

        self.process_info_visible = False
        self.window_info_visible = False

        self.window_name = None

        self.view_time = None

        self.process_path = None
        self.process_title = None

    def componentComplete(self):
        BaseView.componentComplete(self)

    def update(self):
        BaseView.update(self)
        process_model = process_table_model_singleton()
        data = list(map(lambda x: [*x], get_process_data()))
        process_model.update_data(data)

        type_model = type_list_model_singleton()
        data = list(map(lambda x: [*x], get_types()))
        type_model.update_data(data)


        if self.selected_process is not None:
            self.update_window_model()

        if self.selected_window_row is not None:
            window_model = window_table_model_singleton()
            self.set_view_time(get_formatted_time(window_model.windows[self.selected_window_row][1]))
        elif self.selected_process_row is not None:
            self.set_view_time(get_formatted_time(process_model.processes[self.selected_process_row][1]))

    def update_window_model(self):
        window_data = get_window_data_by_process(self.selected_process.id)

        window_model = window_table_model_singleton()
        window_model.update_data(window_data)

    def get_process_info_visible(self):
        return self.process_info_visible

    def set_process_info_visible(self, visible: bool):
        self.process_info_visible = visible
        self.on_process_info_visible.emit()

    def get_window_info_visible(self):
        return self.window_info_visible

    def set_window_info_visible(self, visible: bool):
        self.window_info_visible = visible
        self.on_window_info_visible.emit()

    def get_view_time(self):
        return self.view_time

    def set_view_time(self, time: str):
        self.view_time = time
        self.on_view_time.emit()

    def get_window_name(self):
        return self.window_name

    def set_window_name(self, name: str):
        self.window_name = name
        self.on_window_name.emit()

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
        self.set_window_info_visible(False)

        self.selected_process = process
        self.selected_process_row = row
        self.update_window_model()

        self.set_view_time(get_formatted_time(process_model.processes[row][1]))

        type_model = type_list_model_singleton()
        self.set_process_type.emit(type_model.find(process.type_str))

    @QtCore.Slot(int)
    def windowSelected(self, row: int):
        if row == -1:
            self.selected_window = None
            self.selected_window_row = None
            return

        window_model = window_table_model_singleton()
        window = window_model.windows[row][0]

        self.set_window_name(window.title)

        self.set_process_info_visible(False)
        self.set_window_info_visible(True)

        self.selected_window = window

        self.selected_window_row = row
        window_time = window_model.windows[row][1]
        self.set_view_time(get_formatted_time(window_time))

        type_model = type_list_model_singleton()
        self.set_window_type.emit(type_model.find(window.type_str))

    @QtCore.Slot(int)
    def processTypeSelected(self, row: int):
        type_model = type_list_model_singleton()
        type_str = type_model.types[row][0]
        if type_str == "new":
            self.new_type_created.emit()
            print("new!")
        else:
            database.set_process_type(self.selected_process.id, type_str)
        self.update()

    @QtCore.Slot(int)
    def windowTypeSelected(self, row: int):
        type_model = type_list_model_singleton()
        database.set_window_type(self.selected_window.id, type_model.types[row][0])
        self.update()

    @QtCore.Slot(int)
    def TypeDeleted(self, row: int):
        type_model = type_list_model_singleton()
        database.delete_type(type_model.types[row][0])
        self.update()

    on_process_info_visible = QtCore.Signal()
    on_window_info_visible = QtCore.Signal()

    on_view_time = QtCore.Signal()
    on_window_name = QtCore.Signal()
    on_process_path = QtCore.Signal()
    on_process_title = QtCore.Signal()

    set_process_type = QtCore.Signal(int)
    set_window_type = QtCore.Signal(int)

    new_type_created = QtCore.Signal()

    processInfoVisible = QtCore.Property(bool, get_process_info_visible, notify=on_process_info_visible)
    windowInfoVisible = QtCore.Property(bool, get_window_info_visible, notify=on_window_info_visible)

    viewTime = QtCore.Property(str, get_view_time, notify=on_view_time)
    windowName = QtCore.Property(str, get_window_name, notify=on_window_name)
    processPath = QtCore.Property(str, get_process_path, notify=on_process_path)
    processTitle = QtCore.Property(str, get_process_title, notify=on_process_title)
