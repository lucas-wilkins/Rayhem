from elements.surface import Surface
from elements.surfaces.flat_square import FlatSquare


class SurfaceLibrary:
    def __init__(self):
        self.surfaces: list[type[Surface]] = [FlatSquare]

    def surface_names(self):
        return [surface.display_name() for surface in self.surfaces]

    def default(self):
        return FlatSquare()


surface_library = SurfaceLibrary()