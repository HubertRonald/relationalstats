"""Network statistics for the initial ERGM approximation."""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence

import networkx as nx
import numpy as np
import pandas as pd

from relationalstats.modules.converters import graph_to_dyad_frame
from relationalstats.modules.validation import validate_graph

from .terms import is_nodematch_term, validate_terms


def count_common_neighbors(graph: nx.Graph | nx.DiGraph, u: object, v: object) -> int:
    """Return the number of common neighbors for a node pair."""
    undirected = graph.to_undirected()
    return len(list(nx.common_neighbors(undirected, u, v)))


def has_degree_one(graph: nx.Graph | nx.DiGraph, u: object, v: object) -> int:
    """Return 1 when either endpoint has degree one."""
    undirected = graph.to_undirected()
    return int(undirected.degree(u) == 1 or undirected.degree(v) == 1)


def nodematch(graph: nx.Graph | nx.DiGraph, u: object, v: object, attr: str) -> int:
    """Return 1 when both nodes share the same non-missing attribute value."""
    value_u = graph.nodes[u].get(attr)
    value_v = graph.nodes[v].get(attr)
    return int(value_u is not None and value_u == value_v)


def gwesp_approx(common_neighbors: int, *, alpha: float = 0.5) -> float:
    """Return a simple geometrically weighted shared-partner approximation."""
    if common_neighbors <= 0:
        return 0.0
    return float(1.0 - (1.0 - np.exp(-alpha)) ** common_neighbors)


def build_ergm_feature_frame(
        graph: nx.Graph | nx.DiGraph,
        *,
        terms: Sequence[str] | None = None,
        directed: bool | None = None,
        include_diagonal: bool = False,
    ) -> pd.DataFrame:
    """Build dyad-level outcome and feature columns for the ERGM approximation."""
    validate_graph(graph)
    selected_terms = validate_terms(list(terms) if terms is not None else None)
    frame = graph_to_dyad_frame(
        graph,
        directed=directed,
        include_diagonal=include_diagonal,
        outcome_col="edge",
    )

    for term in selected_terms:
        if term == "edges":
            frame["edges"] = 1.0
        elif term in {"common_neighbors", "transitiveties"}:
            frame[term] = [
                count_common_neighbors(graph, u, v)
                for u, v in zip(frame["source"], frame["target"], strict=True)
            ]
        elif term == "degree1":
            frame[term] = [
                has_degree_one(graph, u, v)
                for u, v in zip(frame["source"], frame["target"], strict=True)
            ]
        elif term == "gwesp":
            common = [
                count_common_neighbors(graph, u, v)
                for u, v in zip(frame["source"], frame["target"], strict=True)
            ]
            frame[term] = [gwesp_approx(value) for value in common]
        elif is_nodematch_term(term):
            attr = term.split(":", 1)[1]
            frame[term] = [
                nodematch(graph, u, v, attr)
                for u, v in zip(frame["source"], frame["target"], strict=True)
            ]

    return frame


def edgewise_shared_partners(graph: nx.Graph | nx.DiGraph) -> list[int]:
    """Return edge-wise shared partner counts."""
    undirected = graph.to_undirected()
    values = [
        count_common_neighbors(undirected, u, v)
        for u, v in undirected.edges()
    ]
    return values if values else [0]


def geodesic_distance_distribution(graph: nx.Graph | nx.DiGraph) -> dict[str, int]:
    """Return geodesic distance counts with `NR` for unreachable pairs."""
    undirected = graph.to_undirected()
    nodes = list(undirected.nodes())
    path_lengths = dict(nx.all_pairs_shortest_path_length(undirected))
    counts: Counter[str] = Counter()

    for i, u in enumerate(nodes):
        for v in nodes[i + 1:]:
            distance = path_lengths.get(u, {}).get(v)
            counts["NR" if distance is None else str(distance)] += 1

    return dict(counts)


def network_gof_statistics(graph: nx.Graph | nx.DiGraph) -> dict[str, object]:
    """Return GOF-style network statistics."""
    validate_graph(graph)
    undirected = graph.to_undirected()
    degrees = [degree for _, degree in undirected.degree()]
    return {
        "edges": graph.number_of_edges(),
        "density": nx.density(graph),
        "avg_degree": float(np.mean(degrees)) if degrees else 0.0,
        "degree_dist": degrees,
        "ewsp": edgewise_shared_partners(undirected),
        "triangles": int(sum(nx.triangles(undirected).values()) // 3),
        "geodesic": geodesic_distance_distribution(undirected),
    }
