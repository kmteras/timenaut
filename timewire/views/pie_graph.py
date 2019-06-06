from typing import List

from PySide2.QtCore import QRectF
from PySide2.QtGui import QPainter, QColor, QPen, QBrush
from PySide2.QtQuick import QQuickPaintedItem

from timewire.views.graph_colors import Color


class PieGraph(QQuickPaintedItem):
    def __init__(self, parent=None, draw_border: bool = False):
        QQuickPaintedItem.__init__(self, parent)
        self.title = None
        self.values: List[float] = [1]
        self.labels: List[str] = ["Default"]
        self.x_padding = 12
        self.y_padding = 12
        self.text_padding = 400
        self.font_size = 12
        self.draw_border = draw_border
        self.colors = None

    def set_values(self, values: List[float]):
        self.values = values

    def set_labels(self, labels: List[str]):
        self.labels = labels

    def set_colors(self, colors: List[str]):
        self.colors = colors

    def paint(self, p) -> None:
        values_total = sum(self.values)

        if len(self.values) == 0 or values_total == 0:
            return

        pen = QPen(QColor(*Color.GRAY))
        p.setPen(pen)
        p.setRenderHint(QPainter.Antialiasing)

        if self.draw_border:
            p.drawRect(0, 0, self.width(), self.height())

        circle_rect = QRectF(
            self.x_padding,
            self.y_padding,
            self.width() - 2 * self.x_padding,
            self.height() - 2 * self.y_padding
        )

        total_drawn_angles = 0

        for i, value in enumerate(self.values):
            angle = int(16 * 360 * value / values_total)

            if self.colors is None:
                p.setBrush(QBrush(QColor(*Color.colors[i])))
            else:
                p.setBrush(QBrush(QColor(self.colors[i])))

            p.drawPie(circle_rect, total_drawn_angles, angle)
            total_drawn_angles += angle
