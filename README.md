
<p align="left">
    <a href="https://www.python.org/" target="_blank">
        <img src="https://img.shields.io/badge/Python-3.10%2B-3670A0?style=flat-square&logo=python&logoColor=ffdd54" />
    </a>
    <a href="https://networkx.org/" target="_blank">
        <img src="https://img.shields.io/badge/NetworkX-Graph%20Analysis-1f77b4?style=flat-square" />
    </a>
    <a href="https://numpy.org/" target="_blank">
        <img src="https://img.shields.io/badge/NumPy-Arrays-013243?style=flat-square&logo=numpy&logoColor=white" />
    </a>
    <a href="https://pandas.pydata.org/" target="_blank">
        <img src="https://img.shields.io/badge/Pandas-DataFrames-150458?style=flat-square&logo=pandas&logoColor=white" />
    </a>
    <a href="https://scipy.org/" target="_blank">
        <img src="https://img.shields.io/badge/SciPy-Sparse%20Matrix-8CAAE6?style=flat-square&logo=scipy&logoColor=white" />
    </a>
    <a href="https://scikit-learn.org/" target="_blank">
        <img src="https://img.shields.io/badge/scikit--learn-ML%20Backend-F7931E?style=flat-square&logo=scikit-learn&logoColor=white" />
    </a>
    <a href="https://www.statsmodels.org/" target="_blank">
        <img src="https://img.shields.io/badge/statsmodels-Statistical%20Models-4051B5?style=flat-square" />
    </a>
    <a href="https://docs.pytest.org/" target="_blank">
        <img src="https://img.shields.io/badge/Pytest-Testing-0A9EDC?style=flat-square&logo=pytest&logoColor=white" />
    </a>
    <a href="https://github.com/features/actions" target="_blank">
        <img src="https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF?style=flat-square&logo=githubactions&logoColor=white" />
    </a>
    <a href="https://packaging.python.org/" target="_blank">
        <img src="https://img.shields.io/badge/Python%20Packaging-pyproject.toml-3775A9?style=flat-square&logo=pypi&logoColor=white" />
    </a>
    <a href="https://opensource.org/license/mit/" target="_blank">
        <img src="https://img.shields.io/badge/License-MIT-success?style=flat-square" />
    </a>
    <img src="https://img.shields.io/badge/Status-Alpha-orange?style=flat-square" />
    <br>
    <img src="https://img.shields.io/github/commit-activity/t/HubertRonald/relationalstats?style=flat-square&color=dodgerblue" />
</p>


# relationalstats

A practical Python toolkit for applied and statistical social network analysis, with research-grade documentation and transparent methodological boundaries.

`relationalstats` is designed to provide modern Python APIs for statistical network analysis workflows inspired by tools such as R `sna`, `ergm`, `tergm` / `stergm`, and `linkprediction`, while remaining explicit about what is equivalent, approximate, experimental, or planned.

## Overview

The package focuses on four main areas:

1. Quadratic Assignment Procedure, QAP.
2. Exponential Random Graph Model, ERGM.
3. Temporal Exponential Random Graph Model, STERGM.
4. Link prediction, including `proxfun_full`, an extensible Python implementation inspired by R `linkprediction::proxfun`.

The first public release focuses on a stable core for:

* QAP logistic models;
* link prediction metrics.

ERGM and STERGM are planned as transparent dyadic logistic approximations first, with full MCMC-based estimation treated as a future research and engineering direction.

## Methodological transparency

This project does not claim full equivalence with R `ergm`, `tergm`, or `stergm` unless explicitly validated.

Initial ERGM and STERGM implementations should be understood as:

```text
dyadic logistic approximations
```

not full MCMC-MLE implementations.

The project prioritizes:

* clear formulas;
* reproducible validation;
* small graph tests;
* R comparison fixtures;
* honest documentation of limitations;
* incremental development toward stronger statistical engines.

## Core dependencies

The package is built on the Scientific Python ecosystem:

* `networkx`
* `numpy`
* `pandas`
* `scipy`
* `statsmodels`
* `scikit-learn`

## Repository structure

```text
relationalstats/
├── .devcontainer/
│   ├── devcontainer.json
│   └── Dockerfile
├── docs/
│   ├── qap/
│   ├── ergm/
│   ├── stergm/
│   ├── linkprediction/
│   └── methodology/
├── examples/
├── scripts/
├── src/
│   └── relationalstats/
│       ├── qap/
│       ├── ergm/
│       ├── stergm/
│       ├── linkprediction/
│       ├── datasets/
│       └── modules/
├── tests/
│   ├── unit/
│   └── validation_against_r/
├── requirements.txt
├── requirements-dev.txt
├── requirements-test.txt
├── requirements-docs.txt
├── requirements-notebooks.txt
├── requirements-api.txt
├── pyproject.toml
└── README.md
```

## Local setup

Create a virtual environment:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
```

Upgrade `pip`:

```bash
python -m pip install --upgrade pip
```

Install core dependencies:

```bash
pip install -r requirements.txt
```

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Install test dependencies:

```bash
pip install -r requirements-test.txt
```

Install documentation dependencies:

```bash
pip install -r requirements-docs.txt
```

Install notebook dependencies:

```bash
pip install -r requirements-notebooks.txt
```

Install the package in editable mode with development extras:

```bash
python -m pip install -e ".[dev,test]"
```

Quick local test

```bash
python3.10 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements-dev.txt
pip install -r requirements-test.txt

python -m pip install -e ".[dev,test]"

