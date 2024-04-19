from PySide6.QtWidgets import QWidget

from loadsave import SerialisableElement
from gui.has_gui_element import HasGuiElement
from gui.has_tree_representation import HasTreeRepresentation

class Component(SerialisableElement, HasGuiElement, HasTreeRepresentation):

    @staticmethod
    def material_surface_selection() -> QWidget:
        pass

    def gui_element(self) -> QWidget:
        pass
