"""Result objects for ERGM approximation models."""

from __future__ import annotations

from dataclasses import dataclass

import networkx as nx
import numpy as np
import pandas as pd


@dataclass(slots=True)
class ERGMResult:
    """Result object returned by ``ERGM.fit``."""

    coefficients_: pd.Series
    standard_errors_: pd.Series
    z_values_: pd.Series
    p_values_: pd.Series
    feature_frame_: pd.DataFrame
    original_graph_: nx.Graph | nx.DiGraph
    terms_: list[str]
    directed_: bool
    include_diagonal_: bool
    backend_: str

    @property
    def odds_ratios_(self) -> pd.Series:
        """Return odds ratios from fitted coefficients."""
        return np.exp(self.coefficients_)

    def to_dataframe(self) -> pd.DataFrame:
        """Return fitted coefficients and diagnostics."""
        return pd.DataFrame(
            {
                "term": self.coefficients_.index,
                "coefficient": self.coefficients_.to_numpy(),
                "odds_ratio": self.odds_ratios_.to_numpy(),
                "std_error": self.standard_errors_.reindex(self.coefficients_.index).to_numpy(),
                "z_value": self.z_values_.reindex(self.coefficients_.index).to_numpy(),
                "backend_p_value": self.p_values_.reindex(self.coefficients_.index).to_numpy(),
            }
        )

    def summary(self) -> str:
        """Return a compact text summary."""
        return (
            "ERGMResult("
            f"terms={self.terms_}, backend='{self.backend_}', "
            f"directed={self.directed_}, approximation='dyadic_logit')"
        )

    def gof(self, *, n_sim: int = 100, seed: int | None = None):
        """Run an approximate GOF simulation from the fitted model."""
        from .gof import simulate_ergm_gof
        return simulate_ergm_gof(self, n_sim=n_sim, seed=seed)
