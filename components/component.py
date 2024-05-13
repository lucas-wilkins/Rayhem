from PySide6.QtWidgets import QWidget

from loadsave import SerialisableElement
from gui.has_gui_element import HasGuiElement
from components.ids import unique_id

class Component(SerialisableElement, HasGuiElement):
    """ Base class for anything in the scene tree """

    def __init__(self, id: int | None = None):
        self.id = unique_id() if id is None else id

    def self_interacting_default(self) -> bool:
        """ Should rays from this component be allowed to hit it again by default"""
        return True