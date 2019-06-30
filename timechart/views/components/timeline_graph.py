from typing import List

import math
from PySide2.QtCore import Qt
from PySide2.QtGui import QPainter, QColor, QPen
from PySide2.QtQuick import QQuickPaintedItem

from timechart.util.graph_colors import Color


class TimelineGraph(QQuickPaintedItem):
    def __init__(self, parent=None, draw_border: bool = False):
        QQuickPaintedItem.__init__(self, parent)
        self.title = None
        self.labels: List[str] = ["Default"]
        self.values: List[List[float]] = []
        self.colors: List[List[str]] = []
        self.x_padding = 16
        self.y_padding = 16
        self.text_padding = 50
        self.font_size = 12
        self.draw_border = draw_border
        self.max_width = 10
        self.bar_gap = 1
        self.axis_width = 6

    def set_labels(self, labels: List[str]):
        self.labels = labels

    def set_values(self, values: List[List[float]]):
        self.values = values

    def set_colors(self, colors: List[List[QColor]]):
        self.colors = colors

    def paint(self, p: QPainter):
        pen = QPen(QColor(*Color.WHITE))
        p.setPen(pen)

        real_width = int(self.width() - 2 * self.x_padding)
        real_height = int(self.height() - 2 * self.y_padding - self.text_padding)

        p.drawRect(self.x_padding, self.y_padding, real_width, real_height)

        bar_amount = len(self.values)
        bar_width = min(math.floor(real_width / bar_amount - self.bar_gap), self.max_width)

        p.setBrush(QColor(*Color.GREEN))
        for i, bar in enumerate(self.values):
            height_shift = 0
            # Draw bars
            for j, stacked_bar in enumerate(bar):
                if stacked_bar > 0:
                    p.setBrush(QColor(self.colors[i][j]))
                    bar_height = int(real_height * (stacked_bar / 600))
                    p.drawRect(self.x_padding + self.axis_width + self.bar_gap + i * (bar_width + self.bar_gap),
                               self.y_padding + real_height - bar_height - height_shift,
                               bar_width, bar_height)
                    height_shift += bar_height

            # Draw time
            if i % 6 == 0:
                p.translate(self.x_padding + self.axis_width + self.bar_gap + i * (bar_width + self.bar_gap),
                            self.y_padding + real_height + 10)
                p.rotate(45)
                p.setPen(QPen(QColor(*Color.BLACK)))
                p.drawText(0, 0, self.labels[i])
                p.setPen(QPen(QColor(*Color.WHITE)))
                p.rotate(-45)
                p.resetTransform()

        # Draw lines
        p.setBrush(QColor(*Color.DARK))
        p.setPen(Qt.NoPen)
        p.drawRect(self.x_padding, self.y_padding + real_height - self.axis_width, real_width, self.axis_width)
        p.drawRect(self.x_padding, self.y_padding, self.axis_width, real_height)
