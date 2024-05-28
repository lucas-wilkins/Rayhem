from PySide6.QtGui import QIcon

from elements.source_rays import SourceRays
from elements.element import Element
from elements.simulation_data import SourceAndTransform

from media.icons import icons


class Source(Element):
    def __init__(self):
        super().__init__()


    def transformed_sources(self) -> list["SourceAndTransform"]:
        return [SourceAndTransform(source=self)]

    def transformed_interfaces(self) -> list["ComponentAndTransform"]:
        return []

    @staticmethod
    def library_icon() -> QIcon | None:
        return icons["source"]

    def create_rays(self) -> SourceRays:
        raise NotImplementedError(f"create_rays not implemented for {self.__class__.__name__}")

