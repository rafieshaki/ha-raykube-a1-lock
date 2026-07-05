"""Config flow (fenetre UI) pour la serrure RAYKUBE A1."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import TuyaLockApi, TuyaLockApiError, TuyaLockAuthError
from .const import (
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
    CONF_DEVICE_ID,
    CONF_REGION,
    DEFAULT_REGION,
    DOMAIN,
    TUYA_ENDPOINTS,
)

STEP_USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_CLIENT_ID): str,
        vol.Required(CONF_CLIENT_SECRET): str,
        vol.Required(CONF_DEVICE_ID): str,
        vol.Required(CONF_REGION, default=DEFAULT_REGION): vol.In(
            list(TUYA_ENDPOINTS.keys())
        ),
    }
)


class RaykubeConfigFlow(ConfigFlow, domain=DOMAIN):
    """Gere la configuration via l'interface."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_DEVICE_ID])
            self._abort_if_unique_id_configured()

            endpoint = TUYA_ENDPOINTS[user_input[CONF_REGION]]
            session = async_get_clientsession(self.hass)
            api = TuyaLockApi(
                session,
                endpoint,
                user_input[CONF_CLIENT_ID],
                user_input[CONF_CLIENT_SECRET],
                user_input[CONF_DEVICE_ID],
            )
            try:
                await api.async_validate()
            except TuyaLockAuthError:
                errors["base"] = "invalid_auth"
            except TuyaLockApiError:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title="Serrure RAYKUBE A1",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_SCHEMA, errors=errors
        )
