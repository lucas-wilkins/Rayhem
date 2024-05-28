from elements.interface import Interface
from elements.element import Element
from elements.simulation_data import InterfaceAndTransform


class DummyInterface(Interface):
    pass

class DummyElement(Element):
    def transformed_interfaces(self) -> list["InterfaceAndTransform"]:
        return [InterfaceAndTransform(interface=DummyInterface())]

    def transformed_sources(self) -> list["SourceAndTransform"]:
        return []


def main():
    el = DummyElement()

    print(el)

if __name__ == "__main__":
    main()