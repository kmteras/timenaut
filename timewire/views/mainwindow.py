from PySide2.QtWidgets import QApplication, QLabel


def start():
    app = QApplication([])
    app.setStyleSheet(open("./res/style/style.qss").read())
    label = QLabel("Timewire")
    label.show()
    app.exec_()
