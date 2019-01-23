import sys

import pkg_resources
from PySide2.QtCore import QTimer, SIGNAL
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QLabel

import core.tracker as tracker


class MainWindow(QApplication):
    def __init__(self):
        QApplication.__init__(self)
        with open(pkg_resources.resource_filename('res.style', 'style.qss'), 'r') as style:
            self.setStyleSheet(style.read())
        self.setApplicationName("timewire")
        self.setWindowIcon(QIcon(pkg_resources.resource_filename('res.img', 'icon.png')))
        self.label = QLabel()
        self.update_text()
        self.label.show()

        self.update_timer = QTimer()
        self.connect(self.update_timer, SIGNAL("timeout()"), self.update_text)
        self.update_timer.start(1000)

    def start(self):
        sys.exit(self.exec_())

    def update_text(self):
        data = tracker.get_process_data()
        self.label.setText(str(data))
