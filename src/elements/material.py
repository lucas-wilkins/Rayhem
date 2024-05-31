from typing import Sequence

import numpy as np

from loadsave import Serialisable
from spectral_sampling.spectral_distribution import SpectralDistribution


class Material(Serialisable):

    @staticmethod
    def display_name() -> str:
        """ Name to be shown in gui """

    def is_dispersive(self) -> bool:
        """ Is this material dispersive? """
        return True

    def split_white_rays(self, ray_data, spectral_sampling_lookup: Sequence[SpectralDistribution]):
        """ Method to split white rays into spectral components """

    def setGLAppearance(self):
        """ GL Calls to set the appearance when rendering polygons """

    def propagate(self, directions: np.ndarray, normals: np.ndarray, wavelengths: np.ndarray):
        pass
