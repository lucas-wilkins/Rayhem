from components.element import Element
from components.transformation import Transformation

class SceneTree:
    def update_component_ids(self):
        pass

    def element_by_id(self, id: int) -> list[Element]:
        pass

    def all_elements(self) -> list[Element]:
        pass

    def path_to_root(self, id) -> tuple[list[Transformation], Element]:
        pass