import logging
import os
import signal
import sys

from PySide2.QtCore import Qt, QCoreApplication
from PySide2.QtGui import QFont
from PySide2.QtQml import QQmlApplicationEngine, qmlRegisterType
from PySide2.QtQuick import QQuickWindow
from PySide2.QtWidgets import QApplication

import timechart.core.database as database
from timechart.core.models.process_table_model import process_table_model_singleton
from timechart.core.models.type_list_model import type_list_model_singleton
from timechart.core.models.window_table_model import window_table_model_singleton
from timechart.util.util import is_debug
from timechart.views.activity_view import ActivityView
from timechart.views.bar_graph import BarGraph
from timechart.views.dashboard_view import DashboardView
from timechart.views.main_window import MainWindow
from timechart.views.pie_graph import PieGraph
from timechart.views.settings_view import SettingsView
from timechart.views.timeline_graph import TimelineGraph


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    application = QApplication()
    application.setApplicationName("Timechart")

    logging.info(f"Scene graph backend: {QQuickWindow.sceneGraphBackend()}")

    logging.info(f"System default font: {QFont().defaultFamily()}")

    montserrat = QFont("qrc:/font/Montserrat-Regular.ttf")
    montserrat.setPointSizeF(12)

    logging.info(f"Application font: {montserrat.family()}")

    QApplication.setFont(montserrat)

    # Database setup
    try:
        database.connect()
    except Exception as e:
        logging.error(e)
        QApplication.quit()
        return

    try:
        qmlRegisterType(PieGraph, "Graphs", 1, 0, "PieGraph")
        qmlRegisterType(BarGraph, "Graphs", 1, 0, "BarGraph")
        qmlRegisterType(TimelineGraph, "Graphs", 1, 0, "TimelineGraph")

        qmlRegisterType(MainWindow, "Views", 1, 0, "MainWindow")
        qmlRegisterType(DashboardView, "Views", 1, 0, "DashboardViewBase")
        qmlRegisterType(ActivityView, "Views", 1, 0, "ActivityView")
        qmlRegisterType(SettingsView, "Views", 1, 0, "SettingsView")

        qml = QQmlApplicationEngine()

        qml.rootContext().setContextProperty("processTableModel", process_table_model_singleton())
        qml.rootContext().setContextProperty("windowTableModel", window_table_model_singleton())
        qml.rootContext().setContextProperty("typeListModel", type_list_model_singleton())

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


logging_format = '%(asctime)s %(levelname)s %(name)s: %(message)s'
debugging_logging_format = '%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(name)s: %(message)s'
base_dir = os.path.abspath(os.path.dirname(__file__))
logging_file = os.path.join(base_dir, 'timechart.log')

if __name__ == "__main__":
    os.putenv("QT_SCALE_FACTOR", "1")

    if is_debug():
        logging.basicConfig(
            level=logging.DEBUG,
            handlers=[
                logging.StreamHandler()
            ],
            format=debugging_logging_format)
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
        import timechart.resources as res

    if not res:
        logging.error("Resources file could not be opened")
    else:
        logging.info("Resources loaded")

    main()
