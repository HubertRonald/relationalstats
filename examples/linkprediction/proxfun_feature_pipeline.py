"""
Synthetic link prediction feature pipeline.

This example demonstrates how to use `relationalstats.linkprediction.proxfun_full`
as a feature generator for a simple supervised link prediction workflow.

The example is intentionally synthetic and public-safe. It does not depend on
private notebooks, course assignments, or external datasets.
"""

from __future__ import annotations

import random

import networkx as nx
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

from relationalstats.linkprediction import proxfun_full


def build_synthetic_graph() -> nx.Graph:
    """Create a small graph with community-like structure."""
    graph = nx.Graph()

    community_a = range(0, 6)
    community_b = range(6, 12)

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
            (6, 7),
            (6, 8),
            (7, 8),
            (7, 9),
            (8, 9),
            (9, 10),
            (10, 11),
            (5, 6),
        ]
    )

    return graph


def sample_positive_pairs(graph: nx.Graph, n_samples: int, seed: int = 42):
    """Sample existing edges as positive examples."""
    rng = random.Random(seed)
    edges = list(graph.edges())
    return rng.sample(edges, min(n_samples, len(edges)))


def sample_negative_pairs(graph: nx.Graph, n_samples: int, seed: int = 42):
    """Sample non-existing edges as negative examples."""
    rng = random.Random(seed)
    non_edges = list(nx.non_edges(graph))
    return rng.sample(non_edges, min(n_samples, len(non_edges)))


def build_feature_dataset(graph: nx.Graph) -> pd.DataFrame:
    """Build a labeled feature dataset using proxfun_full."""
    positive_pairs = sample_positive_pairs(graph, n_samples=10, seed=42)
    negative_pairs = sample_negative_pairs(graph, n_samples=10, seed=123)

    metrics = [
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

    x_pos = proxfun_full(graph, pairs=positive_pairs, metrics=metrics)
    x_pos["label"] = 1

    x_neg = proxfun_full(graph, pairs=negative_pairs, metrics=metrics)
    x_neg["label"] = 0

    return pd.concat([x_pos, x_neg], ignore_index=True)


def main() -> None:
    """Run a small supervised link prediction example."""
    graph = build_synthetic_graph()
    data = build_feature_dataset(graph)

    feature_columns = [
        column
        for column in data.columns
        if column not in {"source", "target", "label"}
    ]

    x_train, x_test, y_train, y_test = train_test_split(
        data[feature_columns],
        data["label"],
        test_size=0.3,
        random_state=42,
        stratify=data["label"],
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(x_train, y_train)

    probabilities = model.predict_proba(x_test)[:, 1]
    auc = roc_auc_score(y_test, probabilities)

    print("Feature columns:")
    print(feature_columns)
    print()
    print(f"ROC AUC: {auc:.3f}")


if __name__ == "__main__":
    main()
