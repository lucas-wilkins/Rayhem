from elements.materials.refractive import RefractiveMaterial


class Quartz(RefractiveMaterial):
    def __init__(self):
        """
        Fused Silica
        """
        super().__init__(
            b=[0.6961663, 0.4079426, 0.8974794],
            c_um2=[4.67914826e-3, 1.35120631e-2, 97.9340025])

    @staticmethod
    def serialisation_name() -> str:
        return "quartz"