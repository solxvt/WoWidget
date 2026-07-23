import time
from typing import Any
from urllib.parse import urlparse

import requests


class BlizzardService:
    """Fetches and validates World of Warcraft data from Blizzard APIs."""

    TOKEN_URL = "https://oauth.battle.net/token"

    def __init__(self) -> None:
        self._access_token = ""
        self._token_expires_at = 0.0

    def validate_credentials(
        self,
        client_id: str,
        client_secret: str,
    ) -> tuple[bool, str]:
        if not client_id or not client_secret:
            return False, "Blizzard credentials are missing."

        try:
            self._request_token(
                client_id=client_id,
                client_secret=client_secret,
                force_refresh=True,
            )

        except requests.HTTPError as error:
            if error.response is not None and error.response.status_code == 401:
                return (
                    False,
                    "Blizzard rejected the Client ID or Client Secret.",
                )

            return False, f"Blizzard validation failed: {error}"

        except requests.RequestException as error:
            return False, f"Unable to contact Blizzard: {error}"

        except Exception as error:
            return False, f"Blizzard validation failed: {error}"

        return True, "Blizzard credentials verified."

    def _request_token(
        self,
        *,
        client_id: str,
        client_secret: str,
        force_refresh: bool = False,
    ) -> str:
        now = time.time()

        if not force_refresh and self._access_token and now < self._token_expires_at:
            return self._access_token

        last_error: Exception | None = None
        response: requests.Response | None = None

        for attempt in range(3):
            try:
                response = requests.post(
                    self.TOKEN_URL,
                    data={
                        "grant_type": "client_credentials",
                    },
                    auth=(
                        client_id,
                        client_secret,
                    ),
                    timeout=(10, 30),
                )

                response.raise_for_status()
                break

            except requests.Timeout as error:
                last_error = error

                if attempt == 2:
                    raise RuntimeError(
                        "Blizzard authentication timed out " "after 3 attempts."
                    ) from error

                time.sleep(2 * (attempt + 1))

            except requests.RequestException:
                raise

        if response is None:
            raise RuntimeError(f"Unable to contact Blizzard: {last_error}")

        token_data = response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            raise RuntimeError("Blizzard returned no access token.")

        expires_in = int(token_data.get("expires_in", 86400))

        self._access_token = access_token
        self._token_expires_at = time.time() + expires_in - 300

        return access_token


    @staticmethod
    def normalize_realm(realm: str) -> str:
        return realm.strip().lower().replace("'", "").replace(" ", "-")

    @staticmethod
    def normalize_character(character: str) -> str:
        return character.strip().lower()



    def _get_json(
        self,
        *,
        path: str,
        namespace: str,
        region: str,
        locale: str,
        access_token: str,
        allow_not_found: bool = False,
    ) -> dict[str, Any] | None:
        url = f"https://{region}.api.blizzard.com" f"{path}"

        last_error: Exception | None = None

        for attempt in range(3):
            try:
                response = requests.get(
                    url,
                    params={
                        "namespace": namespace,
                        "locale": locale,
                    },
                    headers={
                        "Authorization": (f"Bearer {access_token}"),
                    },
                    timeout=(10, 30),
                )

                if allow_not_found and response.status_code == 404:
                    return None

                response.raise_for_status()
                return response.json()

            except requests.Timeout as error:
                last_error = error

                if attempt == 2:
                    raise RuntimeError(f"Blizzard request timed out: {path}") from error

                time.sleep(2 * (attempt + 1))

            except requests.RequestException:
                raise

        raise RuntimeError(f"Unable to contact Blizzard: {last_error}")

    def _get_optional_json(
        self,
        *,
        path: str,
        namespace: str,
        region: str,
        locale: str,
        access_token: str,
    ) -> dict[str, Any]:
        try:
            result = self._get_json(
                path=path,
                namespace=namespace,
                region=region,
                locale=locale,
                access_token=access_token,
                allow_not_found=True,
            )

            return result if isinstance(result, dict) else {}

        except (
            requests.RequestException,
            RuntimeError,
        ):
            return {}

    @staticmethod
    def _path_from_blizzard_url(
        url: str,
    ) -> str:
        parsed_url = urlparse(url)
        return parsed_url.path



    def get_character_profile(
        self,
        *,
        client_id: str,
        client_secret: str,
        region: str,
        realm: str,
        character: str,
        locale: str = "en_US",
    ) -> dict[str, Any]:
        region = region.strip().lower()
        realm_slug = self.normalize_realm(realm)
        character_name = self.normalize_character(character)

        access_token = self._request_token(
            client_id=client_id,
            client_secret=client_secret,
        )

        profile_path = f"/profile/wow/character/" f"{realm_slug}/{character_name}"

        profile = self._get_json(
            path=profile_path,
            namespace=f"profile-{region}",
            region=region,
            locale=locale,
            access_token=access_token,
            allow_not_found=True,
        )

        if profile is None:
            raise LookupError(
                f"Character '{character}' was not found " f"on realm '{realm}'."
            )

        race = profile.get("race") or {}
        character_class = profile.get("character_class") or {}
        active_spec = profile.get("active_spec") or {}
        profile_realm = profile.get("realm") or {}
        faction = profile.get("faction") or {}
        guild = profile.get("guild") or {}

        return {
            "id": profile.get("id"),
            "name": profile.get("name") or character,
            "realm": (profile_realm.get("name") or realm),
            "realm_slug": (profile_realm.get("slug") or realm_slug),
            "region": region,
            "level": profile.get("level"),
            "race": race.get("name") or "Unknown",
            "class": (character_class.get("name") or "Unknown"),
            "spec": (active_spec.get("name") or "Unknown"),
            "faction": (faction.get("name") or "Unknown"),
            "guild": (guild.get("name") or "---"),
        }



    def get_character_bundle(
        self,
        *,
        client_id: str,
        client_secret: str,
        region: str,
        realm: str,
        character: str,
        locale: str = "en_US",
    ) -> dict[str, Any]:
        region = region.strip().lower()
        realm_slug = self.normalize_realm(realm)
        character_name = self.normalize_character(character)

        access_token = self._request_token(
            client_id=client_id,
            client_secret=client_secret,
        )

        namespace = f"profile-{region}"

        base_path = f"/profile/wow/character/" f"{realm_slug}/{character_name}"

        profile = self._get_json(
            path=base_path,
            namespace=namespace,
            region=region,
            locale=locale,
            access_token=access_token,
            allow_not_found=True,
        )

        if profile is None:
            raise LookupError(
                f"Character '{character}' was not found " f"on realm '{realm}'."
            )

        equipment = self._get_json(
            path=f"{base_path}/equipment",
            namespace=namespace,
            region=region,
            locale=locale,
            access_token=access_token,
            allow_not_found=True,
        )

        mythic_plus = self._get_json(
            path=(f"{base_path}/" "mythic-keystone-profile"),
            namespace=namespace,
            region=region,
            locale=locale,
            access_token=access_token,
            allow_not_found=True,
        )

        pvp_summary = self._get_json(
            path=f"{base_path}/pvp-summary",
            namespace=namespace,
            region=region,
            locale=locale,
            access_token=access_token,
            allow_not_found=True,
        )

        raid_encounters = self._get_json(
            path=f"{base_path}/encounters/raids",
            namespace=namespace,
            region=region,
            locale=locale,
            access_token=access_token,
            allow_not_found=True,
        )

        character_media = self._get_json(
            path=f"{base_path}/character-media",
            namespace=namespace,
            region=region,
            locale=locale,
            access_token=access_token,
            allow_not_found=True,
        )

        mounts_collection = self._get_optional_json(
            path=f"{base_path}/collections/mounts",
            namespace=namespace,
            region=region,
            locale=locale,
            access_token=access_token,
        )

        pets_collection = self._get_optional_json(
            path=f"{base_path}/collections/pets",
            namespace=namespace,
            region=region,
            locale=locale,
            access_token=access_token,
        )

        titles_summary = self._get_optional_json(
            path=f"{base_path}/titles",
            namespace=namespace,
            region=region,
            locale=locale,
            access_token=access_token,
        )

        reputations_summary = self._get_optional_json(
            path=f"{base_path}/reputations",
            namespace=namespace,
            region=region,
            locale=locale,
            access_token=access_token,
        )

        achievements_summary = self._get_optional_json(
            path=f"{base_path}/achievements",
            namespace=namespace,
            region=region,
            locale=locale,
            access_token=access_token,
        )

        pvp_brackets: list[dict[str, Any]] = []

        if isinstance(pvp_summary, dict):
            raw_brackets = pvp_summary.get("brackets")

            if isinstance(raw_brackets, list):
                for bracket in raw_brackets:
                    if not isinstance(bracket, dict):
                        continue

                    bracket_url = bracket.get("href")

                    if not bracket_url:
                        continue

                    bracket_path = self._path_from_blizzard_url(bracket_url)

                    bracket_data = self._get_json(
                        path=bracket_path,
                        namespace=namespace,
                        region=region,
                        locale=locale,
                        access_token=access_token,
                        allow_not_found=True,
                    )

                    if isinstance(
                        bracket_data,
                        dict,
                    ):
                        pvp_brackets.append(bracket_data)

        return {
            "profile": profile,
            "equipment": equipment or {},
            "mythic_plus": mythic_plus or {},
            "pvp_summary": pvp_summary or {},
            "pvp_brackets": pvp_brackets,
            "raid_encounters": (raid_encounters or {}),
            "character_media": (character_media or {}),
            "mounts_collection": mounts_collection,
            "pets_collection": pets_collection,
            "titles_summary": titles_summary,
            "reputations_summary": reputations_summary,
            "achievements_summary": achievements_summary,
        }
