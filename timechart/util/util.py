import logging
import os
import sys

import math
from PySide2.QtCore import QStandardPaths

data_file_name = 'timechart.dat'
data_file_name_development = 'timechart_dev.dat'


def get_application_name() -> str:
    return "timechart"


def get_user_data_location() -> str:
    current_snap_app = os.environ.get("SNAP_INSTANCE_NAME")
    if current_snap_app == get_application_name():
        return os.environ.get("SNAP_USER_DATA")
    else:
        return QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)


def get_data_location() -> str:
    current_snap_app = os.environ.get("SNAP_INSTANCE_NAME")
    if current_snap_app == get_application_name():
        return os.environ.get("SNAP_DATA")
    else:
        return QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)


def get_data_file_location() -> str:
    data_folder = get_user_data_location()

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
