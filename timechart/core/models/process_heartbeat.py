from time import time

import math

from timechart.core.models.process import Process
from timechart.core.models.window import Window


class ProcessHeartbeat:
    def __init__(self, process: Process, window: Window):
        self.time = math.floor(time())
        self.process = process
        self.window = window

    def __str__(self):
        return f"{str(self.process)} {str(self.window)} {str(self.time)}"

    def is_valid(self) -> bool:
        return self.window.title is not None and self.window.title != ""
