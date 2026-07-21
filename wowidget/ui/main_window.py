from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCloseEvent, QImage, QPixmap, QShowEvent
from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSlider,
    QSpinBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from wowidget.storage.models import (
    DEFAULT_PORTRAIT_SCALE_PERCENT,
    DEFAULT_PORTRAIT_X_OFFSET,
    DEFAULT_PORTRAIT_Y_OFFSET,
)
from wowidget.ui.character_page import CharacterPage
from wowidget.ui.settings_page import SettingsPage
from wowidget.ui.setup_page import SetupPage
from wowidget.ui.theme import (
    APP_STYLESHEET,
    BACKGROUND_IMAGE_PATH,
)
from wowidget.ui.widgets import (
    BackgroundPage,
    CharacterSummaryWidget,
    InfoRow,
    SectionDivider,
    StatusIndicator,
)
from wowidget.version import APP_VERSION

PORTRAIT_UI_DEFAULT_SCALE = 0
PORTRAIT_UI_DEFAULT_X = 0
PORTRAIT_UI_DEFAULT_Y = 0

PORTRAIT_SCALE_BASE = DEFAULT_PORTRAIT_SCALE_PERCENT
PORTRAIT_X_BASE = DEFAULT_PORTRAIT_X_OFFSET
PORTRAIT_Y_BASE = DEFAULT_PORTRAIT_Y_OFFSET


