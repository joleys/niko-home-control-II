"""The controller link in device_info.

`via_device` is deprecated and stops working in Home Assistant 2027.8.0, and
the replacement is not a rename: `via_device` took the controller's
identifiers, `via_device_id` takes its device registry id.
"""
from custom_components.nhc2.hub import Nhc2Hub
from custom_components.nhc2.nhccoco.devices.device import CoCoDevice

HUB = Nhc2Hub('hobby', 'c0ffee1234')

# One entry as it arrives in a devices.list response.
DEVICE_PAYLOAD = {
    'Uuid': 'de305d54-75b4-431b-adb2-eb6b9e546014',
    'Type': 'action',
    'Technology': 'nikohomecontrol',
    'Model': 'light',
    'Identifier': 'lamp-keuken',
    'Name': 'Keuken',
    'Online': 'True',
    'Parameters': [{'LocationName': 'Keuken'}],
}


def make_device(**overrides) -> CoCoDevice:
    return CoCoDevice({**DEVICE_PAYLOAD, **overrides})


def test_device_info_links_to_the_controller_by_registry_id():
    assert make_device().device_info(HUB)['via_device_id'] == 'c0ffee1234'


def test_device_info_no_longer_emits_the_deprecated_key():
    """Passing both is rejected outright by the device registry."""
    assert 'via_device' not in make_device().device_info(HUB)


def test_device_info_still_identifies_the_device_by_its_own_uuid():
    """The link to the controller changed; the device's own identity must not."""
    info = make_device().device_info(HUB)

    assert info['identifiers'] == {('nhc2', 'de305d54-75b4-431b-adb2-eb6b9e546014')}
    assert info['name'] == 'Keuken'
    assert info['suggested_area'] == 'Keuken'
