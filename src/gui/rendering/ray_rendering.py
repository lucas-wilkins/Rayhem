import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

from calculation.rays import RayBundle
from gui.colour_schemes import ColourScheme

from gui.rendering.GL.renderable import Renderable
from gui.rendering.rendering_parameters import RenderingParameters



class RayRenderer(Renderable):
    def __init__(self, rendering_parameters: RenderingParameters, colour_scheme: ColourScheme):
        self._rays: list[RayBundle] = []
        self.rendering_parameters = rendering_parameters
        self.colour_scheme = colour_scheme

    @property
    def rays(self) -> list[RayBundle]:
        return self._rays

    @rays.setter
    def rays(self, value: list[RayBundle]):
        self._rays = value

    def render_solid(self):
        # Ray rendering

        # Render the escaped rays
        for ray_bundle in self._rays:
            wls = ray_bundle.wavelengths[ray_bundle.escaped]

            start = ray_bundle.origins[ray_bundle.escaped, :]
            end = start + ray_bundle.directions[ray_bundle.escaped, :] * self.rendering_parameters.escaped_length

            # This will interleave the two arrays of points
            vertices = np.concatenate((start, end), axis=1).reshape(-1, 3)

            # colours from the colour scheme
            colors = self.colour_scheme.wavelength_to_rgba(wls)

            # Generate buffers and bind them
            VBOs = glGenBuffers(2)

            # Vertex buffer
            glBindBuffer(GL_ARRAY_BUFFER, VBOs[0])
            glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(3, GL_FLOAT, 0, None)

            # Color buffer
            glBindBuffer(GL_ARRAY_BUFFER, VBOs[1])
            glBufferData(GL_ARRAY_BUFFER, colors.nbytes, colors, GL_STATIC_DRAW)
            glEnableClientState(GL_COLOR_ARRAY)
            glColorPointer(4, GL_FLOAT, 0, None)

            # Draw the line segments
            glDrawArrays(GL_LINES, 0, len(vertices) // 3)