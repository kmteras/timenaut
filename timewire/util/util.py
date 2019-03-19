import logging
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
