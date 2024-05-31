from typing import Sequence

import numpy as np

from elements.simulation_data import IntermediateData
from loadsave import Serialisable
from spectral_sampling.spectral_distribution import SpectralDistribution


class Material(Serialisable):

    @staticmethod
    def display_name() -> str:
        """ Name to be shown in gui """

    def is_dispersive(self) -> bool:
        """ Is this material dispersive? """
        return True

    def setGLAppearance(self):
        """ GL Calls to set the appearance when rendering polygons """
        pass

    def propagate(self, data: IntermediateData) -> IntermediateData:
        """ Describes what a surface of this kind does to rays"""

        raise NotImplementedError(f"propagate not implemented for material {self.__class__.__name__}")

    def editable(self) -> bool:
        return False