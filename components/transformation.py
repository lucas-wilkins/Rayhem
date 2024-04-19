import numpy as np

from gui.has_gui_element import HasGuiElement
from gui.has_tree_representation import HasTreeRepresentation
from loadsave import SerialisableElement

class Transformation(SerialisableElement, HasGuiElement, HasTreeRepresentation):
    """ Translation used to specify the location of things"""

    def __init__(self, rotation: np.ndarray, translation: np.ndarray):
        self.rotation = rotation
        self.translation = translation

    def apply_to_point(self, points: np.ndarray) -> np.ndarray:
        pass

    def apply_to_direction(self, directions: np.ndarray) -> np.ndarray:
        pass