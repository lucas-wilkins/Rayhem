from importlib import resources

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

icons: dict[str, QIcon] = {}

icons["logo"] = QIcon(str(resources.path("media.icon_files", "logo.svg")))

# Ones that might be flipped

icons["transform"] = QIcon(str(resources.path("media.icon_files.light", "transform.svg")))
icons["lens"] = QIcon(str(resources.path("media.icon_files.light", "lens.svg")))
icons["mirror"] = QIcon(str(resources.path("media.icon_files.light", "mirror.svg")))
icons["source"] = QIcon(str(resources.path("media.icon_files.light", "source.svg")))

def setup_dark_mode_icons(app: QApplication):

    if app.styleHints().colorScheme() == Qt.ColorScheme.Dark:
        # Flip colors

        icons["transform"] = QIcon(str(resources.path("media.icon_files.dark", "transform.svg")))
        icons["lens"] = QIcon(str(resources.path("media.icon_files.dark", "lens.svg")))
        icons["mirror"] = QIcon(str(resources.path("media.icon_files.dark", "mirror.svg")))
        icons["source"] = QIcon(str(resources.path("media.icon_files.dark", "source.svg")))
