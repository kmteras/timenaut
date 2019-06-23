from typing import List

from PySide2.QtCore import Qt, QRectF
from PySide2.QtGui import QColor, QPen
from PySide2.QtQuick import QQuickPaintedItem

from timechart.views.graph_colors import Color


class BarGraph(QQuickPaintedItem):
    def __init__(self, parent=None, horizontal: bool = False, draw_border: bool = False):
        QQuickPaintedItem.__init__(self, parent)
        self.title = None
        self.values = [1]
        self.labels = ["1"]
        self.colors = []
        self.x_padding = 12
        self.y_padding = 12
        self.bar_padding_percentage = 0.2
        self.max_bar_width = None  # TODO: implement
        self.text_padding = 100
        self.bar_padding = 10
        self.font_size = 12
        self.horizontal = horizontal
        self.draw_border = draw_border

    def set_values(self, values: List[float]):
        self.values = values

    def set_labels(self, labels: List[str]):
        self.labels = labels

    def set_colors(self, colors):
        self.colors = colors

    def paint(self, painter):
        if len(self.values) == 0 or len(self.labels) == 0:
            return

        if self.horizontal:
            self.draw_horizontal(painter)
        else:
            self.draw_vertical(painter)

    def draw_horizontal(self, p):
        rect_size = (self.height() - 3 * self.x_padding) / len(list(self.values.keys())[:5])
        bar_height = int(rect_size * (1 - self.bar_padding_percentage))

        pen = QPen(QColor(*Color.BLACK))
        p.setPen(pen)

        max_value = 0

        if len(self.values) > 0:
            proc = list(self.values.keys())[0]
            for type_ in self.values[proc]:
                max_value += self.values[proc][type_]["time"]

        if max_value == 0:
            return

        if self.draw_border:
            p.drawRect(0, 0, self.width() - 1, self.height() - 1)

        for i, v in enumerate(list(self.values.keys())[:5]):
            label = ""
            offset = 0
            for type_ in self.values[v].keys():
                value = self.values[v][type_]["time"]

                p.setBrush(QColor(self.values[v][type_]["color"]))

                bar_width = (value / max_value) * (self.height() - 2 * self.y_padding - 30)

                bar_rect = QRectF(
                    self.x_padding + self.text_padding + self.bar_padding + offset,
                    rect_size * i + 2 * self.y_padding,
                    bar_width,
                    bar_height
                )

                p.drawRect(bar_rect)

                offset += bar_width
                label = self.values[v][type_]["title"]

            text_rect = QRectF(
                self.x_padding,
                rect_size * i + 2 * self.y_padding,
                self.text_padding,
                bar_height
            )

            p.drawText(text_rect, Qt.AlignVCenter | Qt.AlignRight, str(label))

    def draw_vertical(self, p):
        rect_size = (self.width() - 3 * self.x_padding) / len(self.values)
        bar_width = int(rect_size * (1 - self.bar_padding_percentage))

        pen = QPen(QColor(*Color.BLACK))
        p.setPen(pen)

        max_value = max(self.values)

        if max_value == 0:
            return

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
