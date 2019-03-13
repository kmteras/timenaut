import logging
import os
import signal
import sys

import pkg_resources
from PySide2.QtCore import QByteArray
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine
from timewire.util.util import is_debug
from timewire.views.main_window import MainWindow


def main():
    application = QApplication()
    application.setApplicationName("Timewire")

    try:
        qml = QQmlApplicationEngine()
        with open(pkg_resources.resource_filename('res.qml', 'main_view.qml'), 'r') as style:
            qml.loadData(QByteArray(bytes(style.read(), "utf-8")))
        win = qml.rootObjects()[0]
        win.show()

        # main_window = MainWindow()
        # main_window.show()
    except Exception as e:
        logging.error(e)
        QApplication.quit()
        return

    # TODO: Maybe not use tracking timer and create a empty timer to process the signal
    signal.signal(signal.SIGINT, quit_signal)

    sys.exit(application.exec_())


def quit_signal(signum, frame):
    QApplication.quit()


logging_format = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'

base_dir = os.path.abspath(os.path.dirname(__file__))
logging_file = os.path.join(base_dir, 'timewire.log')

if __name__ == "__main__":
    if is_debug():
        logging.basicConfig(
            level=logging.DEBUG,
            handlers=[
                logging.FileHandler(logging_file),
                logging.StreamHandler()
            ],
            format=logging_format)
    else:
        logging.basicConfig(
            level=logging.INFO,
            handlers=[
                logging.FileHandler(logging_file)
            ],
            format=logging_format)

    logging.info(os.path.abspath(os.path.dirname(__file__)))

    main()
