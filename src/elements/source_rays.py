from dataclasses import dataclass

import numpy as np

from spectral_sampling.spectral_distribution import SpectralDistribution


@dataclass
class SourceRays:
    """ Rays coming from a source"""
    origins: np.ndarray      # n-by-3
    directions: np.ndarray   # n-by-3
    wavelengths: np.ndarray  # n
    intensities: np.ndarray    # n
    #polarisation: np.ndarray
    distribution: SpectralDistribution
