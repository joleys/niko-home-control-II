"""Support for Niko Home Control II Thermostats."""
import logging

from homeassistant.components.climate import (
    ATTR_TEMPERATURE,
    ClimateEntity
)

from homeassistant.components.climate.const import (
    ATTR_FAN_MODE,
    ATTR_HVAC_MODE,
    ATTR_PRESET_MODE,
    ATTR_SWING_MODE,
    HVAC_MODE_COOL,
    HVAC_MODE_DRY,
    HVAC_MODE_FAN_ONLY,
    HVAC_MODE_HEAT,
    HVAC_MODE_HEAT_COOL,
    HVAC_MODE_OFF,
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_COOL,
    CURRENT_HVAC_IDLE,
    PRESET_SLEEP,
    PRESET_COMFORT,
    PRESET_ECO,
    PRESET_NONE,
    SUPPORT_PRESET_MODE,
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_TARGET_TEMPERATURE_RANGE
)

from nhc2_coco import CoCo
from nhc2_coco.coco_climate import CoCoThermostat
from nhc2_coco.coco_device_class import CoCoDeviceClass

from .const import DOMAIN, KEY_GATEWAY, BRAND, CLIMATE
from .helpers import nhc2_entity_processor

KEY_GATEWAY = KEY_GATEWAY
KEY_ENTITY = 'nhc2_thermostats'

_LOGGER = logging.getLogger(__name__)

HA_STATE_TO_NHC2 = {
    HVAC_MODE_COOL: "Cooling",
    HVAC_MODE_HEAT: "Heating",
    HVAC_MODE_OFF: "None"
}

NHC2_TO_HA_STATE = {
    "Cooling": HVAC_MODE_COOL,
    "Heating": HVAC_MODE_HEAT,
    "None": HVAC_MODE_OFF
}

NHC2_TO_HA_CURRENT_STATE = {
    "Cooling": CURRENT_HVAC_COOL,
    "Heating": CURRENT_HVAC_HEAT,
    "None": CURRENT_HVAC_IDLE
}

HA_PRESET_TO_NHC2 = {
    PRESET_NONE: "Off",
    PRESET_ECO: "Eco",
    PRESET_COMFORT: "Day",
    PRESET_SLEEP: "Night"
}

HVAC_MODES_LIST = list(HA_STATE_TO_NHC2)
FEATURE_LIST = SUPPORT_PRESET_MODE | SUPPORT_TARGET_TEMPERATURE

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Load NHC2 Thermostat basd on a Config Entry."""
    hass.data.setdefault(KEY_ENTITY, {})[config_entry.entry_id] = []
    gateway: CoCo = hass.data[KEY_GATEWAY][config_entry.entry_id]
    _LOGGER.debug('Platform is starting')
    gateway.get_devices(CoCoDeviceClass.THERMOSTATS,
                        nhc2_entity_processor(hass,
                                              config_entry,
                                              async_add_entities,
                                              KEY_ENTITY,
                                              lambda x: NHC2HassThermostat(x))
    )

class NHC2HassThermostat(ClimateEntity):
    """Representation of a Niko Home Control II thermostat."""

    def __init__(self, nhc2thermostat: CoCoThermostat):
        """Initialize a thermostat."""
        self._nhc2thermostat = nhc2thermostat
        self._current_temperature = nhc2thermostat.current_temperature
        nhc2thermostat.on_change = self._on_change
        _LOGGER.debug("Init new thermostat: %s", nhc2thermostat.name)
        _LOGGER.info(self.name + " temperature: " + str(self._current_temperature))

    def _on_change(self):
        self.schedule_update_ha_state()

    def update_properties(self):
        """Handle data changes for node values."""
        pass

    async def async_set_temperature(self, **kwargs):
        """Set new target temperatures."""
        temp = float(kwargs.get(ATTR_TEMPERATURE))
        self._nhc2thermostat.set_temperature(temp)
        self.schedule_update_ha_state()

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        pass

    async def async_set_preset_mode(self, preset_mode):
        """Set new target preset mode."""
        self._nhc2thermostat.set_preset_mode(preset_mode)
        self.schedule_update_ha_state()

    @property
    def state(self):
        """Return the current temperature."""
        return NHC2_TO_HA_STATE[self._nhc2thermostat.hvac_mode]

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._nhc2thermostat.current_temperature

    @property
    def target_temperature(self):
        """Return the target temperature."""
        return self._nhc2thermostat.target_temperature

    @property
    def hvac_action(self):
        """Return thermostat's current operation mode"""
        return NHC2_TO_HA_CURRENT_STATE[self._nhc2thermostat.hvac_mode]

    @property
    def hvac_mode(self):
        """Return thermostat's operation mode"""
        return NHC2_TO_HA_STATE[self._nhc2thermostat.hvac_mode]

    @property
    def hvac_modes(self):
        """Return the list of available hvac operation modes."""
        return HVAC_MODES_LIST

    @property
    def preset_mode(self):
        """Return the current preset mode, e.g., home, away, temp."""
        return self._nhc2thermostat.preset_mode

    @property
    def preset_modes(self):
        """Return the list off supported preset modes."""
        return list(self._nhc2thermostat.preset_modes)

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return self._nhc2thermostat.temperature_unit

    @property
    def target_temperature_low(self):
        """Return the minimum target temperature."""
        return self._nhc2thermostat.target_temperature_low

    @property
    def target_temperature_high(self):
        """Return the maximum target temperature."""
        return self._nhc2thermostat.target_temperature_high

    @property
    def target_temperature_step(self):
        """Return the target temperature step size."""
        return self._nhc2thermostat.target_temperature_step

    @property
    def temp_min(self):
        """Return the minimum temperature."""
        return self._nhc2thermostat.temp_min

    @property
    def temp_max(self):
        """Return the maximum temperature."""
        return self._nhc2thermostat.temp_max

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return FEATURE_LIST

    @property
    def name(self):
        """Return the thermostats name."""
        return self._nhc2thermostat.name

    @property
    def unique_id(self):
        """Return the thermostats UUID."""
        return self._nhc2thermostat.uuid

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {
                (DOMAIN, self.unique_id)
            },
            "name": self.name,
            "manufacturer": BRAND,
            "model": CLIMATE,
            "via_hub": (DOMAIN, self._nhc2thermostat.profile_creation_id),
        }
