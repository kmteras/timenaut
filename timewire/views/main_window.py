import sys

import pkg_resources
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QLabel


class MainWindow(QApplication):
    def __init__(self):
        QApplication.__init__(self)
        with open(pkg_resources.resource_filename('res.style', 'style.qss')) as style:
            self.setStyleSheet(style.read())
        self.setApplicationName("timewire")
        self.setWindowIcon(QIcon("timewire\\image\\icon.png")) #see vist ple parim viis ikooni kätte saamiseks.
        self.label = QLabel("timewire")
        self.label.show()

    def start(self):
        sys.exit(self.exec_())
