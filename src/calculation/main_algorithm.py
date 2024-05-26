import numpy as np

from calculation.rays import RayBundle
from calculation.simulation_parameters import SimulationParameters
from components.simulation_data import SimulationData
from components.source_rays import SourceRays
from spectral_sampling.spectral_distribution import SpectralDistribution


def run_algorithm(input_data: SimulationData, parameters: SimulationParameters):
    """ Main algorithm """

    # Create rays from sources

    distributions: list[SpectralDistribution] = []

    origins = []
    directions = []
    wavelengths = []
    intensities = []
    source_ids = []


    # Build the starting rays
    for index, source_and_transform in enumerate(input_data.sources):

        rays: SourceRays = source_and_transform.source.create_rays()

        distributions.append(rays.distribution)

        # Create contribution to array of source indices
        ids = np.empty_like(rays.intensities)
        ids.fill(index)

        origins.append(source_and_transform.reverse_point_transform(rays.origins))
        directions.append(source_and_transform.reverse_direction_transform(rays.directions))
        wavelengths.append(rays.wavelengths)
        intensities.append(rays.intensities)
        source_ids.append(ids)

    # Build into np arrays
    origins = np.hstack(origins)
    directions = np.hstack(directions)
    intensities = np.concatenate(intensities)
    wavelengths = np.concatenate(wavelengths)
    source_ids = np.concatenate(source_ids)

    # TODO: actual propagation

    escapes = np.ones(source_ids.shape, dtype=bool)

    bundles = [RayBundle(
        origins=origins,
        directions=directions,
        intensities=intensities,
        wavelengths=wavelengths,
        source_ids=source_ids)]


    return bundles