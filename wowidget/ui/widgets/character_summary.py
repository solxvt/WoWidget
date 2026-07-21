from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from wowidget.ui.widgets.section_divider import (
    SectionDivider,
)

COMPACT_SECTIONS = (
    (
        "Character",
        (
            (
                "character_name",
                "Character",
            ),
            (
                "guild_name",
                "Guild",
            ),
            (
                "race_class",
                "Race / Class",
            ),
            (
                "spec",
                "Specialization",
            ),
        ),
    ),
    (
        "Progress",
        (
            (
                "item_level",
                "Item Level",
            ),
            (
                "mythic_score",
                "Mythic+",
            ),
            (
                "pvp_rating",
                "PvP",
            ),
            (
                "raid_progression",
                "Raid",
            ),
        ),
    ),
    (
        "Collections",
        (
            (
                "total_mounts",
                "Mounts",
            ),
            (
                "total_pets",
                "Pets",
            ),
            (
                "titles_owned",
                "Titles",
            ),
        ),
    ),
    (
        "Completion",
        (
            (
                "achievement_points",
                "Achievement Points",
            ),
            (
                "feats_of_strength",
                "Feats of Strength",
            ),
            (
                "exalted_reputations",
                "Exalted Reputations",
            ),
        ),
    ),
)


class CompactSummaryRow(QFrame):
    def __init__(
        self,
        label: str,
    ) -> None:
        super().__init__()

        self.setObjectName("CompactSummaryRow")
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        self.setMinimumHeight(32)

        self.label = QLabel(label)
        self.label.setObjectName("CompactSummaryLabel")

        self.value = QLabel("—")
        self.value.setObjectName("CompactSummaryValue")
        self.value.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        layout = QGridLayout(self)
        layout.setContentsMargins(
            10,
            5,
            10,
            5,
        )
        layout.setHorizontalSpacing(10)

        layout.addWidget(
            self.label,
            0,
            0,
        )
        layout.addWidget(
            self.value,
            0,
            1,
        )

        layout.setColumnStretch(
            0,
            1,
        )
        layout.setColumnStretch(
            1,
            1,
        )

    def set_value(
        self,
        value: Any,
    ) -> None:
        self.value.setText(format_summary_value(value))


class CharacterSummaryWidget(QWidget):
    def __init__(
        self,
    ) -> None:
        super().__init__()

        self._stat_widgets: dict[
            str,
            CompactSummaryRow,
        ] = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            0,
            0,
            12,
            0,
        )
        layout.setSpacing(5)

        for title, fields in COMPACT_SECTIONS:
            layout.addWidget(SectionDivider(title))

            grid = QGridLayout()
            grid.setContentsMargins(
                0,
                0,
                0,
                0,
            )
            grid.setHorizontalSpacing(8)
            grid.setVerticalSpacing(6)

            for index, (
                field_name,
                field_label,
            ) in enumerate(fields):
                row_widget = CompactSummaryRow(field_label)

                self._stat_widgets[field_name] = row_widget

                grid.addWidget(
                    row_widget,
                    index // 2,
                    index % 2,
                )

            grid.setColumnStretch(
                0,
                1,
            )
            grid.setColumnStretch(
                1,
                1,
            )

            layout.addLayout(grid)

        layout.addStretch()

    def set_data(
        self,
        widget_data: dict | None,
    ) -> None:
        data = (
            widget_data
            if isinstance(
                widget_data,
                dict,
            )
            else {}
        )

        for field_name, stat_widget in self._stat_widgets.items():
            stat_widget.set_value(data.get(field_name))


def format_summary_value(
    value: Any,
) -> str:
    if value is None:
        return "—"

    if isinstance(
        value,
        bool,
    ):
        return "Yes" if value else "No"

    if isinstance(
        value,
        int,
    ):
        return f"{value:,}"

    if isinstance(
        value,
        float,
    ):
        if value.is_integer():
            return f"{int(value):,}"

        return f"{value:,.1f}"

    text = str(value).strip()

    if not text:
        return "—"

    if text.lower() in {
        "unknown",
        "unavailable",
        "none",
    }:
        return "—"

    return text
