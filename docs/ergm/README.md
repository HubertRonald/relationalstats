# ERGM approximation

The `relationalstats.ergm` module provides an initial ERGM-inspired
dyadic-logistic approximation.

It is not a full MCMC-MLE implementation equivalent to R `ergm`.

## Public API

```python
from relationalstats.datasets import make_florentine_like_graph
from relationalstats.ergm import ERGM

G = make_florentine_like_graph()

result = ERGM(
    terms=["edges", "common_neighbors", "degree1", "gwesp", "nodematch:faction"],
    backend="sklearn",
    random_state=42,
).fit(G)

result.to_dataframe()
gof = result.gof(n_sim=100, seed=123)
```

## Documentation

- [Terms](terms.md)
- [GOF](gof.md)
- [Limitations](limitations.md)
- [Validation against R](validation-against-r.md)
