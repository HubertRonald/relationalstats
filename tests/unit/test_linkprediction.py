import math

import networkx as nx
import numpy as np
import pytest

from relationalstats.linkprediction import ALL_METRICS, ProxFun, proxfun_full


def test_proxfun_full_local_metrics_on_path_graph():
    G = nx.path_graph(3)

    scores = proxfun_full(
        G,
        pairs=[(0, 2)],
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
        ],
    )

    row = scores.iloc[0]

    assert row["source"] == 0
    assert row["target"] == 2
    assert row["common_neighbors"] == 1
    assert row["jaccard"] == pytest.approx(1.0)
    assert row["adamic_adar"] == pytest.approx(1.0 / math.log(2.0))
    assert row["resource_allocation"] == pytest.approx(0.5)
    assert row["preferential_attachment"] == pytest.approx(1.0)
    assert row["salton"] == pytest.approx(1.0)
    assert row["sorensen"] == pytest.approx(1.0)
    assert row["hub_promoted"] == pytest.approx(1.0)
    assert row["hub_depressed"] == pytest.approx(1.0)
    assert row["lhn_local"] == pytest.approx(1.0)


def test_proxfun_full_pairs_none_scores_non_edges():
    G = nx.path_graph(3)

    scores = proxfun_full(
        G,
        pairs=None,
        metrics=["common_neighbors", "jaccard"],
    )

    assert list(scores.columns) == [
        "source",
        "target",
        "common_neighbors",
        "jaccard",
    ]

    assert len(scores) == 1
    assert tuple(scores[["source", "target"]].iloc[0]) == (0, 2)


def test_proxfun_full_safe_division_for_isolated_node():
    G = nx.Graph()
    G.add_nodes_from([0, 1])

    scores = proxfun_full(
        G,
        pairs=[(0, 1)],
        metrics=[
            "jaccard",
            "salton",
            "sorensen",
            "hub_promoted",
            "hub_depressed",
            "lhn_local",
        ],
    )

    numeric_values = scores.drop(columns=["source", "target"]).iloc[0].to_numpy()

    assert np.all(np.isfinite(numeric_values))
    assert np.all(numeric_values == 0.0)


def test_proxfun_result_api():
    G = nx.path_graph(3)

    result = ProxFun(metrics=["jaccard", "adamic_adar"]).fit(G)

    df = result.to_dataframe()

    assert "jaccard" in df.columns
    assert "adamic_adar" in df.columns

    top = result.top_k(k=1, metric="jaccard")

    assert len(top) == 1
    assert top.iloc[0]["jaccard"] == pytest.approx(1.0)


def test_unknown_metric_raises_error():
    G = nx.path_graph(3)

    with pytest.raises(ValueError):
        proxfun_full(G, pairs=[(0, 2)], metrics=["not_a_metric"])


def test_all_metrics_are_exposed():
    assert "common_neighbors" in ALL_METRICS
    assert "jaccard" in ALL_METRICS
    assert "adamic_adar" in ALL_METRICS
    assert "katz" in ALL_METRICS
    assert "rwr" in ALL_METRICS
    assert "act" in ALL_METRICS
