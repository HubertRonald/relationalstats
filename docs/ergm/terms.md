# ERGM approximation terms

| Term | Meaning |
|---|---|
| `edges` | Constant edge propensity term |
| `common_neighbors` | Number of shared neighbors |
| `transitiveties` | Transitivity proxy based on shared neighbors |
| `degree1` | Whether either endpoint has degree one |
| `gwesp` | Simple geometrically weighted shared-partner approximation |
| `nodematch:<attr>` | Whether both endpoints share a node attribute |

These are dyad-level feature approximations, not full incremental ERGM change
statistics.
