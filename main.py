import argparse
import sys

from PySide6.QtWidgets import QApplication

from wowidget.application import WoWidgetApplication
from wowidget.ui.app_icon import (
    get_application_icon,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="WoWidget",
        add_help=True,
    )

    parser.add_argument(
        "--minimized",
        action="store_true",
        help=("Start WoWidget in the system tray " "without opening the main window."),
    )

    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()

    qt_app = QApplication(sys.argv)
    qt_app.setApplicationName("WoWidget")
    qt_app.setOrganizationName("WoWidget")
    qt_app.setQuitOnLastWindowClosed(False)
    qt_app.setWindowIcon(get_application_icon())

    wowidget = WoWidgetApplication(start_minimized=arguments.minimized)

    wowidget.start()

    return qt_app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
