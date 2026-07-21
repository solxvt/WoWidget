from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QColor,
    QPainter,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QWidget,
)


class IndicatorDot(QWidget):
    def __init__(
        self,
        *,
        color: str = "#7FE6AE",
        diameter: int = 10,
    ) -> None:
        super().__init__()

        self._color = QColor(color)
        self._diameter = diameter

        self.setFixedSize(
            diameter + 4,
            diameter + 4,
        )

    def set_color(
        self,
        color: str,
    ) -> None:
        self._color = QColor(color)
        self.update()

    def paintEvent(
        self,
        event,
    ) -> None:
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing,
            True,
        )

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._color)

        offset = (self.width() - self._diameter) // 2

        painter.drawEllipse(
            offset,
            offset,
            self._diameter,
            self._diameter,
        )

        painter.end()


class StatusIndicator(QWidget):
    COLORS = {
        "good": "#71E5A5",
        "warning": "#F1C96A",
        "error": "#FF758B",
        "neutral": "#9B95AA",
    }

    def __init__(
        self,
        label: str,
    ) -> None:
        super().__init__()

        self.dot = IndicatorDot()

        self.name_label = QLabel(label)
        self.name_label.setObjectName("MutedLabel")

        self.value_label = QLabel("Unknown")
        self.value_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        layout.setSpacing(8)

        layout.addWidget(self.dot)
        layout.addWidget(self.name_label)
        layout.addStretch()
        layout.addWidget(self.value_label)

    def set_status(
        self,
        text: str,
        *,
        state: str = "neutral",
    ) -> None:
        color = self.COLORS.get(
            state,
            self.COLORS["neutral"],
        )

        self.dot.set_color(color)
        self.value_label.setText(text)
