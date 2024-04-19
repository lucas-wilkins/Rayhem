from abc import ABC

from PySide6.QtWidgets import QWidget

class Component:
    
    def properties_widget(self) -> QWidget:
        """ Widget that allows you to adjust this widget """
        raise NotImplementedError()

    def serialised(self) -> dict:
        """ Serialise to a JSON dictionary """
        raise NotImplementedError()

    @staticmethod
    def deserialise(data: dict):
        """ Deserialise a JSON dictionary """
        raise NotImplementedError()