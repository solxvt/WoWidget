import os
import sqlite3
from pathlib import Path

from wowidget.storage.models import (
    PortraitComposition,
    WidgetSettings,
)

APP_FOLDER_NAME = "WoWidget"


def get_app_data_directory() -> Path:
    local_app_data = os.getenv("LOCALAPPDATA")

    if not local_app_data:
        local_app_data = str(Path.home())

    app_directory = Path(local_app_data) / APP_FOLDER_NAME

    app_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return app_directory


DATABASE_PATH = get_app_data_directory() / "wowidget.db"


class SettingsDatabase:
    def __init__(
        self,
        database_path: Path = DATABASE_PATH,
    ) -> None:
        self.database_path = database_path
        self._initialize_database()

    def _connect(
        self,
    ) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)

        connection.row_factory = sqlite3.Row

        return connection

    def _initialize_database(
        self,
    ) -> None:
        with self._connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS widget_settings (
                    id INTEGER PRIMARY KEY CHECK (id = 1),

                    discord_user_id TEXT NOT NULL DEFAULT '',
                    discord_application_id TEXT NOT NULL DEFAULT '',

                    wow_region TEXT NOT NULL DEFAULT 'us',
                    wow_realm TEXT NOT NULL DEFAULT '',
                    wow_character TEXT NOT NULL DEFAULT '',
                    wow_character_id INTEGER,

                    update_interval_minutes INTEGER NOT NULL DEFAULT 30,
                    updates_enabled INTEGER NOT NULL DEFAULT 0,

                    launch_with_windows INTEGER NOT NULL DEFAULT 0,
                    start_minimized INTEGER NOT NULL DEFAULT 0,

                    last_update_check_at TEXT NOT NULL DEFAULT '',

                    last_payload_hash TEXT NOT NULL DEFAULT '',
                    last_check_at TEXT NOT NULL DEFAULT '',
                    last_push_at TEXT NOT NULL DEFAULT '',
                    last_error TEXT NOT NULL DEFAULT '',

                    character_image_url TEXT NOT NULL DEFAULT ''
                )
                """)

            self._ensure_column(
                connection,
                table_name="widget_settings",
                column_name="launch_with_windows",
                column_definition=("INTEGER NOT NULL DEFAULT 0"),
            )

            self._ensure_column(
                connection,
                table_name="widget_settings",
                column_name="start_minimized",
                column_definition=("INTEGER NOT NULL DEFAULT 0"),
            )

            self._ensure_column(
                connection,
                table_name="widget_settings",
                column_name="last_update_check_at",
                column_definition=("TEXT NOT NULL DEFAULT ''"),
            )

            connection.execute("""
                CREATE TABLE IF NOT EXISTS portrait_compositions (
                    character_id INTEGER PRIMARY KEY,
                    scale_percent INTEGER NOT NULL DEFAULT 100,
                    x_offset INTEGER NOT NULL DEFAULT 170,
                    y_offset INTEGER NOT NULL DEFAULT 650,
                    image_url TEXT NOT NULL DEFAULT '',
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """)

            connection.execute("""
                INSERT OR IGNORE INTO widget_settings (id)
                VALUES (1)
                """)

            connection.commit()

    @staticmethod
    def _ensure_column(
        connection: sqlite3.Connection,
        *,
        table_name: str,
        column_name: str,
        column_definition: str,
    ) -> None:
        columns = connection.execute(f"PRAGMA table_info({table_name})").fetchall()

        existing_names = {row["name"] for row in columns}

        if column_name in existing_names:
            return

        connection.execute(
            (
                f"ALTER TABLE {table_name} "
                f"ADD COLUMN {column_name} "
                f"{column_definition}"
            )
        )

    def load_settings(
        self,
    ) -> WidgetSettings:
        with self._connect() as connection:
            row = connection.execute("""
                SELECT *
                FROM widget_settings
                WHERE id = 1
                """).fetchone()

        if row is None:
            return WidgetSettings()

        return WidgetSettings(
            discord_user_id=(row["discord_user_id"]),
            discord_application_id=(row["discord_application_id"]),
            wow_region=(row["wow_region"]),
            wow_realm=(row["wow_realm"]),
            wow_character=(row["wow_character"]),
            wow_character_id=(row["wow_character_id"]),
            update_interval_minutes=(row["update_interval_minutes"]),
            updates_enabled=bool(row["updates_enabled"]),
            launch_with_windows=bool(row["launch_with_windows"]),
            start_minimized=bool(row["start_minimized"]),
            last_update_check_at=(row["last_update_check_at"]),
            last_payload_hash=(row["last_payload_hash"]),
            last_check_at=(row["last_check_at"]),
            last_push_at=(row["last_push_at"]),
            last_error=(row["last_error"]),
            character_image_url=(row["character_image_url"]),
        )

    def save_settings(
        self,
        settings: WidgetSettings,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE widget_settings
                SET
                    discord_user_id = ?,
                    discord_application_id = ?,

                    wow_region = ?,
                    wow_realm = ?,
                    wow_character = ?,
                    wow_character_id = ?,

                    update_interval_minutes = ?,
                    updates_enabled = ?,

                    launch_with_windows = ?,
                    start_minimized = ?,

                    last_update_check_at = ?,

                    last_payload_hash = ?,
                    last_check_at = ?,
                    last_push_at = ?,
                    last_error = ?,

                    character_image_url = ?
                WHERE id = 1
                """,
                (
                    settings.discord_user_id,
                    settings.discord_application_id,
                    settings.wow_region,
                    settings.wow_realm,
                    settings.wow_character,
                    settings.wow_character_id,
                    settings.update_interval_minutes,
                    int(settings.updates_enabled),
                    int(settings.launch_with_windows),
                    int(settings.start_minimized),
                    settings.last_update_check_at,
                    settings.last_payload_hash,
                    settings.last_check_at,
                    settings.last_push_at,
                    settings.last_error,
                    settings.character_image_url,
                ),
            )

            connection.commit()

    def load_portrait_composition(
        self,
        character_id: int,
    ) -> PortraitComposition:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT
                    character_id,
                    scale_percent,
                    x_offset,
                    y_offset,
                    image_url
                FROM portrait_compositions
                WHERE character_id = ?
                """,
                (character_id,),
            ).fetchone()

        if row is None:
            return PortraitComposition(character_id=character_id)

        return PortraitComposition(
            character_id=(row["character_id"]),
            scale_percent=(row["scale_percent"]),
            x_offset=(row["x_offset"]),
            y_offset=(row["y_offset"]),
            image_url=(row["image_url"]),
        )

    def save_portrait_composition(
        self,
        composition: PortraitComposition,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO portrait_compositions (
                    character_id,
                    scale_percent,
                    x_offset,
                    y_offset,
                    image_url,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(character_id)
                DO UPDATE SET
                    scale_percent = excluded.scale_percent,
                    x_offset = excluded.x_offset,
                    y_offset = excluded.y_offset,
                    image_url = excluded.image_url,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (
                    composition.character_id,
                    composition.scale_percent,
                    composition.x_offset,
                    composition.y_offset,
                    composition.image_url,
                ),
            )

            connection.commit()

    def reset_application(
        self,
    ) -> None:
        with self._connect() as connection:
            connection.execute("""
                DELETE FROM portrait_compositions
                """)

            connection.execute("""
                DELETE FROM widget_settings
                WHERE id = 1
                """)

            connection.execute("""
                INSERT INTO widget_settings (id)
                VALUES (1)
                """)

            connection.commit()
