from typing import List

from PySide2.QtGui import QPainter, QColor, QPen
from PySide2.QtWidgets import QWidget


class BarChart(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.title = None
        self.values = [None]
        self.labels = [None]

    def set_values(self, values: List):
        self.values = values

    def set_labels(self, labels: List):
        self.labels = labels

    def paintEvent(self, event):
        p = QPainter()

        rect_size = self.width() / len(self.values)

        p.begin(self)

        # for value in self.values:
        p.setBrush(QColor(155, 155, 155))
        p.setPen(QPen(QColor(155, 155, 155)))
        p.drawRect(10, 10, self.width(), self.height())

        p.end()
