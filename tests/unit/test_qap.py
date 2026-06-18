"""Unit tests for QAPLogit."""

from __future__ import annotations

import numpy as np
import pytest

from relationalstats.datasets import make_qap_toy_data
from relationalstats.qap import QAPLogit


def test_qap_logit_fits_toy_directed_data() -> None:
    y, x_matrices = make_qap_toy_data()

    result = QAPLogit(n_permutations=9, random_state=42).fit(y, x_matrices)
    frame = result.to_dataframe()

    assert result.backend_ == "statsmodels_glm"
    assert result.n_dyads_ == 20
    assert result.n_permutations_ == 9
    assert set(frame["term"]) == {"intercept", "same_group", "distance"}
    assert frame["coefficient"].notna().all()
    assert frame["qap_p_value"].between(0, 1).all()


def test_qap_logit_supports_sklearn_backend() -> None:
    y, x_matrices = make_qap_toy_data()

    result = QAPLogit(
        n_permutations=9,
        random_state=42,
        backend="sklearn",
    ).fit(y, x_matrices)
    frame = result.to_dataframe()

    assert result.backend_ == "sklearn"
    assert result.n_dyads_ == 20
    assert set(frame["term"]) == {"intercept", "same_group", "distance"}
    assert frame["coefficient"].notna().all()
    assert frame["qap_p_value"].between(0, 1).all()
    assert frame["std_error"].isna().all()
    assert frame["z_value"].isna().all()
    assert frame["backend_p_value"].isna().all()


def test_qap_logit_rejects_unknown_backend() -> None:
    with pytest.raises(ValueError, match="backend"):
        QAPLogit(backend="unknown")


def test_qap_logit_rejects_non_positive_sklearn_c() -> None:
    with pytest.raises(ValueError, match="sklearn_C"):
        QAPLogit(backend="sklearn", sklearn_C=0)


def test_qap_logit_undirected_uses_upper_triangle() -> None:
    y, x_matrices = make_qap_toy_data()

    result = QAPLogit(
        n_permutations=3,
        random_state=7,
        directed=False,
    ).fit(y, x_matrices)

    assert result.n_dyads_ == 10


def test_qap_logit_reproducible_with_same_seed() -> None:
    y, x_matrices = make_qap_toy_data()

    result_a = QAPLogit(n_permutations=7, random_state=123).fit(y, x_matrices)
    result_b = QAPLogit(n_permutations=7, random_state=123).fit(y, x_matrices)

    assert result_a.permutation_frame().equals(result_b.permutation_frame())
    assert result_a.to_dataframe().equals(result_b.to_dataframe())


def test_qap_logit_sklearn_reproducible_with_same_seed() -> None:
    y, x_matrices = make_qap_toy_data()

    result_a = QAPLogit(
        n_permutations=7,
        random_state=123,
        backend="sklearn",
    ).fit(y, x_matrices)
    result_b = QAPLogit(
        n_permutations=7,
        random_state=123,
        backend="sklearn",
    ).fit(y, x_matrices)

    assert result_a.permutation_frame().equals(result_b.permutation_frame())
    assert result_a.to_dataframe().equals(result_b.to_dataframe())


def test_qap_logit_fit_dataframe_returns_summary_table() -> None:
    y, x_matrices = make_qap_toy_data()

    frame = QAPLogit(n_permutations=5, random_state=1).fit_dataframe(y, x_matrices)

    assert {"term", "coefficient", "qap_p_value"}.issubset(frame.columns)


def test_qap_logit_rejects_non_square_outcome() -> None:
    y = np.ones((2, 3))
    x_matrices = {"x": np.ones((2, 3))}

    with pytest.raises(ValueError, match="square"):
        QAPLogit(n_permutations=0).fit(y, x_matrices)


def test_qap_logit_rejects_non_binary_outcome() -> None:
    y, x_matrices = make_qap_toy_data()
    y = y.astype(float)
    y[0, 1] = 2.0

    with pytest.raises(ValueError, match="binary"):
        QAPLogit(n_permutations=0).fit(y, x_matrices)
