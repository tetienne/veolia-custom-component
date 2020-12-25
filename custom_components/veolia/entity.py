"""VeoliaEntity class"""
from homeassistant.const import VOLUME_LITERS
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, LAST_REPORT_TIMESTAMP, NAME


class VeoliaEntity(CoordinatorEntity):
    def __init__(self, coordinator, config_entry):
        super().__init__(coordinator)
        self.config_entry = config_entry

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}_{self.name}"

    @property
    def device_info(self):
        return {
            "identifiers": {(self.config_entry.entry_id, DOMAIN)},
            "manufacturer": NAME,
            "name": NAME,
        }

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            "last_report": self.coordinator.data[LAST_REPORT_TIMESTAMP],
        }

    @property
    def icon(self) -> str:
        """Return the usage icon."""
        return "mdi:water"

    @property
    def unit_of_measurement(self) -> str:
        """Return liter as the unit measurement for water."""
        return VOLUME_LITERS
