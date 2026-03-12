import logging
from datetime import timedelta

from homeassistant.helpers.aiohttp_client import async_get_clientsession

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.helpers.device_registry import DeviceInfo

from .const import API_URL, DOMAIN, UNITS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    area = entry.data["area"]
    unit = entry.data["unit"]

    async def async_update_data():
        try:
            session = async_get_clientsession(hass)

            async with session.get(API_URL, timeout=10) as resp:
                data = await resp.json(content_type=None)

            for area_data in data["MonthlyAveragePrice"]:
                if area_data["PriceArea"] == area:
                    return {"price": area_data["Price"], "raw": data}

            raise ValueError("Price area not found")

        except Exception as err:
            raise UpdateFailed(err)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"eon_price_{area}",
        update_method=async_update_data,
        update_interval=timedelta(hours=1),
    )

    await coordinator.async_config_entry_first_refresh()

    async_add_entities([EonPriceSensor(coordinator, area, unit)])



class EonPriceSensor(CoordinatorEntity, SensorEntity):
    _attr_should_poll = False

    def __init__(self, coordinator, area, unit):
        super().__init__(coordinator)

        self._area = area
        self._unit = unit

        self._attr_has_entity_name = True

        self._attr_name = "Monthly Price"
        self._attr_unique_id = f"eon_price_{area}_{unit}"
        self._attr_native_unit_of_measurement = UNITS[unit]
        self._attr_suggested_display_precision = 3
        self._attr_state_class = "measurement"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, area)},
            name=f"E.ON Electricity Price {area}",
            manufacturer="E.ON",
            model="Monthly Average Electricity Price",
        )

    @property
    def native_value(self):
        price = self.coordinator.data["price"]

        if self._unit == "sek":
            return round(price / 100, 4)

        return price

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data["raw"]

        return {
            "month": data["Month"],
            "valid_from": data["FromDate"],
            "valid_to": data["ToDate"],
            "updated": data["Timestamp"],
        }