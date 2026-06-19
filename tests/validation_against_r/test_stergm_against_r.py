"""Validation placeholders for STERGM comparisons against R tergm/stergm."""

from __future__ import annotations

import pytest


def test_stergm_r_validation_fixtures_are_pending() -> None:
    """Document that R STERGM validation fixtures are intentionally pending."""
    pytest.skip(
        "R tergm/stergm validation fixtures are pending. "
        "Current STERGM tests validate Python-side temporal dyad logic."
    )
