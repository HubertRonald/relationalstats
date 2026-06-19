"""Tests for ERGM approximation model and GOF."""

from __future__ import annotations

from relationalstats.datasets import make_florentine_like_graph
from relationalstats.ergm import ERGM


def test_ergm_sklearn_fit_returns_result_table() -> None:
    graph = make_florentine_like_graph()
    result = ERGM(
        terms=["edges", "common_neighbors", "degree1", "gwesp"],
        backend="sklearn",
        random_state=42,
    ).fit(graph)
    frame = result.to_dataframe()
    assert result.backend_ == "sklearn"
    assert set(frame["term"]) == {"edges", "common_neighbors", "degree1", "gwesp"}
    assert frame["coefficient"].notna().all()


def test_ergm_gof_runs_small_number_of_simulations() -> None:
    graph = make_florentine_like_graph()
    result = ERGM(
        terms=["edges", "common_neighbors", "degree1", "gwesp"],
        backend="sklearn",
        random_state=42,
    ).fit(graph)
    gof = result.gof(n_sim=3, seed=123)
    assert gof.n_sim_ == 3
    assert len(gof.simulations_) == 3
    assert "edges" in gof.observed_
    assert {"edges", "density", "avg_degree", "triangles"}.issubset(gof.scalar_frame().columns)
