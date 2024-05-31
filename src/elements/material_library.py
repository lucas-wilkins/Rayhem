from elements.material import Material
from elements.materials.reflecting.ideal_mirror import IdealMirror


class MaterialLibrary:
    """ Library containing the different materials available """

    def __init__(self):
         materials_list = [IdealMirror]

         self.materials: dict[str, type[Material]] = {cls.serialisation_name(): cls for cls in materials_list}

    def surface_names(self):
        return [self.materials[name].display_name() for name in self.materials]

    def default(self):
        """ Default material """
        return IdealMirror()

    def serialise(self, material: Material):
        return {
            "name": material.serialisation_name(),
            "data": material.serialise()
        }

    def deserialise(self, data: dict):
        """ Deserialise a material """

        cls = self.materials[data["name"]]

        return cls.deserialise(data["data"])


material_library = MaterialLibrary()