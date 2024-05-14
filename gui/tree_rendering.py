from gui.element_tree_item import ElementTreeItem
from gui.rendering.GL.renderable import Renderable
from gui.element_tree import ElementTree

class TreeRenderer(Renderable):
    def __init__(self, tree: ElementTree):
        self.tree = tree

    def render_solid(self):
        self._recursive_render(self.tree.sceneTreeRoot)

    def _recursive_render(self, element: ElementTreeItem):
        element.gl_in()
        element.render()

        for child in element.children:
            self._recursive_render(child)

        element.gl_out()

