from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import EntityCategory

from ..nhccoco.devices.audiocontrol_action import CocoAudiocontrolAction
from .nhc_entity import NHCBaseEntity


class Nhc2AudiocontrolActionSpeakerEntity(NHCBaseEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoAudiocontrolAction, hub, gateway):
        """Initialize a sensor."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_speaker'

        self._attr_native_value = self._device.speaker
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def name(self) -> str:
        return 'Speaker'

    @property
    def state(self) -> str:
        return self._device.speaker
