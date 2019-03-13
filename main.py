import logging
import os
import signal
import sys

import pkg_resources
from PySide2.QtCore import QUrl, QByteArray
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide2.QtWidgets import QApplication

import timewire.core.database as database
from timewire.util.util import is_debug
from timewire.views.bar_graph import BarGraph
from timewire.views.main_window import MainWindow
from timewire.views.pie_graph import PieGraph


def main():
    application = QApplication()
    application.setApplicationName("Timewire")

    try:
        database.connect()
        qmlRegisterType(PieGraph, "Graphs", 1, 0, "PieGraph")
        qmlRegisterType(BarGraph, "Graphs", 1, 0, "BarGraph")
        qmlRegisterType(MainWindow, "Views", 1, 0, "MainWindow")

        qml = QQmlApplicationEngine()
        with open(pkg_resources.resource_filename('res.qml', 'main_view.qml'), 'r') as style:
            qml.loadData(QByteArray(bytes(style.read(), "utf-8")))
        win = qml.rootObjects()[0]
        win.show()
        win.init()
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
