"""Shared simulation helpers for relational models."""

from __future__ import annotations

from collections.abc import Sequence

import networkx as nx
import numpy as np
import pandas as pd


def sigmoid(values: np.ndarray | pd.Series) -> np.ndarray:
    """Return logistic probabilities."""
    values = np.asarray(values, dtype=float)
    return 1.0 / (1.0 + np.exp(-values))


def simulate_graph_from_probabilities(
        *,
        nodes: Sequence[object],
        dyads: Sequence[tuple[object, object]],
        probabilities: Sequence[float],
        directed: bool = False,
        seed: int | None = None,
    ) -> nx.Graph | nx.DiGraph:
    """Simulate a graph from dyad-level edge probabilities."""
    rng = np.random.default_rng(seed)
    graph: nx.Graph | nx.DiGraph = nx.DiGraph() if directed else nx.Graph()
    graph.add_nodes_from(nodes)

    for (u, v), probability in zip(dyads, probabilities, strict=True):
        if rng.random() < float(probability):
            graph.add_edge(u, v)

    return graph
