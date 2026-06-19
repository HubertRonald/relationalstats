"""Converters for graphs, matrices, and dyad-level DataFrames."""

from __future__ import annotations

from collections.abc import Iterable

import networkx as nx
import numpy as np
import pandas as pd

from .validation import validate_graph, validate_square_matrix


def iter_dyads(
        nodes: Iterable[object],
        *,
        directed: bool = False,
        include_diagonal: bool = False,
    ) -> list[tuple[object, object]]:
    """Return dyads for a node sequence."""
    node_list = list(nodes)
    if directed:
        return [
            (u, v)
            for u in node_list
            for v in node_list
            if include_diagonal or u != v
        ]

    dyads = []
    for i, u in enumerate(node_list):
        start = i if include_diagonal else i + 1
        for v in node_list[start:]:
            dyads.append((u, v))
    return dyads


def graph_to_dyad_frame(
        graph: nx.Graph | nx.DiGraph,
        *,
        directed: bool | None = None,
        include_diagonal: bool = False,
        outcome_col: str = "edge",
    ) -> pd.DataFrame:
    """Convert a NetworkX graph into a dyad-level DataFrame."""
    validate_graph(graph)
    if directed is None:
        directed = graph.is_directed()

    dyads = iter_dyads(
        graph.nodes(),
        directed=directed,
        include_diagonal=include_diagonal,
    )
    return pd.DataFrame(
        [
            {"source": u, "target": v, outcome_col: int(graph.has_edge(u, v))}
            for u, v in dyads
        ]
    )


def matrix_to_dyad_frame(
        matrix: np.ndarray,
        *,
        directed: bool = True,
        include_diagonal: bool = False,
        outcome_col: str = "value",
    ) -> pd.DataFrame:
    """Convert a square matrix into a dyad-level DataFrame."""
    matrix = validate_square_matrix(matrix, name="matrix")
    dyads = iter_dyads(
        range(matrix.shape[0]),
        directed=directed,
        include_diagonal=include_diagonal,
    )
    return pd.DataFrame(
        [{"source": i, "target": j, outcome_col: matrix[i, j]} for i, j in dyads]
    )
