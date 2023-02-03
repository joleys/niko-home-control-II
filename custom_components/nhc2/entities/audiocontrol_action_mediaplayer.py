from homeassistant.components.media_player import MediaPlayerEntity, MediaPlayerEntityFeature, MediaPlayerState

from ..const import DOMAIN, BRAND

from ..nhccoco.devices.audiocontrol_action import CocoAudiocontrolAction


class Nhc2AudiocontrolActionMediaPlayerEntity(MediaPlayerEntity):
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, device_instance: CocoAudiocontrolAction, hub, gateway):
        """Initialize a button."""
        self._device = device_instance
        self._hub = hub
        self._gateway = gateway

        self._device.after_change_callbacks.append(self.on_change)

        self._attr_available = self._device.is_online
        self._attr_unique_id = device_instance.uuid
        self._attr_should_poll = False

        self._attr_supported_features = MediaPlayerEntityFeature.PAUSE | MediaPlayerEntityFeature.PLAY | \
                                        MediaPlayerEntityFeature.TURN_OFF | MediaPlayerEntityFeature.TURN_ON | \
                                        MediaPlayerEntityFeature.VOLUME_MUTE | MediaPlayerEntityFeature.VOLUME_SET
        self._attr_is_volume_muted = self._device.is_muted
        self._attr_media_title = self._device.title
        self._attr_volume_level = self._device.volume / 100

    @property
    def device_info(self):
        """Return the device info."""
        return {
            'identifiers': {
                (DOMAIN, self._device.uuid)
            },
            'name': self._device.name,
            'manufacturer': BRAND,
            'model': str.title(f'{self._device.model} ({self._device.type})'),
            'via_device': self._hub
        }

    @property
    def state(self) -> str:
        if self._device.is_status_on and self._device.is_playback_playing:
            return MediaPlayerState.PLAYING
        if self._device.is_status_on and self._device.is_playback_paused:
            return MediaPlayerState.PAUSED
        if self._device.is_status_on and self._device.is_playback_buffering:
            return MediaPlayerState.BUFFERING
        if self._device.is_status_off:
            return MediaPlayerState.OFF
        if self._device.is_status_on:
            return MediaPlayerState.ON


    def on_change(self):
        self.schedule_update_ha_state()

    async def async_turn_on(self):
        self._device.turn_on(self._gateway)
        self.on_change()

    async def async_turn_off(self):
        self._device.turn_off(self._gateway)
        self.on_change()

    async def async_mute_volume(self, mute: bool) -> None:
        if mute:
            self._device.mute_on(self._gateway)
        else:
            self._device.mute_off(self._gateway)
        self.on_change()

    async def async_set_volume_level(self, volume: float) -> None:
        self._device.set_volume(self._gateway, int(volume * 100))
        self.on_change()

    async def async_media_play(self) -> None:
        self._device.play(self._gateway)
        self.on_change()

    async def async_media_pause(self) -> None:
        self._device.pause(self._gateway)
        self.on_change()
