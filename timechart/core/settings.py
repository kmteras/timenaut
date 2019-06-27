from timechart.core.singleton import Singleton

DEFAULT_HEARTBEAT_TIME = 60
DEFAULT_IDLE_TIME = 300


class Settings(metaclass=Singleton):
    def __init__(self):
        self.heartbeat_time = DEFAULT_HEARTBEAT_TIME
        self.idle_time = DEFAULT_IDLE_TIME
