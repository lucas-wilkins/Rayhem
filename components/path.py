from components.scene_tree import SceneTree

class PathBase:
    def elements_to_check(self, id: int, tree: SceneTree):
        raise NotImplementedError("elements_to_check not implemented in PathBase")


class Path:
    """ Provides a description of a path through optical elements,
    so that other interactions can be ignored"""

    def __init__(self, path_mapping: dict[int, list[int] | None]):
        self.path_mapping = path_mapping

    def elements_to_check(self, id: int, tree: SceneTree):
        return [tree.element_by_id(check_id) for check_id in self.path_mapping[id]]


class NoPath(PathBase):
    """ Not a path, just everything """

    def elements_to_check(self, id: int, tree: SceneTree):
        return tree.all_elements()

