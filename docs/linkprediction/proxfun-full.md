# proxfun_full

`proxfun_full` is an extensible Python implementation of link prediction scores
inspired by R `linkprediction::proxfun`.

It accepts a NetworkX graph and an optional list of node pairs.

If `pairs=None`, the function scores non-existing edges.

## Functional API

```python
from relationalstats.linkprediction import proxfun_full

scores = proxfun_full(
    G,
    pairs=None,
    metrics=["jaccard", "adamic_adar"],
)
```

## Parameters

| Parameter | Description |
|---|---|
| `G` | Input `networkx.Graph` or `networkx.DiGraph`. |
| `pairs` | Optional iterable of `(source, target)` pairs. If `None`, non-edges are scored. |
| `metrics` | List of metrics to compute. If `None`, all supported metrics are computed. |
| `directed` | If `False`, scoring is performed on an undirected version of the graph. |
| `return_dataframe` | If `True`, returns a `pandas.DataFrame`. |
| `beta_local_path` | Parameter $\beta$ for the local path index. |
| `beta_katz` | Parameter $\beta$ for the Katz index. |
| `rwr_alpha` | Restart probability $\alpha$ for random walk with restart. |

## Estimator-style API

```python
from relationalstats.linkprediction import ProxFun

result = ProxFun(metrics=["jaccard", "adamic_adar"]).fit(G)

df = result.to_dataframe()
top_pairs = result.top_k(k=20, metric="jaccard")
```

## Result object

`ProxFunResult` exposes:

- `scores_`
- `metrics_`
- `directed_`
- `to_dataframe()`
- `top_k()`
- `plot_score_distribution()`

## Notes

The function is designed for practical link prediction workflows. Metric
definitions can vary across software packages, so validation against R
`linkprediction::proxfun` should explicitly align graph direction, node ordering,
pair selection, and metric parameters.
