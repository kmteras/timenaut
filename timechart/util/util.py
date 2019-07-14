import logging
import math
import os
import sys
from shutil import copy

from PySide2.QtCore import QStandardPaths

data_file_name = 'timechart.dat'
data_file_name_development = 'timechart_dev.dat'
program_location = ''


def get_application_name() -> str:
    return "timechart"


def is_snap() -> bool:
    current_snap_app = os.environ.get("SNAP_INSTANCE_NAME")
    return current_snap_app == get_application_name()


def get_user_data_location() -> str:
    if is_snap():
        return os.environ.get("SNAP_USER_DATA")
    else:
        return QStandardPaths.writableLocation(QStandardPaths.AppLocalDataLocation)


def get_auto_start_file_location() -> str:
    return os.path.join(get_user_data_location(), '.config', 'autostart', 'timechart.desktop')


def get_program_location() -> str:
    return program_location


def set_program_location(value: str) -> None:
    global program_location
    program_location = value


def set_auto_start(value: bool):
    if sys.platform != 'linux':
        return

    if value:
        # Set program to start on boot
        logging.info("Enabled start on boot")
        config_dir = os.path.join(get_user_data_location(), '.config')
        if not os.path.isdir(config_dir):
            try:
                os.mkdir(config_dir)
                logging.info(f"Created directory {config_dir}")
            except OSError as e:
                logging.error(e)

        autostart_dir = os.path.join(config_dir, 'autostart')
        if not os.path.isdir(autostart_dir):
            try:
                os.mkdir(autostart_dir)
                logging.info(f"Created directory {autostart_dir}")
            except OSError as e:
                logging.error(e)

        copy(os.path.join(get_program_location(), 'share', 'application', 'timechart.desktop'),
             get_auto_start_file_location())
    else:
        # Set program to not start on boot
        logging.info("Disabled start on boot")
        if os.path.exists(get_auto_start_file_location()):
            os.remove(get_auto_start_file_location())


def get_auto_start() -> bool:
    if sys.platform == 'linux':
        return os.path.isfile(get_auto_start_file_location())
    return False


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
