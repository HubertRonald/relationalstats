# QAP

The `relationalstats.qap` module provides Quadratic Assignment Procedure models
for dyadic relational data.

The first implementation is `QAPLogit`, a logistic-regression model for binary
network outcomes with node-label permutations.

## Public API

```python
from relationalstats.qap import QAPLogit
```

Example:

```python
from relationalstats.datasets import make_qap_toy_data
from relationalstats.qap import QAPLogit

y, x_matrices = make_qap_toy_data()

result = QAPLogit(
    n_permutations=99,
    random_state=42,
    directed=True,
    backend="statsmodels",
).fit(y, x_matrices)

result.to_dataframe()
```

## Backend options

`QAPLogit` supports two logistic-regression backends.

| Backend | Use case | Diagnostics |
|---|---|---|
| `statsmodels` | Default backend for richer model diagnostics | coefficients, standard errors, z-values, backend p-values |
| `sklearn` | Faster regularized backend for larger permutation workflows | coefficients only; diagnostic fields are `NaN` |

Backend p-values are retained only as diagnostics. QAP empirical p-values are
the primary permutation-based inference output.

For validation against R `sna::netlogit`, prefer the `statsmodels` backend
because it is closer to a classical logistic-regression workflow.

## Documentation

- [Formulas](formulas.md)
- [Validation against R](validation-against-r.md)

## Methodological scope

`QAPLogit` is intended for binary dyadic outcomes represented as square matrices.

The model uses:

- a logistic-regression backend for observed coefficients;
- node-label permutations of the dependent matrix;
- plus-one empirical p-values from the permutation distribution.

Backend p-values are retained as diagnostics, but QAP p-values are the primary
permutation-based inference output.
