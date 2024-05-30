import numpy as np

from elements.surface import Surface

class FlatSquare(Surface):
    """ Just a square in the local xy frame, centred at the origin"""
    def __init__(self, size: float = 1.0):
        self.size = size

    @staticmethod
    def serialisation_name() -> str:
        return "Flat Square"

    def serialise(self) -> dict:
        return {"size": self.size}

    @staticmethod
    def deserialise(data: dict):
        return FlatSquare(float(data["size"]))

    def get_collision_points(self, local_origins: np.ndarray, local_directions: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """ Get where the rays collide with this surface

        This is responsible for providing information about which rays collide, as well as where
        If a ray doesn't collide, the internal coordinates don't get used (but it might be efficient to specify them anyway),
        and the distance to collision should be np.inf


        :param local_origins: origins of rays in the local coordinate system for this surface
        :param local_directions: directions of rays (normalised to one) for this coordinate system

        :returns: Coordinates for this element are just the position in the xy plane
        """


        n_points = local_origins.shape[0]

        # initialise
        distances = np.zeros((n_points, ))
        local_coordinates = np.zeros((n_points, 2))

        z_zero = local_directions[:, 2] == 0
        non_z_zero = np.logical_not(z_zero)

        distances[z_zero] = np.inf
        distances[non_z_zero] = -local_origins[non_z_zero, 2] / local_directions[non_z_zero, 2]

        # print(distances)

        x_intersections = distances[non_z_zero] * local_directions[non_z_zero, 0] + local_origins[non_z_zero, 0]
        y_intersections = distances[non_z_zero] * local_directions[non_z_zero, 1] + local_origins[non_z_zero, 1]

        xy_intersections = np.vstack((x_intersections, y_intersections)).T

        xy_out_of_range = np.logical_not(
                            np.logical_and(
                                np.abs(xy_intersections[:, 0]) <= 0.5*self.size,
                                np.abs(xy_intersections[:, 1]) <= 0.5*self.size))

        to_be_inf = non_z_zero.copy()
        to_be_inf[non_z_zero] = xy_out_of_range

        local_coordinates[non_z_zero, :] = xy_intersections
        distances[to_be_inf] = np.inf
        distances[distances <= 0] = np.inf

        return local_coordinates, distances



    def internal_to_local_position(self, internal_coordinates: np.ndarray) -> np.ndarray:
        """ Convert the internal coordinate system (xy plane) to a position in space

        :param internal_coordinates: internal coordinates for a point on the surface
        :returns: corresponding position in local coordinate system """

        z = np.zeros((internal_coordinates.shape[0],1))

        return np.hstack((internal_coordinates, z))

    def internal_to_local_normal(self, internal_coordinates: np.ndarray) -> np.ndarray:
        """ Get the normal to the surface from the internal coordinates - vectors in +z direction

        :param internal_coordinates: internal coordinates for a point on the surface
        :returns: corresponding normal in local coordinate system """

        zeros = np.zeros((internal_coordinates.shape[0],2))
        ones = np.ones((internal_coordinates.shape[0],1))

        return np.hstack((zeros, ones))

    def mesh(self) -> tuple[np.ndarray, np.ndarray]:
        """ Return the tri-mesh for drawing in the local frame """

        points = 0.5*self.size*np.array([
            [-1, -1, 0],
            [-1,  1, 0],
            [ 1,  1, 0],
            [ 1, -1, 0]], dtype=np.float32)

        triangles = np.array([[0, 1, 2], [0, 2, 3]], dtype=int)

        return points, triangles