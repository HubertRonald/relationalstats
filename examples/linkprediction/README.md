# Link prediction examples

This directory contains public examples for the `relationalstats.linkprediction`
module.

The package core lives under:

```text
src/relationalstats/linkprediction/
```

This examples directory is reserved for optional workflows such as:

- feature generation;
- simple supervised link prediction;
- metric comparison;
- optional ML experiments;
- future XGBoost or SHAP demonstrations.

## Current example

```bash
proxfun_feature_pipeline.py
```

This script demonstrates how to:

1. Build a small synthetic graph.
2. Generate positive and negative node pairs.
3. Compute link prediction features with proxfun_full.
4. Train a simple scikit-learn classifier.
5. Evaluate the feature pipeline with ROC AUC.


## Optional ML dependencies

Advanced experiments with XGBoost, SHAP, UMAP, or feature search should not be
part of the package core.

Install optional ML dependencies only when needed:

```bash
python -m pip install -e ".[ml]"
```

## Methodological note

These examples are illustrative. They are not intended to claim benchmark-level
performance or equivalence with R linkprediction.