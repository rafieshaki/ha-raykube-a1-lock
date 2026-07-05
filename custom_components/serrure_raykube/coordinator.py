"""Coordinator de polling pour la serrure RAYKUBE."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import TuyaLockApi, TuyaLockApiError
from .const import REFRESH_AFTER_ACTION, SCAN_INTERVAL_SECONDS

_LOGGER = logging.getLogger(__name__)


class RaykubeCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Recupere periodiquement l'etat de la serrure via le cloud Tuya."""

    def __init__(self, hass: HomeAssistant, api: TuyaLockApi) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="Serrure RAYKUBE",
            update_interval=timedelta(seconds=SCAN_INTERVAL_SECONDS),
        )
        self.api = api

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            return await self.api.async_get_status()
        except TuyaLockApiError as err:
            raise UpdateFailed(str(err)) from err

    async def async_refresh_after_action(self) -> None:
        """Rafraichit l'etat plusieurs fois apres une action pour rattraper le cloud."""
        for delay in REFRESH_AFTER_ACTION:
            await asyncio.sleep(delay)
            await self.async_request_refresh()
