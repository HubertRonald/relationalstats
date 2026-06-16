# Experimental ML workflow for link prediction

This note documents where the exploratory ML pieces from the original
`proxfun_full.py` prototype now belong.

The package core should remain focused on reusable link prediction metrics:

```text
src/relationalstats/linkprediction/
```

Experimental workflows should live under:

```text
examples/linkprediction/
```

## Migrated experimental ideas

The original prototype included exploratory utilities and notes for:

- XGBoost-based feature evaluation;
- automatic metric-combination search;
- feature importance for tree models;
- PCA-based feature exploration;
- correlation heatmaps with `seaborn`;
- AUC distribution plots with `matplotlib`;
- SHAP-based model explanation.

Those ideas are intentionally not part of the installable core API.

They are represented as optional example code in:

```text
examples/linkprediction/ml_feature_search_xgboost.py
```

## Optional dependencies

Install optional ML and plotting dependencies only when needed:

```bash
python -m pip install -e ".[dev,test,plot]"
```

> **NOTE**: XGBoost is optional. On macOS, XGBoost may require the OpenMP runtime
`libomp.dylib`. The example defaults to a scikit-learn classifier to keep the
workflow portable.

## Why this is outside the package core

Keeping this workflow outside `src/relationalstats/` avoids forcing users to
install heavier dependencies such as:

- `xgboost`
- `shap`
- `seaborn`
- `matplotlib`

It also keeps the public API focused on stable graph metrics rather than
notebook-style experimentation.

## Recommended execution

```bash
python examples/linkprediction/ml_feature_search_xgboost.py
```

The script uses a small synthetic graph and does not depend on private notebooks,
course assignments, or external datasets.
