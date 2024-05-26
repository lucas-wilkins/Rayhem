from typing import Sequence

from loadsave import Serialisable
from spectral_sampling.spectral_distribution import SpectralDistribution


class Material(Serialisable):

    @staticmethod
    def split_white_rays(ray_data, spectral_sampling_lookup: Sequence[SpectralDistribution]):
        pass

