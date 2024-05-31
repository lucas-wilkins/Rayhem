from PySide6.QtGui import QIcon

from elements.element import Element
from elements.interface import Interface
from elements.material import Material
from elements.simulation_data import InterfaceAndTransform
from elements.surface import Surface
from elements.surface_library import surface_library
from elements.material_library import material_library

from media.icons import icons


class GenericInterface(Element):
    def __init__(self, material: Material | None = None, surface: Surface | None = None):
        super().__init__()

        self.material: Material = material_library.default() if material is None else material
        self.surface: Surface = surface_library.default() if surface is None else surface

    @staticmethod
    def library_name() -> str:
        return "Generic Interface"

    @staticmethod
    def library_description() -> str:
        return "Generic Interface - choose a surface and material"

    @staticmethod
    def library_icon() -> QIcon | None:
        return icons["interface"]

    @staticmethod
    def serialisation_name() -> str:
        return "generic_interface"

    @staticmethod
    def deserialise(data: dict):
        material = material_library.deserialise(data["material"])
        surface = surface_library.deserialise(data["surface"])
        return GenericInterface(material=material, surface=surface)

    def serialise(self):
        return {
            "surface": surface_library.serialise(self.surface),
            "material": material_library.serialise(self.material) }

    def transformed_sources(self) -> list["SourceAndTransform"]:
        return []

    def transformed_interfaces(self) -> list["InterfaceAndTransform"]:
        return [InterfaceAndTransform(Interface(self.surface, self.material))]

    def render(self):
        self.material.setGLAppearance()
        self.surface.render()
