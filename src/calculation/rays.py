import numpy as np

from components.scene_tree import SceneTree
from gui.path_editor.path import Path

class RayBundle:
    """ Main class dealing with rays """
    def __init__(self,
                 origins: np.ndarray,
                 directions: np.ndarray,
                 intensity: np.ndarray,
                 wavelengths: np.ndarray,
                 polarisation: np.ndarray,
                 polarisation_amount: np.ndarray,
                 escaped: np.ndarray | None):

        self.origins = origins
        self.directions = directions
        self.intensity = intensity
        self.wavelengths = wavelengths
        self.polarisation = polarisation
        self.polarisation_amount = polarisation_amount

        if escaped is None:
            self.escaped = np.zeros((self.origins.shape[0],), dtype=bool)

