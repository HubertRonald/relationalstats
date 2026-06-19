"""Validation placeholders for ERGM statistics against R ergm/network."""

from __future__ import annotations

import pytest


def test_ergm_r_validation_fixtures_are_pending() -> None:
    """Document that R ERGM validation fixtures are intentionally pending."""
    pytest.skip(
        "R ergm/network validation fixtures are pending. "
        "Current ERGM tests validate Python-side approximated statistics."
    )
