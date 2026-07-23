from typing import Any

import requests

from wowidget.config import (
    DISCORD_API_VERSION,
    DISCORD_USER_AGENT,
    DISCORD_WIDGET_API_VERSION,
)


class DiscordService:
    """Validates Discord application credentials and publishes widget data."""

    VALIDATION_API_BASE_URL = f"https://discord.com/api/v{DISCORD_API_VERSION}"
    WIDGET_API_BASE_URL = f"https://discord.com/api/v{DISCORD_WIDGET_API_VERSION}"
    USER_AGENT = DISCORD_USER_AGENT



    def validate_credentials(
        self,
        *,
        application_id: str,
        bot_token: str,
    ) -> tuple[bool, str]:
        if not application_id or not bot_token:
            return False, "Discord credentials are missing."

        try:
            response = requests.get(
                f"{self.VALIDATION_API_BASE_URL}/applications/@me",
                headers={
                    "Authorization": f"Bot {bot_token}",
                    "User-Agent": self.USER_AGENT,
                },
                timeout=(10, 30),
            )

        except requests.RequestException as error:
            return (
                False,
                f"Unable to contact Discord: {error}",
            )

        if response.status_code == 401:
            return (
                False,
                "Discord rejected the Bot Token.",
            )

        if not response.ok:
            return (
                False,
                f"Discord validation failed with status {response.status_code}.",
            )

        application_data = response.json()

        returned_application_id = str(application_data.get("id", ""))

        if returned_application_id != str(application_id):
            return (
                False,
                "The Discord Application ID does not "
                "belong to the supplied Bot Token.",
            )

        application_name = application_data.get("name") or "Discord application"

        return (
            True,
            f"{application_name} verified.",
        )



    def push_widget_data(
        self,
        *,
        application_id: str,
        discord_user_id: str,
        bot_token: str,
        payload: dict[str, Any],
    ) -> int:
        if not application_id:
            raise ValueError("Discord Application ID is missing.")

        if not discord_user_id:
            raise ValueError("Discord User ID is missing.")

        if not bot_token:
            raise ValueError("Discord Bot Token is missing.")

        url = (
            f"{self.WIDGET_API_BASE_URL}"
            f"/applications/{application_id}"
            f"/users/{discord_user_id}"
            "/identities/0/profile"
        )

        try:
            response = requests.patch(
                url,
                headers={
                    "Authorization": f"Bot {bot_token}",
                    "Content-Type": "application/json",
                    "User-Agent": self.USER_AGENT,
                },
                json=payload,
                timeout=(10, 30),
            )

        except requests.Timeout as error:
            raise RuntimeError("Discord widget update timed out.") from error

        except requests.RequestException as error:
            raise RuntimeError(
                f"Unable to contact Discord while updating the widget: {error}"
            ) from error

        if not response.ok:
            response_body = response.text.strip() or "No response body."

            raise RuntimeError(
                "Discord rejected the widget update. "
                f"Status: {response.status_code}. "
                f"Response: {response_body}"
            )

        return response.status_code
