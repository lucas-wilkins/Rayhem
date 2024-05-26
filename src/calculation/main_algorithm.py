from calculation.simulation_parameters import SimulationParameters
from components.simulation_data import SimulationData


def run_algorithm(input_data: SimulationData, parameters: SimulationParameters):
    """ Main algorithm """

    # Create rays from sources

    for source_and_transform in input_data.sources:

        rays = source_and_transform.source.create_rays()