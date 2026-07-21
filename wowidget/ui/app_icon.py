from pathlib import Path
from typing import Final

from PySide6.QtGui import QIcon

ICON_DIRECTORY: Final[Path] = Path(__file__).resolve().parents[1] / "assets" / "icons"

APPLICATION_ICON_PATH: Final[Path] = ICON_DIRECTORY / "wowidget.ico"


def get_application_icon() -> QIcon:
    icon = QIcon(str(APPLICATION_ICON_PATH))

    if icon.isNull():
        icon = QIcon(str(ICON_DIRECTORY / "wowidget.png"))

    return icon
