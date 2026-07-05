"""Entite event pour les alertes de la serrure (batterie faible, coupure)."""
from __future__ import annotations

from homeassistant.components.event import EventEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_DEVICE_ID, DP_ALARM, DOMAIN
from .coordinator import RaykubeCoordinator

EVENT_TYPES = ["low_battery", "power_off"]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: RaykubeCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([RaykubeAlarm(coordinator, entry)])


class RaykubeAlarm(CoordinatorEntity[RaykubeCoordinator], EventEntity):
    """Alerte serrure (DP 21 : low_battery / power_off)."""

    _attr_has_entity_name = True
    _attr_translation_key = "alert"
    _attr_event_types = EVENT_TYPES

    def __init__(self, coordinator: RaykubeCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._device_id = entry.data[CONF_DEVICE_ID]
        self._attr_unique_id = f"{self._device_id}_alert"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
        )
        self._last_value: str | None = None

    @callback
    def _handle_coordinator_update(self) -> None:
        value = self.coordinator.data.get(DP_ALARM)
        if value and value in EVENT_TYPES and value != self._last_value:
            self._last_value = value
            self._trigger_event(value)
        self.async_write_ha_state()
