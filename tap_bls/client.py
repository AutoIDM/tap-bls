"""REST client handling, including blsStream base class."""

from __future__ import annotations

from pathlib import Path

from singer_sdk.streams import RESTStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class BLSStream(RESTStream):
    """bls stream class."""

    url_base = "https://api.bls.gov/publicAPI/v2"

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        return {"Content-Type": "application/json"}
