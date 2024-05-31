import numpy as np

from elements.material import Material
from elements.simulation_data import IntermediateData


class IdealMirror(Material):
    def __init__(self):
        pass

    @staticmethod
    def serialisation_name() -> str:
        return "ideal_mirror"

    def serialise(self) -> dict:
        return {}

    @staticmethod
    def deserialise(data: dict):
        return IdealMirror()

    def is_dispersive(self):
        return False

    def propagate(self, data: IntermediateData) -> IntermediateData:
        """ Reflect in mirror, basically just remove 2x the component in the normal direction"""

        # Note: modifies, rather than replaces values

        component = np.sum(data.local_normals * data.local_directions, axis=1).reshape(-1, 1)

        data.local_directions -= 2*data.local_normals*component

        return data