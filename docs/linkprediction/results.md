# ProxFunResult

`ProxFunResult` is the result container returned by the estimator-style
`ProxFun` API.

It keeps link prediction scores in a pandas DataFrame while exposing convenience
methods for inspection, ranking, and plotting.

## Basic usage

```python
import networkx as nx

from relationalstats.linkprediction import ProxFun

G = nx.path_graph(3)

result = ProxFun(metrics=["jaccard", "adamic_adar"]).fit(G)

df = result.to_dataframe()
top_pairs = result.top_k(k=10, metric="jaccard")
```

## Stored attributes

| Attribute | Description |
|---|---|
| `scores_` | DataFrame with `source`, `target`, and score columns. |
| `metrics_` | Logical metric names requested by the estimator. |
| `directed_` | Whether directed graph semantics were used. |

## Convenience properties

```python
result.pair_columns
result.score_columns
result.is_empty
```

## DataFrame helpers

```python
result.to_dataframe()
result.pairs()
result.metric_frame(["jaccard", "adamic_adar"])
```

## Ranking helpers

By default, `top_k` assumes higher values are better:

```python
result.top_k(k=20, metric="jaccard")
```

For distance-like metrics such as `shortest_path`, use ascending ranking:

```python
result.top_k(k=20, metric="shortest_path", ascending=True)
```

## Plotting

Plotting is optional and imports `matplotlib` lazily:

```python
result.plot_score_distribution("jaccard")
```

## Notes

`metrics_` stores the logical metric request. Concrete DataFrame columns may
differ for composite metrics. For example, the `degree` metric produces:

```text
degree_source
degree_target
```

Use `result.score_columns` to inspect the actual score columns available for
ranking or export.
