from wowidget.controllers import (
    ApplicationController,
)


class WoWidgetApplication:
    def __init__(
        self,
        *,
        start_minimized: bool = False,
    ) -> None:
        self.controller = ApplicationController(start_minimized=start_minimized)

    def start(
        self,
    ) -> None:
        self.controller.start()
