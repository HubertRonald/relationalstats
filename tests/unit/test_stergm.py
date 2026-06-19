"""Tests for STERGM approximation workflows."""

from __future__ import annotations

from relationalstats.datasets import make_stergm_temporal_toy
from relationalstats.stergm import STERGM, build_stergm_datasets


def test_build_stergm_datasets_splits_formation_and_dissolution() -> None:
    graph_t1, graph_t2 = make_stergm_temporal_toy()
    formation, dissolution = build_stergm_datasets(graph_t1, graph_t2)
    assert "formation" in formation.columns
    assert "dissolution" in dissolution.columns
    assert formation["y_t1"].eq(0).all()
    assert dissolution["y_t1"].eq(1).all()
    assert formation["formation"].sum() == 2
    assert dissolution["dissolution"].sum() == 1


def test_stergm_sklearn_fit_returns_stage_tables() -> None:
    graph_t1, graph_t2 = make_stergm_temporal_toy()
    result = STERGM(
        formation_terms=["edges", "common_neighbors", "degree1", "gwesp"],
        dissolution_terms=["edges", "common_neighbors", "degree1", "gwesp"],
        backend="sklearn",
        random_state=42,
    ).fit(graph_t1, graph_t2)
    frame = result.to_dataframe()
    assert set(frame["stage"]) == {"formation", "dissolution"}
    assert frame["coefficient"].notna().all()


def test_stergm_simulate_returns_graph_with_same_nodes() -> None:
    graph_t1, graph_t2 = make_stergm_temporal_toy()
    result = STERGM(
        formation_terms=["edges", "common_neighbors", "degree1", "gwesp"],
        dissolution_terms=["edges", "common_neighbors", "degree1", "gwesp"],
        backend="sklearn",
        random_state=42,
    ).fit(graph_t1, graph_t2)
    simulated = result.simulate(seed=123)
    assert set(simulated.nodes()) == set(graph_t1.nodes())
