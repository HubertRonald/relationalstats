"""Simulation helpers for ERGM approximations."""

from __future__ import annotations

import numpy as np

from relationalstats.modules.simulator import sigmoid, simulate_graph_from_probabilities

from .results import ERGMResult


def predict_ergm_probabilities(result: ERGMResult) -> np.ndarray:
    """Predict dyad probabilities from an ``ERGMResult``."""
    X = result.feature_frame_[result.terms_].astype(float)
    beta = result.coefficients_.reindex(result.terms_).to_numpy()
    return sigmoid(X.to_numpy() @ beta)


def simulate_network_from_ergm_result(result: ERGMResult, *, seed: int | None = None):
    """Simulate one network from a fitted ERGM approximation."""
    probabilities = predict_ergm_probabilities(result)
    dyads = list(zip(result.feature_frame_["source"], result.feature_frame_["target"], strict=True))
    return simulate_graph_from_probabilities(
        nodes=list(result.original_graph_.nodes()),
        dyads=dyads,
        probabilities=probabilities,
        directed=result.directed_,
        seed=seed,
    )
