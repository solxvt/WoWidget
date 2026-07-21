from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
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


class SetupPage(QWidget):
    save_requested = Signal(dict)
    authorize_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("PlainPage")

        content_card = QFrame()
        content_card.setObjectName("GlassCard")
        content_card.setMinimumWidth(820)
        content_card.setMaximumWidth(980)

        card_layout = QVBoxLayout(content_card)
        card_layout.setContentsMargins(
            30,
            28,
            30,
            28,
        )
        card_layout.setSpacing(16)

        title = QLabel("Initial Setup")
        title.setObjectName("PageTitle")

        description = QLabel(
            "Enter the credentials for your Discord widget application "
            "and Blizzard API client. WoWidget will validate the "
            "credentials, register this installation with the "
            "upload service, and store all secrets securely in "
            "Windows Credential Manager."
        )
        description.setObjectName("PageSubtitle")
        description.setWordWrap(True)

        self.discord_application_id_input = QLineEdit()
        self.discord_application_id_input.setPlaceholderText("Discord Application ID")

        self.discord_bot_token_input = QLineEdit()
        self.discord_bot_token_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.discord_client_secret_input = QLineEdit()
        self.discord_client_secret_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.blizzard_client_id_input = QLineEdit()
        self.blizzard_client_id_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.blizzard_client_secret_input = QLineEdit()
        self.blizzard_client_secret_input.setEchoMode(QLineEdit.EchoMode.Password)

        discord_group = QGroupBox("Discord Application")
        discord_form = QFormLayout(discord_group)
        discord_form.setHorizontalSpacing(16)
        discord_form.setVerticalSpacing(12)
        discord_form.setLabelAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        discord_form.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow
        )
        discord_form.addRow(
            "Application ID:",
            self.discord_application_id_input,
        )
        discord_form.addRow(
            "Bot Token:",
            self.discord_bot_token_input,
        )
        discord_form.addRow(
            "Client Secret:",
            self.discord_client_secret_input,
        )

        blizzard_group = QGroupBox("Blizzard API Client")
        blizzard_form = QFormLayout(blizzard_group)
        blizzard_form.setHorizontalSpacing(16)
        blizzard_form.setVerticalSpacing(12)
        blizzard_form.setLabelAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        blizzard_form.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow
        )
        blizzard_form.addRow(
            "Client ID:",
            self.blizzard_client_id_input,
        )
        blizzard_form.addRow(
            "Client Secret:",
            self.blizzard_client_secret_input,
        )

        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)

        self.save_button = QPushButton("Validate and Continue")
        self.save_button.setObjectName("PrimaryButton")
        self.save_button.clicked.connect(self._emit_save_request)

        credential_columns = QHBoxLayout()
        credential_columns.setSpacing(14)
        credential_columns.addWidget(
            discord_group,
            stretch=3,
        )
        credential_columns.addWidget(
            blizzard_group,
            stretch=2,
        )

        card_layout.addWidget(title)
        card_layout.addWidget(description)
        card_layout.addLayout(credential_columns)
        card_layout.addWidget(self.status_label)
        save_row = QHBoxLayout()
        save_row.setSpacing(8)
        save_row.addWidget(
            self.save_button,
            stretch=1,
        )

        self.loading_indicator = LoadingIndicator()
        self.loading_indicator.bind_to(self.save_button)

        save_row.addWidget(self.loading_indicator)

        card_layout.addLayout(save_row)

        self.authorize_button = QPushButton("Authorize Discord Account")
        self.authorize_button.setObjectName("PrimaryButton")
        self.authorize_button.clicked.connect(self.authorize_requested.emit)
        self.authorize_button.hide()

        card_layout.addWidget(self.authorize_button)

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

    def _emit_save_request(
        self,
    ) -> None:
        values = {
            "discord_application_id": self.discord_application_id_input.text().strip(),
            "discord_bot_token": self.discord_bot_token_input.text().strip(),
            "discord_client_secret": self.discord_client_secret_input.text().strip(),
            "blizzard_client_id": self.blizzard_client_id_input.text().strip(),
            "blizzard_client_secret": self.blizzard_client_secret_input.text().strip(),
        }

        self.save_requested.emit(values)

    def set_authorization_ready(
        self,
        ready: bool,
    ) -> None:
        self.authorize_button.setVisible(ready)

    def set_authorization_busy(
        self,
        busy: bool,
    ) -> None:
        self.authorize_button.setEnabled(not busy)
        self.save_button.setEnabled(not busy)
        self.authorize_button.setText(
            ("Waiting for Discord..." if busy else "Authorize Discord Account")
        )
        self.loading_indicator.set_running(busy)

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

    def set_existing_ids(
        self,
        *,
        application_id: str,
    ) -> None:
        self.discord_application_id_input.setText(application_id)
