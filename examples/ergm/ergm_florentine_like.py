"""Florentine-inspired ERGM approximation example."""

from __future__ import annotations

from relationalstats.datasets import make_florentine_like_graph
from relationalstats.ergm import ERGM


def main() -> None:
    graph = make_florentine_like_graph()
    result = ERGM(
        terms=["edges", "common_neighbors", "degree1", "gwesp", "nodematch:faction"],
        backend="sklearn",
        random_state=42,
    ).fit(graph)
    print(result.summary())
    print(result.to_dataframe().to_string(index=False))
    gof = result.gof(n_sim=10, seed=123)
    print("\nObserved GOF scalar statistics:")
    print(gof.observed_scalar_frame().to_string(index=False))


if __name__ == "__main__":
    main()
