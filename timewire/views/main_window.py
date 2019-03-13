import PySide2.QtCore as QtCore
import pkg_resources
from PySide2.QtCore import SIGNAL, QEvent
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QLabel, QSystemTrayIcon, QMenu, QAction, QMainWindow, QApplication, QTextEdit

from timewire.core.database import get_window_data, get_process_data
from timewire.core.tracker import Tracker
from timewire.util.util import is_debug
from timewire.views.bar_graph import BarGraph
from timewire.views.pie_graph import PieGraph


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        if is_debug():
            self.icon = QIcon(pkg_resources.resource_filename('res.img', 'icon_debug.png'))
        else:
            self.icon = QIcon(pkg_resources.resource_filename('res.img', 'icon.png'))

        self.setWindowIcon(self.icon)
        self.label = QLabel(self)
        self.label.resize(700, 100)
        # self.label.setVisible(False)

        self.text_area = QTextEdit(self)
        self.text_area.resize(400, 400)
        self.text_area.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.text_area.setVisible(False)

        self.toggle_show_action = None
        self.quit_action = None
        self.tray_menu = None
        self.tray_icon = None

        self.create_tray()

        self.setFixedSize(800, 600)

        self.update_timer = QtCore.QTimer()
        self.connect(self.update_timer, SIGNAL("timeout()"), self.heartbeat)

        self.update_timer.start(1000)

        self.chart = BarGraph(self, horizontal=True, draw_border=True)
        self.chart.move(350, 100)
        self.chart.set_values([10, 20, 40])
        self.chart.set_labels(["1", "2", "4"])
        self.chart.setFixedSize(350, 350)

        self.pie_graph = PieGraph(self, draw_border=True)
        self.pie_graph.move(10, 100)
        self.pie_graph.setFixedSize(300, 300)

        self.heartbeat()

        if Tracker().errors:
            raise Exception("Tracker initialization had errors")

    def heartbeat(self) -> None:
        process, window = Tracker().get_process_data()
        self.label.setText(f"{str(process)} {str(window)}")

        window_data = get_window_data()

        window_values = [x[2] for x in window_data]
        window_labels = [x[1].get_name_part(0) for x in window_data]

        window_values = window_values[:5] + [sum(window_values[5:])]
        window_labels = window_labels[:5] + ["Other"]

        self.chart.set_values(window_values)
        self.chart.set_labels(window_labels)
        self.chart.update()

        self.pie_graph.set_values(window_values)
        self.pie_graph.set_labels(window_labels)
        self.pie_graph.update()

    def show_action(self):
        self.show()

    def hide_action(self):
        self.hide()

    def _quit_action(self):
        QApplication.quit()

    def create_actions(self):
        self.toggle_show_action = QAction("Show")
        self.connect(self.toggle_show_action, SIGNAL("triggered()"), self.show_action)

        self.quit_action = QAction("Quit")
        self.connect(self.quit_action, SIGNAL("triggered()"), self._quit_action)

    def create_tray(self):
        self.create_actions()
        self.tray_menu = QMenu()
        self.tray_menu.addAction(self.toggle_show_action)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.quit_action)

        self.tray_icon = QSystemTrayIcon(self.icon, self)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

    def changeEvent(self, event: QEvent):
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                event.ignore()
                self.hide()
                return

        QMainWindow.changeEvent(self, event)

    def closeEvent(self, event: QEvent):
        if is_debug():
            event.accept()
            return

        event.ignore()
        self.hide()
