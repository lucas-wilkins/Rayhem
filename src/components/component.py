from loadsave import Serialisable
from components.ids import unique_id

class Component(Serialisable):
    """ Object that represents a component that can interact with light, a collection of interfaces """

    def __init__(self, id: int | None = None):
        self.id = unique_id() if id is None else id

    def self_interacting_default(self) -> bool:
        """ Should rays from this component be allowed to hit it again by default"""
        return True