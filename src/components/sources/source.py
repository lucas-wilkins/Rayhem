from PySide6.QtGui import QIcon

from components.source_rays import SourceRays
from src.components.element import Element
from src.components.simulation_data import SourceAndTransform

from media.icons import icons


class Source(Element):
    def __init__(self):
        super().__init__()


    def transformed_sources(self) -> list["SourceAndTransform"]:
        return [SourceAndTransform(source=self)]

    def transformed_components(self) -> list["ComponentAndTransform"]:
        return []

    @staticmethod
    def library_icon() -> QIcon | None:
        return icons["source"]

    def create_rays(self) -> SourceRays:
        raise NotImplementedError(f"create_rays not implemented for {self.__class__.__name__}")

