import base64
import hashlib
import secrets
import threading
import time
import webbrowser
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from http.server import (
    BaseHTTPRequestHandler,
    ThreadingHTTPServer,
)
from typing import Any
from urllib.parse import (
    parse_qs,
    urlencode,
    urlparse,
)

import requests

from wowidget.config import (
    DISCORD_API_VERSION,
    DISCORD_OAUTH_AUTHORIZE_URL,
    DISCORD_OAUTH_CALLBACK_HOST,
    DISCORD_OAUTH_CALLBACK_PATH,
    DISCORD_OAUTH_CALLBACK_PORT,
    DISCORD_OAUTH_REDIRECT_URI,
    DISCORD_OAUTH_SCOPES,
    DISCORD_OAUTH_TIMEOUT_SECONDS,
    DISCORD_OAUTH_TOKEN_URL,
    DISCORD_USER_AGENT,
)
from wowidget.storage import StorageManager


class DiscordAuthorizationRequiredError(RuntimeError):
    pass


class DiscordOAuthService:
    """Handles Discord authorization, token refresh, and user identity lookup."""

    API_BASE_URL = f"https://discord.com/api/v{DISCORD_API_VERSION}"
    USER_AGENT = DISCORD_USER_AGENT

    def authorize(
        self,
        *,
        application_id: str,
        client_secret: str,
        timeout_seconds: int = DISCORD_OAUTH_TIMEOUT_SECONDS,
    ) -> dict[str, Any]:
        if not application_id:
            raise ValueError("Discord Application ID is missing.")

        if not client_secret:
            raise ValueError("Discord Client Secret is missing.")

        state = secrets.token_urlsafe(32)
        code_verifier = secrets.token_urlsafe(64)
        code_challenge = self._create_code_challenge(code_verifier)

        callback_result: dict[str, str] = {}
        callback_received = threading.Event()

        service = self

        class CallbackHandler(BaseHTTPRequestHandler):
            def do_GET(
                self,
            ) -> None:
                parsed_url = urlparse(self.path)

                if parsed_url.path != DISCORD_OAUTH_CALLBACK_PATH:
                    self.send_response(404)
                    self.end_headers()
                    return

                query = parse_qs(parsed_url.query)

                callback_result["code"] = query.get(
                    "code",
                    [""],
                )[0]
                callback_result["state"] = query.get(
                    "state",
                    [""],
                )[0]
                callback_result["error"] = query.get(
                    "error",
                    [""],
                )[0]
                callback_result["error_description"] = query.get(
                    "error_description",
                    [""],
                )[0]

                body = service._callback_html(
                    success=bool(callback_result["code"])
                ).encode("utf-8")

                self.send_response(200)
                self.send_header(
                    "Content-Type",
                    "text/html; charset=utf-8",
                )
                self.send_header(
                    "Content-Length",
                    str(len(body)),
                )
                self.end_headers()
                self.wfile.write(body)

                callback_received.set()

            def log_message(
                self,
                format_string: str,
                *args: Any,
            ) -> None:
                return

        try:
            server = ThreadingHTTPServer(
                (DISCORD_OAUTH_CALLBACK_HOST, DISCORD_OAUTH_CALLBACK_PORT),
                CallbackHandler,
            )
        except OSError as error:
            raise RuntimeError(
                "WoWidget could not start the Discord "
                "authorization callback on port 5001. "
                "Close any application using that port "
                "and try again."
            ) from error

        server.timeout = 1

        authorization_url = self.build_authorization_url(
            application_id=application_id,
            state=state,
            code_challenge=code_challenge,
        )

        webbrowser.open(
            authorization_url,
            new=2,
        )

        deadline = time.monotonic() + timeout_seconds

        try:
            while not callback_received.is_set() and time.monotonic() < deadline:
                server.handle_request()
        finally:
            server.server_close()

        if not callback_received.is_set():
            raise RuntimeError(
                "Discord authorization timed out. "
                "Press Authorize Discord and try again."
            )

        if callback_result.get("state") != state:
            raise RuntimeError(
                "Discord returned an invalid OAuth state. "
                "Authorization was cancelled for safety."
            )

        if callback_result.get("error"):
            description = (
                callback_result.get("error_description") or callback_result["error"]
            )

            raise RuntimeError(
                f"Discord authorization was not completed: {description}"
            )

        code = callback_result.get(
            "code",
            "",
        )

        if not code:
            raise RuntimeError("Discord returned no authorization code.")

        token_data = self._exchange_code(
            application_id=application_id,
            client_secret=client_secret,
            code=code,
            code_verifier=code_verifier,
        )

        user_data = self.get_current_user(token_data["access_token"])

        return self._build_authorization_result(
            token_data,
            user_data,
        )

    def build_authorization_url(
        self,
        *,
        application_id: str,
        state: str,
        code_challenge: str,
    ) -> str:
        query = urlencode(
            {
                "response_type": "code",
                "client_id": application_id,
                "redirect_uri": DISCORD_OAUTH_REDIRECT_URI,
                "scope": DISCORD_OAUTH_SCOPES,
                "state": state,
                "prompt": "consent",
                "code_challenge": code_challenge,
                "code_challenge_method": "S256",
            }
        )

        return f"{DISCORD_OAUTH_AUTHORIZE_URL}?{query}"

    def refresh_authorization(
        self,
        *,
        application_id: str,
        client_secret: str,
        refresh_token: str,
    ) -> dict[str, Any]:
        if not refresh_token:
            raise DiscordAuthorizationRequiredError(
                "Discord authorization is required. "
                "Open Settings and authorize your "
                "Discord account."
            )

        token_data = self._request_token(
            application_id=application_id,
            client_secret=client_secret,
            form_data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
        )

        user_data = self.get_current_user(token_data["access_token"])

        return self._build_authorization_result(
            token_data,
            user_data,
        )

    def ensure_access_token(
        self,
        *,
        storage: StorageManager,
        application_id: str,
        client_secret: str,
    ) -> str:
        access_token = storage.load_discord_access_token()
        refresh_token = storage.load_discord_refresh_token()
        expires_at = storage.load_discord_token_expiry()

        if access_token and not self._is_expiring_soon(expires_at):
            return access_token

        if not refresh_token:
            raise DiscordAuthorizationRequiredError(
                "Discord authorization is required. "
                "Open Settings and authorize your "
                "Discord account."
            )

        try:
            authorization = self.refresh_authorization(
                application_id=application_id,
                client_secret=client_secret,
                refresh_token=refresh_token,
            )

            storage.save_discord_oauth(authorization)

            return str(authorization["access_token"])

        except Exception as error:
            storage.clear_discord_oauth()

            raise DiscordAuthorizationRequiredError(
                "Discord authorization expired or was "
                "revoked. Open Settings and authorize "
                "your Discord account again."
            ) from error

    def get_current_user(
        self,
        access_token: str,
    ) -> dict[str, Any]:
        try:
            response = requests.get(
                f"{self.API_BASE_URL}/users/@me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "User-Agent": self.USER_AGENT,
                },
                timeout=(10, 30),
            )
            response.raise_for_status()

        except requests.RequestException as error:
            raise RuntimeError(
                f"Discord could not verify the authorized account: {error}"
            ) from error

        try:
            return response.json()
        except ValueError as error:
            raise RuntimeError(
                "Discord returned invalid authorized account information."
            ) from error

    def authorization_status(
        self,
        storage: StorageManager,
    ) -> dict[str, Any]:
        access_token = storage.load_discord_access_token()
        refresh_token = storage.load_discord_refresh_token()
        expires_at = storage.load_discord_token_expiry()
        user_id = storage.load_discord_authorized_user_id()
        display_name = storage.load_discord_authorized_display_name()

        authorized = bool(access_token and refresh_token and user_id)

        expired = bool(expires_at) and self._is_expired(expires_at)

        return {
            "authorized": authorized,
            "expired": expired,
            "refresh_available": bool(refresh_token),
            "expires_at": expires_at,
            "user_id": user_id,
            "display_name": display_name,
        }

    def _exchange_code(
        self,
        *,
        application_id: str,
        client_secret: str,
        code: str,
        code_verifier: str,
    ) -> dict[str, Any]:
        return self._request_token(
            application_id=application_id,
            client_secret=client_secret,
            form_data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": DISCORD_OAUTH_REDIRECT_URI,
                "code_verifier": code_verifier,
            },
        )

    def _request_token(
        self,
        *,
        application_id: str,
        client_secret: str,
        form_data: dict[str, str],
    ) -> dict[str, Any]:
        try:
            response = requests.post(
                DISCORD_OAUTH_TOKEN_URL,
                data=form_data,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": self.USER_AGENT,
                },
                auth=(
                    application_id,
                    client_secret,
                ),
                timeout=(10, 30),
            )
            response.raise_for_status()

        except requests.RequestException as error:
            response_text = ""

            if (
                getattr(
                    error,
                    "response",
                    None,
                )
                is not None
            ):
                response_text = error.response.text.strip()

            detail = f" Response: {response_text}" if response_text else ""

            raise RuntimeError(
                f"Discord rejected the OAuth token request.{detail}"
            ) from error

        try:
            token_data = response.json()
        except ValueError as error:
            raise RuntimeError(
                "Discord returned an invalid OAuth token response."
            ) from error

        access_token = str(
            token_data.get(
                "access_token",
                "",
            )
        ).strip()
        refresh_token = str(
            token_data.get(
                "refresh_token",
                "",
            )
        ).strip()

        if not access_token:
            raise RuntimeError("Discord returned no OAuth access token.")

        if not refresh_token:
            raise RuntimeError("Discord returned no OAuth refresh token.")

        return token_data

    @staticmethod
    def _build_authorization_result(
        token_data: dict[str, Any],
        user_data: dict[str, Any],
    ) -> dict[str, Any]:
        expires_in = max(
            0,
            int(
                token_data.get(
                    "expires_in",
                    0,
                )
                or 0
            ),
        )

        expires_at = (
            datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        ).isoformat(timespec="seconds")

        username = str(
            user_data.get(
                "username",
                "",
            )
        ).strip()
        global_name = str(
            user_data.get(
                "global_name",
                "",
            )
            or ""
        ).strip()

        return {
            "access_token": str(token_data["access_token"]),
            "refresh_token": str(token_data["refresh_token"]),
            "expires_at": expires_at,
            "scope": str(
                token_data.get(
                    "scope",
                    "",
                )
            ),
            "authorized_user_id": str(
                user_data.get(
                    "id",
                    "",
                )
            ),
            "authorized_username": username,
            "authorized_display_name": (global_name or username or "Discord User"),
        }

    @staticmethod
    def _create_code_challenge(
        code_verifier: str,
    ) -> str:
        digest = hashlib.sha256(code_verifier.encode("ascii")).digest()

        return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")

    @staticmethod
    def _is_expiring_soon(
        expires_at: str,
    ) -> bool:
        expiration = DiscordOAuthService._parse_timestamp(expires_at)

        if expiration is None:
            return True

        return expiration <= (datetime.now(timezone.utc) + timedelta(minutes=5))

    @staticmethod
    def _is_expired(
        expires_at: str,
    ) -> bool:
        expiration = DiscordOAuthService._parse_timestamp(expires_at)

        if expiration is None:
            return True

        return expiration <= datetime.now(timezone.utc)

    @staticmethod
    def _parse_timestamp(
        value: str,
    ) -> datetime | None:
        if not value:
            return None

        try:
            parsed = datetime.fromisoformat(value)
        except ValueError:
            return None

        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)

        return parsed.astimezone(timezone.utc)

    @staticmethod
    def _callback_html(
        *,
        success: bool,
    ) -> str:
        heading = (
            "Discord authorization complete"
            if success
            else "Discord authorization cancelled"
        )
        message = "You can close this browser tab and return " "to WoWidget."

        return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>WoWidget</title>
<style>
body {{
    background: #100d1b;
    color: #ffffff;
    font-family: Segoe UI, sans-serif;
    display: grid;
    min-height: 100vh;
    place-items: center;
    margin: 0;
}}
main {{
    background: #19142c;
    border: 1px solid #7353a8;
    border-radius: 16px;
    padding: 32px;
    max-width: 520px;
    text-align: center;
}}
p {{ color: #c9c1db; }}
</style>
</head>
<body>
<main>
<h1>{heading}</h1>
<p>{message}</p>
</main>
</body>
</html>"""
