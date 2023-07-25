"""Stream type classes for tap-bls."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, Iterable

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator

from tap_bls.client import BLSStream

if TYPE_CHECKING:
    import requests

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class TimeseriesPaginator(BaseAPIPaginator):
    """Pagination for the Timeseries stream to query 50 timeseries at once."""

    def __init__(self, series_ids: list) -> None:
        """A Timeseries paginator.

        Args:
            series_ids: An array of series_ids to paginate through.
        """
        # Maximum number of timeseries that the API will allow in a single request.
        sublist_size = 50

        # Split the provided series_ids into sublists each with a maximum of
        # sublist_size entries.
        self.series_ids = [
            series_ids[i : i + sublist_size]
            for i in range(0, len(series_ids), sublist_size)
        ]

        try:
            start_value = self.series_ids.pop(0)
        except IndexError as e:
            msg = "series_ids not found. Did you accidentally provide an empty list?"
            raise RuntimeError(msg) from e

        super().__init__(start_value=start_value)

    def get_next(self, response: requests.Response) -> list | None:  # noqa: ARG002
        """Get the next page token.

        Args:
            response: API response object.

        Returns:
            The next page token.
        """
        try:
            return self.series_ids.pop(0)
        except IndexError:
            return None


class TimeseriesStream(BLSStream):
    """Timeseries data on multiple user-configured timeseries."""

    rest_method = "POST"
    name = "timeseries"
    path = "/timeseries/data"
    primary_keys: ClassVar[list] = ["series_id", "year", "period"]
    schema_filepath = SCHEMAS_DIR / "timeseries.json"
    records_jsonpath = "$.Results.series[*]"

    def get_new_paginator(self) -> TimeseriesPaginator:
        """Get a new TimeseriesPaginator."""
        return TimeseriesPaginator(series_ids=self.config["series_ids"])

    def prepare_request_payload(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: list | None,
    ) -> dict | None:
        """Prepare the data payload for the REST API request.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary with the JSON body for a POST requests.
        """
        payload = {}
        payload["registrationkey"] = self.config["registration_key"]
        payload["startyear"] = self.config["start_year"]
        payload["endyear"] = self.config["end_year"]
        payload["seriesid"] = next_page_token
        return payload

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the json returned by the BLS API.

        Also add the series_id to each record returned. This is done both to make it
        more clear what series each record belongs to and also because it is a necessary
        component of a composite primary key for this stream.

        Yields:
            A dictionary containing the JSON response modified to contain the series_id.
        """
        for series in extract_jsonpath(self.records_jsonpath, input=response.json()):
            series_id = next(extract_jsonpath("$.seriesID", input=series), "NOT FOUND")
            for entry in extract_jsonpath("$.data[*]", input=series):
                entry["series_id"] = series_id
                yield entry
