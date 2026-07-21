from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from wowidget.ui.widgets import LoadingIndicator


class CharacterPage(QWidget):
    search_requested = Signal(dict)
    character_selected = Signal(dict)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("PlainPage")

        self.current_character: dict | None = None

        content_card = QFrame()
        content_card.setObjectName("GlassCard")
        content_card.setMinimumWidth(620)
        content_card.setMaximumWidth(760)

        card_layout = QVBoxLayout(content_card)
        card_layout.setContentsMargins(
            30,
            28,
            30,
            28,
        )
        card_layout.setSpacing(16)

        title = QLabel("Select a Character")
        title.setObjectName("PageTitle")

        description = QLabel(
            "Enter the region, realm, and character name "
            "you want WoWidget to display."
        )
        description.setObjectName("PageSubtitle")
        description.setWordWrap(True)

        self.region_input = QComboBox()
        self.region_input.addItem(
            "United States",
            "us",
        )
        self.region_input.addItem(
            "Europe",
            "eu",
        )
        self.region_input.addItem(
            "Korea",
            "kr",
        )
        self.region_input.addItem(
            "Taiwan",
            "tw",
        )

        self.realm_input = QLineEdit()
        self.realm_input.setPlaceholderText("Example: Area 52")

        self.character_input = QLineEdit()
        self.character_input.setPlaceholderText("Example: Solcide")

        search_group = QGroupBox("Character Lookup")
        search_form = QFormLayout(search_group)
        search_form.setHorizontalSpacing(18)
        search_form.setVerticalSpacing(12)
        search_form.setLabelAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        search_form.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow
        )

        search_form.addRow(
            "Region:",
            self.region_input,
        )
        search_form.addRow(
            "Realm:",
            self.realm_input,
        )
        search_form.addRow(
            "Character:",
            self.character_input,
        )

        self.search_button = QPushButton("Search Character")
        self.search_button.setObjectName("PrimaryButton")
        self.search_button.clicked.connect(self._emit_search_request)

        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)

        self.result_group = QGroupBox("Character Found")
        self.result_group.setVisible(False)

        result_layout = QVBoxLayout(self.result_group)
        result_layout.setContentsMargins(
            18,
            16,
            18,
            18,
        )
        result_layout.setSpacing(10)

        self.character_name_label = QLabel()
        self.character_name_label.setObjectName("SectionTitle")

        self.character_details_label = QLabel()
        self.character_details_label.setObjectName("MutedLabel")
        self.character_details_label.setWordWrap(True)
        self.character_details_label.setMinimumHeight(110)

        self.use_character_button = QPushButton("Use This Character")
        self.use_character_button.setObjectName("PrimaryButton")
        self.use_character_button.clicked.connect(self._emit_character_selected)

        result_layout.addWidget(self.character_name_label)
        result_layout.addWidget(self.character_details_label)
        result_layout.addWidget(self.use_character_button)

        card_layout.addWidget(title)
        card_layout.addWidget(description)
        card_layout.addWidget(search_group)
        search_button_row = QHBoxLayout()
        search_button_row.setSpacing(8)
        search_button_row.addWidget(
            self.search_button,
            stretch=1,
        )

        self.loading_indicator = LoadingIndicator()
        self.loading_indicator.bind_to(self.search_button)

        search_button_row.addWidget(self.loading_indicator)

        card_layout.addLayout(search_button_row)
        card_layout.addWidget(self.status_label)
        card_layout.addWidget(self.result_group)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            24,
            24,
            24,
            24,
        )
        layout.addStretch()
        layout.addWidget(
            content_card,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )
        layout.addStretch()

    def _emit_search_request(
        self,
    ) -> None:
        values = {
            "region": (self.region_input.currentData()),
            "realm": (self.realm_input.text().strip()),
            "character": (self.character_input.text().strip()),
        }

        self.search_requested.emit(values)

    def _emit_character_selected(
        self,
    ) -> None:
        if self.current_character:
            self.character_selected.emit(self.current_character)

    def show_character(
        self,
        character: dict,
    ) -> None:
        self.current_character = character

        self.character_name_label.setText(
            character.get(
                "name",
                "Unknown",
            )
        )

        details = [
            (
                f"{character.get('race', 'Unknown')} "
                f"{character.get('class', 'Unknown')}"
            ),
            (f"Active Spec: " f"{character.get('spec', 'Unknown')}"),
            (f"Level: " f"{character.get('level', 'Unknown')}"),
            (f"Realm: " f"{character.get('realm', 'Unknown')}"),
            (f"Faction: " f"{character.get('faction', 'Unknown')}"),
            (f"Guild: " f"{character.get('guild', '---')}"),
        ]

        self.character_details_label.setText("\n".join(details))

        self.result_group.setVisible(True)

        self.set_status(
            ("Character found. Verify the information " "before continuing.")
        )

    def clear_result(
        self,
    ) -> None:
        self.current_character = None
        self.result_group.setVisible(False)

    def set_busy(
        self,
        busy: bool,
    ) -> None:
        self.search_button.setEnabled(not busy)
        self.realm_input.setEnabled(not busy)
        self.character_input.setEnabled(not busy)
        self.region_input.setEnabled(not busy)

    def set_status(
        self,
        message: str,
        *,
        is_error: bool = False,
    ) -> None:
        self.status_label.setObjectName(
            ("StatusError" if is_error else "StatusSuccess")
        )
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)
        self.status_label.setText(message)

    def set_existing_character(
        self,
        *,
        region: str,
        realm: str,
        character: str,
    ) -> None:
        region_index = self.region_input.findData(region)

        if region_index >= 0:
            self.region_input.setCurrentIndex(region_index)

        self.realm_input.setText(realm)
        self.character_input.setText(character)
