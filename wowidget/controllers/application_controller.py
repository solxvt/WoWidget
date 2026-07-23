import os
import webbrowser
from datetime import (
    datetime,
    timezone,
)
from enum import Enum
from pathlib import Path

from PySide6.QtCore import QThreadPool, QTimer
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QMenu,
    QMessageBox,
    QSystemTrayIcon,
)

from wowidget.config import (
    APP_VERSION,
    GITHUB_REPOSITORY_URL,
    WORKER_BASE_URL,
)
from wowidget.services.blizzard import BlizzardService
from wowidget.services.discord import DiscordService
from wowidget.services.discord_oauth import (
    DiscordOAuthService,
)
from wowidget.services.image_uploader import ImageUploader
from wowidget.services.render_processor import RenderProcessor
from wowidget.services.startup_manager import StartupManager
from wowidget.services.task_worker import TaskWorker
from wowidget.services.update_checker import UpdateChecker
from wowidget.services.widget_update import WidgetUpdateService
from wowidget.services.worker_registration import (
    WorkerRegistrationService,
)
from wowidget.storage import StorageManager, WidgetSettings
from wowidget.storage.database import (
    get_app_data_directory,
)
from wowidget.storage.models import (
    DEFAULT_PORTRAIT_SCALE_PERCENT,
    DEFAULT_PORTRAIT_X_OFFSET,
    DEFAULT_PORTRAIT_Y_OFFSET,
)
from wowidget.ui.app_icon import (
    get_application_icon,
)
from wowidget.ui.main_window import MainWindow


class ApplicationState(Enum):
    FIRST_RUN = "First Run"
    CREDENTIALS_MISSING = "Credentials Missing"
    AUTHORIZATION_REQUIRED = "Authorization Required"
    CHARACTER_NOT_SELECTED = "Character Not Selected"
    READY = "Ready"
    PAUSED = "Paused"
    ERROR = "Error"


