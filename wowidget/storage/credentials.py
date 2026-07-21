import keyring
from keyring.errors import KeyringError

SERVICE_NAME = "WoWidget"

DISCORD_BOT_TOKEN = "discord_bot_token"
DISCORD_CLIENT_SECRET = "discord_client_secret"

DISCORD_ACCESS_TOKEN = "discord_access_token"
DISCORD_REFRESH_TOKEN = "discord_refresh_token"
DISCORD_TOKEN_EXPIRY = "discord_token_expiry"
DISCORD_AUTHORIZED_USER_ID = "discord_authorized_user_id"
DISCORD_AUTHORIZED_USERNAME = "discord_authorized_username"
DISCORD_AUTHORIZED_DISPLAY_NAME = "discord_authorized_display_name"

BLIZZARD_CLIENT_ID = "blizzard_client_id"
BLIZZARD_CLIENT_SECRET = "blizzard_client_secret"

WORKER_INSTALL_TOKEN = "worker_install_token"


class CredentialStore:
    """Stores application secrets in the operating system credential vault."""

    def save(
        self,
        key: str,
        value: str,
    ) -> None:
        try:
            keyring.set_password(
                SERVICE_NAME,
                key,
                value,
            )
        except KeyringError as error:
            raise RuntimeError(f"Unable to save credential '{key}'.") from error

    def load(
        self,
        key: str,
    ) -> str:
        try:
            return (
                keyring.get_password(
                    SERVICE_NAME,
                    key,
                )
                or ""
            )
        except KeyringError as error:
            raise RuntimeError(f"Unable to load credential '{key}'.") from error

    def delete(
        self,
        key: str,
    ) -> None:
        try:
            existing_value = keyring.get_password(
                SERVICE_NAME,
                key,
            )

            if existing_value is not None:
                keyring.delete_password(
                    SERVICE_NAME,
                    key,
                )

        except KeyringError as error:
            raise RuntimeError(f"Unable to delete credential '{key}'.") from error

    def save_discord_credentials(
        self,
        *,
        bot_token: str,
        client_secret: str,
    ) -> None:
        self.save(
            DISCORD_BOT_TOKEN,
            bot_token,
        )

        self.save(
            DISCORD_CLIENT_SECRET,
            client_secret,
        )

    def save_blizzard_credentials(
        self,
        *,
        client_id: str,
        client_secret: str,
    ) -> None:
        self.save(
            BLIZZARD_CLIENT_ID,
            client_id,
        )

        self.save(
            BLIZZARD_CLIENT_SECRET,
            client_secret,
        )

    def save_worker_install_token(
        self,
        install_token: str,
    ) -> None:
        self.save(
            WORKER_INSTALL_TOKEN,
            install_token,
        )

    def load_discord_bot_token(self) -> str:
        return self.load(DISCORD_BOT_TOKEN)

    def load_discord_client_secret(self) -> str:
        return self.load(DISCORD_CLIENT_SECRET)

    def load_blizzard_client_id(self) -> str:
        return self.load(BLIZZARD_CLIENT_ID)

    def load_blizzard_client_secret(self) -> str:
        return self.load(BLIZZARD_CLIENT_SECRET)

    def load_worker_install_token(self) -> str:
        return self.load(WORKER_INSTALL_TOKEN)

    def save_discord_oauth(
        self,
        authorization: dict,
    ) -> None:
        self.save(
            DISCORD_ACCESS_TOKEN,
            str(
                authorization.get(
                    "access_token",
                    "",
                )
            ),
        )
        self.save(
            DISCORD_REFRESH_TOKEN,
            str(
                authorization.get(
                    "refresh_token",
                    "",
                )
            ),
        )
        self.save(
            DISCORD_TOKEN_EXPIRY,
            str(
                authorization.get(
                    "expires_at",
                    "",
                )
            ),
        )
        self.save(
            DISCORD_AUTHORIZED_USER_ID,
            str(
                authorization.get(
                    "authorized_user_id",
                    "",
                )
            ),
        )
        self.save(
            DISCORD_AUTHORIZED_USERNAME,
            str(
                authorization.get(
                    "authorized_username",
                    "",
                )
            ),
        )
        self.save(
            DISCORD_AUTHORIZED_DISPLAY_NAME,
            str(
                authorization.get(
                    "authorized_display_name",
                    "",
                )
            ),
        )

    def load_discord_access_token(
        self,
    ) -> str:
        return self.load(DISCORD_ACCESS_TOKEN)

    def load_discord_refresh_token(
        self,
    ) -> str:
        return self.load(DISCORD_REFRESH_TOKEN)

    def load_discord_token_expiry(
        self,
    ) -> str:
        return self.load(DISCORD_TOKEN_EXPIRY)

    def load_discord_authorized_user_id(
        self,
    ) -> str:
        return self.load(DISCORD_AUTHORIZED_USER_ID)

    def load_discord_authorized_username(
        self,
    ) -> str:
        return self.load(DISCORD_AUTHORIZED_USERNAME)

    def load_discord_authorized_display_name(
        self,
    ) -> str:
        return self.load(DISCORD_AUTHORIZED_DISPLAY_NAME)
