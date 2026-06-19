"""Tests for shared validation helpers."""

from __future__ import annotations

import networkx as nx
import numpy as np
import pytest

from relationalstats.modules.validation import (
    validate_graph,
    validate_same_node_set,
    validate_square_matrix,
)


def test_validate_graph_rejects_empty_graph() -> None:
    with pytest.raises(ValueError, match="at least one"):
        validate_graph(nx.Graph())


def test_validate_square_matrix_rejects_rectangular_matrix() -> None:
    with pytest.raises(ValueError, match="square"):
        validate_square_matrix(np.ones((2, 3)))


def test_validate_same_node_set_rejects_mismatch() -> None:
    graph_a = nx.Graph()
    graph_a.add_nodes_from([1, 2])

    graph_b = nx.Graph()
    graph_b.add_nodes_from([1, 3])

    with pytest.raises(ValueError, match="same node set"):
        validate_same_node_set(graph_a, graph_b)
