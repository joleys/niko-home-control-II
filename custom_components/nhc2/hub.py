"""Handle on the Connected Controller every NHC2 device hangs off of.

`device_registry.async_get_or_create` deprecates `via_device`, which takes the
controller's identifiers, in favour of `via_device_id`, which takes its device
registry id. That id can only be looked up with `hass` in hand, so platforms
resolve it here during setup and hand it to their entities together with the
identifiers the entities already had.
"""
from typing import NamedTuple

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_USERNAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry

from .const import BRAND, DOMAIN


class Nhc2Hub(NamedTuple):
    """The controller's identifier, plus its device registry id."""

    identifier: str
    device_id: str


@callback
def async_controller_identifiers(config_entry: ConfigEntry) -> set[tuple[str, str]]:
    """Return the device registry identifiers of the controller."""
    return {(DOMAIN, config_entry.data[CONF_USERNAME])}


@callback
def async_get_hub(hass: HomeAssistant, config_entry: ConfigEntry) -> Nhc2Hub:
    """Return the hub handle, registering the controller device if needed.

    Registering here is idempotent and only fills in fields the controller
    device would get anyway: `systeminfo.published` calls
    `async_get_or_create` with the same identifiers to add the versions.
    """
    controller = device_registry.async_get(hass).async_get_or_create(
        config_entry_id=config_entry.entry_id,
        identifiers=async_controller_identifiers(config_entry),
        manufacturer=BRAND,
        name='Home Control II',
        model='Connected controller',
    )

    return Nhc2Hub(config_entry.data[CONF_USERNAME], controller.id)
