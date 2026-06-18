"""Metric registry and numeric helpers for link prediction."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np


ALL_METRICS: list[str] = [
    "common_neighbors",
    "jaccard",
    "adamic_adar",
    "preferential_attachment",
    "resource_allocation",
    "salton",
    "sorensen",
    "hub_promoted",
    "hub_depressed",
    "lhn_local",
    "shortest_path",
    "local_path",
    "katz",
    "rwr",
    "degree",
    "act",
]

LOCAL_A2_METRICS: set[str] = {
    "common_neighbors",
    "jaccard",
    "salton",
    "sorensen",
    "hub_promoted",
    "hub_depressed",
    "lhn_local",
    "local_path",
}

GLOBAL_METRICS: set[str] = {
    "katz",
    "rwr",
    "act",
}


def validate_metrics(metrics: Sequence[str] | None) -> list[str]:
    """Validate requested metric names and return a concrete metric list."""
    if metrics is None:
        return list(ALL_METRICS)

    unknown = sorted(set(metrics) - set(ALL_METRICS))
    if unknown:
        raise ValueError(
            "Unknown link prediction metric(s): "
            + ", ".join(unknown)
            + f". Supported metrics are: {', '.join(ALL_METRICS)}."
        )

    return list(metrics)


def safe_divide(numerator: np.ndarray, denominator: np.ndarray) -> np.ndarray:
    """Safely divide arrays and return zero where the denominator is not positive."""
    numerator = np.asarray(numerator, dtype=float)
    denominator = np.asarray(denominator, dtype=float)

    out = np.zeros_like(numerator, dtype=float)

    return np.divide(
        numerator,
        denominator,
        out=out,
        where=denominator > 0,
    )
