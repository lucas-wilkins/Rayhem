from elements.material import Material
from elements.surface import Surface

from loadsave import Serialisable


class Interface(Serialisable):
    """ Class that represents an interface with which light can interact"""
    def __init__(self, surface: Surface, material: Material):
        self.surface: Surface = surface    # Geometry of the interface
        self.material: Material = material  # How the light is affected

