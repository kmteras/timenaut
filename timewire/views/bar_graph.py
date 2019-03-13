from typing import List

from PySide2.QtCore import Qt, QRectF
from PySide2.QtGui import QPainter, QColor, QPen
from PySide2.QtWidgets import QWidget

from timewire.views.graph_colors import Color


class BarGraph(QWidget):
    def __init__(self, parent, horizontal: bool = False, draw_border: bool = False):
        QWidget.__init__(self, parent)
        self.title = None
        self.values = [None]
        self.labels = [None]
        self.x_padding = 12
        self.y_padding = 12
        self.bar_padding_percentage = 0.2
        self.max_bar_width = None  # TODO: implement
        self.text_padding = 10
        self.font_size = 12
        self.horizontal = horizontal
        self.draw_border = draw_border

    def set_values(self, values: List[float]):
        self.values = values

    def set_labels(self, labels: List[str]):
        self.labels = labels

    def paintEvent(self, event):
        if self.horizontal:
            self.draw_horizontal()
        else:
            self.draw_vertical()

    def draw_horizontal(self):
        p = QPainter()

        rect_size = (self.height() - 3 * self.x_padding) / len(self.values)
        bar_height = int(rect_size * (1 - self.bar_padding_percentage))

        p.begin(self)

        pen = QPen(QColor(*Color.BLACK))
        p.setPen(pen)

        max_value = max(self.values)

        if self.draw_border:
            p.drawRect(0, 0, self.width() - 1, self.height() - 1)

        for i, (value, label) in enumerate(zip(self.values, self.labels)):
            p.setBrush(QColor(*Color.colors[i]))
            bar_width = (value / max_value) * (self.height() - 2 * self.y_padding)

            bar_rect = QRectF(
                self.x_padding + self.text_padding,
                rect_size * i + 2 * self.y_padding,
                bar_width,
                bar_height
            )

            p.drawRect(bar_rect)

            text_rect = QRectF(
                self.x_padding,
                bar_rect.y(),
                self.text_padding,
                bar_rect.height()
            )

            p.drawText(text_rect, Qt.AlignVCenter | Qt.AlignRight, str(label))

        p.end()

    def draw_vertical(self):
        p = QPainter()

        rect_size = (self.width() - 3 * self.x_padding) / len(self.values)
        bar_width = int(rect_size * (1 - self.bar_padding_percentage))

        p.begin(self)

        pen = QPen(QColor(*Color.BLACK))
        p.setPen(pen)

        max_value = max(self.values)

        for i, (value, label) in enumerate(zip(self.values, self.labels)):
            p.setBrush(QColor(*Color.colors[i]))
            bar_height = (value / max_value) * (self.height() - 2 * self.y_padding)

            bar_rect = QRectF(
                rect_size * i + 2 * self.x_padding,
                self.height() - bar_height - self.y_padding - self.text_padding,
                bar_width,
                bar_height
            )

            p.drawRect(bar_rect)

            text_rect = QRectF(
                bar_rect.x(),
                self.height() - self.y_padding,
                bar_width,
                self.y_padding
            )

            p.drawText(text_rect, Qt.AlignCenter, str(label))

        p.end()
