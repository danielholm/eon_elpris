import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN, AREAS, UNITS


class EonConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(self, user_input=None):

        if user_input is not None:

            unique_id = f"{user_input['area']}_{user_input['unit']}"
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"E.ON {user_input['area']}",
                data=user_input
            )

        schema = vol.Schema({
            vol.Required("area", default="SE3"): vol.In(AREAS),
            vol.Required("unit", default="ore"): vol.In(UNITS)
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema
        )