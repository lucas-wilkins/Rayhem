from typing import Sequence

import numpy as np

import matplotlib.pyplot as plt

from elements.material import Material
from elements.materials.refractive import RefractiveMaterial


class Sellmeier(RefractiveMaterial):
    """ Dispersive material described by the Sellmeier equation"""
    def __init__(self, b: Sequence[float], c_um2: Sequence[float]):
        self.b = b
        self.c_nm2 = np.array(c_um2) * 1e6
        self.bc = zip(self.b, self.c_nm2)

    def n(self, wavelengths: np.ndarray):
        """ Refractive index as a function of wavelength

        Calculate as: 1 + sum b wl^2 / (wl^2 - c)
        """
        wavelengths_squared = wavelengths**2
        output = np.ones_like(wavelengths)

        for b, c in self.bc:
            output += b * wavelengths_squared / (wavelengths_squared - c)

        return np.sqrt(output)

    def editable(self) -> bool:
        return True

    @staticmethod
    def serialisation_name() -> str:
        return "general_sellmeier"
