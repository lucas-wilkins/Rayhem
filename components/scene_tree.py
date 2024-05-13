from components.component import Component
from components.element import Element
from components.transformation import Transformation

class SceneTree:

    def all_elements(self) -> list[Element]:
        pass

    def all_components(self) -> list[Component]:
        components = []
        for element in self.all_elements():
            components += element.components()

        return components

    def all_ids(self):
        return [component.id for component in self.all_components()]