from elements.surface import Surface
from elements.surfaces.flat_square import FlatSquare


class SurfaceLibrary:
    def __init__(self):
        surface_list = [FlatSquare]
        self.surfaces: dict[str, type[Surface]] = {cls.serialisation_name(): cls for cls in surface_list}

    def surface_names(self):
        return [self.surfaces[name].display_name() for name in self.surfaces]

    def default(self):
        return FlatSquare()

    def serialise(self, surface: Surface):
        """ Serialise a surface instance"""

        return {
            "name": surface.serialisation_name(),
            "data": surface.serialise() }

    def deserialise(self, data: dict) -> Surface:
        """ Deserialise a surface instance"""

        cls = self.surfaces[data["name"]]
        return cls.deserialise(data["data"])


surface_library = SurfaceLibrary()