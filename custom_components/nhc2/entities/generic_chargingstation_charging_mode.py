from homeassistant.components.select import SelectEntity

from ..nhccoco.devices.easee_chargingstation import CocoEaseeChargingstation
from .nhc_entity import NHCBaseEntity


class Nhc2GenericChargingstationChargingModeEntity(NHCBaseEntity, SelectEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoEaseeChargingstation, hub, gateway):
        """Initialize a select entity."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_charging_mode'

        self._attr_options = self._device.possible_charging_modes

    @property
    def name(self) -> str:
        return 'Charging Mode'

    @property
    def current_option(self) -> str:
        return self._device.charging_mode

    async def async_select_option(self, option: str) -> None:
        self._device.set_charging_mode(self._gateway, option)
        self.schedule_update_ha_state()
