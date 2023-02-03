"""Support for NHC2 numbers."""
import logging

from homeassistant.const import CONF_USERNAME

from .nhccoco.coco import CoCo

from .entities.generic_domestichotwaterunit_domestic_hot_water_temperature import \
    Nhc2GenericDomestichotwaterunitDomesticHotWaterTemperatureEntity
from .nhccoco.devices.generic_domestichotwaterunit import CocoGenericDomestichotwaterunit

from .const import DOMAIN, KEY_GATEWAY

KEY_ENTITY = 'nhc2_numbers'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring numbers')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = (DOMAIN, config_entry.data[CONF_USERNAME])

    device_instances = gateway.get_device_instances(CocoGenericDomestichotwaterunit)
    _LOGGER.info('→ Found %s Generic Warm Water Implementation', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(
                Nhc2GenericDomestichotwaterunitDomesticHotWaterTemperatureEntity(device_instance, hub, gateway)
            )

        async_add_entities(entities)
