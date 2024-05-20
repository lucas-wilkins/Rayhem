from dataclasses import dataclass

import numpy as np

class Transformer:
    def __init__(self,
                 forward_rotation: np.ndarray = np.eye(3),
                 backward_rotation: np.ndarray = np.eye(3),
                 forward_translation: np.ndarray = np.zeros((3,)),
                 backward_translation: np.ndarray = np.zeros((3,))):

        self.forward_rotation = np.eye(3) if forward_rotation is None else forward_rotation
        self.backward_rotation = np.eye(3) if backward_rotation is None else backward_rotation
        self.forward_translation = np.zeros((3, )) if forward_translation is None else forward_translation
        self.backward_translation = np.zeros((3, )) if backward_translation is None else backward_translation


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


class ComponentAndTransform(Transformer):
    def __init__(self,
                 component: "Component",
                 forward_rotation: np.ndarray = np.eye(3),
                 backward_rotation: np.ndarray = np.eye(3),
                 forward_translation: np.ndarray = np.zeros((3, )),
                 backward_translation: np.ndarray = np.zeros((3, ))):

        super().__init__(forward_rotation, backward_rotation, forward_translation, backward_translation)

        self.component = component


class SourceAndTransform(Transformer):
    def __init__(self,
                 source: "Source",
                 forward_rotation: np.ndarray | None = None,
                 backward_rotation: np.ndarray | None = None,
                 forward_translation: np.ndarray | None = None,
                 backward_translation: np.ndarray | None = None):

        super().__init__(forward_rotation, backward_rotation, forward_translation, backward_translation)

        self.source = source



@dataclass
class SimulationData:
    sources: list[SourceAndTransform]
    components: list[ComponentAndTransform]
