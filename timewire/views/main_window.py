import sys

import pkg_resources
from PySide2.QtWidgets import QApplication, QLabel


class MainWindow(QApplication):
    def __init__(self):
        QApplication.__init__(self)
        with open(pkg_resources.resource_filename('res.style', 'style.qss')) as style:
            self.setStyleSheet(style.read())
        self.setApplicationName("Timewire")

        self.label = QLabel("Timewire")
        self.label.show()

    def start(self):
        sys.exit(self.exec_())
