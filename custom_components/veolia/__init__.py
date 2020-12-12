"""
Custom integration to integrate Veolia with Home Assistant.

For more details about this integration, please refer to
https://github.com/tetienne/veolia-custom-component
"""
import asyncio
from datetime import datetime, timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from pyolia.client import VeoliaClient

from .const import (
    API,
    CONF_PASSWORD,
    CONF_USERNAME,
    COORDINATOR,
    DOMAIN,
    PLATFORMS,
)

SCAN_INTERVAL = timedelta(days=1)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    username = entry.data.get(CONF_USERNAME)
    password = entry.data.get(CONF_PASSWORD)

    hass.data[DOMAIN][API] = VeoliaClient(username, password)

    async def _get_consumption():
        """Return the water consumption for each day of the current month."""
        now = datetime.now()
        if now.day < 4:
            now = now - timedelta(days=3)
        return await hass.data[DOMAIN][API].get_consumption(now.month, now.year)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="somfy device update",
        update_method=_get_consumption,
        update_interval=SCAN_INTERVAL,
    )

    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][COORDINATOR] = coordinator

    for platform in PLATFORMS:
        hass.async_add_job(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True


async def async_unload_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Unload a config entry."""
    hass.data[DOMAIN].pop(API, None)
    await asyncio.gather(
        *[
            hass.config_entries.async_forward_entry_unload(entry, component)
            for component in PLATFORMS
        ]
    )
    return True
