"""Temporal dyad utilities for STERGM approximations."""

from __future__ import annotations

import networkx as nx
import pandas as pd

from relationalstats.ergm.statistics import count_common_neighbors, gwesp_approx, has_degree_one, nodematch
from relationalstats.modules.converters import iter_dyads
from relationalstats.modules.validation import validate_same_node_set


def build_stergm_datasets(
        graph_t1: nx.Graph | nx.DiGraph,
        graph_t2: nx.Graph | nx.DiGraph,
        *,
        directed: bool | None = None,
        include_diagonal: bool = False,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Build formation and dissolution datasets from two graph snapshots."""
    validate_same_node_set(graph_t1, graph_t2)
    if directed is None:
        directed = graph_t1.is_directed() or graph_t2.is_directed()

    rows = []
    for u, v in iter_dyads(graph_t1.nodes(), directed=directed, include_diagonal=include_diagonal):
        y_t1 = int(graph_t1.has_edge(u, v))
        y_t2 = int(graph_t2.has_edge(u, v))
        rows.append({"source": u, "target": v, "y_t1": y_t1, "y_t2": y_t2})

    frame = pd.DataFrame(rows)
    formation = frame[frame["y_t1"] == 0].copy()
    formation["formation"] = formation["y_t2"]
    dissolution = frame[frame["y_t1"] == 1].copy()
    dissolution["dissolution"] = 1 - dissolution["y_t2"]
    return formation.reset_index(drop=True), dissolution.reset_index(drop=True)


def add_temporal_structural_features(
        frame: pd.DataFrame,
        graph_base: nx.Graph | nx.DiGraph,
        *,
        terms: list[str],
    ) -> pd.DataFrame:
    """Add ERGM-inspired structural features to a temporal dyad frame."""
    out = frame.copy()
    for term in terms:
        if term == "edges":
            out["edges"] = 1.0
        elif term in {"common_neighbors", "transitiveties"}:
            out[term] = [
                count_common_neighbors(graph_base, u, v)
                for u, v in zip(out["source"], out["target"], strict=True)
            ]
        elif term == "degree1":
            out[term] = [
                has_degree_one(graph_base, u, v)
                for u, v in zip(out["source"], out["target"], strict=True)
            ]
        elif term == "gwesp":
            common = [
                count_common_neighbors(graph_base, u, v)
                for u, v in zip(out["source"], out["target"], strict=True)
            ]
            out[term] = [gwesp_approx(value) for value in common]
        elif term.startswith("nodematch:"):
            attr = term.split(":", 1)[1]
            out[term] = [
                nodematch(graph_base, u, v, attr)
                for u, v in zip(out["source"], out["target"], strict=True)
            ]
        elif term == "mutual":
            out[term] = [
                int(graph_base.has_edge(v, u))
                for u, v in zip(out["source"], out["target"], strict=True)
            ]
        else:
            raise ValueError(f"Unknown STERGM term: {term}")
    return out
