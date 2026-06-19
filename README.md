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
    <a href="https://scikit-learn.org/" target="_blank">
        <img src="https://img.shields.io/badge/scikit--learn-ML%20Backend-F7931E?style=flat-square&logo=scikit-learn&logoColor=white" />
    </a>
    <a href="https://www.statsmodels.org/" target="_blank">
        <img src="https://img.shields.io/badge/statsmodels-Statistical%20Models-4051B5?style=flat-square" />
    </a>
    <a href="https://opensource.org/license/mit/" target="_blank">
        <img src="https://img.shields.io/badge/License-MIT-success?style=flat-square" />
    </a>
    <img src="https://img.shields.io/badge/Status-Alpha-orange?style=flat-square" />
</p>

# relationalstats

A practical Python toolkit for applied and statistical social network analysis,
with research-grade documentation and transparent methodological boundaries.

`relationalstats` provides Python APIs for statistical network analysis workflows
inspired by R `sna`, `ergm`, `tergm` / `stergm`, and `linkprediction`, while
remaining explicit about what is equivalent, approximate, experimental, or
planned.

## What is included

| Area | Status |
|---|---|
| Link prediction | Initial core implemented |
| QAPLogit | Initial core implemented |
| ERGM | Initial dyadic-logistic approximation |
| STERGM | Initial separable dyadic-logistic approximation |
| R validation | Placeholders and roadmap; fixtures pending |

## Installation for local development

```bash
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev,test]"
```

Optional extras:

```bash
python -m pip install -e ".[docs]"
python -m pip install -e ".[notebooks,plot]"
python -m pip install -e ".[ml]"
python -m pip install -e ".[r]"
```

## Quick usage

### Link prediction

```python
import networkx as nx
from relationalstats.linkprediction import ProxFun, proxfun_full

G = nx.path_graph(3)

scores = proxfun_full(
    G,
    pairs=[(0, 2)],
    metrics=["common_neighbors", "jaccard", "adamic_adar"],
)

result = ProxFun(metrics=["jaccard", "adamic_adar"]).fit(G)
result.to_dataframe()
```

### QAPLogit

```python
from relationalstats.datasets import make_qap_toy_data
from relationalstats.qap import QAPLogit

y, x_matrices = make_qap_toy_data()

result = QAPLogit(
    n_permutations=99,
    random_state=42,
    backend="statsmodels",
).fit(y, x_matrices)

result.to_dataframe()
```

### ERGM approximation

```python
from relationalstats.datasets import make_florentine_like_graph
from relationalstats.ergm import ERGM

G = make_florentine_like_graph()

result = ERGM(
    terms=["edges", "common_neighbors", "degree1", "gwesp", "nodematch:faction"],
    backend="sklearn",
    random_state=42,
).fit(G)

result.to_dataframe()
result.gof(n_sim=100, seed=123)
```

### STERGM approximation

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
result.simulate(seed=123)
```

## Documentation map

- [Documentation index](docs/README.md)
- [Link prediction](docs/linkprediction/README.md)
- [QAP](docs/qap/README.md)
- [ERGM approximation](docs/ergm/README.md)
- [STERGM approximation](docs/stergm/README.md)
- [Equivalence vs approximation](docs/methodology/equivalence-vs-approximation.md)
- [Reproducibility](docs/methodology/reproducibility.md)
- [Roadmap](docs/methodology/roadmap.md)

## Examples

- [Examples index](examples/README.md)
- [Link prediction examples](examples/linkprediction/README.md)
- [QAP examples](examples/qap/README.md)
- [ERGM examples](examples/ergm/README.md)
- [STERGM examples](examples/stergm/README.md)

Run examples:

```bash
python examples/linkprediction/proxfun_feature_pipeline.py
python examples/qap/qap_logit_toy.py
python examples/qap/qap_logit_backend_comparison.py
python examples/ergm/ergm_florentine_like.py
python examples/stergm/stergm_temporal_toy.py
```

## Repository structure

```text
relationalstats/
├── docs/
│   ├── README.md
│   ├── ergm/
│   ├── linkprediction/
│   ├── methodology/
│   ├── qap/
│   └── stergm/
├── examples/
│   ├── README.md
│   ├── ergm/
│   ├── linkprediction/
│   ├── qap/
│   └── stergm/
├── notebooks/
│   └── README.md
├── scripts/
├── src/
│   └── relationalstats/
│       ├── datasets/
│       ├── ergm/
│       ├── linkprediction/
│       ├── modules/
│       ├── qap/
│       └── stergm/
├── tests/
│   ├── unit/
│   └── validation_against_r/
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml
└── README.md
```

## Running tests

```bash
source .venv/bin/activate
pytest -q
```

Focused test groups:

```bash
pytest tests/unit/test_linkprediction.py tests/unit/test_linkprediction_manual_graphs.py -q
pytest tests/unit/test_qap.py tests/unit/test_qap_permutation.py -q
pytest tests/unit/test_ergm_statistics.py tests/unit/test_ergm_gof.py -q
pytest tests/unit/test_stergm.py -q
```

## Build and distribution validation

```bash
source .venv/bin/activate
rm -rf dist build *.egg-info
python -m pip install build twine
python -m build
python -m twine check "dist/*"
ls -lh dist/
```

## Release flow

```text
feature/* -> develop -> release/vX.Y.Z -> main -> tag vX.Y.Z -> PyPI
```

Pre-release versions should follow PEP 440:

```text
0.1.0a1
0.1.0b1
0.1.0rc1
0.1.0
```

## Methodological transparency

Current ERGM and STERGM implementations are dyadic-logistic approximations, not
full MCMC-MLE implementations equivalent to R `ergm`, `tergm`, or `stergm`.

## Validation against R

Planned validation fixtures include:

- `sna::netlogit` for QAP-style logistic models;
- `linkprediction::proxfun` for link prediction metrics;
- `ergm` and `network` for selected network statistics;
- `tergm` / `stergm` for temporal dyad construction where feasible.

## Academic and private material policy

Solved academic notebooks, private experiments, raw course material, and
non-public validation files should not be committed to the public repository.

## Author

- **Hubert Ronald** - Initial Work - [HubertRonald](https://github.com/HubertRonald)

## License

The source code in this repository is distributed under the MIT License. See
[LICENSE](./LICENSE) for more details.
