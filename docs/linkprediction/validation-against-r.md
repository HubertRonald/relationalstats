# Validation against R linkprediction

This document describes the planned validation strategy for
`relationalstats.linkprediction` against R `linkprediction::proxfun`.

The goal is to validate equivalent metrics on small graphs where expected scores
can be manually inspected and reproduced.

## Scope

The first validation targets are local and semi-local metrics:

- `common_neighbors`
- `jaccard`
- `adamic_adar`
- `preferential_attachment`
- `resource_allocation`
- `salton`
- `sorensen`
- `hub_promoted`
- `hub_depressed`
- `lhn_local`
- `shortest_path`
- `local_path`

Global metrics may be validated later with tolerance-based comparisons:

- `katz`
- `rwr`
- `act`

These metrics depend on matrix conventions, numerical precision, parameter
choices, and graph connectivity assumptions.

## Required R outputs

For each validation fixture, export the following from R:

```text
graph_name
edge_list
directed flag
node ordering
pair list
selected metrics
proxfun output table
parameter values
seed, when applicable
```

The preferred exported format is CSV:

```text
tests/validation_against_r/fixtures/linkprediction/
  toy_graph_edges.csv
  toy_graph_pairs.csv
  toy_graph_r_proxfun_scores.csv
```

## Python validation inputs

The Python validation should reconstruct the same graph using:

```python
import networkx as nx
```

Then run:

```python
from relationalstats.linkprediction import proxfun_full

scores = proxfun_full(
    G,
    pairs=pairs,
    metrics=metrics,
    directed=False,
)
```

## Comparison levels

Validation should classify each metric as one of:

```text
exact
near-exact
tolerance-based
conceptual
not equivalent
```

Recommended rules:

| Level | Meaning |
|---|---|
| `exact` | Scores are equal for integer or deterministic local metrics. |
| `near-exact` | Scores match up to floating-point precision. |
| `tolerance-based` | Scores match within a documented numerical tolerance. |
| `conceptual` | Trends or rankings are similar, but values are not expected to match exactly. |
| `not equivalent` | The R and Python implementations use different definitions or assumptions. |

## Expected validation level by metric

| Metric | Expected validation level |
|---|---|
| `common_neighbors` | exact |
| `jaccard` | near-exact |
| `adamic_adar` | near-exact |
| `preferential_attachment` | exact |
| `resource_allocation` | near-exact |
| `salton` | near-exact |
| `sorensen` | near-exact |
| `hub_promoted` | near-exact |
| `hub_depressed` | near-exact |
| `lhn_local` | near-exact |
| `shortest_path` | near-exact |
| `local_path` | tolerance-based |
| `katz` | tolerance-based |
| `rwr` | tolerance-based |
| `act` | tolerance-based or conceptual |

## Important assumptions

The validation must explicitly align:

1. Node ordering.
2. Directed versus undirected graph interpretation.
3. Whether existing edges are scored.
4. Whether only non-edges are scored.
5. Parameter values for global metrics.
6. Handling of disconnected node pairs.
7. Floating-point tolerance.
8. Treatment of zero-degree nodes.
9. Treatment of self-loops.
10. Whether the graph is simple, weighted, or multigraph-like.

## Recommended toy graphs

Initial validation should use small graphs.

### Path graph

```text
0 -- 1 -- 2
```

Useful for validating:

- common neighbors;
- Jaccard;
- Adamic-Adar;
- resource allocation;
- shortest path.

### Triangle graph

```text
0 -- 1
|  /
2
```

Useful for validating behavior when all pairs are already connected.

### Star graph

```text
    1
    |
2 -- 0 -- 3
    |
    4
```

Useful for validating hub-sensitive metrics.

### Disconnected graph

```text
0 -- 1     2 -- 3
```

Useful for validating shortest path, ACT, and disconnected-pair behavior.

## R fixture generation sketch

A future R script should generate reproducible validation outputs.

Suggested location:

```text
scripts/export_r_validation_outputs.R
```

Suggested output folder:

```text
tests/validation_against_r/fixtures/linkprediction/
```

The script should:

1. Build small graphs.
2. Define a fixed pair list.
3. Run `linkprediction::proxfun`.
4. Export scores to CSV.
5. Save graph edge lists and pair lists.
6. Record package versions.

## Current status

The first package implementation includes Python-side unit tests for manually
verifiable small graphs.

R validation fixtures are planned for a later validation release.
