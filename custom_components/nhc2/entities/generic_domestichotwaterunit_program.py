from homeassistant.components.select import SelectEntity

from ..nhccoco.devices.generic_domestichotwaterunit import CocoGenericDomestichotwaterunit
from .nhc_entity import NHCBaseEntity


class Nhc2GenericDomestichotwaterunitProgramEntity(NHCBaseEntity, SelectEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericDomestichotwaterunit, hub, gateway):
        """Initialize a select entity."""
        super().__init__(device_instance, hub, gateway)

        self._attr_unique_id = device_instance.uuid + '_program'

        self._attr_options = self._device.possible_programs

    @property
    def name(self) -> str:
        return 'Program'

    @property
    def current_option(self) -> str:
        return self._device.program

    async def async_select_option(self, option: str) -> None:
        self._device.set_program(self._gateway, option)
        self.schedule_update_ha_state()
