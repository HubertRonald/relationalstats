"""Synthetic datasets for examples and tests."""

from __future__ import annotations

import numpy as np


def make_qap_toy_data() -> tuple[np.ndarray, dict[str, np.ndarray]]:
    """Return a small directed binary network and dyadic predictors.

    The dataset is intentionally small and deterministic. It is useful for unit
    tests, documentation examples, and quick local smoke checks.
    """
    y = np.array(
        [
            [0, 1, 0, 1, 0],
            [1, 0, 1, 0, 0],
            [0, 1, 0, 1, 1],
            [0, 0, 1, 0, 1],
            [1, 0, 0, 1, 0],
        ],
        dtype=int,
    )

    groups = np.array([0, 0, 1, 1, 1])
    same_group = (groups[:, None] == groups[None, :]).astype(float)

    node_index = np.arange(y.shape[0])
    distance = np.abs(node_index[:, None] - node_index[None, :]).astype(float)

    return y, {
        "same_group": same_group,
        "distance": distance,
    }
