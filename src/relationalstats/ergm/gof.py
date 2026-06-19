"""Goodness-of-fit helpers for ERGM approximations."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .results import ERGMResult
from .simulation import simulate_network_from_ergm_result
from .statistics import network_gof_statistics


@dataclass(slots=True)
class ERGMGofResult:
    """GOF result for an ERGM approximation."""

    observed_: dict[str, object]
    simulations_: list[dict[str, object]]
    n_sim_: int

    def scalar_frame(self) -> pd.DataFrame:
        """Return scalar GOF statistics for simulated networks."""
        return pd.DataFrame(
            [
                {
                    "simulation": idx,
                    "edges": sim["edges"],
                    "density": sim["density"],
                    "avg_degree": sim["avg_degree"],
                    "triangles": sim["triangles"],
                }
                for idx, sim in enumerate(self.simulations_)
            ]
        )

    def observed_scalar_frame(self) -> pd.DataFrame:
        """Return observed scalar GOF statistics."""
        return pd.DataFrame(
            [
                {
                    "edges": self.observed_["edges"],
                    "density": self.observed_["density"],
                    "avg_degree": self.observed_["avg_degree"],
                    "triangles": self.observed_["triangles"],
                }
            ]
        )

    def plot(self):
        """Plot scalar GOF summaries."""
        from relationalstats.modules.plotting import plot_gof_boxplot
        return plot_gof_boxplot(
            self.scalar_frame().drop(columns=["simulation"]),
            self.observed_scalar_frame().iloc[0],
            title="ERGM approximate GOF",
        )


def simulate_ergm_gof(
        result: ERGMResult,
        *,
        n_sim: int = 100,
        seed: int | None = None,
    ) -> ERGMGofResult:
    """Simulate networks and compare GOF-style statistics."""
    if n_sim <= 0:
        raise ValueError("n_sim must be positive.")

    simulations = []
    for idx in range(n_sim):
        current_seed = None if seed is None else seed + idx
        graph_sim = simulate_network_from_ergm_result(result, seed=current_seed)
        simulations.append(network_gof_statistics(graph_sim))

    return ERGMGofResult(
        observed_=network_gof_statistics(result.original_graph_),
        simulations_=simulations,
        n_sim_=n_sim,
    )
