"""Formation-stage helpers for STERGM approximations."""

from __future__ import annotations

import pandas as pd

from relationalstats.qap.backends import fit_logit_backend

from .results import STERGMStageResult


def fit_formation_stage(
        frame: pd.DataFrame,
        *,
        terms: list[str],
        backend: str,
        maxiter: int,
        sklearn_C: float,
        random_state: int | None,
    ) -> STERGMStageResult:
    """Fit the formation stage."""
    backend_result = fit_logit_backend(
        frame["formation"].to_numpy(),
        frame[terms],
        backend=backend,
        add_intercept=False,
        maxiter=maxiter,
        sklearn_C=sklearn_C,
        random_state=random_state,
    )
    return STERGMStageResult(
        stage="formation",
        coefficients_=backend_result.coefficients,
        standard_errors_=backend_result.standard_errors,
        z_values_=backend_result.z_values,
        p_values_=backend_result.p_values,
        frame_=frame,
        outcome_="formation",
        terms_=terms,
        backend_=backend_result.backend,
    )
