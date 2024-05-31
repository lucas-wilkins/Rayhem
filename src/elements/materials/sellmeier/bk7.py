from elements.materials.refractive import RefractiveMaterial


class BK7(RefractiveMaterial):
    def __init__(self):
        """
        Crown Glass BK7
        """
        super().__init__(
            b=[1.03961212, 0.231792344, 1.01046945],
            c_um2=[6.00069867e-3, 2.00179144e-2, 103.560653])

    @staticmethod
    def serialisation_name() -> str:
        return "BK7 Crown Glass"