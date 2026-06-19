"""Synthetic datasets for examples and tests."""

from __future__ import annotations

import networkx as nx
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


def make_florentine_like_graph() -> nx.Graph:
    """Return a small Florentine-inspired graph with attributes."""
    graph = nx.Graph()
    graph.add_nodes_from(
        [
            ("Medici", {"wealth": "high", "faction": "A"}),
            ("Strozzi", {"wealth": "high", "faction": "B"}),
            ("Guadagni", {"wealth": "high", "faction": "A"}),
            ("Albizzi", {"wealth": "medium", "faction": "B"}),
            ("Ridolfi", {"wealth": "medium", "faction": "A"}),
            ("Tornabuoni", {"wealth": "medium", "faction": "A"}),
            ("Pazzi", {"wealth": "low", "faction": "B"}),
            ("Ginori", {"wealth": "low", "faction": "B"}),
        ]
    )
    graph.add_edges_from(
        [
            ("Medici", "Guadagni"),
            ("Medici", "Ridolfi"),
            ("Medici", "Tornabuoni"),
            ("Strozzi", "Albizzi"),
            ("Strozzi", "Pazzi"),
            ("Guadagni", "Tornabuoni"),
            ("Albizzi", "Ginori"),
            ("Ridolfi", "Tornabuoni"),
            ("Pazzi", "Ginori"),
        ]
    )
    return graph


def make_stergm_temporal_toy() -> tuple[nx.Graph, nx.Graph]:
    """Return two graph snapshots for STERGM examples and tests."""
    graph_t1 = nx.Graph()
    graph_t1.add_nodes_from(["A", "B", "C", "D", "E"])
    graph_t1.add_edges_from([("A", "B"), ("B", "C"), ("C", "D")])

    graph_t2 = nx.Graph()
    graph_t2.add_nodes_from(graph_t1.nodes())
    graph_t2.add_edges_from([("A", "B"), ("C", "D"), ("D", "E"), ("A", "E")])
    return graph_t1, graph_t2
