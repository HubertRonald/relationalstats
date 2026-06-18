# Manual small-graph tests

This document explains the manually verifiable link prediction tests used in the
unit test suite.

The goal is to validate simple graph configurations where expected values can
be derived by hand before adding broader validation against R
`linkprediction::proxfun`.

## Scope

The current manual tests focus on local and semi-local metrics:

- `common_neighbors`
- `jaccard`
- `adamic_adar`
- `resource_allocation`
- `preferential_attachment`
- `salton`
- `sorensen`
- `hub_promoted`
- `hub_depressed`
- `lhn_local`
- `degree`
- `shortest_path`
- `local_path`

Global metrics such as `katz`, `rwr`, and `act` are better suited for
tolerance-based tests because they depend on matrix conventions, graph
connectivity assumptions, and numerical precision.

## Path graph

```text
0 -- 1 -- 2
```

For pair `(0, 2)`:

- $\Gamma(0) = \{1\}$
- $\Gamma(2) = \{1\}$
- $\Gamma(0) \cap \Gamma(2) = \{1\}$
- $k_0 = 1$
- $k_2 = 1$
- $k_1 = 2$

Expected values:

| Metric | Expected value |
|---|---:|
| `common_neighbors` | `1` |
| `jaccard` | `1.0` |
| `adamic_adar` | $1 / \log(2)$ |
| `resource_allocation` | $1 / 2$ |
| `preferential_attachment` | `1` |
| `salton` | `1.0` |
| `sorensen` | `1.0` |
| `hub_promoted` | `1.0` |
| `hub_depressed` | `1.0` |
| `lhn_local` | `1.0` |
| `shortest_path` | `2.0` |

## Unequal-degree graph

```text
    3
    |
    0 -- 2 -- 1 -- 4
              | \
              5  6
```

For pair `(0, 1)`:

- $\Gamma(0) = \{2, 3\}$
- $\Gamma(1) = \{2, 4, 5, 6\}$
- $\Gamma(0) \cap \Gamma(1) = \{2\}$
- $k_0 = 2$
- $k_1 = 4$

Expected values:

| Metric | Expected value |
|---|---:|
| `common_neighbors` | `1` |
| `preferential_attachment` | `8` |
| `jaccard` | $1 / 5$ |
| `salton` | $1 / \sqrt{8}$ |
| `sorensen` | $2 / 6$ |
| `hub_promoted` | $1 / 2$ |
| `hub_depressed` | $1 / 4$ |
| `lhn_local` | $1 / 8$ |

## Local path graph

```text
0 -- 1 -- 2 -- 3
```

For pair `(0, 3)`:

- there are no walks of length 2;
- there is one walk of length 3;
- with the default $\beta = 0.01$, the expected score is `0.01`.

The local path formula is:

$$
LP(u, v) = (A^2)_{uv} + \beta(A^3)_{uv}
$$

## Disconnected graph

```text
0 -- 1     2 -- 3
```

For pair `(0, 2)`, `shortest_path` should be infinite because the nodes are in
different connected components.

## Isolated nodes

```text
0     1
```

For pair `(0, 1)`, both nodes have degree zero. Similarity scores whose
denominator would be zero should return `0.0`, not `NaN` or an uninitialized
numeric value.

This validates the package zero-division policy for:

- `jaccard`
- `salton`
- `sorensen`
- `hub_promoted`
- `hub_depressed`
- `lhn_local`

## Test command

```bash
pytest tests/unit/test_linkprediction.py tests/unit/test_linkprediction_manual_graphs.py -q
```

## Relationship to R validation

These tests are Python-side manual checks. They are not a replacement for R
validation fixtures.

Future R validation should compare selected metrics against
`linkprediction::proxfun` using aligned:

- node ordering;
- graph direction;
- pair selection;
- parameter values;
- disconnected-pair handling;
- floating-point tolerance.
