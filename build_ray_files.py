import sys
from PySide6.QtWidgets import QApplication

from components.transformation import Transformation
from gui.main_window import MainWindow


app = QApplication([])
window = MainWindow()

# For the moment, the new_template is just the normal initial state
window.save("new_template.ray")

# Fill tree with random stuff for testing
testNode1 = Transformation()
testNode2 = Transformation()
testNode3 = Transformation()

testNode21 = Transformation()
testNode22 = Transformation()

window.elementsTree.sceneTreeRoot.addChild(testNode1)
window.elementsTree.sceneTreeRoot.addChild(testNode2)
window.elementsTree.sceneTreeRoot.addChild(testNode3)

testNode2.addChild(testNode21)
testNode2.addChild(testNode22)

window.save("test.ray")

window.new()

window.show()

sys.exit(app.exec())