from dataclasses import dataclass
import numpy as np

@dataclass
class RayBundle:
    """ Bundle of rays, one for each step of the calculation """

    origins: np.ndarray
    directions_or_ends: np.ndarray
    intensities: np.ndarray
    wavelengths: np.ndarray
    source_ids: np.ndarray
    # polarisation: np.ndarray
    # polarisation_amount: np.ndarray
    escaped: np.ndarray

