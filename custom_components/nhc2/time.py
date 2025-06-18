"""Support for NHC2 time."""
import logging

from homeassistant.const import CONF_USERNAME

from .nhccoco.coco import CoCo

from .entities.generic_chargingstation_next_charging_time import Nhc2GenericChargingstationNextChargingTimeEntity
from .entities.generic_chargingstation_target_time import Nhc2GenericChargingstationTargetTimeEntity
from .nhccoco.devices.generic_chargingstation import CocoGenericChargingstation

from .const import DOMAIN, KEY_GATEWAY

KEY_ENTITY = 'nhc2_times'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring time')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = (DOMAIN, config_entry.data[CONF_USERNAME])

    device_instances = gateway.get_device_instances(CocoGenericChargingstation)
    _LOGGER.info('→ Found %s Generic Chargingstation Implementation', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            if device_instance.supports_target_time:
                entities.append(Nhc2GenericChargingstationTargetTimeEntity(device_instance, hub, gateway))
            if device_instance.supports_next_charging_time:
                entities.append(Nhc2GenericChargingstationNextChargingTimeEntity(device_instance, hub, gateway))

        async_add_entities(entities)
