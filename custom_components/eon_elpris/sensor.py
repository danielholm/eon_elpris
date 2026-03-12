import aiohttp
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    CoordinatorEntity
)

from .const import DOMAIN, API_URL, UNITS


async def async_setup_entry(hass, entry, async_add_entities):

    area = entry.data["area"]
    unit = entry.data["unit"]

    async def async_update_data():

        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL) as resp:
                data = await resp.json()

        for area_data in data["MonthlyAveragePrice"]:
            if area_data["PriceArea"] == area:
                return area_data["Price"], data

    coordinator = DataUpdateCoordinator(
        hass,
        logger=hass.logger,
        name="eon_price",
        update_method=async_update_data,
        update_interval=timedelta(hours=1),
    )

    await coordinator.async_config_entry_first_refresh()

    async_add_entities([EonPriceSensor(coordinator, area, unit)])


class EonPriceSensor(CoordinatorEntity, SensorEntity):

    def __init__(self, coordinator, area, unit):
        super().__init__(coordinator)

        self._area = area
        self._unit = unit

        self._attr_name = f"E.ON Monthly Price {area}"
        self._attr_unique_id = f"eon_price_{area}"

        self._attr_native_unit_of_measurement = UNITS[unit]
        self._attr_suggested_display_precision = 3

    @property
    def native_value(self):

        price, _ = self.coordinator.data

        if self._unit == "sek":
            return round(price / 100, 4)

        return price

    @property
    def extra_state_attributes(self):

        _, data = self.coordinator.data

        return {
            "month": data["Month"],
            "valid_from": data["FromDate"],
            "valid_to": data["ToDate"],
            "updated": data["Timestamp"]
        }