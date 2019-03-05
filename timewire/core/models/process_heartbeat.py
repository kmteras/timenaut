from time import time

from timewire.core.models.process import Process
from timewire.core.models.window import Window


class ProcessHeartbeat:
    def __init__(self, process: Process, window: Window):
        self.time = time()
        self.process = process
        self.window = window

    def __str__(self):
        return f"{str(self.process)} {str(self.window)} {str(self.time)}"
