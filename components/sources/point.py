from components.sources.source import Source

class PointSource(Source):
    def __init__(self):
        super().__init__()

    @staticmethod
    def library_name() -> str:
        return "Point Source"

    @staticmethod
    def library_description() -> str:
        return "Simple point source."

