from timechart.core.singleton import Singleton

DEFAULT_HEARTBEAT_TIME = 10
DEFAULT_IDLE_TIME = 180


class Settings(metaclass=Singleton):
    def __init__(self):
        self.heartbeat_time = DEFAULT_HEARTBEAT_TIME
        self.idle_time = DEFAULT_IDLE_TIME
