"""Shared validation helpers."""

from __future__ import annotations

import networkx as nx
import numpy as np


def validate_graph(graph: nx.Graph | nx.DiGraph) -> None:
    """Validate a NetworkX graph."""
    if not isinstance(graph, (nx.Graph, nx.DiGraph)):
        raise TypeError("graph must be a networkx Graph or DiGraph.")
    if graph.number_of_nodes() == 0:
        raise ValueError("graph must contain at least one node.")


def validate_same_node_set(
    graph_a: nx.Graph | nx.DiGraph,
    graph_b: nx.Graph | nx.DiGraph,
) -> None:
    """Validate that two graphs contain the same node set."""
    validate_graph(graph_a)
    validate_graph(graph_b)
    if set(graph_a.nodes()) != set(graph_b.nodes()):
        raise ValueError("graphs must contain the same node set.")


def validate_square_matrix(matrix: np.ndarray, *, name: str = "matrix") -> np.ndarray:
    """Return a validated square matrix."""
    matrix = np.asarray(matrix)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError(f"{name} must be a square 2D matrix.")
    return matrix
