"""Sensor platform for Veolia."""
from homeassistant.const import VOLUME_LITERS

from .const import COORDINATOR, DOMAIN
from .entity import VeoliaEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][COORDINATOR]
    async_add_devices([VeoliaDailyUsageSensor(coordinator, entry)])


class VeoliaDailyUsageSensor(VeoliaEntity):
    """Monitors the daily water usage."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return "veolia_daily_consumption"

    @property
    def state(self):
        """Return the state of the sensor."""
        return list(self.coordinator.data.values())[-1]

    @property
    def icon(self) -> str:
        """Return the daily usage icon."""
        return "mdi:water"

    @property
    def unit_of_measurement(self) -> str:
        """Return liter as the unit measurement for water."""
        return VOLUME_LITERS
