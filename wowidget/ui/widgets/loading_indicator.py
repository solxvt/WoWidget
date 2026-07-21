from PySide6.QtCore import (
    QEvent,
    QRectF,
    Qt,
    QTimer,
)
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
)
from PySide6.QtWidgets import QWidget


class LoadingIndicator(QWidget):
    def __init__(
        self,
        *,
        diameter: int = 18,
        line_width: int = 2,
        color: str = "#C9A3FF",
    ) -> None:
        super().__init__()

        self._angle = 0
        self._diameter = diameter
        self._line_width = line_width
        self._color = QColor(color)
        self._watched_widget: QWidget | None = None

        self.setFixedSize(
            diameter,
            diameter,
        )
        self.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            True,
        )
        self.hide()

        self._timer = QTimer(self)
        self._timer.setInterval(45)
        self._timer.timeout.connect(self._advance)

    def bind_to(
        self,
        widget: QWidget,
    ) -> None:
        if self._watched_widget is not None:
            self._watched_widget.removeEventFilter(self)

        self._watched_widget = widget
        widget.installEventFilter(self)

        self.set_running(not widget.isEnabled())

    def set_running(
        self,
        running: bool,
    ) -> None:
        if running:
            self.show()

            if not self._timer.isActive():
                self._timer.start()
        else:
            self._timer.stop()
            self.hide()

    def eventFilter(
        self,
        watched,
        event,
    ) -> bool:
        if (
            watched is self._watched_widget
            and event.type() == QEvent.Type.EnabledChange
        ):
            self.set_running(not watched.isEnabled())

        return super().eventFilter(
            watched,
            event,
        )

    def _advance(
        self,
    ) -> None:
        self._angle = (self._angle + 28) % 360

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

        pen = QPen(self._color)
        pen.setWidth(self._line_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        inset = self._line_width / 2 + 1

        rect = QRectF(
            inset,
            inset,
            self.width() - inset * 2,
            self.height() - inset * 2,
        )

        painter.drawArc(
            rect,
            int(-self._angle * 16),
            int(250 * 16),
        )
