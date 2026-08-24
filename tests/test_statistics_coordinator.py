"""Tests for the statistics coordinator's timestamp handling.

The measurements API on the Connected Controller works in the
controller's local time: request intervals are interpreted as local time
and returned DateTime values are naive local period starts (verified
against a live controller: a completed hourly bucket labeled 07:00 was
returned at 06:07 UTC, which is only possible for local labels).

These tests pin the local-time contract so the one-hour DST shift from
issue #300 cannot regress.
"""
import asyncio
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock
from zoneinfo import ZoneInfo

from freezegun import freeze_time

from custom_components.nhc2.statistics_coordinator import (
    StatisticsCoordinator,
    align_to_hour,
    align_to_midnight,
)

BRUSSELS = ZoneInfo("Europe/Brussels")
UTC = timezone.utc


def make_coordinator(measurements_client=None) -> StatisticsCoordinator:
    return StatisticsCoordinator(
        hass=MagicMock(),
        gateway=MagicMock(),
        measurements_client=measurements_client or MagicMock(),
        config_entry=MagicMock(),
    )


def controller_label(true_hour_utc: datetime) -> str:
    """Label a bucket the way the controller does: naive local period start."""
    return true_hour_utc.astimezone(BRUSSELS).replace(tzinfo=None).isoformat()


class TestAlignment:
    def test_align_to_hour_uses_local_time(self):
        aligned = align_to_hour(datetime(2026, 7, 15, 12, 30, 59, tzinfo=UTC))
        assert aligned == datetime(2026, 7, 15, 12, 0, tzinfo=UTC)
        assert aligned.astimezone(BRUSSELS).minute == 0
        # returned as a UTC instant, aligned to the local hour boundary
        assert aligned.utcoffset().total_seconds() == 0

    def test_align_to_midnight_uses_local_midnight(self):
        aligned = align_to_midnight(datetime(2026, 7, 15, 12, 30, tzinfo=UTC))
        # local midnight 2026-07-15 CEST == 2026-07-14 22:00 UTC
        assert aligned == datetime(2026, 7, 14, 22, 0, tzinfo=UTC)
        assert aligned.utcoffset().total_seconds() == 0

    def test_align_to_midnight_uses_local_midnight_in_winter(self):
        aligned = align_to_midnight(datetime(2026, 1, 15, 12, 30, tzinfo=UTC))
        # local midnight 2026-01-15 CET == 2026-01-14 23:00 UTC
        assert aligned == datetime(2026, 1, 14, 23, 0, tzinfo=UTC)


class TestProcessApiValues:
    def test_naive_timestamp_is_local_in_summer(self):
        coordinator = make_coordinator()
        result = coordinator._process_api_values(
            [{"DateTime": "2026-07-15T14:00:00", "Value": 5.0}], "ElectricalEnergy"
        )
        # 14:00 CEST == 12:00 UTC
        assert result == [
            {"start": datetime(2026, 7, 15, 12, 0, tzinfo=UTC), "value": 5.0}
        ]

    def test_naive_timestamp_is_local_in_winter(self):
        coordinator = make_coordinator()
        result = coordinator._process_api_values(
            [{"DateTime": "2026-01-15T14:00:00", "Value": 5.0}], "ElectricalEnergy"
        )
        # 14:00 CET == 13:00 UTC
        assert result == [
            {"start": datetime(2026, 1, 15, 13, 0, tzinfo=UTC), "value": 5.0}
        ]

    def test_aware_timestamp_is_respected(self):
        coordinator = make_coordinator()
        result = coordinator._process_api_values(
            [{"DateTime": "2026-07-15T14:00:00+00:00", "Value": 1.0}],
            "ElectricalEnergy",
        )
        assert result[0]["start"] == datetime(2026, 7, 15, 14, 0, tzinfo=UTC)

    def test_water_volume_conversion(self):
        coordinator = make_coordinator()
        result = coordinator._process_api_values(
            [{"DateTime": "2026-07-15T14:00:00", "Value": 0.25}], "WaterVolume"
        )
        assert result[0]["value"] == 250

    def test_incomplete_entries_are_skipped(self):
        coordinator = make_coordinator()
        result = coordinator._process_api_values(
            [
                {"DateTime": "2026-07-15T14:00:00"},
                {"Value": 1.0},
                {"DateTime": "2026-07-15T15:00:00", "Value": None},
            ],
            "ElectricalEnergy",
        )
        assert result == []


