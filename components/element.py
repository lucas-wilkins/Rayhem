from PySide6.QtWidgets import QWidget

from components.component import Component
from gui.has_tree_representation import ElementTreeItem

class Element(Component, ElementTreeItem):

    def __init__(self, name: str = "Element"):
        super(ElementTreeItem, self).__init__()

        self.component_id = 0

    def update_component_id(self):
        pass

    def gl_in(self):
        """ Called when going up the GL stack (e.g. pushMatrix)"""

    def gl_out(self):
        """ Called when going down the GL stack (e.g. popMatrix)"""

    def render(self, target):
        """ Draw this element"""

    @staticmethod
    def material_surface_selection() -> QWidget:
        pass
