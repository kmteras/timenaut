import logging
import sys

import timechart.core.database as database
from timechart.core.models.process_heartbeat import ProcessHeartbeat
from timechart.core.models.process import Process
from timechart.core.models.window import Window
from timechart.core.singleton import Singleton
from timechart.core.idle_detector import IdleDetector


class Tracker(metaclass=Singleton):
    def __init__(self):
        self.errors = False

        logging.info("Created tracker singleton")
        if sys.platform == 'linux':
            from timechart.core.linux import tracker_linux
            self.get_process_data_function = tracker_linux.get_process_data
        elif sys.platform == 'win32':
            from timechart.core.win32 import tracker_win32
            self.get_process_data_function = tracker_win32.get_process_data

    def get_process_data(self) -> (Process, Window):
        process, window = self.get_process_data_function()
        heartbeat = ProcessHeartbeat(process, window, idle=IdleDetector().is_idle())
        self.track(heartbeat)
        logging.debug(f"Process data {heartbeat}")

    def track(self, data: ProcessHeartbeat) -> None:
        database.add_heartbeat(data)
