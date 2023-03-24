from ..const import DEVICE_DESCRIPTOR_PROPERTIES, PROPERTY_ELECTRICAL_POWER_TO_GRID, \
    PROPERTY_ELECTRICAL_POWER_FROM_GRID, PROPERTY_ELECTRICAL_POWER_PRODUCTION, \
    PROPERTY_ELECTRICAL_POWER_SELF_CONSUMPTION, PROPERTY_REPORT_INSTANT_USAGE, PROPERTY_REPORT_INSTANT_USAGE_VALUE_TRUE, \
    PROPERTY_ELECTRICAL_POWER_PRODUCTION_THRESHOLD_EXCEEDED, \
    PROPERTY_ELECTRICAL_POWER_PRODUCTION_THRESHOLD_EXCEEDED_VALUE_TRUE, PROPERTY_ELECTRICAL_POWER_CONSUMPTION
from ..helpers import to_float_or_none
from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoGenericEnergyhome(CoCoDevice):
    @property
    def electrical_power_to_grid(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_ELECTRICAL_POWER_TO_GRID))

    @property
    def supports_electrical_power_to_grid(self) -> bool:
        return self.has_property(PROPERTY_ELECTRICAL_POWER_TO_GRID)

    @property
    def electrical_power_from_grid(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_ELECTRICAL_POWER_FROM_GRID))

    @property
    def supports_electrical_power_from_grid(self) -> bool:
        return self.has_property(PROPERTY_ELECTRICAL_POWER_FROM_GRID)

    @property
    def electrical_power_production(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_ELECTRICAL_POWER_PRODUCTION))

    @property
    def supports_electrical_power_production(self) -> bool:
        return self.has_property(PROPERTY_ELECTRICAL_POWER_PRODUCTION)

    @property
    def electrical_power_self_consumption(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_ELECTRICAL_POWER_SELF_CONSUMPTION))

    @property
    def supports_electrical_power_self_consumption(self) -> bool:
        return self.has_property(PROPERTY_ELECTRICAL_POWER_SELF_CONSUMPTION)

    @property
    def electrical_power_consumption(self) -> float:
        return to_float_or_none(self.extract_property_value(PROPERTY_ELECTRICAL_POWER_CONSUMPTION))

    @property
    def supports_electrical_power_consumption(self) -> bool:
        return self.has_property(PROPERTY_ELECTRICAL_POWER_CONSUMPTION)

    @property
    def is_report_instant_usage(self) -> bool:
        return self.extract_property_value(PROPERTY_REPORT_INSTANT_USAGE) == PROPERTY_REPORT_INSTANT_USAGE_VALUE_TRUE

    @property
    def is_electrical_power_production_threshold_exceeded(self) -> bool:
        return self.extract_property_value(PROPERTY_ELECTRICAL_POWER_PRODUCTION_THRESHOLD_EXCEEDED) == \
            PROPERTY_ELECTRICAL_POWER_PRODUCTION_THRESHOLD_EXCEEDED_VALUE_TRUE

    @property
    def is_online(self) -> bool:
        # For some reason NHC return `False` for these devices. Sor overruling this.
        return True

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if DEVICE_DESCRIPTOR_PROPERTIES in payload:
            self.merge_properties(payload[DEVICE_DESCRIPTOR_PROPERTIES])

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()

    def enable_report_instant_usage(self, gateway):
        gateway.add_device_control(
            self.uuid,
            PROPERTY_REPORT_INSTANT_USAGE,
            PROPERTY_REPORT_INSTANT_USAGE_VALUE_TRUE
        )
