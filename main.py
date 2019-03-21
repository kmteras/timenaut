import logging
import os
import signal
import sys

from PySide2.QtGui import QFont
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide2.QtQuick import QQuickWindow
from PySide2.QtWidgets import QApplication

import timewire.core.database as database
from timewire.util.util import is_debug
from timewire.views.activity_view import ActivityView
from timewire.views.bar_graph import BarGraph
from timewire.views.dashboard_view import DashboardView
from timewire.views.main_window import MainWindow
from timewire.views.pie_graph import PieGraph
from timewire.views.settings_view import SettingsView
from timewire.views.timeline_graph import TimelineGraph
from timewire.core.models.process_table_model import ProcessTableModel, process_table_model_singleton


def main():
    application = QApplication()
    application.setApplicationName("Timewire")

    logging.info(f"Screne graph backend: {QQuickWindow.sceneGraphBackend()}")

    montserrat = QFont("qrc:/font/Montserrat-Regular.ttf")
    application.setFont(montserrat)

    try:
        database.connect()
        qmlRegisterType(PieGraph, "Graphs", 1, 0, "PieGraph")
        qmlRegisterType(BarGraph, "Graphs", 1, 0, "BarGraph")
        qmlRegisterType(TimelineGraph, "Graphs", 1, 0, "TimelineGraph")

        qmlRegisterType(MainWindow, "Views", 1, 0, "MainWindow")
        qmlRegisterType(DashboardView, "Views", 1, 0, "DashboardViewBase")
        qmlRegisterType(ActivityView, "Views", 1, 0, "ActivityView")
        qmlRegisterType(SettingsView, "Views", 1, 0, "SettingsView")

        qml = QQmlApplicationEngine()

        m = ProcessTableModel()
        qml.rootContext().setContextProperty("processTableModel", m)

        qml.load("qrc:/qml/main_view.qml")

        win = qml.rootObjects()[0]
        win.show()
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

    res = None

    if is_debug():
        import subprocess

        current_dir = os.path.dirname(os.path.realpath(__file__))

        build_resources_command = [
            'pyside2-rcc',
            f'{os.path.join(os.path.dirname(os.path.realpath(__file__)), "res", "resources.qrc")}',
            '-o', 'resources.py'
        ]

        # To disable qml caching and not being able to update qml files without removing cache files every time
        os.putenv("QML_DISABLE_DISK_CACHE", "true")

        subprocess.run(build_resources_command)
        import resources as res
    else:
        import timewire.resources as res

    if not res:
        logging.error("Resources file could not be opened")
    else:
        logging.info("Resources loaded")

    main()
