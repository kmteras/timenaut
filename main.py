import sys

import pkg_resources
from PySide2.QtWidgets import QApplication

from timewire.views.main_window import MainWindow


def main():
    application = QApplication()
    application.setApplicationName("Timewire")

    with open(pkg_resources.resource_filename('res.style', 'style.qss'), 'r') as style:
        application.setStyleSheet(style.read())

    main_window = MainWindow()
    main_window.show()
    sys.exit(application.exec_())


if __name__ == "__main__":
    main()
