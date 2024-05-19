from spectral_sampling.spectral_distribution import SpectralDistribution

def _equal_distribution(wavelengths):
    n = len(wavelengths)
    return [(comp, 1/n) for comp in wavelengths]

def _wavelength_strings(wavelengths):
    return ", ".join([str(int(wavelength)) + "nm" for wavelength in wavelengths])

_rgb_wavelengths = [450, 550, 600]

_rgb = SpectralDistribution(
    name="RGB",
    description="3 Equal intensity wavelengths, " + _wavelength_strings(_rgb_wavelengths),
    components=_equal_distribution(_rgb_wavelengths)
)

_five_wavelengths = [350, 450, 550, 650, 750]

_five_components = SpectralDistribution(
    name="5 Wavelengths",
    description="5 Equal intensity wavelengths, " + _wavelength_strings(_five_wavelengths),
    components=_equal_distribution(_five_wavelengths)
)

_nine_wavelengths = [350, 400, 450, 500, 550, 600, 650, 700, 750]

_nine_components = SpectralDistribution(
    name="9 Wavelengths",
    description="9 Equal intensity wavelengths, " + _wavelength_strings(_nine_wavelengths),
    components=_equal_distribution(_nine_wavelengths)
)


default_spectral_sampling_methods = [_rgb, _five_components, _nine_components]