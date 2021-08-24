"""Sensor platform for Veolia."""
import datetime

from .const import COORDINATOR, DAILY, DOMAIN, HOURLY
from .entity import VeoliaEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up sensor platform."""
    coordinator = hass.data[DOMAIN][COORDINATOR]
    sensors = [
        VeoliaDailyUsageSensor(coordinator, entry),
        VeoliaMonthlyUsageSensor(coordinator, entry),
    ]
    # HOURLY array is empty when hourly report is not enabled
    if coordinator.data[HOURLY]:
        sensors.append(VeoliaHourlyUsageSensor(coordinator, entry)),

    async_add_devices(sensors)


class VeoliaHourlyUsageSensor(VeoliaEntity):
    """Monitors the hourly water usage."""

    _attr_name = "veolia_hourly_consumption"

    @property
    def state(self):
        """Return the state of the sensor."""
        hour = datetime.datetime.now().hour
        return self.coordinator.data[HOURLY][hour - 1]


class VeoliaDailyUsageSensor(VeoliaEntity):
    """Monitors the daily water usage."""

    _attr_name = "veolia_daily_consumption"

    @property
    def state(self):
        """Return the state of the sensor."""
        state = self.coordinator.data[DAILY][-1]

        if state > 0:
            return state

        return None


class VeoliaMonthlyUsageSensor(VeoliaEntity):
    """Monitors the monthly water usage."""

    _attr_name = "veolia_monthly_consumption"

    @property
    def state(self):
        """Return the state of the sensor."""
        state = sum(self.coordinator.data[DAILY])
        if state > 0:
            return state

        return None
