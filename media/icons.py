from importlib import resources
from PySide6.QtGui import QIcon

transform = QIcon(str(resources.path("media.icon_files", "transform.svg")))
lens = QIcon(str(resources.path("media.icon_files", "lens.svg")))
mirror = QIcon(str(resources.path("media.icon_files", "mirror.svg")))
source = QIcon(str(resources.path("media.icon_files", "source.svg")))

