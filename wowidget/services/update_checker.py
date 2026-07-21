import re
from typing import Any

import requests

from wowidget.config import (
    APP_VERSION,
    GITHUB_API_VERSION,
    GITHUB_LATEST_RELEASE_API_URL,
    GITHUB_REPOSITORY,
)


class UpdateChecker:
    """Checks the configured GitHub repository for a newer release."""

    def check_for_update(
        self,
    ) -> dict[str, Any]:
        if not GITHUB_REPOSITORY or GITHUB_REPOSITORY.startswith("OWNER/"):
            raise RuntimeError("The GitHub repository has not been " "configured yet.")

        try:
            response = requests.get(
                GITHUB_LATEST_RELEASE_API_URL,
                headers={
                    "Accept": ("application/vnd.github+json"),
                    "X-GitHub-Api-Version": (GITHUB_API_VERSION),
                    "User-Agent": (f"WoWidget/{APP_VERSION}"),
                },
                timeout=(10, 20),
            )

            if response.status_code == 404:
                return {
                    "update_available": False,
                    "current_version": APP_VERSION,
                    "latest_version": "",
                    "release_name": "",
                    "release_url": "",
                    "message": (
                        "No public WoWidget releases have been published yet. "
                        "You are likely running a development or release-candidate build."
                    ),
                }

            response.raise_for_status()

        except requests.Timeout as error:
            raise RuntimeError("The GitHub update check timed out.") from error

        except requests.RequestException as error:
            raise RuntimeError(
                "Unable to contact GitHub for updates: " f"{error}"
            ) from error

        try:
            release_data = response.json()

        except ValueError as error:
            raise RuntimeError("GitHub returned an invalid update response.") from error

        tag_name = str(
            release_data.get(
                "tag_name",
                "",
            )
        ).strip()

        latest_version = self._normalize_version(tag_name)

        if not latest_version:
            raise RuntimeError("The latest GitHub release has no valid " "version tag.")

        release_url = str(
            release_data.get(
                "html_url",
                "",
            )
        ).strip()

        release_name = str(
            release_data.get(
                "name",
                "",
            )
        ).strip()

        update_available = self._version_key(latest_version) > self._version_key(
            APP_VERSION
        )

        return {
            "update_available": update_available,
            "current_version": APP_VERSION,
            "latest_version": latest_version,
            "release_name": (release_name or f"WoWidget {latest_version}"),
            "release_url": release_url,
            "message": (
                (f"WoWidget {latest_version} " "is available.")
                if update_available
                else ("You are using the latest " "version of WoWidget.")
            ),
        }

    @staticmethod
    def _normalize_version(
        value: str,
    ) -> str:
        cleaned = value.strip()

        if cleaned.lower().startswith("v"):
            cleaned = cleaned[1:]

        match = re.search(
            r"\d+(?:\.\d+){0,3}",
            cleaned,
        )

        return match.group(0) if match else ""

    @staticmethod
    def _version_key(
        value: str,
    ) -> tuple[int, ...]:
        normalized = UpdateChecker._normalize_version(value)

        if not normalized:
            return (
                0,
                0,
                0,
                0,
            )

        parts = [int(part) for part in normalized.split(".")]

        while len(parts) < 4:
            parts.append(0)

        return tuple(parts[:4])
