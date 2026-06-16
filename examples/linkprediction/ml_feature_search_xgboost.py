"""
Experimental ML workflow for link prediction features.

This example keeps exploratory ML utilities outside the package core.

It demonstrates how to use `relationalstats.linkprediction.proxfun_full` as a
feature generator and then evaluate metric subsets with an optional XGBoost
classifier. Plotting and SHAP explanations are intentionally lazy imports so the
core package does not require `xgboost`, `shap`, `seaborn`, or `matplotlib`.

Install optional dependencies before running the full workflow:

    python -m pip install -e ".[ml,plot]"

This script is public-safe and synthetic. It does not depend on private
notebooks, academic assignments, or external datasets.
"""

from __future__ import annotations

import itertools
import random
from dataclasses import dataclass
from typing import Iterable, Sequence

import networkx as nx
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

from relationalstats.linkprediction import ALL_METRICS, proxfun_full


LOCAL_METRICS = [
    "common_neighbors",
    "jaccard",
    "adamic_adar",
    "resource_allocation",
    "preferential_attachment",
    "salton",
    "sorensen",
    "hub_promoted",
    "hub_depressed",
    "lhn_local",
]


@dataclass(frozen=True)
class FeatureSearchConfig:
    """Configuration for the experimental feature-search workflow."""

    min_k: int = 1
    max_k: int = 4
    test_size: float = 0.30
    random_state: int = 42


def build_synthetic_graph() -> nx.Graph:
    """Create a small graph with two weakly connected communities."""
    graph = nx.Graph()

    community_a = range(0, 8)
    community_b = range(8, 16)

    graph.add_nodes_from(community_a)
    graph.add_nodes_from(community_b)

    graph.add_edges_from(
        [
            (0, 1),
            (0, 2),
            (1, 2),
            (1, 3),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 6),
            (6, 7),
            (8, 9),
            (8, 10),
            (9, 10),
            (9, 11),
            (10, 11),
            (11, 12),
            (12, 13),
            (13, 14),
            (14, 15),
            (7, 8),
        ]
    )

    return graph


def sample_positive_pairs(
    graph: nx.Graph,
    n_samples: int,
    seed: int = 42,
) -> list[tuple[int, int]]:
    """Sample existing edges as positive examples."""
    rng = random.Random(seed)
    edges = list(graph.edges())
    return rng.sample(edges, min(n_samples, len(edges)))


def sample_negative_pairs(
    graph: nx.Graph,
    n_samples: int,
    seed: int = 123,
) -> list[tuple[int, int]]:
    """Sample non-existing edges as negative examples."""
    rng = random.Random(seed)
    non_edges = list(nx.non_edges(graph))
    return rng.sample(non_edges, min(n_samples, len(non_edges)))


def build_feature_dataset(
    graph: nx.Graph,
    metrics: Sequence[str] | None = None,
    n_positive: int = 14,
    n_negative: int = 14,
) -> pd.DataFrame:
    """Build a labeled feature dataset using `proxfun_full`."""
    selected_metrics = list(metrics or LOCAL_METRICS)

    positive_pairs = sample_positive_pairs(
        graph,
        n_samples=n_positive,
        seed=42,
    )
    negative_pairs = sample_negative_pairs(
        graph,
        n_samples=n_negative,
        seed=123,
    )

    x_pos = proxfun_full(graph, pairs=positive_pairs, metrics=selected_metrics)
    x_pos["label"] = 1

    x_neg = proxfun_full(graph, pairs=negative_pairs, metrics=selected_metrics)
    x_neg["label"] = 0

    return pd.concat([x_pos, x_neg], ignore_index=True)


def generate_metric_combinations(
    metrics: Sequence[str],
    min_k: int = 1,
    max_k: int | None = None,
) -> list[tuple[str, ...]]:
    """Generate metric combinations for experimental feature search."""
    upper = len(metrics) if max_k is None else max_k
    combinations: list[tuple[str, ...]] = []

    for k in range(min_k, upper + 1):
        combinations.extend(itertools.combinations(metrics, k))

    return combinations


def _make_classifier(random_state: int = 42, backend: str = "sklearn"):
    """Create a classifier for the experimental feature-search workflow."""
    if backend == "xgboost":
        try:
            from xgboost import XGBClassifier
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(
                "XGBoost could not be loaded. On macOS this may require "
                "the OpenMP runtime, usually `libomp.dylib`. "
                "Use backend='sklearn' for a pure scikit-learn fallback."
            ) from exc

        return XGBClassifier(
            n_estimators=300,
            max_depth=5,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="logloss",
            random_state=random_state,
        )

    from sklearn.ensemble import RandomForestClassifier

    return RandomForestClassifier(
        n_estimators=300,
        max_depth=5,
        random_state=random_state,
        class_weight="balanced",
    )


