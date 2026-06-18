"""Spectral and global matrix helpers for link prediction metrics."""

from __future__ import annotations

from collections.abc import Sequence

import networkx as nx
import numpy as np
from scipy.sparse import csr_matrix, eye
from scipy.sparse.linalg import inv

from .metrics import safe_divide


def katz_matrix(
    adjacency: csr_matrix,
    *,
    beta: float = 0.005,
) -> csr_matrix:
    """Return the Katz score matrix.

    The implementation uses the matrix form:

    ``(I - beta * A)^(-1) - I``.
    """
    if beta <= 0:
        raise ValueError("beta must be positive.")

    identity = eye(adjacency.shape[0], format="csr", dtype=float)

    return inv(identity - beta * adjacency) - identity


def average_commute_time_scores(
    graph: nx.Graph | nx.DiGraph,
    *,
    nodes: Sequence[object],
    pairs: Sequence[tuple[object, object]],
    source_indices: np.ndarray,
    target_indices: np.ndarray,
) -> np.ndarray:
    """Return average-commute-time scores for selected node pairs.

    The score is ``1 / commute_time``. Disconnected pairs receive score ``0.0``.
    This helper uses dense linear algebra and is intended for small to medium
    graphs.
    """
    undirected = graph.to_undirected()

    laplacian = nx.laplacian_matrix(undirected, nodelist=list(nodes)).astype(float)
    laplacian_pinv = np.linalg.pinv(laplacian.toarray())

    volume = 2.0 * undirected.number_of_edges()

    commute = volume * (
        laplacian_pinv[source_indices, source_indices]
        + laplacian_pinv[target_indices, target_indices]
        - 2.0 * laplacian_pinv[source_indices, target_indices]
    )

    scores = safe_divide(np.ones_like(commute, dtype=float), commute)

    connected = np.array(
        [nx.has_path(undirected, source, target) for source, target in pairs],
        dtype=bool,
    )

    scores[~connected] = 0.0

    return scores
