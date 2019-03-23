from PySide2.QtQuick import QQuickItem


class BaseView(QQuickItem):
    def __init__(self):
        QQuickItem.__init__(self)
        self.setX(10)
        self.setY(10)
