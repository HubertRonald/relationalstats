from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass

import networkx as nx
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, diags, eye
from scipy.sparse.csgraph import shortest_path
from scipy.sparse.linalg import inv

from .results import ProxFunResult


ALL_METRICS: list[str] = [
    "common_neighbors",
    "jaccard",
    "adamic_adar",
    "preferential_attachment",
    "resource_allocation",
    "salton",
    "sorensen",
    "hub_promoted",
    "hub_depressed",
    "lhn_local",
    "shortest_path",
    "local_path",
    "katz",
    "rwr",
    "degree",
    "act",
]


LOCAL_A2_METRICS: set[str] = {
    "common_neighbors",
    "jaccard",
    "salton",
    "sorensen",
    "hub_promoted",
    "hub_depressed",
    "lhn_local",
    "local_path",
}


GLOBAL_METRICS: set[str] = {
    "katz",
    "rwr",
    "act",
}


def _validate_graph(G: nx.Graph | nx.DiGraph) -> None:
    if not isinstance(G, (nx.Graph, nx.DiGraph)):
        raise TypeError("G must be a networkx Graph or DiGraph.")

    if G.number_of_nodes() == 0:
        raise ValueError("G must contain at least one node.")


def _validate_metrics(metrics: Sequence[str]) -> list[str]:
    unknown = sorted(set(metrics) - set(ALL_METRICS))
    if unknown:
        raise ValueError(
            "Unknown link prediction metric(s): "
            + ", ".join(unknown)
            + f". Supported metrics are: {', '.join(ALL_METRICS)}."
        )

    return list(metrics)


def _safe_divide(numerator: np.ndarray, denominator: np.ndarray) -> np.ndarray:
    numerator = np.asarray(numerator, dtype=float)
    denominator = np.asarray(denominator, dtype=float)
    out = np.zeros_like(numerator, dtype=float)
    return np.divide(numerator, denominator, out=out, where=denominator > 0)


