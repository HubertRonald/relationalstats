"""Small generic utilities shared across modules."""

from __future__ import annotations

import numpy as np


def safe_mean(values: list[float] | np.ndarray) -> float:
    """Return the finite-value mean or NaN if no finite values exist."""
    array = np.asarray(values, dtype=float)
    array = array[np.isfinite(array)]
    if array.size == 0:
        return float("nan")
    return float(array.mean())
