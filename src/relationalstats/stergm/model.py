"""Initial STERGM approximation model."""

from __future__ import annotations

import networkx as nx
import numpy as np

from relationalstats.modules.simulator import sigmoid

from .dissolution import fit_dissolution_stage
from .formation import fit_formation_stage
from .results import STERGMResult
from .temporal_utils import add_temporal_structural_features, build_stergm_datasets


class STERGM:
    """Separable temporal ERGM approximation using dyadic logistic models."""

    def __init__(
            self,
            *,
            formation_terms: list[str] | None = None,
            dissolution_terms: list[str] | None = None,
            backend: str = "statsmodels",
            directed: bool | None = None,
            include_diagonal: bool = False,
            random_state: int | None = None,
            maxiter: int = 100,
            sklearn_C: float = 1.0,
        ) -> None:
        self.formation_terms = formation_terms or ["edges", "common_neighbors", "degree1", "gwesp"]
        self.dissolution_terms = dissolution_terms or ["edges", "common_neighbors", "degree1", "gwesp"]
        self.backend = backend
        self.directed = directed
        self.include_diagonal = include_diagonal
        self.random_state = random_state
        self.maxiter = maxiter
        self.sklearn_C = sklearn_C

    def fit(self, graph_t1: nx.Graph | nx.DiGraph, graph_t2: nx.Graph | nx.DiGraph) -> STERGMResult:
        """Fit formation and dissolution models."""
        directed = (
            graph_t1.is_directed() or graph_t2.is_directed()
            if self.directed is None
            else self.directed
        )
        formation, dissolution = build_stergm_datasets(
            graph_t1,
            graph_t2,
            directed=directed,
            include_diagonal=self.include_diagonal,
        )
        formation = add_temporal_structural_features(
            formation, graph_t1, terms=self.formation_terms
        )
        dissolution = add_temporal_structural_features(
            dissolution, graph_t1, terms=self.dissolution_terms
        )
        formation_result = fit_formation_stage(
            formation,
            terms=self.formation_terms,
            backend=self.backend,
            maxiter=self.maxiter,
            sklearn_C=self.sklearn_C,
            random_state=self.random_state,
        )
        dissolution_result = fit_dissolution_stage(
            dissolution,
            terms=self.dissolution_terms,
            backend=self.backend,
            maxiter=self.maxiter,
            sklearn_C=self.sklearn_C,
            random_state=self.random_state,
        )
        result = STERGMResult(
            formation_=formation_result,
            dissolution_=dissolution_result,
            graph_t1_=graph_t1.copy(),
            graph_t2_=graph_t2.copy(),
            directed_=directed,
        )
        self.result_ = result
        return result


def _stage_probabilities(stage_result) -> np.ndarray:
    X = stage_result.frame_[stage_result.terms_].astype(float)
    beta = stage_result.coefficients_.reindex(stage_result.terms_).to_numpy()
    return sigmoid(X.to_numpy() @ beta)


def simulate_stergm_next(result: STERGMResult, *, seed: int | None = None):
    """Simulate a next-period graph from a fitted STERGM approximation."""
    rng = np.random.default_rng(seed)
    graph = result.graph_t1_.copy()

    dissolution_prob = _stage_probabilities(result.dissolution_)
    dissolution_dyads = list(zip(result.dissolution_.frame_["source"], result.dissolution_.frame_["target"], strict=True))
    for (u, v), probability in zip(dissolution_dyads, dissolution_prob, strict=True):
        if graph.has_edge(u, v) and rng.random() < probability:
            graph.remove_edge(u, v)

    formation_prob = _stage_probabilities(result.formation_)
    formation_dyads = list(zip(result.formation_.frame_["source"], result.formation_.frame_["target"], strict=True))
    for (u, v), probability in zip(formation_dyads, formation_prob, strict=True):
        if not graph.has_edge(u, v) and rng.random() < probability:
            graph.add_edge(u, v)

    return graph
