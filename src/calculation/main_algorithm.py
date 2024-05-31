import logging

import numpy as np
import time

from calculation.rays import RayBundle
from calculation.simulation_parameters import SimulationParameters
from calculation.summary import Summary
from elements.material import Material
from elements.simulation_data import SimulationData
from elements.source_rays import SourceRays
from elements.surface import Surface
from spectral_sampling.spectral_distribution import SpectralDistribution

logger = logging.getLogger("main_algorithm")

def main_algorithm(input_data: SimulationData, parameters: SimulationParameters) -> list[RayBundle]:
    """ Main algorithm """

    start_time = time.time()

    # If there's no sources there's nothing to do, ongoing we assume >0 sources
    if len(input_data.sources) == 0:
        return [], Summary([], 0)

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

    bundles: list[RayBundle] = []

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

            print("Interface", interface_index, "checking", sum(to_check))

            # Transform rays into the coordinate system of the interface

            local_origins = interface_and_transform.reverse_point_transform(origins[to_check, :])
            local_directions = interface_and_transform.reverse_direction_transform(directions[to_check, :])

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

            # Boolean array that references the initial rays, not the checked ones
            to_check_and_replace = np.zeros((n_rays_in,), dtype=bool)
            to_check_and_replace[to_check] = local_replace_flag

            #  - setting of 1d array elements to single value
            collision_indices[to_check_and_replace] = interface_index
            #  - setting of 1d array elements to 1d array of values
            collision_distances[to_check_and_replace] = distances[local_replace_flag]
            #  - setting of 2d array elements to 2d array of values
            collision_coordinates[to_check_and_replace, :] = coordinates[local_replace_flag, :]
            collision_directions[to_check_and_replace, :] = local_directions[local_replace_flag, :]



        # List of escaped rays
        escaped = collision_indices == -1

        # List of collision points
        directions_or_ends = directions.copy()

        local_data_for_each_interface = []

        #
        # Now we should have data on which rays collided and with what, so we can now work out what to do with them
        #

        for interface_index, interface_and_transform in enumerate(input_data.interfaces):
            relevant_rays = collision_indices == interface_index

            surface: Surface = interface_and_transform.interface.surface

            # print(sum(relevant_rays.astype(int)), "rays hit interface", interface_index)

            # Get the collision point, direction, normal,
            # TODO: Include polarisation stuff
            internal_coordinates = collision_coordinates[relevant_rays, :]
            local_directions = collision_directions[relevant_rays, :]
            local_position = surface.internal_to_local_position(internal_coordinates)
            local_normals = surface.internal_to_local_normal(internal_coordinates)

            # Ray ends to go in to bundle
            directions_or_ends[relevant_rays, :] = interface_and_transform.forward_point_transform(local_position)

            # Grab other information for this component
            local_wavelengths = wavelengths[relevant_rays]
            local_intensities = intensities[relevant_rays]
            local_sources = source_ids[relevant_rays]

            local_data_for_each_interface.append(
                (local_position, local_directions, local_normals, local_wavelengths, local_intensities, local_sources))

        bundles.append(
            RayBundle(origins=origins,
                      directions_or_ends=directions_or_ends,
                      intensities=intensities,
                      wavelengths=wavelengths,
                      source_ids=source_ids,
                      escaped=escaped))

        #
        # We can now check whether there is anything left to propagate
        #

        if np.all(escaped):
            break

        #
        # Expand any white rays into spectral components if needed
        #

        new_local_data_for_each_interface = []
        for interface_index, (interface_and_transform, data) in enumerate(zip(input_data.iterfaces, local_data_for_each_interface)):

            if interface_and_transform.interface.is_dispersive():

                local_position, local_directions, local_normals, local_wavelengths, local_intensities, local_sources = data

                #
                # Plan is:
                #   1: create an array indexing the rays
                #   2: remove white ray indices and duplicate them at the end
                #   3: apply index mapping to everything
                #   4: correct everything that is not a straight copy (wavelength & intensity)
                #

                for source_id, distribution in enumerate(distributions):

                    n_duplications = len(distribution.wavlengths)

                    white_rays = np.isnan(local_wavelengths)
                    use_source = (local_sources == source_id) & white_rays

                    index_array = np.arange(len(local_sources))

                    update_indices = index_array[use_source]
                    keep_indices = index_array[~use_source]

                    n_keep = len(keep_indices)
                    n_update = len(update_indices)

                    # index mapping
                    _updated_indices = (update_indices.reshape(-1, 1) * np.ones((1, n_duplications), dtype=int)).reshape(-1) # Can be faster?
                    index_array = np.concatenate((keep_indices, _updated_indices))

                    local_sources = local_sources[index_array]

                    local_position = local_position[index_array, :]
                    local_directions = local_directions[index_array, :]
                    local_normals = local_normals[index_array, :]

                    # Wavelengths need to be done in a very similar way, flattened matrix of wavelengths
                    # note: the dimension that varies is opposite on this one
                    keep_wavelengths = local_wavelengths[keep_indices]
                    updated_wavelengths = (np.ones((n_update, 1)) * distribution.wavelengths.reshape(1, -1)).reshape(-1)
                    local_wavelengths = np.concatenate((keep_wavelengths, updated_wavelengths))

                    keep_intensities = local_intensities[keep_indices]
                    updated_intensities = (local_intensities[update_indices].reshape(-1, 1) *
                                           distribution.intensities.reshape(1, -1)).reshape(-1)
                    local_intensities = np.concatenate((keep_intensities, updated_intensities))

                new_local_data_for_each_interface.append(
                    (local_position, local_directions, local_normals, local_wavelengths, local_intensities, local_sources))
            else:
                new_local_data_for_each_interface.append(data)

        local_data_for_each_interface = new_local_data_for_each_interface

        #
        # Work out what happens to each ray after it collides.
        #
        # It might branch into multiple rays, but this will be handled by the material
        #

        new_local_data_for_each_interface = []
        for interface_index, (interface_and_transform, data) in enumerate(zip(input_data.iterfaces, local_data_for_each_interface)):
            pass

        #
        # Set up data for next loop
        #

        # Remove any with too small an intensity

    summary = Summary(bundles, time.time() - start_time)

    return bundles, summary