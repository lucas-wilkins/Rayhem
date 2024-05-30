from elements.material import Material
from elements.materials.mirror import Mirror


class MaterialLibrary:
    def __init__(self):
        self.materials: list[type[Material]] = [Mirror]

    def surface_names(self):
        return [material.display_name() for material in self.materials]

    def default(self):
        return Mirror()


material_library = MaterialLibrary()