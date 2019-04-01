class Window:
    def __init__(self, title: str, window_id: int = None, type_str: str = None, type_color: str = None):
        self.id = window_id
        self.title = title
        self.type_str = type_str
        self.type_color = type_color

    def get_name_part(self, index: int = -1) -> str:
        return self.title.split("-")[index]

    def __str__(self):
        return f"Window({self.title})"
