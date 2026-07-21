from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPixmap,
)
from PySide6.QtWidgets import QWidget


class BackgroundPage(QWidget):
    def __init__(
        self,
        *,
        image_path: str | Path,
        overlay_opacity: int = 176,
    ) -> None:
        super().__init__()

        self._image_path = Path(image_path)
        self._overlay_opacity = max(
            0,
            min(
                255,
                overlay_opacity,
            ),
        )

        self._background_pixmap = QPixmap(str(self._image_path))

        self.setAttribute(
            Qt.WidgetAttribute.WA_StyledBackground,
            True,
        )

    def paintEvent(
        self,
        event,
    ) -> None:
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.SmoothPixmapTransform,
            True,
        )

        if not self._background_pixmap.isNull():
            scaled = self._background_pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )

            x_offset = (scaled.width() - self.width()) // 2

            y_offset = (scaled.height() - self.height()) // 2

            source_rect = scaled.rect().adjusted(
                x_offset,
                y_offset,
                -x_offset,
                -y_offset,
            )

            painter.drawPixmap(
                self.rect(),
                scaled,
                source_rect,
            )
        else:
            painter.fillRect(
                self.rect(),
                QColor("#11101A"),
            )

        painter.fillRect(
            self.rect(),
            QColor(
                10,
                8,
                18,
                self._overlay_opacity,
            ),
        )

        painter.end()

        super().paintEvent(event)
