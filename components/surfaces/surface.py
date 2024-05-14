import numpy as np

from loadsave import Serialisable

class Surface(Serialisable):
    """ Base class for surface interfaces"""

    def get_collision_points(self, local_origins: np.ndarray, local_directions: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """ Get where the rays collide with this surface

        This is responsible for providing information about which rays collide, as well as where
        If a ray doesn't collide, the internal coordinates don't get used (but it might be efficient to specify them anyway),
        and the distance to collision should be np.inf


        :param local_origins: origins of rays in the local coordinate system for this surface
        :param local_directions: directions of rays (normalised to one) for this coordinate system

        :returns: 2d position in internal coordinates (as defined by each kind of surface), and, distance from ray origin
        """

        raise NotImplementedError(f"get_collision_points not implemented for {self.__class__}")


    def internal_to_local_position(self, internal_coordinates: np.ndarray) -> np.ndarray:
        """ Convert the internal coordinate system to a position in space

        :param internal_coordinates: internal coordinates for a point on the surface
        :returns: corresponding position in local coordinate system """

        raise NotImplementedError(f"internal_to_local_position not implemented for {self.__class__}")


    def internal_to_local_normal(self, internal_coordinates: np.ndarray) -> np.ndarray:
        """ Get the normal to the surface from the internal coordinates

        :param internal_coordinates: internal coordinates for a point on the surface
        :returns: corresponding normal in local coordinate system """

        raise NotImplementedError(f"internal_to_local_normal not implemented for {self.__class__}")

    def mesh(self):
        """ Return the mesh coordinates for drawing in the local frame """
        raise NotImplementedError(f"mesh not implemented for {self.__class__}")