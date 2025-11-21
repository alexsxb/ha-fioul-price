from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CURRENCY_EURO
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    """Set up Fioul sensor from config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([FioulSensor(coordinator)], True)


class FioulSensor(CoordinatorEntity, SensorEntity):
    """Representation of the Fioul price sensor."""

    _attr_icon = "mdi:oil"
    _attr_name = "Fioul Price"
    _attr_native_unit_of_measurement = CURRENCY_EURO
    _attr_unique_id = "fioul_price"

    def __init__(self, coordinator):
        super().__init__(coordinator)

    @property
    def native_value(self):
        data = self.coordinator.data or {}
        return data.get("price")

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data or {}
        return {
            "date": data.get("date"),
        }