def evaluate_feature_set(
    df: pd.DataFrame,
    features: Sequence[str],
    config: FeatureSearchConfig | None = None,
):
    """Train an XGBoost model for one feature subset and return AUC + model."""
    cfg = config or FeatureSearchConfig()

    x = df[list(features)]
    y = df["label"]

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=cfg.test_size,
        stratify=y,
        random_state=cfg.random_state,
    )

    model = _make_classifier(random_state=cfg.random_state, backend="sklearn")
    model.fit(x_train, y_train)

    probabilities = model.predict_proba(x_test)[:, 1]
    auc = roc_auc_score(y_test, probabilities)

    return {
        "auc": auc,
        "model": model,
        "x_train": x_train,
        "x_test": x_test,
        "y_train": y_train,
        "y_test": y_test,
    }


def feature_search(
    df: pd.DataFrame,
    metrics: Sequence[str],
    config: FeatureSearchConfig | None = None,
) -> pd.DataFrame:
    """Evaluate metric subsets and return a ranked AUC table."""
    cfg = config or FeatureSearchConfig()
    combinations = generate_metric_combinations(metrics, cfg.min_k, cfg.max_k)
    rows = []

    for feature_set in combinations:
        try:
            result = evaluate_feature_set(df, feature_set, cfg)
            rows.append(
                {
                    "features": feature_set,
                    "n_features": len(feature_set),
                    "auc": result["auc"],
                }
            )
        except Exception as exc:  # noqa: BLE001 - experimental reporting.
            rows.append(
                {
                    "features": feature_set,
                    "n_features": len(feature_set),
                    "auc": None,
                    "error": str(exc),
                }
            )

    return pd.DataFrame(rows).sort_values("auc", ascending=False, na_position="last")


def plot_correlation_heatmap(df: pd.DataFrame, features: Sequence[str]) -> None:
    """Plot a correlation heatmap for selected link prediction features."""
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ImportError as exc:
        raise ImportError(
            "Plotting dependencies are required. "
            'Install them with: python -m pip install -e ".[plot]"'
        ) from exc

    corr = df[list(features)].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        corr,
        cmap="coolwarm",
        center=0,
        annot=True,
        fmt=".2f",
    )
    plt.title("Correlation matrix of link prediction features")
    plt.tight_layout()
    plt.show()


def plot_auc_distribution(results: pd.DataFrame) -> None:
    """Plot the distribution of AUC values from feature search."""
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ImportError as exc:
        raise ImportError(
            "Plotting dependencies are required. "
            'Install them with: python -m pip install -e ".[plot]"'
        ) from exc

    valid_results = results.dropna(subset=["auc"])

    sns.histplot(valid_results["auc"], bins=30)
    plt.title("AUC distribution by feature combination")
    plt.xlabel("ROC AUC")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()


def explain_with_shap(model, x: pd.DataFrame) -> None:
    """Create a SHAP summary plot for a fitted tree model."""
    try:
        import shap
    except ImportError as exc:
        raise ImportError(
            "SHAP is required for this explanation example. "
            'Install optional ML dependencies with: python -m pip install -e ".[ml]"'
        ) from exc

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(x)
    shap.summary_plot(shap_values, x)


def main() -> None:
    """Run the experimental feature-search workflow."""
    graph = build_synthetic_graph()
    df = build_feature_dataset(graph, metrics=LOCAL_METRICS)

    config = FeatureSearchConfig(min_k=1, max_k=3)
    results = feature_search(df, LOCAL_METRICS, config)

    print("Available metrics:")
    print(ALL_METRICS)
    print()
    print("Top feature sets:")
    print(results.head(10).to_string(index=False))

    valid_results = results.dropna(subset=["auc"])

    if valid_results.empty:
        print()
        print("No valid feature set was evaluated.")
        print("XGBoost may be missing or its native library could not be loaded.")
        print()
        print("On macOS, this commonly means the OpenMP runtime is missing.")
        print()
        print("MacPorts:")
        print("sudo port install libomp")
        print()
        print("Homebrew:")
        print("brew install libomp")
        print()
        print("Then retry:")
        print("python -c \"import xgboost; print(xgboost.__version__)\"")
        print("python examples/linkprediction/ml_feature_search_xgboost.py")
        return

    best = valid_results.iloc[0]
    best_features = list(best["features"])
    best_eval = evaluate_feature_set(df, best_features, config)

    print()
    print(f"Best features: {best_features}")
    print(f"Best AUC: {best_eval['auc']:.3f}")

    # Optional interactive/visual steps:
    # plot_correlation_heatmap(df, LOCAL_METRICS)
    # plot_auc_distribution(results)
    # explain_with_shap(best_eval["model"], best_eval["x_test"])


if __name__ == "__main__":
    main()
