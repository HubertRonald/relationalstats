"""Tests for ERGM approximation statistics."""

from __future__ import annotations

import networkx as nx
import pytest

from relationalstats.datasets import make_florentine_like_graph
from relationalstats.ergm.statistics import (
    build_ergm_feature_frame,
    count_common_neighbors,
    geodesic_distance_distribution,
    gwesp_approx,
    network_gof_statistics,
    nodematch,
)


def test_common_neighbors_on_path_graph() -> None:
    assert count_common_neighbors(nx.path_graph(3), 0, 2) == 1


def test_gwesp_approx_zero_when_no_shared_partners() -> None:
    assert gwesp_approx(0) == 0.0


def test_nodematch_uses_node_attributes() -> None:
    graph = make_florentine_like_graph()
    assert nodematch(graph, "Medici", "Guadagni", "faction") == 1
    assert nodematch(graph, "Medici", "Strozzi", "faction") == 0


def test_build_ergm_feature_frame_contains_requested_terms() -> None:
    graph = make_florentine_like_graph()
    frame = build_ergm_feature_frame(
        graph,
        terms=["edges", "common_neighbors", "degree1", "gwesp", "nodematch:faction"],
    )
    assert {"edge", "edges", "common_neighbors", "degree1", "gwesp", "nodematch:faction"}.issubset(frame.columns)
    assert frame["edges"].eq(1.0).all()


def test_geodesic_distance_distribution_uses_nr_for_disconnected_pairs() -> None:
    graph = nx.Graph()
    graph.add_edges_from([(0, 1), (2, 3)])
    distribution = geodesic_distance_distribution(graph)
    assert distribution["NR"] == 4


def test_network_gof_statistics_contains_expected_keys() -> None:
    graph = make_florentine_like_graph()
    stats = network_gof_statistics(graph)
    assert {"edges", "density", "avg_degree", "degree_dist", "ewsp", "triangles", "geodesic"}.issubset(stats.keys())
    assert stats["edges"] == graph.number_of_edges()
    assert stats["density"] == pytest.approx(nx.density(graph))
