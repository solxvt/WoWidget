import hashlib
import json
from datetime import datetime
from typing import Any

from wowidget.assets.wow_assets import (
    get_achievement_icon,
    get_faction_icon,
    get_spec_icon,
)
from wowidget.services.blizzard import BlizzardService
from wowidget.services.discord import DiscordService
from wowidget.services.discord_oauth import (
    DiscordOAuthService,
)
from wowidget.services.discord_payload import (
    build_discord_payload,
)
from wowidget.services.image_uploader import (
    ImageUploader,
)
from wowidget.services.render_processor import (
    RenderProcessor,
)
from wowidget.services.widget_data import (
    build_widget_data,
)
from wowidget.storage import (
    StorageManager,
    WidgetSettings,
)
from wowidget.storage.models import (
    PortraitComposition,
)


class WidgetUpdateService:
    """Builds portrait and character data, then publishes it to Discord."""

    def __init__(
        self,
        *,
        storage: StorageManager,
        blizzard_service: BlizzardService,
        discord_service: DiscordService,
        render_processor: RenderProcessor,
        image_uploader: ImageUploader,
        discord_oauth_service: DiscordOAuthService,
    ) -> None:
        self.storage = storage
        self.blizzard_service = blizzard_service
        self.discord_service = discord_service
        self.render_processor = render_processor
        self.image_uploader = image_uploader
        self.discord_oauth_service = discord_oauth_service

    def generate_portrait_preview(
        self,
        settings: WidgetSettings,
        *,
        scale_percent: int,
        x_offset: int,
        y_offset: int,
    ) -> dict[str, Any]:
        self._validate_character_settings(settings)

        blizzard_client_id = self.storage.load_blizzard_client_id()

        blizzard_client_secret = self.storage.load_blizzard_client_secret()

        bundle = self.blizzard_service.get_character_bundle(
            client_id=blizzard_client_id,
            client_secret=blizzard_client_secret,
            region=settings.wow_region,
            realm=settings.wow_realm,
            character=settings.wow_character,
        )

        widget_data = build_widget_data(bundle)

        main_raw_url = str(
            widget_data.get(
                "main_raw_url",
                "",
            )
        ).strip()

        if not main_raw_url:
            raise RuntimeError("Blizzard returned no character render.")

        self.render_processor.fetch_character_source(
            source_url=main_raw_url,
            character_id=settings.wow_character_id,
        )

        preview_result = self.render_processor.generate_preview_bytes(
            character_id=settings.wow_character_id,
            scale_percent=scale_percent,
            x_offset=x_offset,
            y_offset=y_offset,
        )

        return {
            **preview_result,
            "scale_percent": scale_percent,
            "x_offset": x_offset,
            "y_offset": y_offset,
        }

    def update_local_portrait_preview(
        self,
        settings: WidgetSettings,
        *,
        scale_percent: int,
        x_offset: int,
        y_offset: int,
    ) -> dict[str, Any]:
        self._validate_character_settings(settings)

        preview_result = self.render_processor.generate_preview_bytes(
            character_id=settings.wow_character_id,
            scale_percent=scale_percent,
            x_offset=x_offset,
            y_offset=y_offset,
        )

        return {
            **preview_result,
            "scale_percent": scale_percent,
            "x_offset": x_offset,
            "y_offset": y_offset,
        }

    def save_portrait(
        self,
        settings: WidgetSettings,
        *,
        scale_percent: int,
        x_offset: int,
        y_offset: int,
    ) -> dict[str, Any]:
        self._validate_character_settings(settings)

        install_token = self.storage.load_worker_install_token()

        if not install_token:
            raise RuntimeError("The Cloudflare installation token is missing.")

        portrait_path = self.render_processor.save_final_portrait(
            character_id=settings.wow_character_id,
            scale_percent=scale_percent,
            x_offset=x_offset,
            y_offset=y_offset,
        )

        upload_result = self.image_uploader.upload_portrait(
            image_path=portrait_path,
            discord_application_id=settings.discord_application_id,
            character_id=settings.wow_character_id,
            install_token=install_token,
        )

        public_url = str(
            upload_result.get(
                "public_url",
                "",
            )
        ).strip()

        if not public_url:
            raise RuntimeError("The portrait upload returned no public image URL.")

        settings.character_image_url = public_url
        settings.last_payload_hash = ""

        composition = PortraitComposition(
            character_id=settings.wow_character_id,
            scale_percent=scale_percent,
            x_offset=x_offset,
            y_offset=y_offset,
            image_url=public_url,
        )

        self.storage.save_portrait_composition(composition)

        self.storage.save_settings(settings)

        return {
            "portrait_path": str(portrait_path),
            "public_url": public_url,
            "uploaded_at": upload_result.get(
                "uploaded_at",
                "",
            ),
            "size_bytes": upload_result.get(
                "size_bytes",
                0,
            ),
        }

    def update_widget(
        self,
        settings: WidgetSettings,
        *,
        force_push: bool = False,
    ) -> dict[str, Any]:
        self._validate_character_settings(settings)

        blizzard_client_id = self.storage.load_blizzard_client_id()

        blizzard_client_secret = self.storage.load_blizzard_client_secret()

        discord_client_secret = self.storage.load_discord_client_secret()

       
        self.discord_oauth_service.ensure_access_token(
            storage=self.storage,
            application_id=settings.discord_application_id,
            client_secret=discord_client_secret,
        )


        discord_bot_token = self.storage.load_discord_bot_token()

        checked_at = self._current_timestamp()

        bundle = self.blizzard_service.get_character_bundle(
            client_id=blizzard_client_id,
            client_secret=blizzard_client_secret,
            region=settings.wow_region,
            realm=settings.wow_realm,
            character=settings.wow_character,
        )

        widget_data = build_widget_data(bundle)

        widget_data["character_image_url"] = settings.character_image_url

        class_name = str(
            widget_data.get(
                "class",
                "",
            )
        ).strip()

        spec_name = str(
            widget_data.get(
                "spec",
                "",
            )
        ).strip()

        faction_name = str(
            widget_data.get(
                "faction",
                "",
            )
        ).strip()

        widget_data["spec_icon_url"] = get_spec_icon(
            class_name,
            spec_name,
        )

        widget_data["faction_icon_url"] = get_faction_icon(faction_name)

        widget_data["achievement_icon_url"] = get_achievement_icon()

        payload = build_discord_payload(widget_data)

        payload_hash = self._hash_payload(payload)

        payload_changed = payload_hash != settings.last_payload_hash

        if not force_push and not payload_changed:
            settings.last_check_at = checked_at
            settings.last_error = ""

            self.storage.save_settings(settings)

            return {
                "pushed": False,
                "reason": "unchanged",
                "checked_at": checked_at,
                "payload_hash": payload_hash,
                "widget_data": widget_data,
            }

        status_code = self.discord_service.push_widget_data(
            application_id=settings.discord_application_id,
            discord_user_id=settings.discord_user_id,
            bot_token=discord_bot_token,
            payload=payload,
        )

        pushed_at = self._current_timestamp()

        settings.last_check_at = checked_at
        settings.last_push_at = pushed_at
        settings.last_payload_hash = payload_hash
        settings.last_error = ""

        self.storage.save_settings(settings)

        return {
            "pushed": True,
            "status_code": status_code,
            "checked_at": checked_at,
            "pushed_at": pushed_at,
            "payload_hash": payload_hash,
            "widget_data": widget_data,
        }

    def record_update_error(
        self,
        settings: WidgetSettings,
        message: str,
    ) -> None:
        settings.last_check_at = self._current_timestamp()

        settings.last_error = message

        self.storage.save_settings(settings)

    @staticmethod
    def _validate_character_settings(
        settings: WidgetSettings,
    ) -> None:
        if not settings.discord_application_id:
            raise RuntimeError("Discord Application ID is missing.")

        if not settings.discord_user_id:
            raise RuntimeError("Discord User ID is missing.")

        if not settings.wow_region:
            raise RuntimeError("WoW region is missing.")

        if not settings.wow_realm:
            raise RuntimeError("WoW realm is missing.")

        if not settings.wow_character:
            raise RuntimeError("WoW character name is missing.")

        if not settings.wow_character_id:
            raise RuntimeError("Blizzard character ID is missing.")

    @staticmethod
    def _current_timestamp() -> str:
        return datetime.now().astimezone().strftime("%m/%d/%Y - %H:%M")

    @staticmethod
    def _hash_payload(
        payload: dict,
    ) -> str:
        serialized_payload = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
        )

        return hashlib.sha256(serialized_payload.encode("utf-8")).hexdigest()
