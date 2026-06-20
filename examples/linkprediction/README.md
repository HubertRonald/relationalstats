# Link prediction examples

This directory contains public examples for the `relationalstats.linkprediction` module.

The package core lives under:

```text
src/relationalstats/linkprediction/
```

This examples directory is reserved for optional workflows such as:

- feature generation;
- simple supervised link prediction;
- metric comparison;
- optional machine learning experiments;
- XGBoost-based feature search;
- SHAP-based model explanation;
- exploratory plotting.

## Current examples

```text
proxfun_feature_pipeline.py
```

Demonstrates how to:

1. Build a small synthetic graph.
2. Generate positive and negative node pairs.
3. Compute link prediction features with `proxfun_full`.
4. Train a simple scikit-learn classifier.
5. Evaluate the feature pipeline with ROC AUC.

```text
ml_feature_search_xgboost.py
```

Demonstrates how to:

1. Build a synthetic link prediction dataset.
2. Generate metric combinations.
3. Evaluate feature subsets with XGBoost.
4. Rank feature combinations by ROC AUC.
5. Optionally plot correlations and AUC distributions.
6. Optionally explain a fitted tree model with SHAP.

## Optional ML dependencies

Advanced experiments with XGBoost, SHAP, UMAP, or feature search should not be part of the package core.

Install optional ML and plotting dependencies only when needed:

```bash
python -m pip install -e ".[dev,test,plot]"
```

> **NOTE**: XGBoost is optional. On macOS, XGBoost may require the OpenMP runtime
`libomp.dylib`. The example defaults to a scikit-learn classifier to keep the
workflow portable.

## Methodological note

These examples are illustrative. They are not intended to claim benchmark-level performance or equivalence with R `linkprediction`.

They are intentionally synthetic and public-safe.

The reported AUC depends on the synthetic graph, sampling strategy, model choice,
and train/test split. It should be interpreted only as an execution check and
not as a performance benchmark.