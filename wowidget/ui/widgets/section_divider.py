from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QWidget,
)


class SectionDivider(QWidget):
    def __init__(
        self,
        title: str,
    ) -> None:
        super().__init__()

        title_label = QLabel(title)
        title_label.setObjectName("SectionTitle")

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setObjectName("DividerLine")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(
            0,
            4,
            0,
            4,
        )
        layout.setSpacing(12)

        layout.addWidget(title_label)
        layout.addWidget(
            line,
            stretch=1,
        )
