import logging

import numpy as np
import time

from calculation.rays import RayBundle
from calculation.simulation_parameters import SimulationParameters
from calculation.summary import Summary
from elements.simulation_data import SimulationData
from elements.source_rays import SourceRays
from spectral_sampling.spectral_distribution import SpectralDistribution

logger = logging.getLogger("main_algorithm")

def main_algorithm(input_data: SimulationData, parameters: SimulationParameters) -> list[RayBundle]:
    """ Main algorithm """

    start_time = time.time()

    # If there's no sources there's nothing to do, ongoing we assume >0 sources
    if len(input_data.sources) == 0:
        return []

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
        ids = np.empty(rays.intensities.shape, dtype=int)
        ids.fill(index)

        origins.append(source_and_transform.forward_point_transform(rays.origins))
        directions.append(source_and_transform.forward_direction_transform(rays.directions))
        wavelengths.append(rays.wavelengths)
        intensities.append(rays.intensities)
        source_ids.append(ids)

    # Build into np arrays
    origins = np.vstack(origins)
    directions = np.vstack(directions)
    intensities = np.concatenate(intensities)
    wavelengths = np.concatenate(wavelengths)
    source_ids = np.concatenate(source_ids)
    states = source_ids.copy()

    # Check shape of everything
    n = source_ids.shape[0]
    assert origins.shape[0] == n
    assert origins.shape[1] == 3
    assert directions.shape[0] == n
    assert directions.shape[1] == 3
    assert intensities.shape[0] == n
    assert len(intensities.shape) == 1
    assert wavelengths.shape[0] == n
    assert len(wavelengths.shape) == 1

    # TODO: proper pathing stuff
    # We will need a boolean matrix that says which
    # components need to be checked for each state
    #  i.e. for a given component
    #       when the ray has a given state
    #       should I check the component
    #
    #  This should be derived from the path representation
    #
    #  we should be able to do:
    #   check_matrix[states, interface_index] -> boolean whether to check
    #
    # * Care must be taken to deal with the escaped state properly *
    #


    # For now, check everything, assume no change in state
    check_matrix = np.ones((len(input_data.sources), len(input_data.interfaces)), dtype=bool)

    # main loop
    for iteration in range(parameters.maximum_iterations):

        n_rays_in = len(intensities)

        # Space to store the collision points
        collision_coordinates = np.empty((n_rays_in, 2), dtype=float)

        # Distance to collisions
        collision_distances = np.empty(n_rays_in)
        collision_distances.fill(np.inf)

        # Indices for the interface that has had a collision
        collision_indices = np.empty(n_rays_in, dtype=int)
        collision_indices.fill(-1)

        # Directions at the collision points in the local frame for the interface
        collision_directions = np.empty((n_rays_in, 3))

        for interface_index, interface_and_transform in enumerate(input_data.interfaces):
            interface = interface_and_transform.interface
            to_check = check_matrix[states, interface_index]

            # Transform rays into the coordinate system of the interface

            local_origins = interface_and_transform.reverse_point_transform(origins[to_check])
            local_directions = interface_and_transform.reverse_direction_transform(origins[to_check])

            # Calculate the distances and collision points

            coordinates, distances = interface.surface.get_collision_points(local_origins, local_directions)

            # We don't want to count really small distances of the order of numerical precision,
            # these are probably(!) self interactions that are not real, it could be
            # an exceptional glancing blow on a curved surface or something like that - but these
            # are extreme cases, and why the user can change it

            distances[distances < parameters.minimum_distance] = np.inf

            # Update the distance to collision map when the distances are shorter than the shortest so far,
            # basically doing a search for a minimum here

            local_replace_flag = collision_distances[to_check] > distances

            #  - setting of 1d array elements to single value
            collision_indices[to_check][local_replace_flag] = interface_index
            #  - setting of 1d array elements to 1d array of values
            collision_distances[to_check][local_replace_flag] = distances[local_replace_flag]
            #  - setting of 2d array elements to 2d array of values
            collision_coordinates[to_check, :][local_replace_flag, :] = coordinates[local_replace_flag, :]
            collision_directions[to_check, :][local_replace_flag, :] = local_directions[local_replace_flag, :]

        # Now we should have data on which rays collided and with what, so we can now work out what to do with them

        for interface_index, interface_and_transform in enumerate(input_data.interfaces):
            relevant_rays = collision_indices == interface_index

            print(sum(relevant_rays.astype(int)), "rays hit interface", interface_index)


    escaped = np.ones(source_ids.shape, dtype=bool)

    bundles = [RayBundle(
        origins=origins,
        directions=directions,
        intensities=intensities,
        wavelengths=wavelengths,
        source_ids=source_ids,
        escaped=escaped)]

    summary = Summary(bundles, time.time() - start_time)

    return bundles, summary