class TestNoHourShift:
    """Regression tests for issue #300: buckets must land in their true hour."""

    def _round_trip_mismatches(self, start_utc: datetime, hours: int) -> list:
        coordinator = make_coordinator()
        mismatches = []
        for i in range(hours):
            true_hour = start_utc + timedelta(hours=i)
            result = coordinator._process_api_values(
                [{"DateTime": controller_label(true_hour), "Value": 1.0}],
                "ElectricalEnergy",
            )
            if result[0]["start"] != true_hour:
                mismatches.append((true_hour, result[0]["start"]))
        return mismatches

    def test_winter_week_round_trips_exactly(self):
        assert not self._round_trip_mismatches(
            datetime(2027, 1, 10, 0, tzinfo=UTC), 168
        )

    def test_summer_week_round_trips_exactly(self):
        assert not self._round_trip_mismatches(
            datetime(2027, 7, 11, 0, tzinfo=UTC), 168
        )

    def test_spring_forward_round_trips_exactly(self):
        # DST starts 2027-03-28 02:00 CET -> 03:00 CEST; the skipped local
        # hour never appears as a label, so every bucket maps back exactly.
        assert not self._round_trip_mismatches(
            datetime(2027, 3, 27, 20, tzinfo=UTC), 12
        )

    def test_fall_back_has_exactly_one_ambiguous_hour(self):
        # DST ends 2026-10-25 03:00 CEST -> 02:00 CET: the local hour 02:00
        # occurs twice but the API's naive label cannot distinguish the two
        # passes. Exactly one hour per year is ambiguous; anything more than
        # that single known collision is a regression.
        mismatches = self._round_trip_mismatches(
            datetime(2026, 10, 24, 20, tzinfo=UTC), 12
        )
        assert mismatches == [
            (
                datetime(2026, 10, 25, 1, 0, tzinfo=UTC),  # second 02:00 local
                datetime(2026, 10, 25, 0, 0, tzinfo=UTC),  # mapped to the first
            )
        ]


class TestRequestWindow:
    def test_fetch_sends_naive_local_interval(self):
        client = MagicMock()
        client.get_aggregated_measurements = AsyncMock(return_value=None)
        coordinator = make_coordinator(client)

        device = MagicMock()
        device.uuid = "uuid"
        asyncio.run(
            coordinator._fetch_aggregated_data(
                device,
                "ElectricalEnergy",
                datetime(2026, 7, 15, 10, 0, tzinfo=UTC),
                datetime(2026, 7, 15, 12, 0, tzinfo=UTC),
                "hour",
                63,
            )
        )

        args = client.get_aggregated_measurements.await_args.args
        interval_start, interval_end = args[3], args[4]
        # 10:00/12:00 UTC == 12:00/14:00 CEST, sent naive
        assert interval_start == datetime(2026, 7, 15, 12, 0)
        assert interval_start.tzinfo is None
        assert interval_end == datetime(2026, 7, 15, 14, 0)
        assert interval_end.tzinfo is None


class TestCalculateTimeRange:
    @freeze_time("2026-07-15 10:30:00+00:00")
    def test_recent_import_has_no_one_hour_fudge(self):
        coordinator = make_coordinator()
        statistic_id = "nhc2:test_electricalenergy"
        last_start = datetime(2026, 7, 15, 8, 0, tzinfo=UTC)
        last_stats = {statistic_id: [{"start": last_start.timestamp(), "sum": 1.0}]}

        start_time, end_time = coordinator._calculate_time_range(
            statistic_id, last_stats, longterm=False
        )

        # resume exactly one hour after the last stored bucket ...
        assert start_time == last_start + timedelta(hours=1)
        # ... up to the start of the current (incomplete) local hour
        assert end_time == datetime(2026, 7, 15, 10, 0, tzinfo=UTC)

    @freeze_time("2026-07-15 10:30:00+00:00")
    def test_recent_import_without_history_starts_two_months_back(self):
        coordinator = make_coordinator()
        start_time, end_time = coordinator._calculate_time_range(
            "nhc2:test_electricalenergy", {}, longterm=False
        )

        # local midnight 60 days ago: 2026-05-16 00:00 CEST == 05-15 22:00 UTC
        assert start_time == datetime(2026, 5, 15, 22, 0, tzinfo=UTC)
        assert end_time == datetime(2026, 7, 15, 10, 0, tzinfo=UTC)

    @freeze_time("2026-07-15 10:30:00+00:00")
    def test_no_new_data_returns_none(self):
        coordinator = make_coordinator()
        statistic_id = "nhc2:test_electricalenergy"
        # last bucket is the most recent complete hour -> nothing to fetch
        last_start = datetime(2026, 7, 15, 9, 0, tzinfo=UTC)
        last_stats = {statistic_id: [{"start": last_start.timestamp(), "sum": 1.0}]}

        assert (
            coordinator._calculate_time_range(statistic_id, last_stats, longterm=False)
            is None
        )
