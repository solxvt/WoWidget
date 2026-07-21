from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QWidget,
)


class InfoRow(QWidget):
    def __init__(
        self,
        label: str,
        value: str = "—",
    ) -> None:
        super().__init__()

        self.name_label = QLabel(label)
        self.name_label.setObjectName("MutedLabel")

        self.value_label = QLabel(value)
        self.value_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.value_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        layout.setSpacing(12)

        layout.addWidget(self.name_label)
        layout.addStretch()
        layout.addWidget(self.value_label)

    def set_value(
        self,
        value,
    ) -> None:
        text = str(value).strip()

        self.value_label.setText(text or "—")
