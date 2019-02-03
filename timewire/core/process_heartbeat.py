from datetime import datetime
from typing import Dict


class ProcessHeartbeat:
    def __init__(self, data: Dict):
        self.data = {}
        self.init(**data)

    def init(self, **kwargs):
        for k, v in kwargs.items():
            if k == "_type":
                continue

            self.data[k] = v

        if 'time' not in self.data:
            self.data['time'] = datetime.now().strftime("%H:%M")

    def __dict__(self):
        return self.data

    def __str__(self):
        return str(self.data)
