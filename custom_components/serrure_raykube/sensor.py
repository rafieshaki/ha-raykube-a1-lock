"""Capteur batterie pour la serrure RAYKUBE A1."""
from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    BATTERY_MAP,
    CONF_DEVICE_ID,
    DP_BATTERY,
    DP_LOCK_MOTOR_STATE,
    DOMAIN,
)
from .coordinator import RaykubeCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: RaykubeCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            RaykubeBattery(coordinator, entry),
            RaykubeStateSensor(coordinator, entry),
        ]
    )


class RaykubeBattery(CoordinatorEntity[RaykubeCoordinator], SensorEntity):
    """Niveau de batterie (DP 9)."""

    _attr_has_entity_name = True
    _attr_translation_key = "battery"
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: RaykubeCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._device_id = entry.data[CONF_DEVICE_ID]
        self._attr_unique_id = f"{self._device_id}_battery"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
        )

    @property
    def native_value(self) -> int | None:
        raw = self.coordinator.data.get(DP_BATTERY)
        if raw is None:
            return None
        return BATTERY_MAP.get(raw)


class RaykubeStateSensor(CoordinatorEntity[RaykubeCoordinator], SensorEntity):
    """Etat verrou en texte (DP 47) : Verrouille / Deverrouille."""

    _attr_has_entity_name = True
    _attr_translation_key = "lock_state"
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = ["locked", "unlocked"]

    def __init__(self, coordinator: RaykubeCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._device_id = entry.data[CONF_DEVICE_ID]
        self._attr_unique_id = f"{self._device_id}_state"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
        )

    @property
    def native_value(self) -> str | None:
        value = self.coordinator.data.get(DP_LOCK_MOTOR_STATE)
        if value is None:
            return None
        # DP 47 : true = deverrouille, false = verrouille
        return "unlocked" if value else "locked"
