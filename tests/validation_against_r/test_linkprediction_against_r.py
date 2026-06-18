"""Validation placeholders for R linkprediction comparisons."""

from __future__ import annotations

import pytest


def test_linkprediction_r_validation_fixtures_are_pending() -> None:
    """Document that R validation fixtures are intentionally not committed yet."""
    pytest.skip(
        "R linkprediction validation fixtures are pending. "
        "Manual Python small-graph tests are used until fixture export is added."
    )
