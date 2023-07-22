"""bls tap class."""

from __future__ import annotations

from datetime import datetime, timezone

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_bls import streams


class Tapbls(Tap):
    """bls tap class."""

    name = "tap-bls"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "registration_key",
            th.StringType,
            required=True,
            secret=True,
            description=(
                "Your registration key. Should look like "
                "`a7f5b9e2c0d48ba1e6d8c90763e45f7d`."
            ),
        ),
        th.Property(
            "start_year",
            th.IntegerType,
            required=True,
            default=datetime.now(timezone.utc).year - 7,
            description=(
                "Only records with a year equal to or greater `start_year` will be "
                "synced."
            ),
        ),
        th.Property(
            "end_year",
            th.IntegerType,
            required=True,
            default=datetime.now(timezone.utc).year,
            description=(
                "Only records with a year equal to or less than `end_year` will be "
                "synced."
            ),
        ),
        th.Property(
            "series_ids",
            th.ArrayType(th.StringType),
            required=True,
            description=(
                "An array of series IDs to sync. If more than 50 are provided, they "
                "will be split into groups of 50 before querying."
            ),
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.BLSStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [streams.TimeseriesStream(self)]


if __name__ == "__main__":
    Tapbls.cli()
