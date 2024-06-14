from ..const import PROPERTY_STATUS, PROPERTY_STATUS_VALUE_ON, PROPERTY_STATUS_VALUE_OFF, \
    PROPERTY_PLAYBACK, PROPERTY_PLAYBACK_VALUE_BUFFERING, PROPERTY_PLAYBACK_VALUE_PAUSED, \
    PROPERTY_PLAYBACK_VALUE_PLAYING, PROPERTY_VOLUME, PROPERTY_MUTED, PROPERTY_MUTED_VALUE_TRUE, \
    PROPERTY_MUTED_VALUE_FALSE, PROPERTY_TITLE, PROPERTY_VOLUME_ALIGNED, PROPERTY_VOLUME_ALIGNED_VALUE_TRUE, \
    PROPERTY_TITLE_ALIGNED, PROPERTY_TITLE_ALIGNED_VALUE_TRUE, PROPERTY_CONNECTED, PROPERTY_CONNECTED_VALUE_TRUE, \
    PARAMETER_SPEAKER

from ..helpers import to_int_or_none

from .device import CoCoDevice


class CocoAudiocontrolAction(CoCoDevice):
    @property
    def status(self) -> str:
        return self.extract_property_value(PROPERTY_STATUS)

    @property
    def is_status_on(self) -> bool:
        return self.status == PROPERTY_STATUS_VALUE_ON

    @property
    def is_status_off(self) -> bool:
        return self.status == PROPERTY_STATUS_VALUE_OFF

    @property
    def playback(self) -> str:
        return self.extract_property_value(PROPERTY_PLAYBACK)

    @property
    def is_playback_playing(self) -> bool:
        return self.playback == PROPERTY_PLAYBACK_VALUE_PLAYING

    @property
    def is_playback_paused(self) -> bool:
        return self.playback == PROPERTY_PLAYBACK_VALUE_PAUSED

    @property
    def is_playback_buffering(self) -> bool:
        return self.playback == PROPERTY_PLAYBACK_VALUE_BUFFERING

    @property
    def volume(self) -> int:
        return to_int_or_none(self.extract_property_value(PROPERTY_VOLUME))

    @property
    def muted(self) -> str:
        return self.extract_property_value(PROPERTY_MUTED)

    @property
    def is_muted(self) -> bool:
        return self.muted == PROPERTY_MUTED_VALUE_TRUE

    @property
    def title(self) -> str:
        return self.extract_property_value(PROPERTY_TITLE)

    @property
    def volume_aligned(self) -> str:
        return self.extract_property_value(PROPERTY_VOLUME_ALIGNED)

    @property
    def is_volume_aligned(self) -> bool:
        return self.volume_aligned == PROPERTY_VOLUME_ALIGNED_VALUE_TRUE

    @property
    def title_aligned(self) -> str:
        return self.extract_property_value(PROPERTY_TITLE_ALIGNED)

    @property
    def is_title_aligned(self) -> bool:
        return self.title_aligned == PROPERTY_TITLE_ALIGNED_VALUE_TRUE

    @property
    def connected(self) -> str:
        return self.extract_property_value(PROPERTY_CONNECTED)

    @property
    def is_connected(self) -> bool:
        return self.connected == PROPERTY_CONNECTED_VALUE_TRUE

    @property
    def speaker(self) -> str:
        return self.extract_parameter_value(PARAMETER_SPEAKER)

    def turn_on(self, gateway):
        gateway.add_device_control(self.uuid, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_ON)

    def turn_off(self, gateway):
        gateway.add_device_control(self.uuid, PROPERTY_STATUS, PROPERTY_STATUS_VALUE_OFF)

    def set_volume(self, gateway, volume: int):
        gateway.add_device_control(self.uuid, PROPERTY_VOLUME, str(volume))

    def mute_on(self, gateway):
        gateway.add_device_control(self.uuid, PROPERTY_MUTED, PROPERTY_MUTED_VALUE_TRUE)

    def mute_off(self, gateway):
        gateway.add_device_control(self.uuid, PROPERTY_MUTED, PROPERTY_MUTED_VALUE_FALSE)

    def play(self, gateway):
        gateway.add_device_control(self.uuid, PROPERTY_PLAYBACK, PROPERTY_PLAYBACK_VALUE_PLAYING)

    def pause(self, gateway):
        gateway.add_device_control(self.uuid, PROPERTY_PLAYBACK, PROPERTY_PLAYBACK_VALUE_PAUSED)
