"""Tests standard tap features using the built-in SDK tests library."""

from singer_sdk.testing import get_tap_test_class

from tap_bls.tap import Tapbls

SAMPLE_CONFIG = {
    "series_ids": ["LAUCN040010000000005", "LAUCN040010000000006"],
    # Read registration key from environment variables.
}


# Run standard built-in tap tests from the SDK:
TestTapbls = get_tap_test_class(
    tap_class=Tapbls,
    config=SAMPLE_CONFIG,
)
