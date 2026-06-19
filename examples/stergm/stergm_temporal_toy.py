"""Temporal toy STERGM approximation example."""

from __future__ import annotations

from relationalstats.datasets import make_stergm_temporal_toy
from relationalstats.stergm import STERGM


def main() -> None:
    graph_t1, graph_t2 = make_stergm_temporal_toy()
    result = STERGM(
        formation_terms=["edges", "common_neighbors", "degree1", "gwesp"],
        dissolution_terms=["edges", "common_neighbors", "degree1", "gwesp"],
        backend="sklearn",
        random_state=42,
    ).fit(graph_t1, graph_t2)
    print(result.summary())
    print(result.to_dataframe().to_string(index=False))
    simulated = result.simulate(seed=123)
    print(f"\nt1 edges: {graph_t1.number_of_edges()}")
    print(f"t2 observed edges: {graph_t2.number_of_edges()}")
    print(f"t2 simulated edges: {simulated.number_of_edges()}")


if __name__ == "__main__":
    main()
