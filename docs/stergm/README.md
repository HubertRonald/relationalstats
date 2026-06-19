# STERGM approximation

The `relationalstats.stergm` module provides an initial separable temporal
dyadic-logistic approximation.

It is not a full MCMC-MLE implementation equivalent to R `tergm` or `stergm`.

## Public API

```python
from relationalstats.datasets import make_stergm_temporal_toy
from relationalstats.stergm import STERGM

G1, G2 = make_stergm_temporal_toy()

result = STERGM(
    formation_terms=["edges", "common_neighbors", "degree1", "gwesp"],
    dissolution_terms=["edges", "common_neighbors", "degree1", "gwesp"],
    backend="sklearn",
    random_state=42,
).fit(G1, G2)

result.to_dataframe()
simulated = result.simulate(seed=123)
```

## Documentation

- [Temporal dyads](temporal-dyads.md)
- [Limitations](limitations.md)
- [Validation against R](validation-against-r.md)
