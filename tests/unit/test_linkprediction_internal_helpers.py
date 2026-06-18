"""Tests for internal link prediction helper modules."""

from __future__ import annotations

import networkx as nx
import numpy as np
import pytest
from scipy.sparse import csr_matrix

from relationalstats.linkprediction.metrics import (
    ALL_METRICS,
    GLOBAL_METRICS,
    LOCAL_A2_METRICS,
    safe_divide,
    validate_metrics,
)
from relationalstats.linkprediction.random_walk import (
    random_walk_with_restart_matrix,
    transition_matrix,
)
from relationalstats.linkprediction.spectral import (
    average_commute_time_scores,
    katz_matrix,
)


def test_validate_metrics_returns_all_metrics_when_none() -> None:
    assert validate_metrics(None) == ALL_METRICS


def test_validate_metrics_rejects_unknown_metric() -> None:
    with pytest.raises(ValueError, match="Unknown link prediction metric"):
        validate_metrics(["jaccard", "not_a_metric"])


def test_metric_groups_expose_expected_members() -> None:
    assert "jaccard" in LOCAL_A2_METRICS
    assert "local_path" in LOCAL_A2_METRICS
    assert "katz" in GLOBAL_METRICS
    assert "rwr" in GLOBAL_METRICS
    assert "act" in GLOBAL_METRICS


def test_safe_divide_returns_zero_when_denominator_is_zero() -> None:
    numerator = np.array([1.0, 1.0, 0.0])
    denominator = np.array([2.0, 0.0, 0.0])

    result = safe_divide(numerator, denominator)

    assert result.tolist() == [0.5, 0.0, 0.0]


def test_transition_matrix_row_normalizes_non_isolated_nodes() -> None:
    adjacency = csr_matrix(
        np.array(
            [
                [0.0, 1.0, 1.0],
                [1.0, 0.0, 0.0],
                [1.0, 0.0, 0.0],
            ]
        )
    )
    degree = np.array([2.0, 1.0, 1.0])

    transition = transition_matrix(adjacency, degree).toarray()

    assert transition[0].tolist() == [0.0, 0.5, 0.5]
    assert transition[1].tolist() == [1.0, 0.0, 0.0]
    assert transition[2].tolist() == [1.0, 0.0, 0.0]


def test_random_walk_with_restart_rejects_invalid_alpha() -> None:
    adjacency = csr_matrix(np.eye(2))
    degree = np.array([1.0, 1.0])

    with pytest.raises(ValueError, match="alpha"):
        random_walk_with_restart_matrix(adjacency, degree, alpha=0.0)


def test_katz_matrix_on_empty_edge_graph_has_zero_off_diagonal_scores() -> None:
    adjacency = csr_matrix(np.zeros((2, 2)))

    matrix = katz_matrix(adjacency, beta=0.005).toarray()

    assert np.allclose(matrix, np.zeros((2, 2)))


def test_katz_matrix_rejects_non_positive_beta() -> None:
    adjacency = csr_matrix(np.eye(2))

    with pytest.raises(ValueError, match="beta"):
        katz_matrix(adjacency, beta=0.0)


def test_average_commute_time_scores_on_path_graph() -> None:
    graph = nx.path_graph(3)
    nodes = list(graph.nodes())
    pairs = [(0, 2)]
    source_indices = np.array([0])
    target_indices = np.array([2])

    scores = average_commute_time_scores(
        graph,
        nodes=nodes,
        pairs=pairs,
        source_indices=source_indices,
        target_indices=target_indices,
    )

    assert scores[0] == pytest.approx(1 / 8)


def test_average_commute_time_scores_returns_zero_for_disconnected_pair() -> None:
    graph = nx.Graph()
    graph.add_edges_from([(0, 1), (2, 3)])
    nodes = list(graph.nodes())
    pairs = [(0, 2)]
    source_indices = np.array([0])
    target_indices = np.array([2])

    scores = average_commute_time_scores(
        graph,
        nodes=nodes,
        pairs=pairs,
        source_indices=source_indices,
        target_indices=target_indices,
    )

    assert scores[0] == pytest.approx(0.0)
