"""Unit tests for QAP permutation utilities."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from relationalstats.datasets import make_qap_toy_data
from relationalstats.qap import (
    dyad_frame,
    empirical_p_values,
    generate_permutations,
    permute_square_matrix,
)


def test_permute_square_matrix_reorders_rows_and_columns() -> None:
    matrix = np.array(
        [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
        ]
    )
    permutation = np.array([2, 0, 1])

    result = permute_square_matrix(matrix, permutation)

    expected = matrix[np.ix_(permutation, permutation)]

    assert np.array_equal(result, expected)


def test_permute_square_matrix_rejects_invalid_permutation() -> None:
    matrix = np.eye(3)

    with pytest.raises(ValueError, match="permutation"):
        permute_square_matrix(matrix, np.array([0, 0, 1]))


def test_generate_permutations_is_reproducible() -> None:
    perms_a = generate_permutations(5, 3, random_state=42)
    perms_b = generate_permutations(5, 3, random_state=42)

    assert all(np.array_equal(a, b) for a, b in zip(perms_a, perms_b, strict=True))


def test_dyad_frame_directed_excludes_diagonal_by_default() -> None:
    y, x_matrices = make_qap_toy_data()

    frame = dyad_frame(y, x_matrices, directed=True)

    assert len(frame) == 20
    assert (frame["source"] != frame["target"]).all()
    assert {"source", "target", "y", "same_group", "distance"}.issubset(frame.columns)


def test_dyad_frame_undirected_uses_upper_triangle() -> None:
    y, x_matrices = make_qap_toy_data()

    frame = dyad_frame(y, x_matrices, directed=False)

    assert len(frame) == 10
    assert (frame["source"] < frame["target"]).all()


def test_dyad_frame_rejects_predictor_shape_mismatch() -> None:
    y, x_matrices = make_qap_toy_data()
    x_matrices = dict(x_matrices)
    x_matrices["bad"] = np.ones((2, 2))

    with pytest.raises(ValueError, match="shape"):
        dyad_frame(y, x_matrices)


def test_empirical_p_values_uses_plus_one_correction() -> None:
    observed = pd.Series({"x": 2.0})
    permutations = pd.DataFrame({"x": [0.0, 1.0, 2.0, 3.0]})

    p_values = empirical_p_values(observed, permutations)

    assert p_values["x"] == pytest.approx(3 / 5)
