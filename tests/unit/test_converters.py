"""Tests for shared converter helpers."""

from __future__ import annotations

import networkx as nx
import numpy as np

from relationalstats.modules.converters import (
    graph_to_dyad_frame,
    iter_dyads,
    matrix_to_dyad_frame,
)


def test_iter_dyads_undirected_excludes_diagonal() -> None:
    assert iter_dyads(["A", "B", "C"], directed=False) == [
        ("A", "B"),
        ("A", "C"),
        ("B", "C"),
    ]


def test_iter_dyads_directed_excludes_diagonal() -> None:
    assert iter_dyads(["A", "B"], directed=True) == [("A", "B"), ("B", "A")]


def test_graph_to_dyad_frame_undirected() -> None:
    graph = nx.path_graph(3)

    frame = graph_to_dyad_frame(graph, directed=False)

    assert len(frame) == 3
    assert frame["edge"].sum() == 2


def test_matrix_to_dyad_frame_directed() -> None:
    matrix = np.array([[0, 1], [0, 0]])

    frame = matrix_to_dyad_frame(matrix, directed=True)

    assert len(frame) == 2
    assert frame["value"].sum() == 1
