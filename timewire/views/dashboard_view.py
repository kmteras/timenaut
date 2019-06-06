import collections

from timewire.core.database import get_process_data, get_type_data, get_timeline_data
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

    def componentComplete(self):
        BaseView.componentComplete(self)
        self.bar_graph: BarGraph = self.findChild(BarGraph, "barGraph")
        self.bar_graph.horizontal = True
        self.pie_graph: PieGraph = self.findChild(PieGraph, "pieGraph")
        self.timeline_graph: TimelineGraph = self.findChild(TimelineGraph, "timelineGraph")

        self.update()

    def update(self):
        BaseView.update(self)
        update_type_graph(self.pie_graph)
        update_process_graph(self.bar_graph)
        update_timeline(self.timeline_graph)


def update_type_graph(graph):
    type_data = get_type_data()

    graph.set_values([x[1] for x in type_data])
    graph.set_labels([x[0] for x in type_data])
    graph.set_colors([x[2] for x in type_data])
    graph.update()


def update_process_graph(graph):
    process_data = get_process_data()

    process_values = [x[1] for x in process_data]
    process_labels = [x[0].get_process_title() for x in process_data]

    process_values = process_values[:5]
    process_labels = process_labels[:5]

    graph.set_values(process_values)
    graph.set_labels(process_labels)
    graph.update()


def update_timeline(graph):
    data = get_timeline_data()

    d = collections.OrderedDict()

    for v in range(24):
        for m in range(6):
            d[f'2019-06-05 {v:02d}:{m * 10:02d}:00'] = {}

    leftover_time = {}

    for v in data:
        if v[2][:10] == '2019-06-05':
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
