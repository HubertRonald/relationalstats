"""Full link prediction metric computation."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass

import networkx as nx
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, diags
from scipy.sparse.csgraph import shortest_path

from .metrics import ALL_METRICS, LOCAL_A2_METRICS, safe_divide, validate_metrics
from .random_walk import random_walk_with_restart_matrix
from .results import ProxFunResult
from .spectral import average_commute_time_scores, katz_matrix


def _validate_graph(G: nx.Graph | nx.DiGraph) -> None:
    """Validate an input graph."""
    if not isinstance(G, (nx.Graph, nx.DiGraph)):
        raise TypeError("G must be a networkx Graph or DiGraph.")

    if G.number_of_nodes() == 0:
        raise ValueError("G must contain at least one node.")


def _default_pairs(
    G: nx.Graph | nx.DiGraph,
    *,
    directed: bool,
) -> list[tuple[object, object]]:
    """Return default node pairs to score."""
    nodes = list(G.nodes())

    if directed:
        return [
            (u, v)
            for u in nodes
            for v in nodes
            if u != v and not G.has_edge(u, v)
        ]

    G_undirected = G.to_undirected()

    return list(nx.non_edges(G_undirected))


def _prepare_pairs(
    G: nx.Graph | nx.DiGraph,
    pairs: Iterable[tuple[object, object]] | None,
    *,
    directed: bool,
) -> list[tuple[object, object]]:
    """Validate and materialize node pairs."""
    if pairs is None:
        return _default_pairs(G, directed=directed)

    prepared = list(pairs)

    if not prepared:
        return []

    nodes = set(G.nodes())
    missing_nodes = sorted(
        {node for pair in prepared for node in pair if node not in nodes},
        key=str,
    )

    if missing_nodes:
        raise ValueError(f"Pairs contain nodes not present in G: {missing_nodes}")

    return prepared


def _graph_for_scoring(
    G: nx.Graph | nx.DiGraph,
    *,
    directed: bool,
) -> nx.Graph | nx.DiGraph:
    """Return the graph representation used for scoring."""
    if directed:
        return G.copy()

    return G.to_undirected()


def proxfun_full(
    G: nx.Graph | nx.DiGraph,
    pairs: Iterable[tuple[object, object]] | None = None,
    metrics: Sequence[str] | None = None,
    *,
    directed: bool = False,
    return_dataframe: bool = True,
    beta_local_path: float = 0.01,
    beta_katz: float = 0.005,
    rwr_alpha: float = 0.15,
) -> pd.DataFrame | dict[str, np.ndarray]:
    """Compute link prediction scores for selected node pairs."""
    _validate_graph(G)

    selected_metrics = validate_metrics(metrics)
    H = _graph_for_scoring(G, directed=directed)
    selected_pairs = _prepare_pairs(H, pairs, directed=directed)

    df = pd.DataFrame(selected_pairs, columns=["source", "target"])

    if df.empty:
        if return_dataframe:
            return df

        return {"source": np.array([]), "target": np.array([])}

    nodes = list(H.nodes())
    node_to_idx = {node: idx for idx, node in enumerate(nodes)}

    source_indices = df["source"].map(node_to_idx).to_numpy()
    target_indices = df["target"].map(node_to_idx).to_numpy()

    adjacency = nx.to_scipy_sparse_array(
        H,
        nodelist=nodes,
        format="csr",
        dtype=float,
    )
    adjacency = csr_matrix(adjacency)

    degree = np.asarray(adjacency.sum(axis=1)).ravel()

    adjacency_squared = None
    common_neighbors = None

    if any(metric in selected_metrics for metric in LOCAL_A2_METRICS):
        adjacency_squared = adjacency @ adjacency
        common_neighbors = np.asarray(
            adjacency_squared[source_indices, target_indices]
        ).ravel()

    if "common_neighbors" in selected_metrics:
        df["common_neighbors"] = common_neighbors

    if "degree" in selected_metrics:
        df["degree_source"] = degree[source_indices]
        df["degree_target"] = degree[target_indices]

    if "jaccard" in selected_metrics:
        union = degree[source_indices] + degree[target_indices] - common_neighbors
        df["jaccard"] = safe_divide(common_neighbors, union)

    if "adamic_adar" in selected_metrics:
        weights = np.zeros_like(degree, dtype=float)
        mask = degree > 1
        weights[mask] = 1.0 / np.log(degree[mask])

        adamic_adar_matrix = adjacency @ diags(weights) @ adjacency
        df["adamic_adar"] = np.asarray(
            adamic_adar_matrix[source_indices, target_indices]
        ).ravel()

    if "resource_allocation" in selected_metrics:
        weights = np.zeros_like(degree, dtype=float)
        mask = degree > 0
        weights[mask] = 1.0 / degree[mask]

        resource_allocation_matrix = adjacency @ diags(weights) @ adjacency
        df["resource_allocation"] = np.asarray(
            resource_allocation_matrix[source_indices, target_indices]
        ).ravel()

    if "preferential_attachment" in selected_metrics:
        df["preferential_attachment"] = (
            degree[source_indices] * degree[target_indices]
        )

    if "salton" in selected_metrics:
        denominator = np.sqrt(degree[source_indices] * degree[target_indices])
        df["salton"] = safe_divide(common_neighbors, denominator)

    if "sorensen" in selected_metrics:
        denominator = degree[source_indices] + degree[target_indices]
        df["sorensen"] = safe_divide(2.0 * common_neighbors, denominator)

    if "hub_promoted" in selected_metrics:
        denominator = np.minimum(degree[source_indices], degree[target_indices])
        df["hub_promoted"] = safe_divide(common_neighbors, denominator)

    if "hub_depressed" in selected_metrics:
        denominator = np.maximum(degree[source_indices], degree[target_indices])
        df["hub_depressed"] = safe_divide(common_neighbors, denominator)

    if "lhn_local" in selected_metrics:
        denominator = degree[source_indices] * degree[target_indices]
        df["lhn_local"] = safe_divide(common_neighbors, denominator)

    if "shortest_path" in selected_metrics:
        distance_matrix = shortest_path(
            adjacency,
            directed=directed,
            unweighted=True,
        )
        df["shortest_path"] = distance_matrix[source_indices, target_indices]

    if "local_path" in selected_metrics:
        if adjacency_squared is None:
            adjacency_squared = adjacency @ adjacency

        adjacency_cubed = adjacency_squared @ adjacency
        local_path_matrix = adjacency_squared + beta_local_path * adjacency_cubed

        df["local_path"] = np.asarray(
            local_path_matrix[source_indices, target_indices]
        ).ravel()

    if "katz" in selected_metrics:
        matrix = katz_matrix(adjacency, beta=beta_katz)
        df["katz"] = np.asarray(matrix[source_indices, target_indices]).ravel()

    if "rwr" in selected_metrics:
        matrix = random_walk_with_restart_matrix(
            adjacency,
            degree,
            alpha=rwr_alpha,
        )
        df["rwr"] = np.asarray(matrix[source_indices, target_indices]).ravel()

    if "act" in selected_metrics:
        df["act"] = average_commute_time_scores(
            H,
            nodes=nodes,
            pairs=selected_pairs,
            source_indices=source_indices,
            target_indices=target_indices,
        )

    if return_dataframe:
        return df

    return {column: df[column].to_numpy() for column in df.columns}


@dataclass
class ProxFun:
    """Estimator-style interface for link prediction scores."""

    metrics: Sequence[str] | None = None
    directed: bool = False
    beta_local_path: float = 0.01
    beta_katz: float = 0.005
    rwr_alpha: float = 0.15

    def fit(
        self,
        G: nx.Graph | nx.DiGraph,
        pairs: Iterable[tuple[object, object]] | None = None,
    ) -> ProxFunResult:
        """Fit the estimator-style scorer and return a result object."""
        scores = proxfun_full(
            G,
            pairs=pairs,
            metrics=self.metrics,
            directed=self.directed,
            return_dataframe=True,
            beta_local_path=self.beta_local_path,
            beta_katz=self.beta_katz,
            rwr_alpha=self.rwr_alpha,
        )

        return ProxFunResult(
            scores_=scores,
            metrics_=(
                list(self.metrics)
                if self.metrics is not None
                else list(ALL_METRICS)
            ),
            directed_=self.directed,
        )

    def fit_transform(
        self,
        G: nx.Graph | nx.DiGraph,
        pairs: Iterable[tuple[object, object]] | None = None,
    ) -> pd.DataFrame:
        """Fit the scorer and return scores as a DataFrame."""
        return self.fit(G, pairs=pairs).to_dataframe()
