import collections
import datetime

import PySide2.QtCore as QtCore

from timechart.core.database import get_process_data_type, get_type_data, get_timeline_data
from timechart.views.components.bar_graph import BarGraph
from timechart.views.base_view import BaseView
from timechart.views.components.pie_graph import PieGraph
from timechart.views.components.timeline_graph import TimelineGraph


# TODO: make a base class
class DashboardView(BaseView):
    def __init__(self):
        BaseView.__init__(self)
        self.bar_graph = None
        self.pie_graph = None
        self.timeline_graph = None
        self.date_ = None
        self.set_date(datetime.date.today())

    def componentComplete(self):
        BaseView.componentComplete(self)
        self.bar_graph: BarGraph = self.findChild(BarGraph, "barGraph")
        self.bar_graph.horizontal = True
        self.pie_graph: PieGraph = self.findChild(PieGraph, "pieGraph")
        self.timeline_graph: TimelineGraph = self.findChild(TimelineGraph, "timelineGraph")

        self.update()

    def update(self):
        BaseView.update(self)
        update_type_graph(self.pie_graph, date=self.date_)
        update_process_graph(self.bar_graph, date=self.date_)
        update_timeline(self.timeline_graph, str(self.date_))

    def set_date(self, d):
        self.date_ = d
        self.on_date.emit()

    def get_date(self):
        return str(self.date_)

    def next_day(self):
        self.set_date(self.date_ + datetime.timedelta(days=1))
        self.update()

    def prev_day(self):
        self.set_date(self.date_ + datetime.timedelta(days=-1))
        self.update()

    @QtCore.Slot()
    def prevDay(self):
        self.prev_day()

    @QtCore.Slot()
    def nextDay(self):
        self.next_day()

    on_date = QtCore.Signal()

    date = QtCore.Property(str, get_date, notify=on_date)


def update_type_graph(graph, date=None):
    type_data = get_type_data(date_=date)

    graph.set_values([x["count"] for x in type_data])
    graph.set_labels([x["type"] for x in type_data])
    graph.set_colors([x["color"] for x in type_data])
    graph.update()


def update_process_graph(graph, date=None):
    process_data = get_process_data_type(date_=date)

    p = collections.OrderedDict()

    for process in process_data:
        if process[0].id not in p:
            p[process[0].id] = {}
            p[process[0].id][process[0].type_str] = {"title": process[0].get_process_title(), "time": process[1],
                                                     "color": process[0].type_color}
        else:
            p[process[0].id][process[0].type_str] = {"title": process[0].get_process_title(), "time": process[1],
                                                     "color": process[0].type_color}

    graph.set_values(p)
    graph.update()


def update_timeline(graph: TimelineGraph, date=datetime.datetime.now().isoformat()[:10]):
    data = get_timeline_data()

    labels = []
    values = []
    colors = []

    current_date = date

    for v in range(24):
        for m in range(6):
            labels.append(f'{v:02d}:{m * 10:02d}')
            values.append([])
            colors.append([])

    graph.set_labels(labels)

    leftover_time = {}

    for h in range(24):
        for m in range(6):
            for v in data:
                if v['date_time'][:16] == f"{current_date} {h:02d}:{m * 10:02d}":
                    time = v['duration']

                    if v['color'] in leftover_time:
                        time += leftover_time[v['color']]
                        leftover_time[v['color']] = 0

                    total_already = sum(values[h * 6 + m])
                    time = min(total_already + time, 600) - total_already
                    leftover_time[v['color']] = max(0, v['duration'] - time)

                    values[h * 6 + m].append(time)
                    colors[h * 6 + m].append(v['color'])

            for v in leftover_time.keys():
                if leftover_time[v] > 0:
                    time = leftover_time[v]

                    total_already = sum(values[h * 6 + m])
                    time = min(total_already + time, 600) - total_already
                    leftover_time[v] = max(0, leftover_time[v] - time)

                    values[h * 6 + m].append(time)
                    colors[h * 6 + m].append(v)

    graph.set_values(values)
    graph.set_colors(colors)

    graph.update()
