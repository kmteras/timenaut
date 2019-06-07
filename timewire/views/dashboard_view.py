import collections
import datetime

import PySide2.QtCore as QtCore

from timewire.core.database import get_process_data_type, get_type_data, get_timeline_data
from timewire.views.bar_graph import BarGraph
from timewire.views.base_view import BaseView
from timewire.views.pie_graph import PieGraph
from timewire.views.timeline_graph import TimelineGraph


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

    graph.set_values([x[1] for x in type_data])
    graph.set_labels([x[0] for x in type_data])
    graph.set_colors([x[2] for x in type_data])
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


def update_timeline(graph, date=datetime.datetime.now().isoformat()[:10]):
    data = get_timeline_data()

    d = collections.OrderedDict()

    current_date = date

    for v in range(24):
        for m in range(6):
            d[f'{current_date} {v:02d}:{m * 10:02d}:00'] = {}

    leftover_time = {}

    for v in data:
        if v[2][:10] == current_date:
            time = v[1]

            if v[3] in leftover_time:
                time += leftover_time[v[3]]
                leftover_time[v[3]] = 0

            # TODO: this does not carry over time if total of different types is over
            if v[1] > 600:
                leftover_time[v[3]] = v[1] - 600
                time = 600

            d[v[2]][v[0]] = {"time": time, "color": v[3]}

    graph.set_values(d)

    graph.update()
