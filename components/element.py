from PySide6.QtWidgets import QWidget

from components.component import Component
class Element(Component):

    def __init__(self):
        self.component_id = 0

    def update_component_id(self):
        pass

    @staticmethod
    def material_surface_selection() -> QWidget:
        pass