class ApplicationController:
    def __init__(
        self,
        *,
        start_minimized: bool = False,
    ) -> None:
        self.start_minimized_requested = start_minimized
        self.storage = StorageManager()
        self.settings = WidgetSettings()
        self.startup_manager = StartupManager()
        self.update_checker = UpdateChecker()

        self.blizzard_service = BlizzardService()
        self.discord_service = DiscordService()
        self.discord_oauth_service = DiscordOAuthService()
        self.render_processor = RenderProcessor()

        self.image_uploader = ImageUploader(WORKER_BASE_URL)

        self.worker_registration_service = WorkerRegistrationService(WORKER_BASE_URL)

        self.widget_update_service = WidgetUpdateService(
            storage=self.storage,
            blizzard_service=self.blizzard_service,
            discord_service=self.discord_service,
            render_processor=self.render_processor,
            image_uploader=self.image_uploader,
            discord_oauth_service=(self.discord_oauth_service),
        )

        self.thread_pool = QThreadPool.globalInstance()
        self.active_workers: set[TaskWorker] = set()

        self.widget_update_in_progress = False
        self.portrait_generate_in_progress = False
        self.portrait_save_in_progress = False
        self.portrait_preview_in_progress = False
        self.pending_portrait_composition: dict | None = None
        self.latest_widget_data: dict = {}

        self.discord_authorization_in_progress = False
        self.discord_authorization_source = ""

        self.update_check_in_progress = False
        self.update_check_is_manual = False

        self.update_timer = QTimer()
        self.update_timer.setSingleShot(False)
        self.update_timer.timeout.connect(self.handle_scheduled_widget_update)

        self.portrait_preview_timer = QTimer()
        self.portrait_preview_timer.setSingleShot(True)
        self.portrait_preview_timer.setInterval(35)
        self.portrait_preview_timer.timeout.connect(
            self._apply_pending_portrait_preview
        )

        self.window = MainWindow()
        self.tray_icon = QSystemTrayIcon()

        self.window.minimize_requested.connect(self.window.hide)
        self.window.setup_save_requested.connect(self.handle_setup_save)
        self.window.character_search_requested.connect(self.handle_character_search)
        self.window.character_selected.connect(self.handle_character_selected)
        self.window.portrait_generate_requested.connect(self.handle_generate_portrait)
        self.window.portrait_save_requested.connect(self.handle_save_portrait)
        self.window.portrait_composition_changed.connect(
            self.handle_portrait_composition_changed
        )
        self.window.portrait_reset_requested.connect(self.handle_portrait_reset)
        self.window.widget_update_requested.connect(self.handle_manual_widget_update)
        self.window.updates_toggle_requested.connect(self.handle_updates_toggle)
        self.window.change_character_requested.connect(self.handle_change_character)

        self.window.settings_open_requested.connect(self.handle_open_settings)
        self.window.settings_save_requested.connect(self.handle_save_settings)
        self.window.settings_back_requested.connect(self.handle_settings_back)
        self.window.open_app_data_requested.connect(self.handle_open_app_data)
        self.window.open_generated_requested.connect(self.handle_open_generated)
        self.window.github_requested.connect(self.handle_open_github)
        self.window.reregister_requested.connect(self.handle_reregister_installation)
        self.window.discord_authorize_requested.connect(self.handle_discord_authorize)
        self.window.discord_refresh_requested.connect(self.handle_discord_refresh)
        self.window.check_updates_requested.connect(self.handle_manual_update_check)
        self.window.reset_requested.connect(self.handle_reset_application)

        self._build_tray()

    def _build_tray(self) -> None:
        icon = get_application_icon()

        self.window.setWindowIcon(icon)
        self.tray_icon.setIcon(icon)
        self.tray_icon.setToolTip("WoWidget")

        tray_menu = QMenu()

        open_action = QAction(
            "Open WoWidget",
            self.window,
        )
        open_action.triggered.connect(self.show_window)

        hide_action = QAction(
            "Minimize to Tray",
            self.window,
        )
        hide_action.triggered.connect(self.window.hide)

        exit_action = QAction(
            "Exit",
            self.window,
        )
        exit_action.triggered.connect(self.exit_application)

        tray_menu.addAction(open_action)
        tray_menu.addAction(hide_action)
        tray_menu.addSeparator()
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self._handle_tray_activation)
        self.tray_icon.show()

    def _handle_tray_activation(
        self,
        reason: QSystemTrayIcon.ActivationReason,
    ) -> None:
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_window()

    def _show_tray_message(
        self,
        title: str,
        message: str,
        *,
        is_error: bool = False,
    ) -> None:
        icon = (
            QSystemTrayIcon.MessageIcon.Critical
            if is_error
            else QSystemTrayIcon.MessageIcon.Information
        )

        self.tray_icon.showMessage(
            title,
            message,
            icon,
            5000,
        )

    def _credentials_are_complete(self) -> bool:
        try:
            values = [
                self.storage.load_discord_bot_token(),
                self.storage.load_discord_client_secret(),
                self.storage.load_blizzard_client_id(),
                self.storage.load_blizzard_client_secret(),
            ]
        except RuntimeError:
            return False

        return all(values)

    def _character_is_selected(self) -> bool:
        return all(
            [
                self.settings.wow_region,
                self.settings.wow_realm,
                self.settings.wow_character,
                self.settings.wow_character_id,
            ]
        )

    def _determine_state(
        self,
    ) -> ApplicationState:
        has_application_settings = bool(
            self.settings.discord_application_id
            or self.settings.discord_user_id
            or self.settings.wow_character
        )

        if not has_application_settings:
            return ApplicationState.FIRST_RUN

        if not self._credentials_are_complete():
            return ApplicationState.CREDENTIALS_MISSING

        if not self.settings.discord_application_id:
            return ApplicationState.CREDENTIALS_MISSING

        oauth_status = self.discord_oauth_service.authorization_status(self.storage)

        if not oauth_status.get("authorized"):
            return ApplicationState.AUTHORIZATION_REQUIRED

        if not self._character_is_selected():
            return ApplicationState.CHARACTER_NOT_SELECTED

        if not self.settings.updates_enabled:
            return ApplicationState.PAUSED

        return ApplicationState.READY

    def _get_state_description(
        self,
        state: ApplicationState,
    ) -> str:
        descriptions = {
            ApplicationState.FIRST_RUN: "WoWidget has not been configured yet.",
            ApplicationState.CREDENTIALS_MISSING: (
                "One or more Discord or Blizzard "
                "credentials still need to be configured."
            ),
            ApplicationState.AUTHORIZATION_REQUIRED: (
                "Discord authorization is required before "
                "WoWidget can update your widget."
            ),
            ApplicationState.CHARACTER_NOT_SELECTED: (
                "Credentials are configured. Select a "
                "World of Warcraft character to continue."
            ),
            ApplicationState.READY: (
                "WoWidget is running and will automatically "
                "check for widget changes."
            ),
            ApplicationState.PAUSED: (
                "WoWidget is configured, but automatic updates are currently paused."
            ),
            ApplicationState.ERROR: "WoWidget encountered an application error.",
        }

        return descriptions[state]

    def handle_setup_save(
        self,
        values: dict,
    ) -> None:
        required_fields = {
            "discord_application_id": "Discord Application ID",
            "discord_bot_token": "Discord Bot Token",
            "discord_client_secret": "Discord Client Secret",
            "blizzard_client_id": "Blizzard Client ID",
            "blizzard_client_secret": "Blizzard Client Secret",
        }

        missing_fields = [
            label for key, label in required_fields.items() if not values.get(key)
        ]

        if missing_fields:
            self.window.setup_page.set_status(
                "Please complete the following fields: " + ", ".join(missing_fields),
                is_error=True,
            )
            return

        if not values["discord_application_id"].isdigit():
            self.window.setup_page.set_status(
                "Discord Application ID must contain only numbers.",
                is_error=True,
            )
            return

        self.window.setup_page.save_button.setEnabled(False)
        self.window.setup_page.set_status(
            "Validating credentials and registering this WoWidget installation..."
        )

        worker = TaskWorker(
            self._validate_setup_credentials,
            values,
        )

        self._start_worker(
            worker,
            succeeded=self._handle_validation_result,
            failed=self._handle_validation_error,
            finished=self._finish_setup_validation,
        )

    def _validate_setup_credentials(
        self,
        values: dict,
    ) -> dict:
        blizzard_valid, blizzard_message = self.blizzard_service.validate_credentials(
            values["blizzard_client_id"],
            values["blizzard_client_secret"],
        )

        if not blizzard_valid:
            return {
                "success": False,
                "message": blizzard_message,
            }

        discord_valid, discord_message = self.discord_service.validate_credentials(
            application_id=values["discord_application_id"],
            bot_token=values["discord_bot_token"],
        )

        if not discord_valid:
            return {
                "success": False,
                "message": discord_message,
            }

        try:
            registration = self.worker_registration_service.register_installation(
                discord_application_id=values["discord_application_id"],
                discord_bot_token=values["discord_bot_token"],
            )
        except Exception as error:
            return {
                "success": False,
                "message": (
                    "Discord and Blizzard credentials "
                    "were valid, but WoWidget could not "
                    f"register this installation: {error}"
                ),
            }

        install_token = str(
            registration.get(
                "install_token",
                "",
            )
        ).strip()

        if not install_token:
            return {
                "success": False,
                "message": (
                    "The WoWidget registration service "
                    "returned no installation token."
                ),
            }

        application_name = str(
            registration.get(
                "discord_application_name",
                "Discord application",
            )
        ).strip()

        return {
            "success": True,
            "message": (
                f"{blizzard_message} "
                f"{discord_message} "
                f"Registered {application_name} "
                "with the WoWidget upload service."
            ),
            "values": values,
            "install_token": install_token,
        }

    def _handle_validation_result(
        self,
        result: dict,
    ) -> None:
        if not result.get("success"):
            self.window.setup_page.set_status(
                result.get(
                    "message",
                    "Credential validation failed.",
                ),
                is_error=True,
            )
            return

        self._save_validated_setup(
            result["values"],
            install_token=result["install_token"],
        )

    def _handle_validation_error(
        self,
        message: str,
    ) -> None:
        self.window.setup_page.set_status(
            f"Credential validation failed: {message}",
            is_error=True,
        )

    def _finish_setup_validation(
        self,
    ) -> None:
        self.window.setup_page.save_button.setEnabled(True)

    def _save_validated_setup(
        self,
        values: dict,
        *,
        install_token: str,
    ) -> None:
        try:
            self.settings.discord_application_id = values["discord_application_id"]
            self.settings.discord_user_id = ""
            self.storage.clear_discord_oauth()

            self.storage.save_settings(self.settings)
            self.storage.save_discord_credentials(
                bot_token=values["discord_bot_token"],
                client_secret=values["discord_client_secret"],
            )
            self.storage.save_blizzard_credentials(
                client_id=values["blizzard_client_id"],
                client_secret=values["blizzard_client_secret"],
            )

            self.storage.save_worker_install_token(install_token)
        except Exception as error:
            self.window.setup_page.set_status(
                f"Unable to save setup information: {error}",
                is_error=True,
            )
            return

        self.window.setup_page.set_status(
            (
                "Credentials verified and saved. "
                "Complete the one-time Discord "
                "authorization to continue."
            )
        )
        self.window.setup_page.set_authorization_ready(True)

    def handle_discord_authorize(
        self,
    ) -> None:
        if self.discord_authorization_in_progress:
            return

        self.discord_authorization_in_progress = True
        self.discord_authorization_source = (
            "setup"
            if (self.window.pages.currentWidget() is self.window.setup_page)
            else "settings"
        )

        if self.discord_authorization_source == "setup":
            self.window.setup_page.set_authorization_busy(True)
            self.window.setup_page.set_status(
                "Opening Discord authorization in " "your browser..."
            )
        else:
            self.window.settings_page.set_authorization_busy(True)
            self.window.settings_page.set_status(
                "Opening Discord authorization in " "your browser..."
            )

        worker = TaskWorker(self._perform_discord_authorization)

        self._start_worker(
            worker,
            succeeded=(self._handle_discord_authorization_result),
            failed=(self._handle_discord_authorization_error),
            finished=self._finish_discord_authorization,
        )

    def _perform_discord_authorization(
        self,
    ) -> dict:
        return self.discord_oauth_service.authorize(
            application_id=self.settings.discord_application_id,
            client_secret=self.storage.load_discord_client_secret(),
        )

    def _handle_discord_authorization_result(
        self,
        authorization: dict,
    ) -> None:
        self.storage.save_discord_oauth(authorization)

        self.settings.discord_user_id = str(
            authorization.get(
                "authorized_user_id",
                "",
            )
        )

        self.settings.last_error = ""

        self.storage.save_settings(self.settings)

        display_name = str(
            authorization.get(
                "authorized_display_name",
                "Discord User",
            )
        )

        if self.discord_authorization_source == "setup":
            self.window.setup_page.set_status(
                (
                    f"Discord authorized as "
                    f"{display_name}. Continue by "
                    "selecting your character."
                )
            )
            self.window.setup_page.set_authorization_ready(False)
            self.refresh_window()
            self.show_correct_page()
        else:
            self.refresh_window()
            self.handle_open_settings()
            self.window.settings_page.set_status(
                f"Discord authorized successfully as {display_name}."
            )

    def _handle_discord_authorization_error(
        self,
        message: str,
    ) -> None:
        if self.discord_authorization_source == "setup":
            self.window.setup_page.set_status(
                f"Discord authorization failed: {message}",
                is_error=True,
            )
        else:
            self.window.settings_page.set_status(
                f"Discord authorization failed: {message}",
                is_error=True,
            )

    def _finish_discord_authorization(
        self,
    ) -> None:
        if self.discord_authorization_source == "setup":
            self.window.setup_page.set_authorization_busy(False)
        else:
            self.window.settings_page.set_authorization_busy(False)

        self.discord_authorization_in_progress = False
        self.discord_authorization_source = ""

    def handle_discord_refresh(
        self,
    ) -> None:
        if self.discord_authorization_in_progress:
            return

        self.discord_authorization_in_progress = True
        self.discord_authorization_source = "settings"

        self.window.settings_page.set_authorization_busy(True)
        self.window.settings_page.set_status("Refreshing the Discord access token...")

        worker = TaskWorker(self._perform_discord_refresh)

        self._start_worker(
            worker,
            succeeded=self._handle_discord_refresh_result,
            failed=self._handle_discord_refresh_error,
            finished=self._finish_discord_authorization,
        )

    def _perform_discord_refresh(
        self,
    ) -> dict:
        return self.discord_oauth_service.refresh_authorization(
            application_id=self.settings.discord_application_id,
            client_secret=self.storage.load_discord_client_secret(),
            refresh_token=self.storage.load_discord_refresh_token(),
        )

    def _handle_discord_refresh_result(
        self,
        authorization: dict,
    ) -> None:
        self.storage.save_discord_oauth(authorization)

        self.settings.discord_user_id = str(
            authorization.get(
                "authorized_user_id",
                "",
            )
        )
        self.settings.last_error = ""

        self.storage.save_settings(self.settings)

        self.refresh_window()
        self.handle_open_settings()
        self.window.settings_page.set_status(
            "Discord access token refreshed successfully."
        )

    def _handle_discord_refresh_error(
        self,
        message: str,
    ) -> None:
        self.storage.clear_discord_oauth()
        self.refresh_window()
        self.handle_open_settings()
        self.window.settings_page.set_status(
            f"Discord token refresh failed. Authorize Discord again. {message}",
            is_error=True,
        )

    def handle_character_search(
        self,
        values: dict,
    ) -> None:
        realm = values.get(
            "realm",
            "",
        )
        character = values.get(
            "character",
            "",
        )
        region = values.get(
            "region",
            "us",
        )

        if not realm or not character:
            self.window.character_page.set_status(
                "Enter both a realm and character name.",
                is_error=True,
            )
            return

        try:
            client_id = self.storage.load_blizzard_client_id()
            client_secret = self.storage.load_blizzard_client_secret()
        except RuntimeError as error:
            self.window.character_page.set_status(
                str(error),
                is_error=True,
            )
            return

        self.window.character_page.clear_result()
        self.window.character_page.set_busy(True)
        self.window.character_page.set_status(
            "Searching Blizzard for this character..."
        )

        worker = TaskWorker(
            self.blizzard_service.get_character_profile,
            client_id=client_id,
            client_secret=client_secret,
            region=region,
            realm=realm,
            character=character,
        )

        self._start_worker(
            worker,
            succeeded=self._handle_character_search_result,
            failed=self._handle_character_search_error,
            finished=self._finish_character_search,
        )

    def _handle_character_search_result(
        self,
        character: dict,
    ) -> None:
        self.window.character_page.show_character(character)

    def _handle_character_search_error(
        self,
        message: str,
    ) -> None:
        self.window.character_page.set_status(
            f"Character lookup failed: {message}",
            is_error=True,
        )

    def _finish_character_search(
        self,
    ) -> None:
        self.window.character_page.set_busy(False)

    def handle_character_selected(
        self,
        character: dict,
    ) -> None:
        character_id = character.get("id")

        if not character_id:
            self.window.character_page.set_status(
                "The selected character has no Blizzard ID.",
                is_error=True,
            )
            return

        self._stop_update_timer()

        self.settings.wow_region = character.get("region") or "us"
        self.settings.wow_realm = character.get("realm_slug") or character.get(
            "realm",
            "",
        )
        self.settings.wow_character = character.get(
            "name",
            "",
        )
        self.settings.wow_character_id = int(character_id)

        composition = self.storage.load_portrait_composition(
            self.settings.wow_character_id
        )

        self.settings.updates_enabled = False
        self.settings.character_image_url = composition.image_url
        self.settings.last_payload_hash = ""
        self.settings.last_check_at = ""
        self.settings.last_push_at = ""
        self.settings.last_error = ""
        self.latest_widget_data = {}

        try:
            self.storage.save_settings(self.settings)
        except Exception as error:
            self.window.character_page.set_status(
                f"Unable to save character: {error}",
                is_error=True,
            )
            return

        self.window.character_page.clear_result()
        self._load_portrait_editor_state()
        self.refresh_window()
        self.window.show_status_page()

        self.window.set_operation_status(
            (
                "Character changed successfully. "
                "Generate or review the portrait before "
                "starting updates."
            )
        )

    def handle_change_character(
        self,
    ) -> None:
        if (
            self.widget_update_in_progress
            or self.portrait_generate_in_progress
            or self.portrait_save_in_progress
        ):
            self.window.set_operation_status(
                "Wait for the current operation to finish.",
                is_error=True,
            )
            return

        self.pause_updates(show_message=False)
        self.window.character_page.clear_result()
        self.window.show_character_page(
            region=self.settings.wow_region,
            realm=self.settings.wow_realm,
            character=self.settings.wow_character,
        )
        self.window.character_page.set_status(
            (
                "Search for a new character. Your current "
                "character remains selected until you press "
                "Use This Character."
            )
        )

    def handle_generate_portrait(
        self,
        composition: dict,
    ) -> None:
        if not self._character_is_selected():
            self.window.set_operation_status(
                "Select a character before generating a portrait.",
                is_error=True,
            )
            return

        if self.portrait_generate_in_progress or self.portrait_save_in_progress:
            return

        self.portrait_generate_in_progress = True
        self.window.set_portrait_generate_busy(True)
        self.window.set_operation_status(
            "Fetching the latest appearance and generating a preview..."
        )

        worker = TaskWorker(
            self.widget_update_service.generate_portrait_preview,
            self.settings,
            **composition,
        )

        self._start_worker(
            worker,
            succeeded=self._handle_generate_portrait_result,
            failed=self._handle_generate_portrait_error,
            finished=self._finish_generate_portrait,
        )

    def _handle_generate_portrait_result(
        self,
        result: dict,
    ) -> None:
        image_bytes = result.get(
            "image_bytes",
            b"",
        )
        width = int(
            result.get(
                "width",
                0,
            )
        )
        height = int(
            result.get(
                "height",
                0,
            )
        )

        self.window.show_portrait_bytes(
            image_bytes,
            width=width,
            height=height,
        )

        self.window.set_operation_status(
            (
                "Portrait generated. Adjust the controls, "
                "then press Save Portrait when satisfied."
            )
        )

    def _handle_generate_portrait_error(
        self,
        message: str,
    ) -> None:
        self.window.set_operation_status(
            f"Portrait generation failed: {message}",
            is_error=True,
        )

    def _finish_generate_portrait(
        self,
    ) -> None:
        self.portrait_generate_in_progress = False
        self.window.set_portrait_generate_busy(False)

    def handle_portrait_composition_changed(
        self,
        composition: dict,
    ) -> None:
        if not self._character_is_selected():
            return

        if not self.render_processor.has_cached_source(self.settings.wow_character_id):
            return

        self.pending_portrait_composition = composition
        self.portrait_preview_timer.start()

    def _apply_pending_portrait_preview(
        self,
    ) -> None:
        if (
            not self.pending_portrait_composition
            or self.portrait_generate_in_progress
            or self.portrait_save_in_progress
            or self.portrait_preview_in_progress
        ):
            return

        composition = self.pending_portrait_composition
        self.pending_portrait_composition = None
        self.portrait_preview_in_progress = True

        worker = TaskWorker(
            self.widget_update_service.update_local_portrait_preview,
            self.settings,
            **composition,
        )

        self._start_worker(
            worker,
            succeeded=self._handle_local_preview_result,
            failed=self._handle_local_preview_error,
            finished=self._finish_local_preview,
        )

    def _handle_local_preview_result(
        self,
        result: dict,
    ) -> None:
        image_bytes = result.get(
            "image_bytes",
            b"",
        )
        width = int(
            result.get(
                "width",
                0,
            )
        )
        height = int(
            result.get(
                "height",
                0,
            )
        )

        self.window.show_portrait_bytes(
            image_bytes,
            width=width,
            height=height,
        )

        self.window.set_operation_status(
            "Preview adjusted. Save Portrait to publish it."
        )

    def _handle_local_preview_error(
        self,
        message: str,
    ) -> None:
        self.window.set_operation_status(
            f"Unable to update portrait preview: {message}",
            is_error=True,
        )

    def _finish_local_preview(
        self,
    ) -> None:
        self.portrait_preview_in_progress = False

        if self.pending_portrait_composition:
            self.portrait_preview_timer.start()

    def handle_save_portrait(
        self,
        composition: dict,
    ) -> None:
        if not self._character_is_selected():
            self.window.set_operation_status(
                "Select a character before saving a portrait.",
                is_error=True,
            )
            return

        if not self.render_processor.has_cached_source(self.settings.wow_character_id):
            self.window.set_operation_status(
                "Generate the portrait before saving it.",
                is_error=True,
            )
            return

        if (
            self.portrait_generate_in_progress
            or self.portrait_save_in_progress
            or self.portrait_preview_in_progress
        ):
            self.window.set_operation_status(
                "Wait for the current portrait operation to finish.",
                is_error=True,
            )
            return

        self.portrait_save_in_progress = True
        self.window.set_portrait_save_busy(True)
        self.window.set_operation_status(
            "Saving composition and publishing the portrait..."
        )

        worker = TaskWorker(
            self.widget_update_service.save_portrait,
            self.settings,
            **composition,
        )

        self._start_worker(
            worker,
            succeeded=self._handle_save_portrait_result,
            failed=self._handle_save_portrait_error,
            finished=self._finish_save_portrait,
        )

    def _handle_save_portrait_result(
        self,
        result: dict,
    ) -> None:
        self.settings = self.storage.load_settings()

        portrait_path = result.get(
            "portrait_path",
            "",
        )

        if portrait_path:
            self.window.show_portrait(portrait_path)

        self.refresh_window()
        self.window.set_operation_status(
            (
                "Portrait composition saved and published. "
                "Press Update Widget Now to display it."
            )
        )

    def _handle_save_portrait_error(
        self,
        message: str,
    ) -> None:
        self.window.set_operation_status(
            f"Portrait save failed: {message}",
            is_error=True,
        )

    def _finish_save_portrait(
        self,
    ) -> None:
        self.portrait_save_in_progress = False
        self.window.set_portrait_save_busy(False)

    def handle_portrait_reset(
        self,
    ) -> None:
        self.window.set_portrait_composition(
            scale_percent=DEFAULT_PORTRAIT_SCALE_PERCENT,
            x_offset=DEFAULT_PORTRAIT_X_OFFSET,
            y_offset=DEFAULT_PORTRAIT_Y_OFFSET,
        )

        composition = self.window.get_portrait_composition()

        self.handle_portrait_composition_changed(composition)

    def _load_portrait_editor_state(
        self,
    ) -> None:
        character_id = self.settings.wow_character_id

        if not character_id:
            self.window.set_portrait_composition(
                scale_percent=DEFAULT_PORTRAIT_SCALE_PERCENT,
                x_offset=DEFAULT_PORTRAIT_X_OFFSET,
                y_offset=DEFAULT_PORTRAIT_Y_OFFSET,
            )
            self.window.clear_portrait()
            return

        composition = self.storage.load_portrait_composition(character_id)

        self.window.set_portrait_composition(
            scale_percent=composition.scale_percent,
            x_offset=composition.x_offset,
            y_offset=composition.y_offset,
        )

        portrait_path = self.render_processor.get_existing_portrait_path(character_id)

        if portrait_path is None:
            self.window.clear_portrait()
            return

        self.window.show_portrait(portrait_path)

    def handle_manual_widget_update(
        self,
    ) -> None:
        oauth_status = self.discord_oauth_service.authorization_status(self.storage)

        if not oauth_status.get("authorized"):
            self.window.set_operation_status(
                (
                    "Discord authorization is required. "
                    "Open Settings and authorize your "
                    "Discord account."
                ),
                is_error=True,
            )
            self.refresh_window()
            return

        if not self._character_is_selected():
            self.window.set_operation_status(
                "Select a character before updating.",
                is_error=True,
            )
            return

        if self.widget_update_in_progress:
            self.window.set_operation_status(
                "A widget update is already running.",
                is_error=True,
            )
            return

        self.widget_update_in_progress = True
        self.window.set_widget_update_busy(True)
        self.window.set_operation_status(
            "Fetching Blizzard data and updating Discord..."
        )

        worker = TaskWorker(
            self.widget_update_service.update_widget,
            self.settings,
            force_push=True,
        )

        self._start_worker(
            worker,
            succeeded=self._handle_manual_update_result,
            failed=self._handle_manual_update_error,
            finished=self._finish_widget_update,
        )

    def _handle_manual_update_result(
        self,
        result: dict,
    ) -> None:
        self.settings = self.storage.load_settings()

        self.latest_widget_data = dict(
            result.get(
                "widget_data",
                {},
            )
        )

        self.refresh_window()

        status_code = result.get(
            "status_code",
            "Unknown",
        )

        self.window.set_operation_status(
            f"Widget updated successfully. Discord status: {status_code}."
        )

    def _handle_manual_update_error(
        self,
        message: str,
    ) -> None:
        self._record_update_error(message)
        self.window.set_operation_status(
            f"Widget update failed: {message}",
            is_error=True,
        )

    def _finish_widget_update(
        self,
    ) -> None:
        self.widget_update_in_progress = False
        self.window.set_widget_update_busy(False)

    def handle_updates_toggle(
        self,
    ) -> None:
        if self.settings.updates_enabled:
            self.pause_updates()
        else:
            self.start_updates()

    def start_updates(
        self,
        *,
        show_message: bool = True,
    ) -> None:
        oauth_status = self.discord_oauth_service.authorization_status(self.storage)

        if not oauth_status.get("authorized"):
            self.window.set_operation_status(
                (
                    "Discord authorization is required "
                    "before automatic updates can start."
                ),
                is_error=True,
            )
            self.refresh_window()
            return

        if not self._character_is_selected():
            self.window.set_operation_status(
                "Select a character before starting automatic updates.",
                is_error=True,
            )
            return

        interval_minutes = max(
            1,
            int(self.settings.update_interval_minutes or 30),
        )

        self.settings.update_interval_minutes = interval_minutes
        self.settings.updates_enabled = True

        try:
            self.storage.save_settings(self.settings)
        except Exception as error:
            self.settings.updates_enabled = False
            self.window.set_operation_status(
                f"Unable to start automatic updates: {error}",
                is_error=True,
            )
            return

        self._start_update_timer()
        self.refresh_window()

        if show_message:
            self.window.set_operation_status(
                (
                    "Automatic updates started. "
                    f"WoWidget will check every "
                    f"{interval_minutes} minutes."
                )
            )

    def pause_updates(
        self,
        *,
        show_message: bool = True,
    ) -> None:
        self._stop_update_timer()
        self.settings.updates_enabled = False

        try:
            self.storage.save_settings(self.settings)
        except Exception as error:
            self.window.set_operation_status(
                f"Unable to save the paused state: {error}",
                is_error=True,
            )
            return

        self.refresh_window()

        if show_message:
            self.window.set_operation_status("Automatic updates paused.")

    def _start_update_timer(
        self,
    ) -> None:
        interval_minutes = max(
            1,
            int(self.settings.update_interval_minutes or 30),
        )

        self.update_timer.start(interval_minutes * 60 * 1000)

    def _stop_update_timer(
        self,
    ) -> None:
        if self.update_timer.isActive():
            self.update_timer.stop()

    def handle_scheduled_widget_update(
        self,
    ) -> None:
        if not self.settings.updates_enabled:
            return

        if not self._character_is_selected():
            self.pause_updates(show_message=False)
            return

        if self.widget_update_in_progress:
            return

        self.widget_update_in_progress = True

        worker = TaskWorker(
            self.widget_update_service.update_widget,
            self.settings,
            force_push=False,
        )

        self._start_worker(
            worker,
            succeeded=self._handle_scheduled_update_result,
            failed=self._handle_scheduled_update_error,
            finished=self._finish_scheduled_update,
        )

    def _handle_scheduled_update_result(
        self,
        result: dict,
    ) -> None:
        self.settings = self.storage.load_settings()

        self.latest_widget_data = dict(
            result.get(
                "widget_data",
                {},
            )
        )

        self.refresh_window()

        if result.get("pushed"):
            self.window.set_operation_status(
                (
                    "Automatic update completed. "
                    "Widget changes were pushed to Discord."
                )
            )

            if not self.window.isVisible():
                self._show_tray_message(
                    "WoWidget Updated",
                    "Character changes were detected and pushed to Discord.",
                )
        else:
            self.window.set_operation_status(
                "Automatic check completed. No widget changes were detected."
            )

    def _handle_scheduled_update_error(
        self,
        message: str,
    ) -> None:
        self._record_update_error(message)
        self.window.set_operation_status(
            f"Automatic widget update failed: {message}",
            is_error=True,
        )

        if not self.window.isVisible():
            self._show_tray_message(
                "WoWidget Update Failed",
                message,
                is_error=True,
            )

    def _finish_scheduled_update(
        self,
    ) -> None:
        self.widget_update_in_progress = False

    def _record_update_error(
        self,
        message: str,
    ) -> None:
        try:
            self.widget_update_service.record_update_error(
                self.settings,
                message,
            )
            self.settings = self.storage.load_settings()
        except Exception:
            pass

        self.refresh_window()

    def _restore_scheduler_state(
        self,
    ) -> None:
        if self.settings.updates_enabled and self._character_is_selected():
            self._start_update_timer()
        else:
            self._stop_update_timer()

    def handle_open_settings(
        self,
    ) -> None:
        self.window.show_settings_page(
            launch_with_windows=(self.settings.launch_with_windows),
            start_minimized=(self.settings.start_minimized),
            update_interval_minutes=(self.settings.update_interval_minutes),
            authorization_status=(
                self.discord_oauth_service.authorization_status(self.storage)
            ),
        )

    def handle_settings_back(
        self,
    ) -> None:
        self.window.show_status_page()

    def handle_save_settings(
        self,
        values: dict,
    ) -> None:
        previous_interval = self.settings.update_interval_minutes
        previous_launch = self.settings.launch_with_windows
        previous_minimized = self.settings.start_minimized

        try:
            self.settings.update_interval_minutes = max(
                5,
                int(
                    values.get(
                        "update_interval_minutes",
                        30,
                    )
                ),
            )
            self.settings.launch_with_windows = bool(
                values.get(
                    "launch_with_windows",
                    False,
                )
            )
            self.settings.start_minimized = bool(
                values.get(
                    "start_minimized",
                    False,
                )
            )

            self.startup_manager.reconcile(
                launch_with_windows=(self.settings.launch_with_windows),
                start_minimized=(self.settings.start_minimized),
            )

            self.storage.save_settings(self.settings)

            if self.settings.updates_enabled:
                self._start_update_timer()

        except Exception as error:
            self.settings.update_interval_minutes = previous_interval
            self.settings.launch_with_windows = previous_launch
            self.settings.start_minimized = previous_minimized

            self.window.settings_page.set_status(
                f"Unable to save settings: {error}",
                is_error=True,
            )
            return

        self.refresh_window()
        self.window.settings_page.set_status("Settings saved successfully.")

    def handle_open_app_data(
        self,
    ) -> None:
        self._open_folder(get_app_data_directory())

    def handle_open_generated(
        self,
    ) -> None:
        generated_directory = get_app_data_directory() / "generated"

        generated_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._open_folder(generated_directory)

    def handle_open_github(
        self,
    ) -> None:
        webbrowser.open(
            GITHUB_REPOSITORY_URL,
            new=2,
        )

    def handle_reregister_installation(
        self,
    ) -> None:
        self.window.settings_page.set_registration_busy(True)
        self.window.settings_page.set_status("Repairing Cloudflare registration...")

        worker = TaskWorker(self._perform_reregistration)

        self._start_worker(
            worker,
            succeeded=self._handle_reregistration_result,
            failed=self._handle_reregistration_error,
            finished=self._finish_reregistration,
        )

    def _perform_reregistration(
        self,
    ) -> dict:
        bot_token = self.storage.load_discord_bot_token()

        if not bot_token:
            raise RuntimeError("Discord bot token is missing.")

        registration = self.worker_registration_service.register_installation(
            discord_application_id=self.settings.discord_application_id,
            discord_bot_token=bot_token,
        )

        install_token = str(
            registration.get(
                "install_token",
                "",
            )
        ).strip()

        if not install_token:
            raise RuntimeError(
                "The registration service returned no installation token."
            )

        self.storage.save_worker_install_token(install_token)

        return registration

    def _handle_reregistration_result(
        self,
        result: dict,
    ) -> None:
        application_name = str(
            result.get(
                "discord_application_name",
                "Discord application",
            )
        ).strip()

        self.window.settings_page.set_status(
            f"{application_name} was re-registered successfully."
        )

    def _handle_reregistration_error(
        self,
        message: str,
    ) -> None:
        self.window.settings_page.set_status(
            f"Registration repair failed: {message}",
            is_error=True,
        )

    def _finish_reregistration(
        self,
    ) -> None:
        self.window.settings_page.set_registration_busy(False)

    def handle_reset_application(
        self,
    ) -> None:
        try:
            self._stop_update_timer()
            self.startup_manager.disable()
            self.storage.reset_application()
            self.settings = WidgetSettings()
            self.latest_widget_data = {}

        except Exception as error:
            self.window.settings_page.set_status(
                f"Unable to reset WoWidget: {error}",
                is_error=True,
            )
            return

        self.refresh_window()
        self.show_correct_page()

    @staticmethod
    def _open_folder(
        folder: Path,
    ) -> None:
        folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        if os.name == "nt":
            os.startfile(str(folder))
            return

        webbrowser.open(folder.as_uri())

    def handle_manual_update_check(
        self,
    ) -> None:
        self._begin_update_check(manual=True)

    def _check_for_updates_on_startup(
        self,
    ) -> None:
        if not self._update_check_is_due():
            return

        self._begin_update_check(manual=False)

    def _update_check_is_due(
        self,
    ) -> bool:
        raw_timestamp = (self.settings.last_update_check_at or "").strip()

        if not raw_timestamp:
            return True

        try:
            last_check = datetime.fromisoformat(raw_timestamp)

            if last_check.tzinfo is None:
                last_check = last_check.replace(tzinfo=timezone.utc)

        except ValueError:
            return True

        elapsed = datetime.now(timezone.utc) - last_check.astimezone(timezone.utc)

        return elapsed.total_seconds() >= 86400

    def _begin_update_check(
        self,
        *,
        manual: bool,
    ) -> None:
        if self.update_check_in_progress:
            return

        self.update_check_in_progress = True
        self.update_check_is_manual = manual

        if manual:
            self.window.settings_page.set_update_check_busy(True)
            self.window.settings_page.set_status(
                "Checking GitHub for a newer release..."
            )

        worker = TaskWorker(self.update_checker.check_for_update)

        self._start_worker(
            worker,
            succeeded=self._handle_update_check_result,
            failed=self._handle_update_check_error,
            finished=self._finish_update_check,
        )

    def _handle_update_check_result(
        self,
        result: dict,
    ) -> None:
        self._record_update_check_time()

        if result.get("update_available"):
            self._show_update_available_dialog(result)
            return

        if self.update_check_is_manual:
            self.window.settings_page.set_status(
                result.get(
                    "message",
                    "You are using the latest version of WoWidget.",
                )
            )

    def _handle_update_check_error(
        self,
        message: str,
    ) -> None:
        self._record_update_check_time()

        if self.update_check_is_manual:
            self.window.settings_page.set_status(
                f"Update check failed: {message}",
                is_error=True,
            )

    def _finish_update_check(
        self,
    ) -> None:
        self.update_check_in_progress = False

        if self.update_check_is_manual:
            self.window.settings_page.set_update_check_busy(False)

        self.update_check_is_manual = False

    def _record_update_check_time(
        self,
    ) -> None:
        self.settings.last_update_check_at = datetime.now(timezone.utc).isoformat(
            timespec="seconds"
        )

        try:
            self.storage.save_settings(self.settings)
        except Exception:
            pass

    def _show_update_available_dialog(
        self,
        result: dict,
    ) -> None:
        latest_version = str(
            result.get(
                "latest_version",
                "",
            )
        ).strip()

        release_url = str(
            result.get(
                "release_url",
                "",
            )
        ).strip()

        message_box = QMessageBox(self.window)
        message_box.setWindowTitle("WoWidget Update Available")
        message_box.setIcon(QMessageBox.Icon.Information)
        message_box.setText(f"WoWidget {latest_version} is available.")
        message_box.setInformativeText(
            f"You currently have WoWidget {APP_VERSION} installed.\n\n"
            "Download and run the new installer to update WoWidget in place. "
            "Your saved settings, credentials, and portrait data will remain intact."
        )

        open_button = message_box.addButton(
            "Download Update",
            QMessageBox.ButtonRole.AcceptRole,
        )
        message_box.addButton(
            "Later",
            QMessageBox.ButtonRole.RejectRole,
        )

        message_box.exec()

        if message_box.clickedButton() is open_button and release_url:
            webbrowser.open(
                release_url,
                new=2,
            )

    def set_launch_with_windows(
        self,
        enabled: bool,
    ) -> None:
        previous_value = self.settings.launch_with_windows

        self.settings.launch_with_windows = bool(enabled)

        try:
            self.startup_manager.set_enabled(
                self.settings.launch_with_windows,
                start_minimized=(self.settings.start_minimized),
            )

            self.storage.save_settings(self.settings)

        except Exception:
            self.settings.launch_with_windows = previous_value
            raise

    def set_start_minimized(
        self,
        enabled: bool,
    ) -> None:
        previous_value = self.settings.start_minimized

        self.settings.start_minimized = bool(enabled)

        try:
            if self.settings.launch_with_windows:
                self.startup_manager.enable(
                    start_minimized=(self.settings.start_minimized)
                )

            self.storage.save_settings(self.settings)

        except Exception:
            self.settings.start_minimized = previous_value
            raise

    def _reconcile_startup_preferences(
        self,
    ) -> None:
        try:
            self.startup_manager.reconcile(
                launch_with_windows=(self.settings.launch_with_windows),
                start_minimized=(self.settings.start_minimized),
            )
        except RuntimeError as error:
            self.settings.last_error = str(error)

            try:
                self.storage.save_settings(self.settings)
            except Exception:
                pass

    def _start_worker(
        self,
        worker: TaskWorker,
        *,
        succeeded,
        failed,
        finished,
    ) -> None:
        self.active_workers.add(worker)
        worker.signals.succeeded.connect(succeeded)
        worker.signals.failed.connect(failed)
        worker.signals.finished.connect(finished)
        worker.signals.finished.connect(lambda: self.active_workers.discard(worker))
        self.thread_pool.start(worker)

    def _connection_readiness(
        self,
    ) -> dict:
        try:
            blizzard_ready = all(
                [
                    self.storage.load_blizzard_client_id(),
                    self.storage.load_blizzard_client_secret(),
                ]
            )
        except RuntimeError:
            blizzard_ready = False

        try:
            discord_ready = all(
                [
                    self.settings.discord_application_id,
                    self.settings.discord_user_id,
                    self.storage.load_discord_bot_token(),
                    self.storage.load_discord_client_secret(),
                ]
            )
        except RuntimeError:
            discord_ready = False

        try:
            cloudflare_ready = bool(self.storage.load_worker_install_token())
        except RuntimeError:
            cloudflare_ready = False

        oauth_status = self.discord_oauth_service.authorization_status(self.storage)

        return {
            "blizzard_ready": blizzard_ready,
            "discord_ready": discord_ready,
            "discord_authorized": bool(oauth_status.get("authorized")),
            "cloudflare_ready": cloudflare_ready,
        }

    def refresh_window(
        self,
    ) -> None:
        state = self._determine_state()

        self.window.display_state(
            state_name=state.value,
            state_description=self._get_state_description(state),
            character_name=self.settings.wow_character,
            realm=self.settings.wow_realm,
            region=self.settings.wow_region,
            updates_enabled=self.settings.updates_enabled,
            update_interval_minutes=(self.settings.update_interval_minutes),
            last_check_at=self.settings.last_check_at,
            last_push_at=self.settings.last_push_at,
            last_error=self.settings.last_error,
        )

        readiness = self._connection_readiness()

        self.window.display_connection_status(
            blizzard_ready=readiness["blizzard_ready"],
            discord_ready=readiness["discord_ready"],
            discord_authorized=readiness["discord_authorized"],
            cloudflare_ready=readiness["cloudflare_ready"],
            updater_running=(self.settings.updates_enabled),
        )

        self.window.display_character_summary(self.latest_widget_data)

        self._load_portrait_editor_state()

        self.tray_icon.setToolTip(f"WoWidget — {state.value}")

    def load_saved_state(
        self,
    ) -> None:
        self.settings = self.storage.load_settings()

        self._reconcile_startup_preferences()
        self._restore_scheduler_state()
        self.refresh_window()

    def show_correct_page(
        self,
    ) -> None:
        state = self._determine_state()

        if state in {
            ApplicationState.FIRST_RUN,
            ApplicationState.CREDENTIALS_MISSING,
        }:
            self.window.show_setup_page(
                application_id=self.settings.discord_application_id,
            )
            self.window.setup_page.set_authorization_ready(False)
            return

        if state == ApplicationState.AUTHORIZATION_REQUIRED:
            if not self._character_is_selected():
                self.window.show_setup_page(
                    application_id=self.settings.discord_application_id,
                )
                self.window.setup_page.set_authorization_ready(True)
                self.window.setup_page.set_status(
                    (
                        "Credentials are saved. Complete "
                        "Discord authorization to continue."
                    )
                )
            else:
                self.window.show_status_page()
            return

        if state == ApplicationState.CHARACTER_NOT_SELECTED:
            self.window.show_character_page(
                region=self.settings.wow_region,
                realm=self.settings.wow_realm,
                character=self.settings.wow_character,
            )
            return

        self.window.show_status_page()

    def show_window(
        self,
    ) -> None:
        self.refresh_window()
        self.show_correct_page()
        self.window.show()
        self.window.raise_()
        self.window.activateWindow()

    def exit_application(
        self,
    ) -> None:
        self._stop_update_timer()
        self.portrait_preview_timer.stop()

        self.window.allow_application_close()
        self.tray_icon.hide()
        self.window.close()

        qt_app = QApplication.instance()

        if qt_app is not None:
            qt_app.quit()

    def start(
        self,
    ) -> None:
        self.load_saved_state()
        self.show_correct_page()

        should_start_minimized = (
            self.start_minimized_requested or self.settings.start_minimized
        )

        if should_start_minimized:
            self.window.hide()
        else:
            self.window.show()

        QTimer.singleShot(
            1500,
            self._check_for_updates_on_startup,
        )
