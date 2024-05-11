from PySide6.QtWidgets import QWidget

from loadsave import SerialisableElement
from gui.has_gui_element import HasGuiElement

class Component(SerialisableElement, HasGuiElement):
    """ Base class for anything in the scene tree """

    def update_component_id(self):
        pass
