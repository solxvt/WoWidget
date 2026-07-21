from typing import Any

import requests


class WorkerRegistrationService:
    def __init__(
        self,
        worker_base_url: str,
    ) -> None:
        self.worker_base_url = worker_base_url.rstrip("/")

    def register_installation(
        self,
        *,
        discord_application_id: str,
        discord_bot_token: str,
    ) -> dict[str, Any]:
        application_id = str(discord_application_id).strip()

        bot_token = str(discord_bot_token).strip()

        if not application_id.isdigit():
            raise ValueError("Discord Application ID is invalid.")

        if not bot_token:
            raise ValueError("Discord bot token is missing.")

        register_url = f"{self.worker_base_url}/register"

        try:
            response = requests.post(
                register_url,
                json={
                    "discord_application_id": (application_id),
                    "discord_bot_token": bot_token,
                },
                timeout=(10, 45),
            )

        except requests.Timeout as error:
            raise RuntimeError("Cloudflare registration timed out.") from error

        except requests.RequestException as error:
            raise RuntimeError(
                "Unable to contact the WoWidget " f"registration service: {error}"
            ) from error

        content_type = (
            response.headers.get(
                "Content-Type",
                "",
            )
            .split(";")[0]
            .strip()
            .lower()
        )

        response_text = response.text.strip()

        if content_type != "application/json":
            preview = response_text[:1000] if response_text else "<empty response body>"

            raise RuntimeError(
                "The registration service returned "
                "a non-JSON response.\n"
                f"URL: {register_url}\n"
                f"Status: {response.status_code}\n"
                f"Content-Type: "
                f"{content_type or '<missing>'}\n"
                f"Response: {preview}"
            )

        try:
            response_data = response.json()
        except requests.JSONDecodeError as error:
            raise RuntimeError(
                "The registration service claimed "
                "to return JSON, but it could not "
                "be decoded.\n"
                f"Status: {response.status_code}\n"
                f"Response: {response_text[:1000]}"
            ) from error

        if not response.ok:
            error_message = response_data.get(
                "error",
                ("The registration service " "rejected this installation."),
            )

            raise RuntimeError(f"{error_message} " f"(HTTP {response.status_code})")

        install_token = str(
            response_data.get(
                "install_token",
                "",
            )
        ).strip()

        returned_application_id = str(
            response_data.get(
                "discord_application_id",
                "",
            )
        ).strip()

        if returned_application_id != application_id:
            raise RuntimeError(
                "The registration service returned "
                "an unexpected Discord Application ID."
            )

        if not install_token:
            raise RuntimeError(
                "The registration service returned " "no installation token."
            )

        return response_data
