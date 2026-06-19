# Scalability notes

`relationalstats.linkprediction` uses sparse matrix operations where possible.

## Sparse-friendly metrics

The following metrics can benefit from sparse adjacency matrix operations:

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
- `local_path`

## Potentially expensive metrics

The following metrics may require global matrix operations:

- `katz`
- `rwr`
- `act`

These should be used carefully on large graphs.

## Katz

Katz uses the matrix expression:

$$
Katz = (I - \beta A)^{-1} - I
$$

This may become expensive when the graph has many nodes.

## Random walk with restart

Random walk with restart uses:

$$
RWR = \left(I - (1 - \alpha)P\right)^{-1}
$$

where $P$ is the row-normalized transition matrix.

## Average commute time

Average commute time uses the pseudoinverse of the Laplacian:

$$
C(u, v) = \text{vol}(G)\left(L^+_{uu} + L^+_{vv} - 2L^+_{uv}\right)
$$

This requires dense linear algebra in the current implementation.

## Future optimization directions

Future versions may investigate:

- better sparse linear solvers;
- approximate global metrics;
- Numba acceleration;
- GraphBLAS-compatible backends;
- compiled backends for large-scale graph statistics.
