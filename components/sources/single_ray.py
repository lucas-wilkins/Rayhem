from components.sources.source import Source


class SingleRay(Source):

    def __init__(self):
        super().__init__()

    @staticmethod
    def library_name() -> str:
        return "Single Ray"

    @staticmethod
    def library_description() -> str:
        return "Single ray."
