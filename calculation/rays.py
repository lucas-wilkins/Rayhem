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
                 last_element: np.ndarray | None,
                 escaped: np.ndarray | None):

        self.origins = origins
        self.directions = directions
        self.intensity = intensity
        self.wavelengths = wavelengths
        self.polarisation = polarisation
        self.polarisation_amount = polarisation_amount

        if last_element is None:
            self.last_element = -np.ones((self.origins.shape[0],), dtype=int)

        if escaped is None:
            self.escaped = np.zeros((self.origins.shape[0],), dtype=bool)

    def propagate(self, tree: SceneTree, path: Path | None, remove_escapees: bool):
        """ Main propagation algorithm """
        pass

