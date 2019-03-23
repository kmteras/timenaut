import logging
import math
import os
import sys

from PySide2.QtCore import QStandardPaths

data_file_name = 'timewire.dat'
data_file_name_development = 'timewire_dev.dat'


def get_data_file_location() -> str:
    data_folder = QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)

    if not os.path.isdir(data_folder):
        logging.warning(f"{data_folder} does not exist")
        try:
            os.mkdir(data_folder)
            logging.info(f"Created directory {data_folder}")
        except OSError as e:
            logging.error(e)

    if is_debug():
        return os.path.join(data_folder, data_file_name_development)

    return os.path.join(data_folder, data_file_name)


def is_debug() -> bool:
    return not getattr(sys, 'frozen', False)


def get_formatted_time(time_int: int) -> str:
    hours = math.floor(time_int / (60 * 60))
    minutes = math.floor((time_int - hours * 60 * 60) / 60)
    seconds = time_int - hours * 60 * 60 - minutes * 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"

    if minutes > 0:
        return f"{minutes}:{seconds:02d}"

    return f"{seconds}"
