import logging
import sys

from PySide2.QtWidgets import QApplication

import timewire.core.database as database
from core.models.process_heartbeat import ProcessHeartbeat
from timewire.core.models.process import Process
from timewire.core.models.window import Window
from timewire.core.singleton import Singleton


class Tracker(metaclass=Singleton):
    def __init__(self):
        self.errors = False
        logging.info("Created tracker singleton")
        if sys.platform == 'linux':
            from timewire.core.linux import tracker_linux
            self.get_process_data_function = tracker_linux.get_process_data
        elif sys.platform == 'win32':
            from timewire.core.win32 import tracker_win32
            self.get_process_data_function = tracker_win32.get_process_data

        try:
            database.connect()
        except Exception as e:
            logging.error(e)
            QApplication.quit()
            self.errors = True
            return

    def get_process_data(self) -> (Process, Window):
        process, window = self.get_process_data_function()
        heartbeat = ProcessHeartbeat(process, window)
        self.track(heartbeat)
        logging.debug(f"Process data {heartbeat}")
        return process, window

    def track(self, data: ProcessHeartbeat) -> None:
        database.add_heartbeat(data)
