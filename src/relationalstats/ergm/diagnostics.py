"""Diagnostics helpers for ERGM approximations."""

from __future__ import annotations

import pandas as pd


def feature_summary(frame: pd.DataFrame, *, outcome: str = "edge") -> pd.DataFrame:
    """Return a simple feature summary for an ERGM dyad frame."""
    columns = [c for c in frame.columns if c not in {"source", "target", outcome}]
    return frame[columns].describe().T