pytest tests/unit/test_linkprediction.py -q
```

```markdown
## Build validation

To validate the package build locally:

```bash
rm -rf dist build *.egg-info
python -m pip install build twine
python -m build
python -m twine check "dist/*"
```

## Devcontainer setup

This repository includes a VS Code compatible devcontainer.

Open the repository in VS Code and choose:

```text
Dev Containers: Reopen in Container
```

The devcontainer uses Python 3.12 and installs development, testing, documentation, and notebook dependencies.

This is useful when the local operating system has older Python or system dependency constraints.

### Default devcontainer

The default devcontainer is intentionally lightweight.

It installs only the package core plus development and test dependencies:

```bash
python -m pip install -e ".[dev,test]"

Notebook, plotting, ML, documentation, and R-validation dependencies are not installed by default.

Install them only when needed:

python -m pip install -e ".[notebooks,plot]"
python -m pip install -e ".[ml]"
python -m pip install -e ".[docs]"
python -m pip install -e ".[r]"
```

## Quick usage

Functional link prediction API:

```python
import networkx as nx

from relationalstats.linkprediction import proxfun_full

G = nx.path_graph(3)

scores = proxfun_full(
    G,
    pairs=[(0, 2)],
    metrics=["common_neighbors", "jaccard", "adamic_adar"],
)

print(scores)
```

Estimator-style API:

```python
import networkx as nx

from relationalstats.linkprediction import ProxFun

G = nx.path_graph(3)

result = ProxFun(metrics=["jaccard", "adamic_adar"]).fit(G)

result.to_dataframe()
result.top_k(k=10, metric="jaccard")
```

## Running tests

Run the link prediction unit tests:

```bash
pytest tests/unit/test_linkprediction.py -q
```

Run all tests:

```bash
pytest -q
```

Run tests with coverage:

```bash
pytest --cov=src/relationalstats tests/
```

## Dependency groups

```text
requirements.txt
  Core runtime package installation.

requirements-dev.txt
  Development tools such as linting, build, packaging, and pre-commit.

requirements-test.txt
  Test dependencies.

requirements-docs.txt
  Documentation dependencies.

requirements-notebooks.txt
  Jupyter and notebook dependencies.

requirements-api.txt
  Reserved for a future API or service layer.
```

## Public roadmap

```text
v0.1.0a1
  First installable alpha.
  Link prediction core.
  Package skeleton.
  Basic tests.
  Local development setup.

v0.1.0
  First public release.
  Stable link prediction core.
  Initial QAPLogit implementation.
  Documentation foundation.

v0.2.0
  ERGM dyadic logistic approximation.
  ERGM statistics and GOF diagnostics.

v0.3.0
  STERGM dyadic temporal approximation.
  Formation and dissolution models.

v0.4.0
  Validation against R outputs and reproducible fixtures.

v1.0.0
  Stable public API.
```

## Validation against R

The project aims to include validation fixtures against selected R packages:

* `sna::netlogit` for QAP-style logistic models;
* `ergm` and `network` for network statistics;
* `ergm::gof` for conceptual GOF diagnostics;
* `linkprediction::proxfun` for equivalent link prediction metrics.

Validation levels will be documented as:

```text
exact
near-exact
tolerance-based
conceptual
not equivalent
```

## Academic and private material policy

Solved academic notebooks, private experiments, raw course material, and non-public validation files should not be committed to the public repository.

Local-only paths such as the following should remain ignored:

```text
notebooks/legacy/
notebooks/private/
validation/private/
r_outputs/private/
data/private/
fixtures/private/
```

Public examples should be rewritten as clean, original, reusable examples that do not expose solved academic assignments.


## Examples and experimental workflows

The package core lives under:

```text
src/relationalstats/
```

Stable and reusable link prediction metrics live under:

```text
src/relationalstats/linkprediction/
```

Public examples, optional experiments, and exploratory workflows live under:

```text
examples/
```

For link prediction, public examples live under:

```text
examples/linkprediction/
```

Current examples include:

```bash
python examples/linkprediction/proxfun_feature_pipeline.py
python examples/linkprediction/ml_feature_search_xgboost.py
```

The first example demonstrates how to use `proxfun_full` as a feature generator
for a simple supervised link prediction workflow.

The second example keeps the original exploratory ML direction outside the
package core. It covers optional ideas such as:

* XGBoost-based feature evaluation;
* metric-combination search;
* exploratory feature importance;
* correlation plots;
* SHAP-based model explanation.

The XGBoost/SHAP workflow requires optional dependencies:

```bash
python -m pip install -e ".[ml,plot]"
```

Solved academic notebooks, private experiments, raw course material, and
non-public validation work should not be committed to this repository.

Local-only material should remain under ignored paths such as:

```text
notebooks/legacy/
notebooks/private/
scratch/
experiments/
```

These examples are synthetic, public-safe, and separate from private notebooks or
academic course material.

## ERGM and STERGM approximations

`relationalstats` now includes initial ERGM-inspired and STERGM-inspired
approximations.

These modules are dyadic-logistic approximations, not full MCMC-MLE equivalents
to R `ergm`, `tergm`, or `stergm`.


## Author

* **Hubert Ronald** - Initial Work - [HubertRonald](https://github.com/HubertRonald)
* See also the list of [contributors](https://github.com/HubertRonald/relationalstats/contributors) who participated in this project.

## License and Copyright

The source code in this repository is distributed under the MIT License. See the [LICENSE](./LICENSE) file for more details.
