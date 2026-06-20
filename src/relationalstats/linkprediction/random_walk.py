"""Random-walk helpers for link prediction metrics."""

from __future__ import annotations

import numpy as np
from scipy.sparse import csr_matrix, diags, eye
from scipy.sparse.linalg import inv


def transition_matrix(
    adjacency: csr_matrix,
    degree: np.ndarray,
) -> csr_matrix:
    """Return the row-normalized transition matrix for an adjacency matrix."""
    row_inv_degree = np.zeros_like(degree, dtype=float)

    mask = degree > 0
    row_inv_degree[mask] = 1.0 / degree[mask]

    return diags(row_inv_degree) @ adjacency


def random_walk_with_restart_matrix(
    adjacency: csr_matrix,
    degree: np.ndarray,
    *,
    alpha: float = 0.15,
) -> csr_matrix:
    """Return the random-walk-with-restart score matrix.

    Parameters
    ----------
    adjacency:
        Sparse adjacency matrix.
    degree:
        Degree vector aligned to the adjacency matrix node order.
    alpha:
        Restart probability. Must satisfy ``0 < alpha <= 1``.
    """
    if not 0 < alpha <= 1:
        raise ValueError("alpha must satisfy 0 < alpha <= 1.")

    transition = transition_matrix(adjacency, degree)
    identity = eye(adjacency.shape[0], format="csr", dtype=float)

    return inv(identity - (1.0 - alpha) * transition)
