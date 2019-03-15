import PySide2.QtCore as QtCore
from PySide2.QtCore import SIGNAL
from PySide2.QtGui import QIcon, QCloseEvent, QFocusEvent, QWindow
from PySide2.QtQuick import QQuickView
from PySide2.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication

from timewire.core.database import get_window_data, get_process_data
from timewire.core.tracker import Tracker
from timewire.util.util import is_debug
from timewire.views.bar_graph import BarGraph
from timewire.views.pie_graph import PieGraph


class MainWindow(QQuickView):
    def __init__(self):
        QQuickView.__init__(self)
        self.toggle_show_action = None
        self.quit_action = None
        self.tray_menu = None
        self.tray_icon = None

        if is_debug():
            self.icon = QIcon(":/img/icon_debug.png")
        else:
            self.icon = QIcon(":/img/icon.png")

        self.setIcon(self.icon)
        self.create_tray()

        self.update_timer = QtCore.QTimer()
        self.connect(self.update_timer, SIGNAL("timeout()"), self.heartbeat)

        self.update_timer.start(1000)

        self.bar_graph: BarGraph = None
        self.pie_graph: PieGraph = None

        if Tracker().errors:
            raise Exception("Tracker initialization had errors")

    def init(self):
        self.bar_graph: BarGraph = self.findChild(BarGraph, "barGraph")
        self.bar_graph.horizontal = True
        self.pie_graph: PieGraph = self.findChild(PieGraph, "pieGraph")

        self.heartbeat()

    def heartbeat(self) -> None:
        Tracker().get_process_data()

        self.update_window_graph(self.pie_graph)
        self.update_process_graph(self.bar_graph)

    def update_window_graph(self, graph):
        window_data = get_window_data()

        window_values = [x[2] for x in window_data]
        window_labels = [x[1].get_name_part(0) for x in window_data]

        window_values = window_values[:5] + [sum(window_values[5:])]
        window_labels = window_labels[:5] + ["Other"]

        graph.set_values(window_values)
        graph.set_labels(window_labels)
        graph.update()

    def update_process_graph(self, graph):
        process_data = get_process_data()

        process_values = [x[1] for x in process_data]
        process_labels = [x[0].get_process_title() for x in process_data]

        process_values = process_values[:5] + [sum(process_values[5:])]
        process_labels = process_labels[:5] + ["Other"]

        graph.set_values(process_values)
        graph.set_labels(process_labels)
        graph.update()

    def showEvent(self, event):
        self.raise_()
        self.requestActivate()
        QQuickView.showEvent(self, event)

    def create_actions(self):
        self.toggle_show_action = QAction("Show")
        self.connect(self.toggle_show_action, SIGNAL("triggered()"), self.show)

        self.quit_action = QAction("Quit")
        self.connect(self.quit_action, SIGNAL("triggered()"), QApplication.quit)

    def create_tray(self):
        self.create_actions()
        self.tray_menu = QMenu()
        self.tray_menu.addAction(self.toggle_show_action)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.quit_action)

        self.tray_icon = QSystemTrayIcon(self.icon, self)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

    def event(self, event):
        if type(event) == QCloseEvent:
            if not is_debug():
                event.ignore()
                self.hide()
        elif type(event) == QFocusEvent:
            if self.visibility() == QWindow.Visibility.Minimized:
                self.hide()
                event.ignore()

        return QQuickView.event(self, event)
