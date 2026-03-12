from .const import DOMAIN

async def async_setup(hass, config):
    """Set up the E.ON integration."""
    return True


async def async_setup_entry(hass, entry):
    """Set up E.ON from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
