"""Backend estimators for QAP models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression


BackendName = Literal["statsmodels", "statsmodels_glm", "glm", "sklearn", "scikit-learn", "scikit_learn"]


@dataclass(slots=True)
class LogitBackendResult:
    """Container for fitted logistic-regression backend outputs."""

    coefficients: pd.Series
    standard_errors: pd.Series
    z_values: pd.Series
    p_values: pd.Series
    backend: str


def _nan_diagnostics(index: pd.Index) -> pd.Series:
    """Return a NaN-valued diagnostic series for backends without inference."""
    return pd.Series(np.nan, index=index, dtype=float)


def fit_logit_glm(
        y: np.ndarray | pd.Series,
        X: pd.DataFrame,
        *,
        add_intercept: bool = True,
        maxiter: int = 100,
    ) -> LogitBackendResult:
    """Fit a binomial GLM used by the QAP logistic model.

    Parameters
    ----------
    y:
        Binary outcome vector.
    X:
        Predictor DataFrame.
    add_intercept:
        Whether to prepend an intercept column.
    maxiter:
        Maximum number of iterations for the GLM optimizer.

    Notes
    -----
    The QAP layer supplies permutation-based p-values. The backend p-values are
    retained as model diagnostics, but should not be interpreted as QAP-adjusted
    inference.
    """
    y_array = np.asarray(y, dtype=float)

    if add_intercept:
        design = X.copy()
        design.insert(0, "intercept", 1.0)
    else:
        design = X.copy()

    model = sm.GLM(
        y_array,
        design.astype(float),
        family=sm.families.Binomial(),
    )
    fitted = model.fit(maxiter=maxiter)

    return LogitBackendResult(
        coefficients=fitted.params,
        standard_errors=fitted.bse,
        z_values=fitted.tvalues,
        p_values=fitted.pvalues,
        backend="statsmodels_glm",
    )


def fit_logit_sklearn(
        y: np.ndarray | pd.Series,
        X: pd.DataFrame,
        *,
        add_intercept: bool = True,
        maxiter: int = 100,
        C: float = 1.0,
        random_state: int | None = None,
    ) -> LogitBackendResult:
    """Fit a scikit-learn logistic-regression backend.

    This backend is useful for faster QAP permutation workflows. It does not
    provide standard errors, z-values, or model-based p-values, so those
    diagnostics are returned as NaN.

    Parameters
    ----------
    y:
        Binary outcome vector.
    X:
        Predictor DataFrame.
    add_intercept:
        Whether to include an intercept through scikit-learn.
    maxiter:
        Maximum number of iterations for the solver.
    C:
        Inverse regularization strength used by scikit-learn.
    random_state:
        Optional random seed passed to the estimator.
    """
    y_array = np.asarray(y, dtype=int)
    design = X.astype(float)

    model = LogisticRegression(
        C=C,
        fit_intercept=add_intercept,
        max_iter=maxiter,
        random_state=random_state,
        solver="lbfgs",
    )
    model.fit(design, y_array)

    if add_intercept:
        index = pd.Index(["intercept", *design.columns])
        values = np.concatenate([model.intercept_, model.coef_.ravel()])
    else:
        index = pd.Index(list(design.columns))
        values = model.coef_.ravel()

    coefficients = pd.Series(values, index=index, dtype=float)

    return LogitBackendResult(
        coefficients=coefficients,
        standard_errors=_nan_diagnostics(coefficients.index),
        z_values=_nan_diagnostics(coefficients.index),
        p_values=_nan_diagnostics(coefficients.index),
        backend="sklearn",
    )


def fit_logit_backend(
        y: np.ndarray | pd.Series,
        X: pd.DataFrame,
        *,
        backend: BackendName = "statsmodels",
        add_intercept: bool = True,
        maxiter: int = 100,
        sklearn_C: float = 1.0,
        random_state: int | None = None,
    ) -> LogitBackendResult:
    """Fit a logistic-regression backend by name."""
    normalized_backend = backend.lower()

    if normalized_backend in {"statsmodels", "statsmodels_glm", "glm"}:
        return fit_logit_glm(
            y,
            X,
            add_intercept=add_intercept,
            maxiter=maxiter,
        )

    if normalized_backend in {"sklearn", "scikit-learn", "scikit_learn"}:
        return fit_logit_sklearn(
            y,
            X,
            add_intercept=add_intercept,
            maxiter=maxiter,
            C=sklearn_C,
            random_state=random_state,
        )

    raise ValueError(
        "backend must be one of: 'statsmodels', 'statsmodels_glm', 'glm', "
        "'sklearn', 'scikit-learn', or 'scikit_learn'."
    )
