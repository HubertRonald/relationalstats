"""Validation placeholders for QAP comparisons against R sna::netlogit."""

from __future__ import annotations

import pytest


def test_qap_netlogit_validation_fixtures_are_pending() -> None:
    """Document that R validation fixtures are intentionally not committed yet."""
    pytest.skip(
        "R sna::netlogit validation fixtures are pending. "
        "Unit tests currently cover the Python QAPLogit implementation."
    )
