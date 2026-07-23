from wowidget.storage.credentials import (
    BLIZZARD_CLIENT_ID,
    BLIZZARD_CLIENT_SECRET,
    DISCORD_ACCESS_TOKEN,
    DISCORD_AUTHORIZED_DISPLAY_NAME,
    DISCORD_AUTHORIZED_USER_ID,
    DISCORD_AUTHORIZED_USERNAME,
    DISCORD_BOT_TOKEN,
    DISCORD_CLIENT_SECRET,
    DISCORD_REFRESH_TOKEN,
    DISCORD_TOKEN_EXPIRY,
    WORKER_INSTALL_TOKEN,
    CredentialStore,
)
from wowidget.storage.database import (
    SettingsDatabase,
)
from wowidget.storage.models import (
    PortraitComposition,
    WidgetSettings,
)


class StorageManager:
    """Provides one interface for settings, portraits, and secure credentials."""

    def __init__(self) -> None:
        self.database = SettingsDatabase()
        self.credentials = CredentialStore()



    def load_settings(self) -> WidgetSettings:
        return self.database.load_settings()

    def save_settings(
        self,
        settings: WidgetSettings,
    ) -> None:
        self.database.save_settings(settings)



    def load_portrait_composition(
        self,
        character_id: int,
    ) -> PortraitComposition:
        return self.database.load_portrait_composition(character_id)

    def save_portrait_composition(
        self,
        composition: PortraitComposition,
    ) -> None:
        self.database.save_portrait_composition(composition)



    def save_discord_credentials(
        self,
        *,
        bot_token: str,
        client_secret: str,
    ) -> None:
        self.credentials.save_discord_credentials(
            bot_token=bot_token,
            client_secret=client_secret,
        )

    def load_discord_bot_token(self) -> str:
        return self.credentials.load_discord_bot_token()

    def load_discord_client_secret(self) -> str:
        return self.credentials.load_discord_client_secret()



    def save_discord_oauth(
        self,
        authorization: dict,
    ) -> None:
        self.credentials.save_discord_oauth(authorization)

    def load_discord_access_token(
        self,
    ) -> str:
        return self.credentials.load_discord_access_token()

    def load_discord_refresh_token(
        self,
    ) -> str:
        return self.credentials.load_discord_refresh_token()

    def load_discord_token_expiry(
        self,
    ) -> str:
        return self.credentials.load_discord_token_expiry()

    def load_discord_authorized_user_id(
        self,
    ) -> str:
        return self.credentials.load_discord_authorized_user_id()

    def load_discord_authorized_username(
        self,
    ) -> str:
        return self.credentials.load_discord_authorized_username()

    def load_discord_authorized_display_name(
        self,
    ) -> str:
        return self.credentials.load_discord_authorized_display_name()

    def clear_discord_oauth(
        self,
    ) -> None:
        for key in (
            DISCORD_ACCESS_TOKEN,
            DISCORD_REFRESH_TOKEN,
            DISCORD_TOKEN_EXPIRY,
            DISCORD_AUTHORIZED_USER_ID,
            DISCORD_AUTHORIZED_USERNAME,
            DISCORD_AUTHORIZED_DISPLAY_NAME,
        ):
            self.credentials.delete(key)



    def save_blizzard_credentials(
        self,
        *,
        client_id: str,
        client_secret: str,
    ) -> None:
        self.credentials.save_blizzard_credentials(
            client_id=client_id,
            client_secret=client_secret,
        )

    def load_blizzard_client_id(self) -> str:
        return self.credentials.load_blizzard_client_id()

    def load_blizzard_client_secret(self) -> str:
        return self.credentials.load_blizzard_client_secret()



    def save_worker_install_token(
        self,
        install_token: str,
    ) -> None:
        self.credentials.save_worker_install_token(install_token)

    def load_worker_install_token(self) -> str:
        return self.credentials.load_worker_install_token()



    def clear_discord_credentials(self) -> None:
        self.credentials.delete(DISCORD_BOT_TOKEN)

        self.credentials.delete(DISCORD_CLIENT_SECRET)

    def clear_blizzard_credentials(self) -> None:
        self.credentials.delete(BLIZZARD_CLIENT_ID)

        self.credentials.delete(BLIZZARD_CLIENT_SECRET)

    def clear_worker_install_token(self) -> None:
        self.credentials.delete(WORKER_INSTALL_TOKEN)

    def reset_application(
        self,
    ) -> None:
        self.clear_discord_credentials()
        self.clear_discord_oauth()
        self.clear_blizzard_credentials()
        self.clear_worker_install_token()
        self.database.reset_application()
