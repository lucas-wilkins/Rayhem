from src.components.component import Component
from src.components.element import Element
from src.components.simulation_data import ComponentAndTransform


class DummyComponent(Component):
    pass

class DummyElement(Element):
    def transformed_components(self) -> list["ComponentAndTransform"]:
        return [ComponentAndTransform(component=DummyComponent())]

    def transformed_sources(self) -> list["SourceAndTransform"]:
        return []


def main():
    el = DummyElement()

    print(el)

if __name__ == "__main__":
    main()