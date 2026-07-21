from pathlib import Path
from typing import Any

import requests


class ImageUploader:
    def __init__(
        self,
        worker_base_url: str,
    ) -> None:
        self.worker_base_url = worker_base_url.rstrip("/")

    def upload_portrait(
        self,
        *,
        image_path: str | Path,
        discord_application_id: str,
        character_id: int,
        install_token: str,
    ) -> dict[str, Any]:
        path = Path(image_path)

        if not path.is_file():
            raise FileNotFoundError(f"Portrait file not found: {path}")

        application_id = str(discord_application_id).strip()

        if not application_id.isdigit():
            raise ValueError("Discord Application ID is invalid.")

        if not character_id:
            raise ValueError("Blizzard character ID is missing.")

        if not install_token:
            raise ValueError("WoWidget installation token is missing.")

        try:
            image_bytes = path.read_bytes()
        except OSError as error:
            raise RuntimeError("Unable to read the generated portrait.") from error

        upload_url = f"{self.worker_base_url}/portrait"

        try:
            response = requests.put(
                upload_url,
                headers={
                    "Authorization": (f"Bearer {install_token}"),
                    "Content-Type": "image/png",
                    "X-WoWidget-Application-Id": (application_id),
                    "X-WoWidget-Character-Id": (str(character_id)),
                },
                data=image_bytes,
                timeout=(10, 60),
            )

        except requests.Timeout as error:
            raise RuntimeError("Portrait upload timed out.") from error

        except requests.RequestException as error:
            raise RuntimeError(
                "Unable to contact the WoWidget " f"upload service: {error}"
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
                "The upload service returned a non-JSON response.\n"
                f"URL: {upload_url}\n"
                f"Status: {response.status_code}\n"
                f"Content-Type: {content_type or '<missing>'}\n"
                f"Response: {preview}"
            )

        try:
            response_data = response.json()
        except requests.JSONDecodeError as error:
            raise RuntimeError(
                "The upload service claimed to return JSON, "
                "but the response could not be decoded.\n"
                f"Status: {response.status_code}\n"
                f"Response: {response_text[:1000]}"
            ) from error

        if not response.ok:
            error_message = response_data.get(
                "error",
                "The upload service rejected the portrait.",
            )

            raise RuntimeError(f"{error_message} (HTTP {response.status_code})")

        public_url = str(
            response_data.get(
                "public_url",
                "",
            )
        ).strip()

        if not public_url:
            raise RuntimeError("The upload service returned no public portrait URL.")

        return response_data
