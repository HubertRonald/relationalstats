"""Initial ERGM approximation model."""

from __future__ import annotations

import networkx as nx

from relationalstats.qap.backends import fit_logit_backend

from .results import ERGMResult
from .statistics import build_ergm_feature_frame
from .terms import validate_terms


class ERGM:
    """Pedagogical dyadic-logistic ERGM approximation.

    This class is not a full MCMC-MLE ERGM implementation.
    """

    def __init__(
            self,
            *,
            terms: list[str] | None = None,
            backend: str = "statsmodels",
            directed: bool = False,
            include_diagonal: bool = False,
            random_state: int | None = None,
            maxiter: int = 100,
            sklearn_C: float = 1.0,
        ) -> None:
        self.terms = validate_terms(terms)
        self.backend = backend
        self.directed = directed
        self.include_diagonal = include_diagonal
        self.random_state = random_state
        self.maxiter = maxiter
        self.sklearn_C = sklearn_C

    def fit(self, graph: nx.Graph | nx.DiGraph) -> ERGMResult:
        """Fit the dyadic-logistic ERGM approximation."""
        frame = build_ergm_feature_frame(
            graph,
            terms=self.terms,
            directed=self.directed,
            include_diagonal=self.include_diagonal,
        )
        backend_result = fit_logit_backend(
            frame["edge"].to_numpy(),
            frame[self.terms],
            backend=self.backend,
            add_intercept=False,
            maxiter=self.maxiter,
            sklearn_C=self.sklearn_C,
            random_state=self.random_state,
        )
        result = ERGMResult(
            coefficients_=backend_result.coefficients,
            standard_errors_=backend_result.standard_errors,
            z_values_=backend_result.z_values,
            p_values_=backend_result.p_values,
            feature_frame_=frame,
            original_graph_=graph.copy(),
            terms_=self.terms,
            directed_=self.directed,
            include_diagonal_=self.include_diagonal,
            backend_=backend_result.backend,
        )
        self.result_ = result
        self.feature_frame_ = frame
        return result
