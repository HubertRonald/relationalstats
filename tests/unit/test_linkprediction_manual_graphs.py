"""Manual small-graph tests for link prediction metrics."""

from __future__ import annotations

import math

import networkx as nx
import pytest

from relationalstats.linkprediction import ProxFun, proxfun_full


def _single_score_row(
    graph: nx.Graph,
    pair: tuple[int, int],
    metrics: list[str],
):
    """Return the only score row for a single pair."""
    scores = proxfun_full(graph, pairs=[pair], metrics=metrics)

    assert len(scores) == 1
    assert list(scores[["source", "target"]].iloc[0]) == list(pair)

    return scores.iloc[0]


def test_path_graph_manual_local_metrics() -> None:
    """Validate local metrics on the path graph 0 -- 1 -- 2."""
    graph = nx.path_graph(3)

    row = _single_score_row(
        graph,
        pair=(0, 2),
        metrics=[
            "common_neighbors",
            "jaccard",
            "adamic_adar",
            "resource_allocation",
            "preferential_attachment",
            "salton",
            "sorensen",
            "hub_promoted",
            "hub_depressed",
            "lhn_local",
            "degree",
            "shortest_path",
        ],
    )

    assert row["common_neighbors"] == 1
    assert row["jaccard"] == pytest.approx(1.0)
    assert row["adamic_adar"] == pytest.approx(1 / math.log(2))
    assert row["resource_allocation"] == pytest.approx(1 / 2)
    assert row["preferential_attachment"] == 1
    assert row["salton"] == pytest.approx(1.0)
    assert row["sorensen"] == pytest.approx(1.0)
    assert row["hub_promoted"] == pytest.approx(1.0)
    assert row["hub_depressed"] == pytest.approx(1.0)
    assert row["lhn_local"] == pytest.approx(1.0)
    assert row["degree_source"] == 1
    assert row["degree_target"] == 1
    assert row["shortest_path"] == pytest.approx(2.0)


def test_asymmetric_degrees_manual_hub_sensitive_metrics() -> None:
    """Validate metrics where node degrees differ but one neighbor is shared.

    Graph:

        3
        |
        0 -- 2 -- 1 -- 4
                  | \
                  5  6

    Pair (0, 1):

    - degree(0) = 2
    - degree(1) = 4
    - common neighbors = {2}
    """
    graph = nx.Graph()
    graph.add_edges_from(
        [
            (0, 2),
            (0, 3),
            (1, 2),
            (1, 4),
            (1, 5),
            (1, 6),
        ]
    )

    row = _single_score_row(
        graph,
        pair=(0, 1),
        metrics=[
            "common_neighbors",
            "jaccard",
            "preferential_attachment",
            "salton",
            "sorensen",
            "hub_promoted",
            "hub_depressed",
            "lhn_local",
            "degree",
        ],
    )

    assert row["common_neighbors"] == 1
    assert row["degree_source"] == 2
    assert row["degree_target"] == 4
    assert row["preferential_attachment"] == 8
    assert row["jaccard"] == pytest.approx(1 / 5)
    assert row["salton"] == pytest.approx(1 / math.sqrt(8))
    assert row["sorensen"] == pytest.approx(2 / 6)
    assert row["hub_promoted"] == pytest.approx(1 / 2)
    assert row["hub_depressed"] == pytest.approx(1 / 4)
    assert row["lhn_local"] == pytest.approx(1 / 8)


def test_local_path_on_length_three_path() -> None:
    """Validate local path on 0 -- 1 -- 2 -- 3.

    For pair (0, 3):

    - there are no walks of length 2;
    - there is one walk of length 3;
    - with default beta = 0.01, local_path = 0.01.
    """
    graph = nx.path_graph(4)

    row = _single_score_row(
        graph,
        pair=(0, 3),
        metrics=["shortest_path", "local_path"],
    )

    assert row["shortest_path"] == pytest.approx(3.0)
    assert row["local_path"] == pytest.approx(0.01)


def test_pairs_none_scores_non_edges_on_path_graph() -> None:
    """When pairs is None, non-existing edges should be scored."""
    graph = nx.path_graph(3)

    scores = proxfun_full(
        graph,
        pairs=None,
        metrics=["common_neighbors", "jaccard"],
    )

    normalized_pairs = {
        tuple(sorted((source, target)))
        for source, target in zip(scores["source"], scores["target"], strict=True)
    }

    assert normalized_pairs == {(0, 2)}

    row = scores.iloc[0]
    assert row["common_neighbors"] == 1
    assert row["jaccard"] == pytest.approx(1.0)


def test_disconnected_graph_shortest_path_is_infinite() -> None:
    """Validate disconnected-pair behavior for shortest path."""
    graph = nx.Graph()
    graph.add_edges_from([(0, 1), (2, 3)])

    row = _single_score_row(
        graph,
        pair=(0, 2),
        metrics=["shortest_path"],
    )

    assert math.isinf(row["shortest_path"])


def test_zero_degree_nodes_return_safe_zero_similarity_scores() -> None:
    """Validate zero-division policy on two isolated nodes."""
    graph = nx.Graph()
    graph.add_nodes_from([0, 1])

    row = _single_score_row(
        graph,
        pair=(0, 1),
        metrics=[
            "common_neighbors",
            "jaccard",
            "salton",
            "sorensen",
            "hub_promoted",
            "hub_depressed",
            "lhn_local",
            "degree",
        ],
    )

    assert row["common_neighbors"] == 0
    assert row["degree_source"] == 0
    assert row["degree_target"] == 0
    assert row["jaccard"] == pytest.approx(0.0)
    assert row["salton"] == pytest.approx(0.0)
    assert row["sorensen"] == pytest.approx(0.0)
    assert row["hub_promoted"] == pytest.approx(0.0)
    assert row["hub_depressed"] == pytest.approx(0.0)
    assert row["lhn_local"] == pytest.approx(0.0)


def test_estimator_api_matches_manual_path_graph_expectations() -> None:
    """Validate ProxFun estimator API on a manually verifiable graph."""
    graph = nx.path_graph(3)

    result = ProxFun(metrics=["common_neighbors", "jaccard"]).fit(graph)
    scores = result.to_dataframe()

    normalized_pairs = {
        tuple(sorted((source, target)))
        for source, target in zip(scores["source"], scores["target"], strict=True)
    }

    assert normalized_pairs == {(0, 2)}

    top = result.top_k(k=1, metric="jaccard")
    assert len(top) == 1
    assert top.iloc[0]["common_neighbors"] == 1
    assert top.iloc[0]["jaccard"] == pytest.approx(1.0)