def _default_pairs(
    G: nx.Graph | nx.DiGraph,
    *,
    directed: bool,
) -> list[tuple[object, object]]:
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
    if pairs is None:
        return _default_pairs(G, directed=directed)

    prepared = list(pairs)

    if not prepared:
        return []

    nodes = set(G.nodes())
    missing_nodes = sorted(
        {
            node
            for pair in prepared
            for node in pair
            if node not in nodes
        },
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
    """
    Compute link prediction scores for selected node pairs.

    Parameters
    ----------
    G:
        Input networkx graph.
    pairs:
        Node pairs to score. If None, scores are computed for non-existing edges.
    metrics:
        Metrics to compute. If None, all supported metrics are used.
    directed:
        If False, scoring is performed on an undirected version of the graph.
        If True, the adjacency matrix preserves edge direction.
    return_dataframe:
        If True, return a pandas DataFrame with source, target and score columns.
        If False, return a dictionary of arrays.
    beta_local_path:
        Beta parameter for the local path index.
    beta_katz:
        Beta parameter for the Katz index.
    rwr_alpha:
        Restart probability for random walk with restart.

    Notes
    -----
    Katz, RWR and ACT are global matrix-based metrics and may be expensive
    for large networks.
    """
    _validate_graph(G)

    if metrics is None:
        metrics = ALL_METRICS

    metrics = _validate_metrics(metrics)

    H = _graph_for_scoring(G, directed=directed)
    selected_pairs = _prepare_pairs(H, pairs, directed=directed)

    df = pd.DataFrame(selected_pairs, columns=["source", "target"])

    if df.empty:
        return df if return_dataframe else {"source": np.array([]), "target": np.array([])}

    nodes = list(H.nodes())
    node_to_idx = {node: idx for idx, node in enumerate(nodes)}
    n = len(nodes)

    u_idx = df["source"].map(node_to_idx).to_numpy()
    v_idx = df["target"].map(node_to_idx).to_numpy()

    A = nx.to_scipy_sparse_array(H, nodelist=nodes, format="csr", dtype=float)
    A = csr_matrix(A)

    deg = np.asarray(A.sum(axis=1)).ravel()
    deg_safe = deg.copy()
    deg_safe[deg_safe == 0] = 1.0

    A2 = None
    cn = None

    if any(metric in metrics for metric in LOCAL_A2_METRICS):
        A2 = A @ A
        cn = np.asarray(A2[u_idx, v_idx]).ravel()

    if "common_neighbors" in metrics:
        df["common_neighbors"] = cn

    if "degree" in metrics:
        df["degree_source"] = deg[u_idx]
        df["degree_target"] = deg[v_idx]

    if "jaccard" in metrics:
        union = deg[u_idx] + deg[v_idx] - cn
        df["jaccard"] = _safe_divide(cn, union)

    if "adamic_adar" in metrics:
        weights = np.zeros_like(deg, dtype=float)
        mask = deg > 1
        weights[mask] = 1.0 / np.log(deg[mask])

        aa_matrix = A @ diags(weights) @ A
        df["adamic_adar"] = np.asarray(aa_matrix[u_idx, v_idx]).ravel()

    if "resource_allocation" in metrics:
        weights = np.zeros_like(deg, dtype=float)
        mask = deg > 0
        weights[mask] = 1.0 / deg[mask]

        ra_matrix = A @ diags(weights) @ A
        df["resource_allocation"] = np.asarray(ra_matrix[u_idx, v_idx]).ravel()

    if "preferential_attachment" in metrics:
        df["preferential_attachment"] = deg[u_idx] * deg[v_idx]

    if "salton" in metrics:
        denominator = np.sqrt(deg[u_idx] * deg[v_idx])
        df["salton"] = _safe_divide(cn, denominator)

    if "sorensen" in metrics:
        denominator = deg[u_idx] + deg[v_idx]
        df["sorensen"] = _safe_divide(2.0 * cn, denominator)

    if "hub_promoted" in metrics:
        denominator = np.minimum(deg[u_idx], deg[v_idx])
        df["hub_promoted"] = _safe_divide(cn, denominator)

    if "hub_depressed" in metrics:
        denominator = np.maximum(deg[u_idx], deg[v_idx])
        df["hub_depressed"] = _safe_divide(cn, denominator)

    if "lhn_local" in metrics:
        denominator = deg[u_idx] * deg[v_idx]
        df["lhn_local"] = _safe_divide(cn, denominator)

    if "shortest_path" in metrics:
        dist_matrix = shortest_path(A, directed=directed, unweighted=True)
        df["shortest_path"] = dist_matrix[u_idx, v_idx]

    if "local_path" in metrics:
        if A2 is None:
            A2 = A @ A
        A3 = A2 @ A
        local_path_matrix = A2 + beta_local_path * A3
        df["local_path"] = np.asarray(local_path_matrix[u_idx, v_idx]).ravel()

    if "katz" in metrics:
        I = eye(n, format="csr", dtype=float)
        katz_matrix = inv(I - beta_katz * A) - I
        df["katz"] = np.asarray(katz_matrix[u_idx, v_idx]).ravel()

    if "rwr" in metrics:
        row_inv_degree = np.zeros_like(deg, dtype=float)
        mask = deg > 0
        row_inv_degree[mask] = 1.0 / deg[mask]

        P = diags(row_inv_degree) @ A
        I = eye(n, format="csr", dtype=float)
        rwr_matrix = inv(I - (1.0 - rwr_alpha) * P)
        df["rwr"] = np.asarray(rwr_matrix[u_idx, v_idx]).ravel()

    if "act" in metrics:
        # ACT is computed using the Moore-Penrose pseudoinverse of the Laplacian.
        # This is dense and expensive, so it is intentionally kept explicit.
        L = nx.laplacian_matrix(H.to_undirected(), nodelist=nodes).astype(float)
        L_plus = np.linalg.pinv(L.toarray())
        volume = 2.0 * H.to_undirected().number_of_edges()

        commute = volume * (
            L_plus[u_idx, u_idx]
            + L_plus[v_idx, v_idx]
            - 2.0 * L_plus[u_idx, v_idx]
        )

        act = _safe_divide(np.ones_like(commute, dtype=float), commute)

        # For disconnected pairs, commute time is not meaningful.
        H_undirected = H.to_undirected()
        connected = np.array(
            [nx.has_path(H_undirected, u, v) for u, v in selected_pairs],
            dtype=bool,
        )
        act[~connected] = 0.0

        df["act"] = act

    if return_dataframe:
        return df

    return {column: df[column].to_numpy() for column in df.columns}


@dataclass
class ProxFun:
    """
    Estimator-style interface for link prediction scores.

    Examples
    --------
    >>> model = ProxFun(metrics=["jaccard", "adamic_adar"])
    >>> result = model.fit(G)
    >>> result.to_dataframe()
    """

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
            metrics_=list(self.metrics) if self.metrics is not None else list(ALL_METRICS),
            directed_=self.directed,
        )

    def fit_transform(
        self,
        G: nx.Graph | nx.DiGraph,
        pairs: Iterable[tuple[object, object]] | None = None,
    ) -> pd.DataFrame:
        return self.fit(G, pairs=pairs).to_dataframe()
