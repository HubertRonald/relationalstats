# Link prediction

The `relationalstats.linkprediction` module provides link prediction metrics for
NetworkX graphs.

The first public implementation includes `proxfun_full`, an extensible Python
implementation inspired by R `linkprediction::proxfun`.

## Public API

```python
from relationalstats.linkprediction import ProxFun, proxfun_full
```

Functional API:

```python
scores = proxfun_full(
    G,
    pairs=None,
    metrics=["jaccard", "adamic_adar", "resource_allocation"],
)
```

Estimator-style API:

```python
result = ProxFun(metrics=["jaccard", "adamic_adar"]).fit(G)

result.scores_
result.to_dataframe()
result.top_k(k=20, metric="jaccard")
```

## Documentation

- [Metric formulas](metrics.md)
- [proxfun_full API notes](proxfun-full.md)
- [Scalability notes](scalability.md)
- [Validation against R](validation-against-r.md)

## Scope

This module focuses on practical link prediction metrics for small and medium
networks, with sparse matrix support for several local metrics.

Global metrics such as Katz, random walk with restart, and average commute time
may be expensive for large networks.

## Methodological note

Metric definitions can vary across packages. Validation against R
`linkprediction::proxfun` should always align:

- graph direction;
- node ordering;
- pair selection;
- zero-division behavior;
- global metric parameters;
- disconnected-pair handling.
