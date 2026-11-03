"""Next Charging Time sensor: time of day -> absolute timestamp.

The controller only reports a time of day (HH:MM). The sensor is a
timestamp sensor, so it must expose a full date and time; otherwise
the frontend shows 'Invalid timestamp'.
"""
from datetime import datetime, time

from zoneinfo import ZoneInfo

from custom_components.nhc2.entities.generic_chargingstation_next_charging_time import (
    next_charging_timestamp,
)

BRUSSELS = ZoneInfo("Europe/Brussels")


def test_time_still_in_the_future_is_todays_date():
    now = datetime(2026, 10, 21, 9, 4, 13, tzinfo=BRUSSELS)

    assert next_charging_timestamp(time(12, 15), now) == datetime(2026, 10, 21, 12, 15, tzinfo=BRUSSELS)


def test_time_already_passed_rolls_over_to_tomorrow():
    now = datetime(2026, 10, 21, 22, 30, tzinfo=BRUSSELS)

    assert next_charging_timestamp(time(12, 15), now) == datetime(2026, 10, 22, 12, 15, tzinfo=BRUSSELS)


def test_rollover_across_the_month_boundary():
    now = datetime(2026, 10, 31, 23, 59, tzinfo=BRUSSELS)

    assert next_charging_timestamp(time(0, 0), now) == datetime(2026, 11, 1, 0, 0, tzinfo=BRUSSELS)