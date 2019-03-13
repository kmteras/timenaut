class Process:
    def __init__(self, path: str):
        self.path = path

    def __str__(self):
        return f"Process({self.path})"
