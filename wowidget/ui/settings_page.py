from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from wowidget.config import (
    APP_VERSION,
)
from wowidget.ui.theme import (
    BACKGROUND_IMAGE_PATH,
)
from wowidget.ui.widgets import (
    BackgroundPage,
    LoadingIndicator,
)


class SettingsPage(BackgroundPage):
    save_requested = Signal(dict)
    back_requested = Signal()

    open_app_data_requested = Signal()
    open_generated_requested = Signal()
    github_requested = Signal()

    reregister_requested = Signal()
    discord_authorize_requested = Signal()
    discord_refresh_requested = Signal()
    check_updates_requested = Signal()
    reset_requested = Signal()

    def __init__(self) -> None:
        super().__init__(
            image_path=BACKGROUND_IMAGE_PATH,
            overlay_opacity=184,
        )

        page_card = QFrame()
        page_card.setObjectName("GlassCard")
        page_card.setMinimumWidth(900)
        page_card.setMaximumWidth(1120)
        page_card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        card_layout = QVBoxLayout(page_card)
        card_layout.setContentsMargins(
            24,
            22,
            24,
            22,
        )
        card_layout.setSpacing(14)

        title = QLabel("Settings")
        title.setObjectName("PageTitle")

        description = QLabel(
            "Manage startup behavior, automatic update "
            "preferences, registration, and local files."
        )
        description.setObjectName("PageSubtitle")
        description.setWordWrap(True)

        general_group = QGroupBox("General")
        general_group.setMinimumHeight(150)
        general_group.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        general_form = QFormLayout(general_group)
        general_form.setSpacing(12)

        self.launch_with_windows_checkbox = QCheckBox(
            "Launch WoWidget when Windows starts"
        )
        self.launch_with_windows_checkbox.setMinimumHeight(28)

        self.start_minimized_checkbox = QCheckBox("Start minimized to the system tray")
        self.start_minimized_checkbox.setMinimumHeight(28)

        self.update_interval_spinbox = QSpinBox()
        self.update_interval_spinbox.setRange(
            5,
            1440,
        )
        self.update_interval_spinbox.setSuffix(" minutes")
        self.update_interval_spinbox.setMinimumHeight(38)

        general_form.addRow(self.launch_with_windows_checkbox)
        general_form.addRow(self.start_minimized_checkbox)
        general_form.addRow(
            "Automatic update interval:",
            self.update_interval_spinbox,
        )

        locations_group = QGroupBox("Files and Support")
        locations_group.setMinimumHeight(155)
        locations_group.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        locations_layout = QVBoxLayout(locations_group)
        locations_layout.setSpacing(9)

        self.open_app_data_button = QPushButton("Open WoWidget Data Folder")
        self.open_app_data_button.setMinimumHeight(38)
        self.open_app_data_button.clicked.connect(self.open_app_data_requested.emit)

        self.open_generated_button = QPushButton("Open Generated Portraits")
        self.open_generated_button.setMinimumHeight(38)
        self.open_generated_button.clicked.connect(self.open_generated_requested.emit)

        self.github_button = QPushButton("Visit WoWidget on GitHub")
        self.github_button.setMinimumHeight(38)
        self.github_button.clicked.connect(self.github_requested.emit)

        self.version_label = QLabel(f"Installed version: {APP_VERSION}")
        self.version_label.setObjectName("MutedLabel")

        self.check_updates_button = QPushButton("Check for Updates")
        self.check_updates_button.setMinimumHeight(38)
        self.check_updates_button.clicked.connect(self.check_updates_requested.emit)

        self.update_loading_indicator = LoadingIndicator()
        self.update_loading_indicator.bind_to(self.check_updates_button)

        update_check_row = QHBoxLayout()
        update_check_row.setSpacing(8)
        update_check_row.addWidget(
            self.check_updates_button,
            stretch=1,
        )
        update_check_row.addWidget(self.update_loading_indicator)

        locations_layout.addWidget(self.version_label)

        files_grid = QGridLayout()
        files_grid.setHorizontalSpacing(10)
        files_grid.setVerticalSpacing(10)

        files_grid.addWidget(
            self.open_app_data_button,
            0,
            0,
        )
        files_grid.addWidget(
            self.open_generated_button,
            0,
            1,
        )
        files_grid.addWidget(
            self.github_button,
            1,
            0,
        )
        files_grid.addLayout(
            update_check_row,
            1,
            1,
        )

        files_grid.setColumnStretch(
            0,
            1,
        )
        files_grid.setColumnStretch(
            1,
            1,
        )

        locations_layout.addLayout(files_grid)

        authorization_group = QGroupBox("Discord Authorization")
        authorization_group.setMinimumHeight(165)
        authorization_group.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        authorization_layout = QVBoxLayout(authorization_group)
        authorization_layout.setSpacing(9)

        self.authorization_status_label = QLabel("Status: Authorization required")
        self.authorization_status_label.setWordWrap(True)

        self.authorization_user_label = QLabel("Authorized account: None")
        self.authorization_user_label.setObjectName("MutedLabel")

        self.authorization_expiry_label = QLabel("Access token: Not authorized")
        self.authorization_expiry_label.setObjectName("MutedLabel")

        authorization_buttons = QHBoxLayout()
        authorization_buttons.setSpacing(10)

        self.authorize_discord_button = QPushButton("Authorize Discord")
        self.authorize_discord_button.setObjectName("PrimaryButton")
        self.authorize_discord_button.setMinimumHeight(38)
        self.authorize_discord_button.clicked.connect(
            self.discord_authorize_requested.emit
        )

        self.refresh_token_button = QPushButton("Refresh Access Token")
        self.refresh_token_button.setMinimumHeight(38)
        self.refresh_token_button.clicked.connect(self.discord_refresh_requested.emit)

        self.authorization_loading_indicator = LoadingIndicator()

        authorization_buttons.addWidget(
            self.authorize_discord_button,
            stretch=1,
        )
        authorization_buttons.addWidget(
            self.refresh_token_button,
            stretch=1,
        )
        authorization_buttons.addWidget(self.authorization_loading_indicator)

        authorization_layout.addWidget(self.authorization_status_label)
        authorization_layout.addWidget(self.authorization_user_label)
        authorization_layout.addWidget(self.authorization_expiry_label)
        authorization_layout.addLayout(authorization_buttons)

        maintenance_group = QGroupBox("Maintenance")
        maintenance_group.setMinimumHeight(155)
        maintenance_group.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        maintenance_layout = QVBoxLayout(maintenance_group)
        maintenance_layout.setSpacing(9)

        maintenance_description = QLabel(
            "Re-registering replaces the local Cloudflare "
            "installation token. Resetting removes saved "
            "settings and credentials from this computer."
        )
        maintenance_description.setObjectName("MutedLabel")
        maintenance_description.setWordWrap(True)

        self.reregister_button = QPushButton("Repair Cloudflare Registration")
        self.reregister_button.setMinimumHeight(38)
        self.reregister_button.clicked.connect(self.reregister_requested.emit)

        self.reset_button = QPushButton("Reset WoWidget")
        self.reset_button.setObjectName("DangerButton")
        self.reset_button.setMinimumHeight(38)
        self.reset_button.clicked.connect(self._confirm_reset)

        maintenance_layout.addWidget(maintenance_description)
        registration_row = QHBoxLayout()
        registration_row.setSpacing(8)
        registration_row.addWidget(
            self.reregister_button,
            stretch=1,
        )

        self.registration_loading_indicator = LoadingIndicator()
        self.registration_loading_indicator.bind_to(self.reregister_button)

        registration_row.addWidget(self.registration_loading_indicator)

        maintenance_layout.addLayout(registration_row)
        maintenance_layout.addWidget(self.reset_button)

        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)

        bottom_layout = QHBoxLayout()

        self.back_button = QPushButton("Back")
        self.back_button.setMinimumHeight(38)
        self.back_button.clicked.connect(self.back_requested.emit)

        self.save_button = QPushButton("Save Settings")
        self.save_button.setObjectName("PrimaryButton")
        self.save_button.setMinimumHeight(38)
        self.save_button.clicked.connect(self._emit_save)

        bottom_layout.addWidget(self.back_button)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.save_button)

        card_layout.addWidget(title)
        card_layout.addWidget(description)
        card_layout.addWidget(general_group)
        card_layout.addWidget(locations_group)
        card_layout.addWidget(authorization_group)
        card_layout.addWidget(maintenance_group)
        card_layout.addWidget(self.status_label)
        card_layout.addLayout(bottom_layout)

        scroll_content = QWidget()
        scroll_content.setObjectName("SettingsScrollContent")
        scroll_content.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground,
            True,
        )

        scroll_content_layout = QHBoxLayout(scroll_content)
        scroll_content_layout.setContentsMargins(
            44,
            34,
            44,
            34,
        )
        scroll_content_layout.addStretch()
        scroll_content_layout.addWidget(
            page_card,
            stretch=1,
        )
        scroll_content_layout.addStretch()

        scroll_area = QScrollArea()
        scroll_area.setObjectName("SettingsScroll")
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea#SettingsScroll {
                background: transparent;
                border: none;
            }

            QScrollArea#SettingsScroll > QWidget > QWidget {
                background: transparent;
            }
            """)
        scroll_area.viewport().setAutoFillBackground(False)
        scroll_area.setWidget(scroll_content)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        layout.addWidget(scroll_area)

    def set_values(
        self,
        *,
        launch_with_windows: bool,
        start_minimized: bool,
        update_interval_minutes: int,
    ) -> None:
        self.launch_with_windows_checkbox.setChecked(launch_with_windows)

        self.start_minimized_checkbox.setChecked(start_minimized)

        self.update_interval_spinbox.setValue(update_interval_minutes)

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

    def set_authorization_status(
        self,
        *,
        authorized: bool,
        expired: bool,
        display_name: str,
        expires_at: str,
        refresh_available: bool,
    ) -> None:
        if authorized and not expired:
            status_text = "Status: Connected"
            object_name = "StatusSuccess"
        elif refresh_available:
            status_text = "Status: Access token expired — " "refresh available"
            object_name = "StatusError"
        else:
            status_text = "Status: Authorization required"
            object_name = "StatusError"

        self.authorization_status_label.setObjectName(object_name)
        self.authorization_status_label.style().unpolish(
            self.authorization_status_label
        )
        self.authorization_status_label.style().polish(self.authorization_status_label)
        self.authorization_status_label.setText(status_text)

        self.authorization_user_label.setText(
            (
                f"Authorized account: {display_name}"
                if display_name
                else "Authorized account: None"
            )
        )
        self.authorization_expiry_label.setText(
            (
                f"Access token expires: {expires_at}"
                if expires_at
                else "Access token: Not authorized"
            )
        )

        self.refresh_token_button.setEnabled(refresh_available)

    def set_authorization_busy(
        self,
        busy: bool,
    ) -> None:
        self.authorize_discord_button.setEnabled(not busy)
        self.refresh_token_button.setEnabled(not busy)
        self.authorization_loading_indicator.set_running(busy)

    def set_registration_busy(
        self,
        busy: bool,
    ) -> None:
        self.reregister_button.setEnabled(not busy)

        self.reregister_button.setText(
            ("Repairing Registration..." if busy else "Repair Cloudflare Registration")
        )

        self.registration_loading_indicator.set_running(busy)

    def set_update_check_busy(
        self,
        busy: bool,
    ) -> None:
        self.check_updates_button.setEnabled(not busy)

        self.check_updates_button.setText(
            ("Checking for Updates..." if busy else "Check for Updates")
        )

        self.update_loading_indicator.set_running(busy)

    def _emit_save(
        self,
    ) -> None:
        self.save_requested.emit(
            {
                "launch_with_windows": (self.launch_with_windows_checkbox.isChecked()),
                "start_minimized": (self.start_minimized_checkbox.isChecked()),
                "update_interval_minutes": (self.update_interval_spinbox.value()),
            }
        )

    def _confirm_reset(
        self,
    ) -> None:
        result = QMessageBox.warning(
            self,
            "Reset WoWidget",
            (
                "This will remove saved settings, "
                "credentials, character selections, and "
                "portrait compositions from this computer.\n\n"
                "Cloudflare-hosted portrait files are not "
                "deleted.\n\n"
                "Continue?"
            ),
            (QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No),
            QMessageBox.StandardButton.No,
        )

        if result == QMessageBox.StandardButton.Yes:
            self.reset_requested.emit()
