# proxfun_full

`proxfun_full` is an extensible Python implementation of link prediction scores
inspired by R `linkprediction::proxfun`.

It accepts a NetworkX graph and an optional list of node pairs.

If `pairs=None`, the function scores non-existing edges.

```python
from relationalstats.linkprediction import proxfun_full

scores = proxfun_full(
    G,
    pairs=None,
    metrics=["jaccard", "adamic_adar"],
)
```