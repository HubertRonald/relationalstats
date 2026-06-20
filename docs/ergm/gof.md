# ERGM GOF approximation

The initial GOF workflow simulates networks from fitted dyad probabilities and
compares observed and simulated network statistics:

- edges;
- density;
- average degree;
- triangles;
- degree distribution;
- edge-wise shared partners;
- geodesic distance distribution with `NR`.

This approximates the spirit of R `ergm::gof`, but is not equivalent to the full
R implementation.