class MainWindow(QMainWindow):
    minimize_requested = Signal()

    setup_save_requested = Signal(dict)

    character_search_requested = Signal(dict)
    character_selected = Signal(dict)
    change_character_requested = Signal()

    portrait_generate_requested = Signal(dict)
    portrait_save_requested = Signal(dict)
    portrait_composition_changed = Signal(dict)
    portrait_reset_requested = Signal()

    widget_update_requested = Signal()
    updates_toggle_requested = Signal()

    settings_open_requested = Signal()
    settings_save_requested = Signal(dict)
    settings_back_requested = Signal()
    open_app_data_requested = Signal()
    open_generated_requested = Signal()
    github_requested = Signal()
    reregister_requested = Signal()
    discord_authorize_requested = Signal()
    discord_refresh_requested = Signal()
    check_updates_requested = Signal()
    reset_requested = Signal()

    def __init__(self) -> None:
        super().__init__()

        self._application_close_allowed = False
        self._synchronizing_portrait_controls = False
        self._initial_window_geometry_applied = False

        self.setWindowTitle(f"WoWidget {APP_VERSION}")
        self.resize(
            1120,
            800,
        )
        self.setMinimumSize(
            900,
            620,
        )
        self.setStyleSheet(APP_STYLESHEET)

        self.pages = QStackedWidget()

        self.status_page = self._build_status_page()
        self.setup_page = SetupPage()
        self.character_page = CharacterPage()
        self.settings_page = SettingsPage()

        self.setup_page.save_requested.connect(self.setup_save_requested.emit)
        self.setup_page.authorize_requested.connect(
            self.discord_authorize_requested.emit
        )

        self.character_page.search_requested.connect(
            self.character_search_requested.emit
        )
        self.character_page.character_selected.connect(self.character_selected.emit)

        self.settings_page.save_requested.connect(self.settings_save_requested.emit)
        self.settings_page.back_requested.connect(self.settings_back_requested.emit)
        self.settings_page.open_app_data_requested.connect(
            self.open_app_data_requested.emit
        )
        self.settings_page.open_generated_requested.connect(
            self.open_generated_requested.emit
        )
        self.settings_page.github_requested.connect(self.github_requested.emit)
        self.settings_page.reregister_requested.connect(self.reregister_requested.emit)
        self.settings_page.discord_authorize_requested.connect(
            self.discord_authorize_requested.emit
        )
        self.settings_page.discord_refresh_requested.connect(
            self.discord_refresh_requested.emit
        )
        self.settings_page.check_updates_requested.connect(
            self.check_updates_requested.emit
        )
        self.settings_page.reset_requested.connect(self.reset_requested.emit)

        self.pages.addWidget(self.status_page)
        self.pages.addWidget(self.setup_page)
        self.pages.addWidget(self.character_page)
        self.pages.addWidget(self.settings_page)

        self.setCentralWidget(self.pages)

    def showEvent(
        self,
        event: QShowEvent,
    ) -> None:
        super().showEvent(event)

        if self._initial_window_geometry_applied:
            return

        screen = self.screen()

        if screen is None:
            return

        available = screen.availableGeometry()

        target_width = min(
            1120,
            max(
                self.minimumWidth(),
                available.width() - 80,
            ),
        )
        target_height = min(
            800,
            max(
                self.minimumHeight(),
                available.height() - 80,
            ),
        )

        self.resize(
            target_width,
            target_height,
        )

        centered_x = available.x() + (available.width() - self.width()) // 2
        centered_y = available.y() + (available.height() - self.height()) // 2

        self.move(
            centered_x,
            centered_y,
        )

        self._initial_window_geometry_applied = True

    def _build_status_page(
        self,
    ) -> QWidget:
        page = BackgroundPage(
            image_path=BACKGROUND_IMAGE_PATH,
            overlay_opacity=172,
        )

        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(
            24,
            22,
            24,
            20,
        )
        main_layout.setSpacing(14)

        header_card = QFrame()
        header_card.setObjectName("GlassCard")

        header_layout = QVBoxLayout(header_card)
        header_layout.setContentsMargins(
            20,
            16,
            20,
            16,
        )

        self.title_label = QLabel("WoWidget")
        self.title_label.setObjectName("PageTitle")

        self.subtitle_label = QLabel(
            "Keep your World of Warcraft Discord widget updated automatically."
        )
        self.subtitle_label.setObjectName("PageSubtitle")
        self.subtitle_label.setWordWrap(True)

        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.subtitle_label)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(14)

        information_frame = QFrame()
        information_frame.setObjectName("GlassCard")
        information_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        information_layout = QVBoxLayout(information_frame)
        information_layout.setContentsMargins(
            20,
            18,
            20,
            18,
        )
        information_layout.setSpacing(9)

        self.state_label = QLabel("Loading application state...")
        self.state_label.setObjectName("StateTitle")

        self.character_label = QLabel()
        self.character_label.setObjectName("MutedLabel")
        self.character_label.setWordWrap(True)

        self.state_description_label = QLabel()
        self.state_description_label.setWordWrap(True)

        information_layout.addWidget(self.state_label)
        information_layout.addWidget(self.character_label)
        information_layout.addWidget(self.state_description_label)

        self.authorization_warning_label = QLabel(
            "Discord authorization is required. "
            "Open Settings and authorize your "
            "Discord account before updating."
        )
        self.authorization_warning_label.setObjectName("StatusError")
        self.authorization_warning_label.setWordWrap(True)
        self.authorization_warning_label.hide()

        information_layout.addWidget(self.authorization_warning_label)

        information_layout.addWidget(SectionDivider("Connection Status"))

        connection_grid = QGridLayout()
        connection_grid.setHorizontalSpacing(26)
        connection_grid.setVerticalSpacing(8)

        self.blizzard_indicator = StatusIndicator("Blizzard")
        self.discord_indicator = StatusIndicator("Discord")
        self.cloudflare_indicator = StatusIndicator("Cloudflare")
        self.updater_indicator = StatusIndicator("Updater")

        connection_grid.addWidget(
            self.blizzard_indicator,
            0,
            0,
        )
        connection_grid.addWidget(
            self.discord_indicator,
            0,
            1,
        )
        connection_grid.addWidget(
            self.cloudflare_indicator,
            1,
            0,
        )
        connection_grid.addWidget(
            self.updater_indicator,
            1,
            1,
        )

        information_layout.addLayout(connection_grid)

        information_layout.addWidget(SectionDivider("Update Information"))

        self.last_check_row = InfoRow("Last Check")
        self.last_push_row = InfoRow("Last Widget Push")
        self.interval_row = InfoRow("Update Interval")

        information_layout.addWidget(self.last_check_row)
        information_layout.addWidget(self.last_push_row)
        information_layout.addWidget(self.interval_row)

        self.character_summary = CharacterSummaryWidget()

        self.character_summary_scroll = QScrollArea()
        self.character_summary_scroll.setObjectName("CharacterSummaryScroll")
        self.character_summary_scroll.setWidgetResizable(True)
        self.character_summary_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.character_summary_scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.character_summary_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.character_summary_scroll.setMinimumHeight(190)
        self.character_summary_scroll.setWidget(self.character_summary)

        information_layout.addWidget(
            self.character_summary_scroll,
            stretch=1,
        )

        self.operation_status_label = QLabel("")
        self.operation_status_label.setWordWrap(True)

        information_layout.addWidget(self.operation_status_label)

        portrait_frame = QFrame()
        portrait_frame.setObjectName("GlassCard")
        portrait_frame.setFixedWidth(370)
        portrait_frame.setMinimumHeight(380)

        portrait_outer_layout = QVBoxLayout(portrait_frame)
        portrait_outer_layout.setContentsMargins(
            6,
            10,
            6,
            10,
        )

        portrait_scroll = QScrollArea()
        portrait_scroll.setObjectName("PortraitScroll")
        portrait_scroll.setWidgetResizable(True)
        portrait_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        portrait_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        portrait_scroll.setFrameShape(QFrame.Shape.NoFrame)

        portrait_content = QWidget()
        portrait_content.setMinimumWidth(342)

        portrait_layout = QVBoxLayout(portrait_content)
        portrait_layout.setContentsMargins(
            12,
            6,
            12,
            8,
        )
        portrait_layout.setSpacing(9)

        portrait_title = QLabel("Portrait Editor")
        portrait_title.setObjectName("SectionTitle")
        portrait_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.portrait_preview_label = QLabel("Generate a portrait to begin")
        self.portrait_preview_label.setFixedSize(
            320,
            320,
        )
        self.portrait_preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.portrait_preview_label.setObjectName("InnerCard")

        portrait_layout.addWidget(portrait_title)
        portrait_layout.addWidget(
            self.portrait_preview_label,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )
        portrait_layout.addSpacing(12)

        self.scale_slider, self.scale_spinbox = self._add_portrait_control(
            portrait_layout,
            label="Scale",
            minimum=-80,
            maximum=80,
            value=PORTRAIT_UI_DEFAULT_SCALE,
            field_width=76,
        )

        self.x_slider, self.x_spinbox = self._add_portrait_control(
            portrait_layout,
            label="Horizontal",
            minimum=-500,
            maximum=500,
            value=PORTRAIT_UI_DEFAULT_X,
            field_width=76,
        )

        self.y_slider, self.y_spinbox = self._add_portrait_control(
            portrait_layout,
            label="Vertical",
            minimum=-500,
            maximum=500,
            value=PORTRAIT_UI_DEFAULT_Y,
            field_width=76,
        )

        portrait_button_layout = QHBoxLayout()
        portrait_button_layout.setSpacing(8)

        self.generate_portrait_button = QPushButton("Generate Portrait")
        self.generate_portrait_button.clicked.connect(self._emit_portrait_generate)

        self.save_portrait_button = QPushButton("Save Portrait")
        self.save_portrait_button.setObjectName("PrimaryButton")
        self.save_portrait_button.clicked.connect(self._emit_portrait_save)

        portrait_button_layout.addWidget(self.generate_portrait_button)
        portrait_button_layout.addWidget(self.save_portrait_button)

        self.reset_portrait_button = QPushButton("Reset Composition")
        self.reset_portrait_button.clicked.connect(self.portrait_reset_requested.emit)

        portrait_layout.addLayout(portrait_button_layout)
        portrait_layout.addWidget(self.reset_portrait_button)
        portrait_layout.addStretch()

        portrait_scroll.setWidget(portrait_content)
        portrait_outer_layout.addWidget(portrait_scroll)

        content_layout.addWidget(
            information_frame,
            stretch=1,
        )
        content_layout.addWidget(portrait_frame)

        action_card = QFrame()
        action_card.setObjectName("GlassCard")

        action_layout = QHBoxLayout(action_card)
        action_layout.setContentsMargins(
            14,
            12,
            14,
            12,
        )
        action_layout.setSpacing(9)

        self.update_widget_button = QPushButton("Update Widget Now")
        self.update_widget_button.setObjectName("PrimaryButton")
        self.update_widget_button.clicked.connect(self.widget_update_requested.emit)

        self.toggle_updates_button = QPushButton("Start Updates")
        self.toggle_updates_button.clicked.connect(self.updates_toggle_requested.emit)

        self.change_character_button = QPushButton("Change Character")
        self.change_character_button.clicked.connect(
            self.change_character_requested.emit
        )

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.settings_open_requested.emit)

        self.minimize_button = QPushButton("Minimize to Tray")
        self.minimize_button.clicked.connect(self.minimize_requested.emit)

        action_layout.addWidget(self.update_widget_button)
        action_layout.addWidget(self.toggle_updates_button)
        action_layout.addWidget(self.change_character_button)
        action_layout.addWidget(self.settings_button)
        action_layout.addWidget(self.minimize_button)

        main_layout.addWidget(header_card)
        main_layout.addLayout(
            content_layout,
            stretch=1,
        )
        main_layout.addWidget(action_card)

        return page

    def _add_portrait_control(
        self,
        layout: QVBoxLayout,
        *,
        label: str,
        minimum: int,
        maximum: int,
        value: int,
        field_width: int,
    ) -> tuple[QSlider, QSpinBox]:
        title = QLabel(label)
        title.setObjectName("MutedLabel")

        row = QHBoxLayout()
        row.setSpacing(10)

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(
            minimum,
            maximum,
        )
        slider.setValue(value)

        spinbox = QSpinBox()
        spinbox.setRange(
            minimum,
            maximum,
        )
        spinbox.setValue(value)
        spinbox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        spinbox.setKeyboardTracking(False)
        spinbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        spinbox.setFixedWidth(field_width)

        slider.valueChanged.connect(
            lambda new_value, target=spinbox: (
                self._sync_portrait_control(
                    target,
                    new_value,
                )
            )
        )

        spinbox.valueChanged.connect(
            lambda new_value, target=slider: (
                self._sync_portrait_control(
                    target,
                    new_value,
                )
            )
        )

        slider.valueChanged.connect(self._emit_portrait_composition_changed)
        spinbox.valueChanged.connect(self._emit_portrait_composition_changed)

        row.addWidget(
            slider,
            stretch=1,
        )
        row.addWidget(spinbox)

        layout.addWidget(title)
        layout.addLayout(row)

        return slider, spinbox

    def _sync_portrait_control(
        self,
        target,
        value: int,
    ) -> None:
        if target.value() == value:
            return

        target.blockSignals(True)
        target.setValue(value)
        target.blockSignals(False)

    def _emit_portrait_generate(
        self,
    ) -> None:
        self.portrait_generate_requested.emit(self.get_portrait_composition())

    def _emit_portrait_save(
        self,
    ) -> None:
        self.portrait_save_requested.emit(self.get_portrait_composition())

    def _emit_portrait_composition_changed(
        self,
        *_,
    ) -> None:
        if self._synchronizing_portrait_controls:
            return

        self.portrait_composition_changed.emit(self.get_portrait_composition())

    def get_portrait_composition(
        self,
    ) -> dict:
        return {
            # The UI displays adjustments relative to the
            # established default composition.
            "scale_percent": (PORTRAIT_SCALE_BASE + self.scale_spinbox.value()),
            "x_offset": (PORTRAIT_X_BASE + self.x_spinbox.value()),
            # Positive UI values move the character upward.
            "y_offset": (PORTRAIT_Y_BASE - self.y_spinbox.value()),
        }

    def set_portrait_composition(
        self,
        *,
        scale_percent: int,
        x_offset: int,
        y_offset: int,
    ) -> None:
        self._synchronizing_portrait_controls = True

        try:
            controls = (
                (
                    self.scale_slider,
                    self.scale_spinbox,
                    (scale_percent - PORTRAIT_SCALE_BASE),
                ),
                (
                    self.x_slider,
                    self.x_spinbox,
                    (x_offset - PORTRAIT_X_BASE),
                ),
                (
                    self.y_slider,
                    self.y_spinbox,
                    (PORTRAIT_Y_BASE - y_offset),
                ),
            )

            for slider, spinbox, value in controls:
                slider.setValue(value)
                spinbox.setValue(value)
        finally:
            self._synchronizing_portrait_controls = False

    def closeEvent(
        self,
        event: QCloseEvent,
    ) -> None:
        if self._application_close_allowed:
            event.accept()
            return

        event.ignore()
        self.minimize_requested.emit()

    def allow_application_close(
        self,
    ) -> None:
        self._application_close_allowed = True

    def show_setup_page(
        self,
        *,
        application_id: str = "",
    ) -> None:
        self.setup_page.set_existing_ids(
            application_id=application_id,
        )

        self.pages.setCurrentWidget(self.setup_page)

    def show_character_page(
        self,
        *,
        region: str = "us",
        realm: str = "",
        character: str = "",
    ) -> None:
        self.character_page.set_existing_character(
            region=region,
            realm=realm,
            character=character,
        )

        self.pages.setCurrentWidget(self.character_page)

    def show_status_page(
        self,
    ) -> None:
        self.pages.setCurrentWidget(self.status_page)

    def show_settings_page(
        self,
        *,
        launch_with_windows: bool,
        start_minimized: bool,
        update_interval_minutes: int,
        authorization_status: dict | None = None,
    ) -> None:
        self.settings_page.set_values(
            launch_with_windows=launch_with_windows,
            start_minimized=start_minimized,
            update_interval_minutes=(update_interval_minutes),
        )

        status = (
            authorization_status
            if isinstance(
                authorization_status,
                dict,
            )
            else {}
        )

        self.settings_page.set_authorization_status(
            authorized=bool(status.get("authorized")),
            expired=bool(status.get("expired")),
            display_name=str(
                status.get(
                    "display_name",
                    "",
                )
            ),
            expires_at=str(
                status.get(
                    "expires_at",
                    "",
                )
            ),
            refresh_available=bool(status.get("refresh_available")),
        )

        self.pages.setCurrentWidget(self.settings_page)

    def display_state(
        self,
        *,
        state_name: str,
        state_description: str,
        character_name: str,
        realm: str,
        region: str,
        updates_enabled: bool,
        update_interval_minutes: int,
        last_check_at: str,
        last_push_at: str,
        last_error: str,
    ) -> None:
        self.state_label.setText(state_name)

        if character_name and realm:
            character_text = (
                f"Selected character: {character_name} — " f"{realm} ({region.upper()})"
            )
        else:
            character_text = "Selected character: None"

        self.character_label.setText(character_text)
        self.state_description_label.setText(state_description)

        self.toggle_updates_button.setText(
            ("Pause Updates" if updates_enabled else "Start Updates")
        )

        self.last_check_row.set_value(last_check_at or "Never")
        self.last_push_row.set_value(last_push_at or "Never")
        self.interval_row.set_value(f"{update_interval_minutes} minutes")

        if last_error:
            self.set_operation_status(
                last_error,
                is_error=True,
            )

    def display_connection_status(
        self,
        *,
        blizzard_ready: bool,
        discord_ready: bool,
        discord_authorized: bool,
        cloudflare_ready: bool,
        updater_running: bool,
    ) -> None:
        self.blizzard_indicator.set_status(
            ("Ready" if blizzard_ready else "Missing"),
            state=("good" if blizzard_ready else "error"),
        )

        if not discord_ready:
            discord_text = "Missing"
            discord_state = "error"
        elif not discord_authorized:
            discord_text = "Authorization Required"
            discord_state = "warning"
        else:
            discord_text = "Ready"
            discord_state = "good"

        self.discord_indicator.set_status(
            discord_text,
            state=discord_state,
        )

        self.authorization_warning_label.setVisible(
            discord_ready and not discord_authorized
        )

        self.cloudflare_indicator.set_status(
            ("Ready" if cloudflare_ready else "Missing"),
            state=("good" if cloudflare_ready else "error"),
        )

        self.updater_indicator.set_status(
            ("Running" if updater_running else "Paused"),
            state=("good" if updater_running else "warning"),
        )

    def display_character_summary(
        self,
        widget_data: dict | None,
    ) -> None:
        self.character_summary.set_data(widget_data)

    def show_portrait(
        self,
        image_path: str | Path,
    ) -> None:
        path = Path(image_path)

        if not path.exists():
            self.clear_portrait()
            return

        pixmap = QPixmap(str(path))

        if pixmap.isNull():
            self.clear_portrait()
            return

        scaled_pixmap = pixmap.scaled(
            self.portrait_preview_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.portrait_preview_label.setPixmap(scaled_pixmap)
        self.portrait_preview_label.setText("")

    def show_portrait_bytes(
        self,
        image_bytes: bytes,
        *,
        width: int,
        height: int,
    ) -> None:
        if not image_bytes or width <= 0 or height <= 0:
            self.clear_portrait()
            return

        bytes_per_line = width * 4

        image = QImage(
            image_bytes,
            width,
            height,
            bytes_per_line,
            QImage.Format.Format_RGBA8888,
        ).copy()

        if image.isNull():
            self.clear_portrait()
            return

        pixmap = QPixmap.fromImage(image)

        scaled_pixmap = pixmap.scaled(
            self.portrait_preview_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.portrait_preview_label.setPixmap(scaled_pixmap)
        self.portrait_preview_label.setText("")

    def clear_portrait(
        self,
    ) -> None:
        self.portrait_preview_label.clear()
        self.portrait_preview_label.setText("Generate a portrait to begin")

    def set_portrait_generate_busy(
        self,
        busy: bool,
    ) -> None:
        self.generate_portrait_button.setEnabled(not busy)
        self.save_portrait_button.setEnabled(not busy)
        self.change_character_button.setEnabled(not busy)

        self.generate_portrait_button.setText(
            ("Generating..." if busy else "Generate Portrait")
        )

    def set_portrait_save_busy(
        self,
        busy: bool,
    ) -> None:
        self.generate_portrait_button.setEnabled(not busy)
        self.save_portrait_button.setEnabled(not busy)
        self.change_character_button.setEnabled(not busy)

        self.save_portrait_button.setText(("Saving..." if busy else "Save Portrait"))

    def set_widget_update_busy(
        self,
        busy: bool,
    ) -> None:
        self.update_widget_button.setEnabled(not busy)
        self.change_character_button.setEnabled(not busy)

        self.update_widget_button.setText(
            ("Updating Widget..." if busy else "Update Widget Now")
        )

    def set_operation_status(
        self,
        message: str,
        *,
        is_error: bool = False,
    ) -> None:
        self.operation_status_label.setObjectName(
            ("StatusError" if is_error else "StatusSuccess")
        )
        self.operation_status_label.style().unpolish(self.operation_status_label)
        self.operation_status_label.style().polish(self.operation_status_label)
        self.operation_status_label.setText(message)
