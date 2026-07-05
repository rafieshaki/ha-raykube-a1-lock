"""Entite lock pour la serrure RAYKUBE A1."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.lock import LockEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_DEVICE_ID, DP_LOCK_MOTOR_STATE, DOMAIN
from .coordinator import RaykubeCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: RaykubeCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RaykubeLock(coordinator, entry)])


class RaykubeLock(CoordinatorEntity[RaykubeCoordinator], LockEntity):
    """Serrure RAYKUBE A1 via cloud Tuya."""

    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, coordinator: RaykubeCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._device_id = entry.data[CONF_DEVICE_ID]
        self._attr_unique_id = f"{self._device_id}_lock"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name="Serrure RAYKUBE A1",
            manufacturer="RAYKUBE",
            model="A1 Ultra",
        )

    @property
    def is_locked(self) -> bool | None:
        """DP 47 : true = deverrouille, false = verrouille."""
        value = self.coordinator.data.get(DP_LOCK_MOTOR_STATE)
        if value is None:
            return None
        return not bool(value)

    async def async_lock(self, **kwargs: Any) -> None:
        _LOGGER.debug("async_lock appele")
        try:
            await self.coordinator.api.async_lock()
            _LOGGER.debug("async_lock: commande envoyee avec succes")
        except Exception as err:
            _LOGGER.error("async_lock: echec: %s", err)
            raise
        await self.coordinator.async_refresh_after_action()

    async def async_unlock(self, **kwargs: Any) -> None:
        _LOGGER.debug("async_unlock appele")
        try:
            await self.coordinator.api.async_unlock()
            _LOGGER.debug("async_unlock: commande envoyee avec succes")
        except Exception as err:
            _LOGGER.error("async_unlock: echec: %s", err)
            raise
        await self.coordinator.async_refresh_after_action()
