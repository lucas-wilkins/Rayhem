from gui.rendering.GL.renderable import Renderable


class RayRenderer(Renderable):
    def __init__(self):
        self._rays = None

    @property
    def rays(self):
        return self._rays

    @rays.setter
    def rays(self, value):
        self._rays = value

    def render_solid(self):
        # Ray rendering here
        pass