import PySide2.QtCore as QtCore
from PySide2.QtCore import SIGNAL
from PySide2.QtGui import QIcon, QCloseEvent, QFocusEvent, QWindow
from PySide2.QtQuick import QQuickView
from PySide2.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication

from timewire.core.tracker import Tracker
from timewire.util.util import is_debug
from timewire.views.base_view import BaseView


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

        if Tracker().errors:
            raise Exception("Tracker initialization had errors")

    def heartbeat(self) -> None:
        Tracker().get_process_data()
        active_view = self.get_active_window()
        if active_view is not None:
            active_view.update()

    def get_active_window(self) -> BaseView:
        children = self.findChildren(BaseView)
        for child in children:
            if child.isVisible():
                return child
        return None

    @QtCore.Slot()
    def ready(self):
        self.heartbeat()

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
