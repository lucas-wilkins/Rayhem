from PySide6.QtWidgets import QApplication
import sys
from media import icons

app = QApplication([])

# Need to do this before importing MainWindow, or the wrong icons will already be loaded
icons.setup_dark_mode_icons(app)


from src.gui.main_window import MainWindow

window = MainWindow()

window.load("test.ray")

window.show()

sys.exit(app.exec())
