from .device import CoCoDevice

import logging

_LOGGER = logging.getLogger(__name__)


class CocoNasoSmartplug(CoCoDevice):
    @property
    def electrical_power(self) -> float:
        return float(self.extract_property_value('ElectricalPower'))

    @property
    def report_instant_usage(self) -> bool:
        return self.extract_property_value('ReportInstantUsage') == 'True'

    @property
    def feedback_enabled(self) -> bool:
        return self.extract_parameter_value('FeedbackEnabled') == 'True'

    @property
    def measuring_only(self) -> bool:
        return self.extract_parameter_value('MeasuringOnly') == 'True'

    def on_change(self, topic: str, payload: dict):
        _LOGGER.debug(f'{self.name} changed. Topic: {topic} | Data: {payload}')
        if 'Properties' in payload:
            self.merge_properties(payload['Properties'])

        if self._after_change_callbacks:
            for callback in self._after_change_callbacks:
                callback()
