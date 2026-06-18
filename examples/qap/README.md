# QAP examples

This directory contains public-safe examples for QAP models.

Current examples:

```bash
python examples/qap/qap_logit_toy.py
python examples/qap/qap_logit_backend_comparison.py
```

The toy examples use a synthetic directed binary network and two dyadic
predictors:

- `same_group`
- `distance`

## Backend options

`QAPLogit` supports two logistic-regression backends:

- `backend="statsmodels"`: default backend with richer diagnostics;
- `backend="sklearn"`: faster regularized backend for larger permutation runs.

The scikit-learn backend does not provide standard errors, z-values, or
model-based backend p-values. QAP empirical p-values are still computed from the
permutation distribution.

The output should be interpreted as a workflow demonstration, not as a benchmark
or substantive social-science claim.
