from homeassistant.components.select import SelectEntity

from ..nhccoco.devices.generic_domestichotwaterunit import CocoGenericDomestichotwaterunit


class Nhc2GenericDomestichotwaterunitProgramEntity(SelectEntity):
    _attr_has_entity_name = True

    def __init__(self, device_instance: CocoGenericDomestichotwaterunit, hub, gateway):
        """Initialize a select entity."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid + '_program'
        self._attr_should_poll = False
        self._attr_device_info = self._device.device_info(self._hub)

        self._attr_options = self._device.possible_programs

    @property
    def name(self) -> str:
        return 'Program'

    @property
    def current_option(self) -> str:
        return self._device.program

    def on_change(self):
        self.schedule_update_ha_state()

    async def async_select_option(self, option: str) -> None:
        self._device.set_program(self._gateway, option)
        self.on_change()
