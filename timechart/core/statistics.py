import logging

from timechart.core.singleton import Singleton
from timechart.core.tracker import Tracker


class Statistics(metaclass=Singleton):
    def __init__(self):
        pass

    # def get_window_times(self):
    #     data = Tracker()
    #
    #     stats = {}
    #
    #     for day in data['days']:
    #         for heartbeat in data['days'][day]:
    #             if heartbeat.data["title"] in stats:
    #                 stats[heartbeat.data["title"]] += 1
    #             else:
    #                 stats[heartbeat.data["title"]] = 1
    #
    #     logging.debug(stats)
    #
    #     return stats
