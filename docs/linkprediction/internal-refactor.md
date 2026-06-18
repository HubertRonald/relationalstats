# Internal link prediction refactor

This document describes the internal split of the link prediction implementation.

The public API remains:

```python
from relationalstats.linkprediction import ProxFun, ProxFunResult, proxfun_full
```

The refactor only separates internal responsibilities so the module can grow
without keeping every implementation detail inside `proxfun_full.py`.

## Module responsibilities

```text
src/relationalstats/linkprediction/
  metrics.py
  random_walk.py
  spectral.py
  proxfun_full.py
  results.py
```

## `metrics.py`

Contains metric registry and lightweight numeric helpers:

- `ALL_METRICS`
- `LOCAL_A2_METRICS`
- `GLOBAL_METRICS`
- `validate_metrics`
- `safe_divide`

This module should remain dependency-light and focused on metric names,
validation, and shared numeric behavior.

## `random_walk.py`

Contains random-walk-specific helpers:

- transition matrix construction;
- random walk with restart matrix computation.

This keeps diffusion-oriented computations separate from the orchestration layer.

## `spectral.py`

Contains global matrix and spectral helpers:

- Katz matrix computation;
- average commute time scoring.

These methods can be expensive and may later receive approximate or optimized
implementations.

## `proxfun_full.py`

Remains the orchestration layer.

It is responsible for:

- validating the graph;
- preparing node pairs;
- building the adjacency matrix;
- coordinating requested metric computation;
- returning a DataFrame or dictionary output;
- exposing the estimator-style `ProxFun` interface.

## `results.py`

Contains `ProxFunResult`, the result object used by the estimator-style API.

## What this refactor does not do

This refactor does not change the public API.

It also does not introduce R validation fixtures, new datasets, or QAP/ERGM/
STERGM functionality.

Those are separate roadmap items.

## Validation

```bash
pytest tests/unit/test_linkprediction.py        tests/unit/test_linkprediction_manual_graphs.py        tests/unit/test_linkprediction_internal_helpers.py -q
```
