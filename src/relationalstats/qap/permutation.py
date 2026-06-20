"""Permutation utilities for QAP models."""

from __future__ import annotations

from collections.abc import Mapping

import numpy as np
import pandas as pd


def permute_square_matrix(
        matrix: np.ndarray,
        permutation: np.ndarray,
    ) -> np.ndarray:
    """Permute rows and columns of a square matrix using the same node order."""
    matrix = np.asarray(matrix)

    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("matrix must be a square 2D array.")

    permutation = np.asarray(permutation)

    if sorted(permutation.tolist()) != list(range(matrix.shape[0])):
        raise ValueError("permutation must contain each node index exactly once.")

    return matrix[np.ix_(permutation, permutation)]


def generate_permutations(
        n_nodes: int,
        n_permutations: int,
        *,
        random_state: int | None = None,
    ) -> list[np.ndarray]:
    """Generate random node-label permutations."""
    if n_nodes <= 0:
        raise ValueError("n_nodes must be positive.")

    if n_permutations < 0:
        raise ValueError("n_permutations must be non-negative.")

    rng = np.random.default_rng(random_state)

    return [rng.permutation(n_nodes) for _ in range(n_permutations)]


def dyad_frame(
        y: np.ndarray,
        x_matrices: Mapping[str, np.ndarray],
        *,
        directed: bool = True,
        include_diagonal: bool = False,
    ) -> pd.DataFrame:
    """Build a dyad-level DataFrame from an outcome matrix and predictors."""
    y = np.asarray(y)

    if y.ndim != 2 or y.shape[0] != y.shape[1]:
        raise ValueError("y must be a square 2D matrix.")

    if not x_matrices:
        raise ValueError("x_matrices must contain at least one predictor matrix.")

    n_nodes = y.shape[0]

    for name, matrix in x_matrices.items():
        if name in {"y", "intercept"}:
            raise ValueError(f"'{name}' is a reserved column name.")

        matrix = np.asarray(matrix)

        if matrix.shape != y.shape:
            raise ValueError(
                f"Predictor matrix '{name}' must have shape {y.shape}; "
                f"got {matrix.shape}."
            )

    if directed:
        rows, cols = np.where(np.ones_like(y, dtype=bool))
        if not include_diagonal:
            mask = rows != cols
            rows = rows[mask]
            cols = cols[mask]
    else:
        k = 0 if include_diagonal else 1
        rows, cols = np.triu_indices(n_nodes, k=k)

    data: dict[str, np.ndarray] = {
        "source": rows,
        "target": cols,
        "y": y[rows, cols],
    }

    for name, matrix in x_matrices.items():
        matrix = np.asarray(matrix)
        data[name] = matrix[rows, cols]

    return pd.DataFrame(data)


def empirical_p_values(
        observed: pd.Series,
        permutation_statistics: pd.DataFrame,
        *,
        two_tailed: bool = True,
    ) -> pd.Series:
    """Compute plus-one empirical QAP p-values.

    The plus-one correction avoids returning zero p-values when the number of
    permutations is finite.
    """
    p_values: dict[str, float] = {}

    for name, observed_value in observed.items():
        if name not in permutation_statistics:
            p_values[name] = np.nan
            continue

        values = permutation_statistics[name].dropna().to_numpy(dtype=float)

        if values.size == 0:
            p_values[name] = np.nan
            continue

        if two_tailed:
            count = np.sum(np.abs(values) >= abs(float(observed_value)))
        else:
            count = np.sum(values >= float(observed_value))

        p_values[name] = (count + 1.0) / (values.size + 1.0)

    return pd.Series(p_values, name="qap_p_value")
