"""Result containers for link prediction workflows."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

import pandas as pd


PAIR_COLUMNS: tuple[str, str] = ("source", "target")


@dataclass(slots=True)
class ProxFunResult:
    """Container for link prediction scores produced by ``ProxFun``.

    Parameters
    ----------
    scores_:
        DataFrame containing at least ``source`` and ``target`` columns plus one
        or more score columns.
    metrics_:
        Logical metric names requested by the estimator. This field is metadata;
        concrete DataFrame columns can differ for composite metrics such as
        ``degree``, which produces ``degree_source`` and ``degree_target``.
    directed_:
        Whether the scores were computed using directed graph semantics.
    """

    scores_: pd.DataFrame
    metrics_: Sequence[str] = field(default_factory=list)
    directed_: bool = False

    def __post_init__(self) -> None:
        """Validate the result object after initialization."""
        if not isinstance(self.scores_, pd.DataFrame):
            raise TypeError("scores_ must be a pandas DataFrame.")

        missing_columns = [
            column for column in PAIR_COLUMNS if column not in self.scores_.columns
        ]
        if missing_columns:
            raise ValueError(
                "scores_ must contain pair columns: "
                + ", ".join(PAIR_COLUMNS)
                + f". Missing: {missing_columns}"
            )

        self.metrics_ = list(self.metrics_)

    def __len__(self) -> int:
        """Return the number of scored node pairs."""
        return len(self.scores_)

    @property
    def pair_columns(self) -> list[str]:
        """Return the pair-identifying columns."""
        return list(PAIR_COLUMNS)

    @property
    def score_columns(self) -> list[str]:
        """Return concrete score columns present in ``scores_``."""
        return [column for column in self.scores_.columns if column not in PAIR_COLUMNS]

    @property
    def is_empty(self) -> bool:
        """Return whether the result has no scored pairs."""
        return self.scores_.empty

    def to_dataframe(self, *, copy: bool = True) -> pd.DataFrame:
        """Return scores as a pandas DataFrame."""
        if copy:
            return self.scores_.copy()

        return self.scores_

    def pairs(self) -> pd.DataFrame:
        """Return only the scored node pairs."""
        return self.scores_.loc[:, self.pair_columns].copy()

    def metric_frame(
        self,
        metrics: Sequence[str] | None = None,
        *,
        include_pairs: bool = True,
    ) -> pd.DataFrame:
        """Return selected metric columns, optionally including pair columns."""
        selected_metrics = list(metrics) if metrics is not None else self.score_columns

        missing_metrics = [
            metric for metric in selected_metrics if metric not in self.scores_.columns
        ]
        if missing_metrics:
            raise ValueError(
                "Metric column(s) not available in scores_: "
                + ", ".join(missing_metrics)
            )

        columns = selected_metrics
        if include_pairs:
            columns = self.pair_columns + selected_metrics

        return self.scores_.loc[:, columns].copy()

    def require_metric(self, metric: str | None = None) -> str:
        """Return a valid metric column or raise a helpful error."""
        if not self.score_columns:
            raise ValueError("No score columns available.")

        selected_metric = metric or self.score_columns[0]

        if selected_metric not in self.scores_.columns:
            available = ", ".join(self.score_columns)
            raise ValueError(
                f"Metric '{selected_metric}' is not available in scores_. "
                f"Available score columns are: {available}."
            )

        return selected_metric

    def sort_by(
        self,
        metric: str | None = None,
        *,
        ascending: bool = False,
        na_position: str = "last",
    ) -> pd.DataFrame:
        """Return scores sorted by a selected metric column."""
        selected_metric = self.require_metric(metric)

        return (
            self.scores_
            .sort_values(
                selected_metric,
                ascending=ascending,
                na_position=na_position,
            )
            .copy()
        )

    def top_k(
        self,
        k: int = 20,
        metric: str | None = None,
        ascending: bool = False,
        *,
        dropna: bool = True,
    ) -> pd.DataFrame:
        """Return the top-k scored pairs for a selected metric."""
        if k <= 0:
            raise ValueError("k must be a positive integer.")

        selected_metric = self.require_metric(metric)
        scores = self.scores_

        if dropna:
            scores = scores.dropna(subset=[selected_metric])

        return (
            scores
            .sort_values(selected_metric, ascending=ascending)
            .head(k)
            .copy()
        )

    def plot_score_distribution(self, metric: str):
        """Plot a score distribution for one metric.

        Matplotlib is imported lazily so plotting remains an optional dependency.
        """
        selected_metric = self.require_metric(metric)

        import matplotlib.pyplot as plt

        ax = self.scores_[selected_metric].plot(kind="hist", bins=30)
        ax.set_title(f"Score distribution: {selected_metric}")
        ax.set_xlabel(selected_metric)
        ax.set_ylabel("Frequency")
        plt.tight_layout()

        return ax
