import json

from timewire.core.process_heartbeat import ProcessHeartbeat


class TrackerEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ProcessHeartbeat):
            return {
                "_type": "heartbeat",
                **o.data
            }
        return super(TrackerEncoder, self).default(o)


class TrackerDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, o):
        if '_type' not in o:
            return o
        object_type = o['_type']
        if object_type == 'heartbeat':
            return ProcessHeartbeat(o)
        return o
