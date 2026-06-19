"""Result objects for STERGM approximations."""

from __future__ import annotations

from dataclasses import dataclass

import networkx as nx
import numpy as np
import pandas as pd


@dataclass(slots=True)
class STERGMStageResult:
    """Result for one STERGM stage."""

    stage: str
    coefficients_: pd.Series
    standard_errors_: pd.Series
    z_values_: pd.Series
    p_values_: pd.Series
    frame_: pd.DataFrame
    outcome_: str
    terms_: list[str]
    backend_: str

    @property
    def odds_ratios_(self) -> pd.Series:
        """Return odds ratios."""
        return np.exp(self.coefficients_)

    def to_dataframe(self) -> pd.DataFrame:
        """Return stage coefficients and diagnostics."""
        return pd.DataFrame(
            {
                "stage": self.stage,
                "term": self.coefficients_.index,
                "coefficient": self.coefficients_.to_numpy(),
                "odds_ratio": self.odds_ratios_.to_numpy(),
                "std_error": self.standard_errors_.reindex(self.coefficients_.index).to_numpy(),
                "z_value": self.z_values_.reindex(self.coefficients_.index).to_numpy(),
                "backend_p_value": self.p_values_.reindex(self.coefficients_.index).to_numpy(),
            }
        )


@dataclass(slots=True)
class STERGMResult:
    """Result object returned by ``STERGM.fit``."""

    formation_: STERGMStageResult
    dissolution_: STERGMStageResult
    graph_t1_: nx.Graph | nx.DiGraph
    graph_t2_: nx.Graph | nx.DiGraph
    directed_: bool

    def to_dataframe(self) -> pd.DataFrame:
        """Return formation and dissolution result tables."""
        return pd.concat(
            [self.formation_.to_dataframe(), self.dissolution_.to_dataframe()],
            ignore_index=True,
        )

    def summary(self) -> str:
        """Return a compact text summary."""
        return (
            "STERGMResult("
            f"formation_terms={self.formation_.terms_}, "
            f"dissolution_terms={self.dissolution_.terms_}, "
            f"directed={self.directed_}, approximation='separable_dyadic_logit')"
        )

    def simulate(self, *, seed: int | None = None):
        """Simulate one next-period graph from the fitted STERGM approximation."""
        from .model import simulate_stergm_next
        return simulate_stergm_next(self, seed=seed)
