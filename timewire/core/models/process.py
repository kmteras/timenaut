import re
import sys


class Process:
    def __init__(self, path: str):
        if path == "":
            self.path = None
        else:
            self.path = path

    def __str__(self):
        return f"Process({self.path})"

    def get_process_title(self) -> str:
        if self.path is None:
            return "unknown"

        if sys.platform == 'win32':
            regex = "\\\\(.+\\\\)*(.+)\\."
        else:
            regex = "\\/(?:.+\\/\\/)*(.+)\\/(.*)"

        m = re.match(regex, self.path)
        return m.group(2)
