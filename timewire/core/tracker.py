import json
import logging
import sys
from datetime import datetime
from typing import Dict

from timewire.core.process_heartbeat import ProcessHeartbeat
from timewire.core.singleton import Singleton
from timewire.core.tracker_serializer import TrackerEncoder, TrackerDecoder
from timewire.util.util import get_data_file_location


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

        self.tracking_data = {}
        self.load()

    def get_process_data(self) -> Dict:
        data = self.get_process_data_function()
        heartbeat = ProcessHeartbeat(data)
        self.track(heartbeat)
        logging.debug(f"Process data {heartbeat}")
        return data

    def track(self, data: ProcessHeartbeat):
        time_string = datetime.today().strftime("%d-%m-%Y")

        if time_string not in self.tracking_data:
            self.tracking_data[time_string] = []

        self.tracking_data[time_string].append(data)

    def save(self):
        file_location = get_data_file_location()
        logging.info(f"Saving tracking data to {file_location}")

        with open(file_location, 'w') as file:
            file.write(json.dumps(self.tracking_data, cls=TrackerEncoder))

        logging.info("Saving finished")

    def load(self):
        file_location = get_data_file_location()
        logging.info(f"Loading tracking data from {file_location}")

        try:
            with open(file_location, 'r') as file:
                file_data = file.read()
                data = json.loads(file_data, cls=TrackerDecoder)
                self.tracking_data = data
                logging.debug(self.tracking_data)
        except FileNotFoundError as e:
            logging.info(f"{file_location} does not exist, not loading anything")
        except json.JSONDecodeError as e:
            logging.error(f"Error loading file data: {e}")
            # TODO: Make backup of corrupted file

        logging.info("Loading finished")
