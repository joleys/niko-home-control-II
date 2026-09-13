"""Support for NHC2 media players."""
import logging

from .nhccoco.coco import CoCo

from .entities.audiocontrol_action_mediaplayer import Nhc2AudiocontrolActionMediaPlayerEntity
from .nhccoco.devices.audiocontrol_action import CocoAudiocontrolAction

from .const import KEY_GATEWAY

from .hub import async_get_hub

KEY_ENTITY = 'nhc2_media_players'

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    _LOGGER.info('Configuring media players')

    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []

    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    hub = async_get_hub(hass, config_entry)

    device_instances = gateway.get_device_instances(CocoAudiocontrolAction)
    _LOGGER.info('→ Found %s NHC Audio Control Actions', len(device_instances))
    if len(device_instances) > 0:
        entities = []
        for device_instance in device_instances:
            entities.append(Nhc2AudiocontrolActionMediaPlayerEntity(device_instance, hub, gateway))

        async_add_entities(entities)
