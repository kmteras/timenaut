import PySide2.QtCore as QtCore
import pkg_resources
from PySide2.QtCore import SIGNAL, QEvent
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QLabel, QSystemTrayIcon, QMenu, QAction, QMainWindow, QApplication

from timewire.core.tracker import Tracker


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.icon = QIcon(pkg_resources.resource_filename('res.img', 'icon.png'))
        self.setWindowIcon(self.icon)
        self.label = QLabel(self)
        self.label.resize(700, 100)
        self.update_text()

        self.toggle_show_action = None
        self.quit_action = None
        self.tray_menu = None
        self.tray_icon = None

        self.create_tray()

        self.setFixedSize(800, 600)

        self.update_timer = QtCore.QTimer()
        self.connect(self.update_timer, SIGNAL("timeout()"), self.update_text)

        self.update_timer.start(1000)

    def update_text(self):
        data = Tracker().get_process_data()
        self.label.setText(str(data))

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
        event.ignore()
        self.hide()
