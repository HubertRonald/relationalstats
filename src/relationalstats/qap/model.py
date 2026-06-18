"""QAP logistic regression models."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Literal

import numpy as np
import pandas as pd

from .backends import fit_logit_backend
from .permutation import (
    dyad_frame,
    empirical_p_values,
    generate_permutations,
    permute_square_matrix,
)
from .results import QAPLogitResult


QAPLogitBackend = Literal["statsmodels", "statsmodels_glm", "glm", "sklearn", "scikit-learn", "scikit_learn"]


def _validate_binary_outcome(y: np.ndarray) -> None:
    """Validate binary outcome values."""
    values = set(np.unique(y[~pd.isna(y)]).tolist())

    if not values.issubset({0, 1, 0.0, 1.0, False, True}):
        raise ValueError("y must be binary with values 0/1.")


class QAPLogit:
    """Logistic regression with QAP node-label permutations.

    Parameters
    ----------
    n_permutations:
        Number of node-label permutations used for empirical QAP p-values.
    random_state:
        Optional random seed for reproducible permutations.
    directed:
        If ``True``, all off-diagonal ordered dyads are used. If ``False``, only
        the upper triangle is used.
    include_diagonal:
        Whether to include self-dyads.
    two_tailed:
        Whether to compute two-tailed empirical p-values.
    backend:
        Logistic-regression backend. Use ``"statsmodels"`` for richer
        diagnostics or ``"sklearn"`` for a faster regularized backend.
    maxiter:
        Maximum number of iterations for the logistic backend.
    sklearn_C:
        Inverse regularization strength for the scikit-learn backend.

    Notes
    -----
    This is an initial QAP logistic model for binary dyadic outcomes. It uses a
    logistic-regression backend for observed coefficients and repeated
    node-label permutations of the outcome matrix for QAP empirical p-values.

    Backend p-values are diagnostic only. QAP p-values are the primary
    permutation-based inference output.
    """

    def __init__(
            self,
            *,
            n_permutations: int = 999,
            random_state: int | None = None,
            directed: bool = True,
            include_diagonal: bool = False,
            two_tailed: bool = True,
            backend: QAPLogitBackend = "statsmodels",
            maxiter: int = 100,
            sklearn_C: float = 1.0,
        ) -> None:
        if n_permutations < 0:
            raise ValueError("n_permutations must be non-negative.")

        if sklearn_C <= 0:
            raise ValueError("sklearn_C must be positive.")

        # Validate early so configuration errors fail before fitting.
        fit_logit_backend.__annotations__

        normalized_backend = backend.lower()
        allowed = {
            "statsmodels",
            "statsmodels_glm",
            "glm",
            "sklearn",
            "scikit-learn",
            "scikit_learn",
        }
        if normalized_backend not in allowed:
            raise ValueError(
                "backend must be one of: 'statsmodels', 'statsmodels_glm', "
                "'glm', 'sklearn', 'scikit-learn', or 'scikit_learn'."
            )

        self.n_permutations = n_permutations
        self.random_state = random_state
        self.directed = directed
        self.include_diagonal = include_diagonal
        self.two_tailed = two_tailed
        self.backend = backend
        self.maxiter = maxiter
        self.sklearn_C = sklearn_C

    def fit(
        self,
        y: np.ndarray,
        x_matrices: Mapping[str, np.ndarray],
    ) -> QAPLogitResult:
        """Fit the QAP logistic model."""
        y = np.asarray(y)

        if y.ndim != 2 or y.shape[0] != y.shape[1]:
            raise ValueError("y must be a square 2D matrix.")

        _validate_binary_outcome(y)

        frame = dyad_frame(
            y,
            x_matrices,
            directed=self.directed,
            include_diagonal=self.include_diagonal,
        )

        x_columns = [
            column
            for column in frame.columns
            if column not in {"source", "target", "y"}
        ]

        backend_result = fit_logit_backend(
            frame["y"].to_numpy(),
            frame[x_columns],
            backend=self.backend,
            add_intercept=True,
            maxiter=self.maxiter,
            sklearn_C=self.sklearn_C,
            random_state=self.random_state,
        )

        permutations = generate_permutations(
            y.shape[0],
            self.n_permutations,
            random_state=self.random_state,
        )

        permutation_rows: list[pd.Series] = []

        for permutation in permutations:
            permuted_y = permute_square_matrix(y, permutation)

            permuted_frame = dyad_frame(
                permuted_y,
                x_matrices,
                directed=self.directed,
                include_diagonal=self.include_diagonal,
            )

            try:
                permuted_result = fit_logit_backend(
                    permuted_frame["y"].to_numpy(),
                    permuted_frame[x_columns],
                    backend=self.backend,
                    add_intercept=True,
                    maxiter=self.maxiter,
                    sklearn_C=self.sklearn_C,
                    random_state=self.random_state,
                )
                permutation_rows.append(permuted_result.coefficients)
            except Exception:
                permutation_rows.append(
                    pd.Series(np.nan, index=backend_result.coefficients.index)
                )

        permutation_statistics = pd.DataFrame(permutation_rows)

        qap_p_values = empirical_p_values(
            backend_result.coefficients,
            permutation_statistics,
            two_tailed=self.two_tailed,
        )

        result = QAPLogitResult(
            coefficients_=backend_result.coefficients,
            standard_errors_=backend_result.standard_errors,
            z_values_=backend_result.z_values,
            p_values_=backend_result.p_values,
            qap_p_values_=qap_p_values,
            permutation_statistics_=permutation_statistics,
            n_permutations_=self.n_permutations,
            n_dyads_=len(frame),
            directed_=self.directed,
            include_diagonal_=self.include_diagonal,
            backend_=backend_result.backend,
        )

        self.result_ = result
        self.dyad_frame_ = frame

        return result

    def fit_dataframe(
            self,
            y: np.ndarray,
            x_matrices: Mapping[str, np.ndarray],
        ) -> pd.DataFrame:
        """Fit the model and return the result table."""
        return self.fit(y, x_matrices).to_dataframe()
