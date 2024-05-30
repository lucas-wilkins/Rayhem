import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

from loadsave import Serialisable

class Surface(Serialisable):
    """ Base class for surface interfaces"""

    @staticmethod
    def display_name() -> str:
        """ Name to show in display """


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

    def mesh(self) -> tuple[np.ndarray, np.ndarray]:
        """ Return the mesh coordinates for drawing in the local frame """
        raise NotImplementedError(f"mesh not implemented for {self.__class__}")

    def render(self):
        # TODO: Make mesh rendering gooder

        # print(f"Rendering {self.__class__.__name__}")

        vertices, triangles = self.mesh()

        glColor3f(1.0, 1.0, 1.0)

        # This works, but is potentially slow
        glBegin(GL_TRIANGLES)
        for triangle in triangles:
            for index in triangle:
                vertex = vertices[index, :]
                glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()

        #
        ## This doesn't work, but lets not worry about it now
        #

        # vertices = vertices.astype(np.float32).reshape(-1)
        # triangles = triangles.astype(np.uint32).reshape(-1)
        #
        # glEnableClientState(GL_VERTEX_ARRAY)
        #
        #
        # VBO = glGenBuffers(1)
        # glBindBuffer(GL_ARRAY_BUFFER, VBO)
        # glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        #
        # EBO = glGenBuffers(1)
        # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        # glBufferData(GL_ELEMENT_ARRAY_BUFFER, triangles.nbytes, triangles, GL_STATIC_DRAW)
        #
        # glVertexPointer(3, GL_FLOAT, 0, vertices)
        # glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, None)
        #
        # glDisableClientState(GL_VERTEX_ARRAY)