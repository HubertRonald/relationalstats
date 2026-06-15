# Scalability notes

Local metrics are computed using sparse adjacency matrices when possible.

The following metrics may require global matrix operations and can be expensive:

- `katz`
- `rwr`
- `act`

Future optimization directions may include:

- Numba;
- sparse linear solvers;
- GraphBLAS-compatible backends;
- compiled backends for large-scale graph statistics.
