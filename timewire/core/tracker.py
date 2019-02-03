import sys
from typing import Dict
import logging

from timewire.core.singleton import Singleton


# Change return type to custom TypedDict
class Tracker(metaclass=Singleton):
    def __init__(self):
        logging.info("Created tracker singleton")
        if sys.platform == 'linux':
            from timewire.core.linux import tracker_linux
            self.get_process_data_function = tracker_linux.get_process_data
        elif sys.platform == 'win32':
            from timewire.core.win32 import tracker_win32
            self.get_process_data_function = tracker_win32.get_process_data

    def get_process_data(self) -> Dict:
        data = self.get_process_data_function()
        logging.debug(f"Process data {data}")
        return data

    def save(self):
        logging.info("Saving tracking data")

    def load(self):
        logging.info("Loading tracking data")
