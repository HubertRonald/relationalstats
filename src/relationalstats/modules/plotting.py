"""Shared plotting helpers with lazy optional imports."""

from __future__ import annotations

import pandas as pd


def plot_gof_boxplot(
    simulations: pd.DataFrame,
    observed: pd.Series,
    *,
    title: str = "GOF summary",
):
    """Plot simulated GOF statistics with observed values overlaid."""
    import matplotlib.pyplot as plt

    ax = simulations.plot(kind="box", figsize=(10, 5), title=title)
    for idx, column in enumerate(simulations.columns, start=1):
        ax.scatter(idx, observed[column], zorder=5)
    ax.set_ylabel("Statistic value")
    plt.tight_layout()
    return ax
