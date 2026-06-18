# Validation against R

Future validation should compare `QAPLogit` against R `sna::netlogit`.

The current repository includes a skipped placeholder test under:

```text
tests/validation_against_r/test_qap_against_sna_netlogit.py
```

## Required alignment

Validation should explicitly align:

- directed versus undirected dyad handling;
- diagonal inclusion or exclusion;
- predictor matrix ordering;
- permutation count;
- random seed or exported permutation indices;
- coefficient naming;
- empirical p-value convention;
- tolerance for floating-point comparisons.

## Backend note

Use the `statsmodels` backend for R validation.

The `sklearn` backend is useful for faster regularized permutation workflows, but
it does not expose standard errors, z-values, or model-based p-values.

## Current status

R validation fixtures are pending.

Until fixture export is added, the Python implementation is covered by:

```bash
pytest tests/unit/test_qap.py tests/unit/test_qap_permutation.py -q
```
