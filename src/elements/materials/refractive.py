import numpy as np

from elements.material import Material
from elements.simulation_data import IntermediateData


class RefractiveMaterial(Material):
    """ Transparent material that does refraction - defines a refactive index as a function of wavelength """
    def is_dispersive(self):
        return True

    def n(self, wavelength: np.ndarray):
        """ Refractive index as function of wavelength """
        raise NotImplementedError(f"n (refractive index) not implemented for {self.__class__.__name__}")

    def propagate(self, data: IntermediateData) -> IntermediateData:
        pass



    def plot_on(self, axes):
        wavelengths = np.arange(350.0, 900.0, 1.0)

        n = self.n(wavelengths)
        axes.plot(wavelengths, n)
        axes.xlabel("Wavelength /nm")
        axes.ylabel("Refractive Index")

