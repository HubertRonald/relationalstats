"""Diagnostics helpers for QAP workflows."""

from __future__ import annotations

import pandas as pd


def binary_outcome_summary(frame: pd.DataFrame, *, outcome: str = "y") -> pd.Series:
    """Return a compact summary for a binary dyadic outcome column."""
    if outcome not in frame:
        raise ValueError(f"Column '{outcome}' is not present in frame.")

    values = frame[outcome]

    return pd.Series(
        {
            "n_dyads": int(values.shape[0]),
            "positive_rate": float(values.mean()),
            "n_positive": int(values.sum()),
            "n_negative": int((1 - values).sum()),
        }
    )
