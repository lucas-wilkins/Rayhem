from PySide6.QtWidgets import QWidget

from loadsave import SerialisableElement
from gui.has_gui_element import HasGuiElement
from gui.has_tree_representation import HasTreeRepresentation

class Component(SerialisableElement, HasGuiElement, HasTreeRepresentation):
    """ Base class for anything in the scene tree """

    def update_component_id(self):
        pass
