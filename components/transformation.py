import numpy as np

from gui.has_gui_element import HasGuiElement
from gui.has_tree_representation import HasTreeRepresentation
from loadsave import SerialisableElement

class Transformation(SerialisableElement, HasGuiElement, HasTreeRepresentation):
    """ Translation used to specify the location of things"""

    def __init__(self, rotation: np.ndarray, translation: np.ndarray):
        self.rotation = rotation
        self.translation = translation
        self.inv_rotation = np.linalg.inv(rotation)

    def forward_point_transform(self, points: np.ndarray):
        """ Transform points from local frame to parent frame"""
        rotated = np.dot(points, self.rotation)
        return rotated + self.translation

    def reverse_point_transform(self, points: np.ndarray):
        """ Transform points from parent frame to local frame"""
        translated = points - self.translation
        return np.dot(translated, self.inv_rotation)

    def forward_direction_transform(self, directions: np.ndarray):
        """ Transform directions from local frame to parent frame"""
        return np.dot(directions, self.rotation)

    def reverse_direction_transform(self, directions: np.ndarray):
        """ Transform directions from parent frame to local frame"""
        return np.dot(directions, self.inv_rotation)