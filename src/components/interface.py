from components.material import Material
from components.surface import Surface

from loadsave import Serialisable


class Interface(Serialisable):
    """ Class that represents an interface with which light can interact"""
    def __init__(self, surface: Surface, material: Material):
        self.surface = surface    # Geometry of the interface
        self.material = material  # How the light is affected

