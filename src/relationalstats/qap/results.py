"""Result containers for QAP models."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(slots=True)
class QAPLogitResult:
    """Result object returned by ``QAPLogit.fit``."""

    coefficients_: pd.Series
    standard_errors_: pd.Series
    z_values_: pd.Series
    p_values_: pd.Series
    qap_p_values_: pd.Series
    permutation_statistics_: pd.DataFrame
    n_permutations_: int
    n_dyads_: int
    directed_: bool
    include_diagonal_: bool
    backend_: str = "statsmodels_glm"

    def to_dataframe(self) -> pd.DataFrame:
        """Return coefficient and p-value diagnostics as a DataFrame."""
        frame = pd.DataFrame(
            {
                "coefficient": self.coefficients_,
                "std_error": self.standard_errors_,
                "z_value": self.z_values_,
                "backend_p_value": self.p_values_,
                "qap_p_value": self.qap_p_values_,
            }
        )

        frame.index.name = "term"

        return frame.reset_index()

    def permutation_frame(self) -> pd.DataFrame:
        """Return permutation coefficient statistics."""
        return self.permutation_statistics_.copy()

    def summary(self) -> str:
        """Return a compact text summary."""
        return (
            "QAPLogitResult("
            f"n_dyads={self.n_dyads_}, "
            f"n_permutations={self.n_permutations_}, "
            f"directed={self.directed_}, "
            f"backend='{self.backend_}'"
            ")"
        )
