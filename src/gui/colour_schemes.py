import numpy as np


class ColourScheme:

    def __init__(self, background: np.ndarray, white_ray: np.ndarray, max_intensity: float):
        """
        Colour scheme definition

        :param background: RGB for background
        :param white_ray: RGB for white rays
        :param max_intensity: Maximum intensity (where alpha channel = 1)
        """

        self.background = background
        self.white_ray = white_ray
        self.max_intensity = max_intensity

    def wavelength_to_rgba(self, wavelengths: np.ndarray):
        """ Convert wavelengths and intensities to RGBA values """

        return np.ones((wavelengths.shape[0], 4))


_white = np.ones((3,))
_black = np.zeros((3,))
_dark_bg = np.array([0.1, 0.15, 0.2])

dark = ColourScheme(background=_dark_bg, white_ray=_white, max_intensity=1.0)
light = ColourScheme(background=_white, white_ray=_black, max_intensity=1.0)

dark_opaque = ColourScheme(background=_dark_bg, white_ray=_white, max_intensity=0.0)
light_opaque = ColourScheme(background=_white, white_ray=_black, max_intensity=0.0)

