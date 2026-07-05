"""Integration Serrure RAYKUBE A1 (cloud Tuya)."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import TuyaLockApi
from .const import (
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
    CONF_DEVICE_ID,
    CONF_REGION,
    DOMAIN,
    TUYA_ENDPOINTS,
)
from .coordinator import RaykubeCoordinator

PLATFORMS = [Platform.LOCK, Platform.SENSOR, Platform.EVENT]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configure l'integration depuis une entree UI."""
    session = async_get_clientsession(hass)
    endpoint = TUYA_ENDPOINTS[entry.data[CONF_REGION]]
    api = TuyaLockApi(
        session,
        endpoint,
        entry.data[CONF_CLIENT_ID],
        entry.data[CONF_CLIENT_SECRET],
        entry.data[CONF_DEVICE_ID],
    )

    coordinator = RaykubeCoordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Decharge l'integration."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
