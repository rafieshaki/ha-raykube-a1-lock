"""Client API cloud Tuya pour la serrure RAYKUBE A1.

Methode de lock/unlock reprise de xtend_tuya (azerty9971), validee par l'usage :
  1. POST /v1.0/devices/{id}/door-lock/password-ticket  -> ticket_id
  2. POST /v1.0/smart-lock/devices/{id}/password-free/door-operate
         body {"ticket_id": ..., "open": "true"|"false"}
     open=false -> verrouille, open=true -> deverrouille

Signature HMAC-SHA256 standard Tuya.
Communique uniquement avec les endpoints officiels Tuya.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import time
import logging
from typing import Any

import aiohttp

_LOGGER = logging.getLogger(__name__)

TOKEN_PATH = "/v1.0/token?grant_type=1"


class TuyaLockApiError(Exception):
    """Erreur retournee par l'API Tuya."""


class TuyaLockAuthError(TuyaLockApiError):
    """Erreur d'authentification (credentials invalides)."""


class TuyaLockApi:
    """Client minimal Tuya Cloud dedie a une serrure."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        endpoint: str,
        client_id: str,
        client_secret: str,
        device_id: str,
    ) -> None:
        self._session = session
        self._endpoint = endpoint.rstrip("/")
        self._client_id = client_id
        self._client_secret = client_secret
        self._device_id = device_id
        self._token: str | None = None
        self._token_expire: float = 0.0

    # ---------- Signature ----------

    def _sign(self, method: str, path: str, body: str, token: str = "") -> tuple[str, str]:
        t = str(int(time.time() * 1000))
        content_sha256 = hashlib.sha256(body.encode("utf-8")).hexdigest()
        string_to_sign = f"{method}\n{content_sha256}\n\n{path}"
        sign_str = self._client_id + token + t + string_to_sign
        signature = (
            hmac.new(
                self._client_secret.encode("utf-8"),
                sign_str.encode("utf-8"),
                hashlib.sha256,
            )
            .hexdigest()
            .upper()
        )
        return signature, t

    async def _request(
        self,
        method: str,
        path: str,
        body_dict: dict[str, Any] | None = None,
        with_token: bool = True,
    ) -> dict[str, Any]:
        if with_token:
            await self._ensure_token()
            token = self._token or ""
        else:
            token = ""

        body = json.dumps(body_dict) if body_dict is not None else ""
        signature, t = self._sign(method, path, body, token)

        headers = {
            "client_id": self._client_id,
            "sign": signature,
            "t": t,
            "sign_method": "HMAC-SHA256",
            "Content-Type": "application/json",
        }
        if with_token:
            headers["access_token"] = token

        url = self._endpoint + path
        try:
            async with self._session.request(
                method, url, headers=headers, data=body or None, timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                data = await resp.json()
        except aiohttp.ClientError as err:
            raise TuyaLockApiError(f"Erreur reseau: {err}") from err

        if not data.get("success", False):
            code = data.get("code")
            msg = data.get("msg", "erreur inconnue")
            # 1010/1004 = token/sign invalide -> souvent credentials
            if code in (1004, 1010, 1106, 1114):
                raise TuyaLockAuthError(f"Auth Tuya echouee (code {code}): {msg}")
            raise TuyaLockApiError(f"Tuya API (code {code}): {msg}")

        return data

    # ---------- Token ----------

    async def _ensure_token(self) -> None:
        if self._token and time.time() < self._token_expire - 60:
            return
        data = await self._request("GET", TOKEN_PATH, with_token=False)
        result = data.get("result", {})
        self._token = result.get("access_token")
        expire = result.get("expire_time", 7200)
        self._token_expire = time.time() + float(expire)
        if not self._token:
            raise TuyaLockAuthError("Token Tuya absent de la reponse")

    async def async_validate(self) -> None:
        """Valide les credentials en recuperant un token puis l'etat."""
        await self._ensure_token()
        await self.async_get_status()

    # ---------- Etat ----------

    async def async_get_status(self) -> dict[str, Any]:
        """Retourne les DP sous forme {code: value}."""
        path = f"/v1.0/devices/{self._device_id}/status"
        data = await self._request("GET", path)
        result = data.get("result", [])
        return {item["code"]: item["value"] for item in result if "code" in item}

    # ---------- Ticket ----------

    async def _get_ticket(self) -> str:
        path = f"/v1.0/devices/{self._device_id}/door-lock/password-ticket"
        data = await self._request("POST", path, body_dict={})
        _LOGGER.debug("Reponse ticket: %s", data)
        ticket_id = data.get("result", {}).get("ticket_id")
        if not ticket_id:
            raise TuyaLockApiError("ticket_id absent de la reponse")
        return ticket_id

    # ---------- Lock / Unlock ----------

    async def _door_operate(self, open_value: str) -> None:
        ticket_id = await self._get_ticket()
        path = f"/v1.0/smart-lock/devices/{self._device_id}/password-free/door-operate"
        data = await self._request(
            "POST", path, body_dict={"ticket_id": ticket_id, "open": open_value}
        )
        _LOGGER.debug("Reponse door-operate (open=%s): %s", open_value, data)

    async def async_lock(self) -> None:
        """Verrouille (open=false)."""
        await self._door_operate("false")

    async def async_unlock(self) -> None:
        """Deverrouille (open=true)."""
        await self._door_operate("true")
