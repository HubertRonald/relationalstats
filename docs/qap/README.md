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
).fit(y, x_matrices)

result.to_dataframe()
```

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
