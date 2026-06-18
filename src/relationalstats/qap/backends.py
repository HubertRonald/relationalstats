"""Backend estimators for QAP models."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
import statsmodels.api as sm


@dataclass(slots=True)
class LogitBackendResult:
    """Container for fitted logistic-regression backend outputs."""

    coefficients: pd.Series
    standard_errors: pd.Series
    z_values: pd.Series
    p_values: pd.Series


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
    )
