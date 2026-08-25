"""Shared fixtures."""
from zoneinfo import ZoneInfo

import pytest

from homeassistant.util import dt as dt_util

BRUSSELS = ZoneInfo("Europe/Brussels")


@pytest.fixture(autouse=True)
def brussels_timezone():
    """Run every test with HA configured for Europe/Brussels."""
    original = dt_util.DEFAULT_TIME_ZONE
    dt_util.DEFAULT_TIME_ZONE = BRUSSELS
    yield
    dt_util.DEFAULT_TIME_ZONE = original
