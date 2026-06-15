from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class ProxFunResult:
    """
    Result object for link prediction scores.
    """

    scores_: pd.DataFrame
    metrics_: list[str]
    directed_: bool = False

    def to_dataframe(self) -> pd.DataFrame:
        """Return scores as a pandas DataFrame."""
        return self.scores_.copy()

    def top_k(
        self,
        k: int = 20,
        metric: str | None = None,
        ascending: bool = False,
    ) -> pd.DataFrame:
        """
        Return the top-k scored pairs for a selected metric.

        If metric is None, the first available metric column is used.
        """
        if k <= 0:
            raise ValueError("k must be a positive integer.")

        score_columns = [
            column
            for column in self.scores_.columns
            if column not in {"source", "target"}
        ]

        if not score_columns:
            raise ValueError("No score columns available.")

        selected_metric = metric or score_columns[0]

        if selected_metric not in self.scores_.columns:
            raise ValueError(f"Metric '{selected_metric}' is not available in scores_.")

        return (
            self.scores_
            .sort_values(selected_metric, ascending=ascending)
            .head(k)
            .copy()
        )

    def plot_score_distribution(self, metric: str):
        """
        Plot a score distribution for one metric.

        Requires matplotlib. This dependency is intentionally imported lazily.
        """
        if metric not in self.scores_.columns:
            raise ValueError(f"Metric '{metric}' is not available in scores_.")

        import matplotlib.pyplot as plt

        ax = self.scores_[metric].plot(kind="hist", bins=30)
        ax.set_title(f"Score distribution: {metric}")
        ax.set_xlabel(metric)
        ax.set_ylabel("Frequency")
        plt.tight_layout()
        return ax
