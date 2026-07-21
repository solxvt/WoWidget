from dataclasses import dataclass

DEFAULT_PORTRAIT_SCALE_PERCENT = 100
DEFAULT_PORTRAIT_X_OFFSET = 170
DEFAULT_PORTRAIT_Y_OFFSET = 650


@dataclass
class WidgetSettings:
    discord_user_id: str = ""
    discord_application_id: str = ""

    wow_region: str = "us"
    wow_realm: str = ""
    wow_character: str = ""
    wow_character_id: int | None = None

    update_interval_minutes: int = 30
    updates_enabled: bool = False

    launch_with_windows: bool = False
    start_minimized: bool = False

    last_update_check_at: str = ""

    last_payload_hash: str = ""
    last_check_at: str = ""
    last_push_at: str = ""
    last_error: str = ""

    character_image_url: str = ""


@dataclass
class PortraitComposition:
    character_id: int
    scale_percent: int = DEFAULT_PORTRAIT_SCALE_PERCENT
    x_offset: int = DEFAULT_PORTRAIT_X_OFFSET
    y_offset: int = DEFAULT_PORTRAIT_Y_OFFSET
    image_url: str = ""
