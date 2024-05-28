from dataclasses import dataclass

import numpy as np

class Transformer:
    def __init__(self,
                 forward_rotation: np.ndarray = np.eye(3),
                 backward_rotation: np.ndarray = np.eye(3),
                 translation: np.ndarray = np.zeros((3,))):

        self.forward_rotation = np.eye(3) if forward_rotation is None else forward_rotation
        self.backward_rotation = np.eye(3) if backward_rotation is None else backward_rotation
        self.translation = np.zeros((1, 3)) if translation is None else translation

    def forward_point_transform(self, points: np.ndarray):
        """ Transform points from local frame to parent frame"""
        rotated = np.dot(points, self.forward_rotation)
        return rotated + self.translation

    def reverse_point_transform(self, points: np.ndarray):
        """ Transform points from parent frame to local frame"""

        translated = points - self.translation

        return np.dot(translated, self.backward_rotation)

    def forward_direction_transform(self, directions: np.ndarray):
        """ Transform directions from local frame to parent frame"""
        return np.dot(directions, self.forward_rotation)

    def reverse_direction_transform(self, directions: np.ndarray):
        """ Transform directions from parent frame to local frame"""
        return np.dot(directions, self.backward_rotation)


class InterfaceAndTransform(Transformer):
    def __init__(self,
                 interface: "Interface",
                 forward_rotation: np.ndarray = np.eye(3),
                 backward_rotation: np.ndarray = np.eye(3),
                 translation: np.ndarray = np.zeros((3, ))):

        super().__init__(forward_rotation, backward_rotation, translation)

        self.component = interface


class SourceAndTransform(Transformer):
    def __init__(self,
                 source: "Source",
                 forward_rotation: np.ndarray | None = None,
                 backward_rotation: np.ndarray | None = None,
                 translation: np.ndarray | None = None):

        super().__init__(forward_rotation, backward_rotation, translation)

        self.source = source



@dataclass
class SimulationData:
    sources: list[SourceAndTransform]
    components: list[InterfaceAndTransform]
