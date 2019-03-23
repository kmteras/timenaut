class Window:
    def __init__(self, title: str, window_id: int = None):
        self.id = window_id
        self.title = title

    def get_name_part(self, index: int = -1) -> str:
        return self.title.split("-")[index]

    def __str__(self):
        return f"Window({self.title})"
