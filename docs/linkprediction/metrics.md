# Link prediction metrics

This document summarizes the initial link prediction metrics supported by
`relationalstats.linkprediction.proxfun_full`.

## Notation

- $G = (V, E)$: graph.
- $u, v \in V$: node pair to score.
- $\Gamma(u)$: neighborhood of node $u$.
- $k_u = |\Gamma(u)|$: degree of node $u$.
- $A$: adjacency matrix.
- $(A^\ell)_{uv}$: number of walks of length $\ell$ from $u$ to $v$.

For the first release, the recommended default is `directed=False`, which scores
pairs on an undirected version of the graph.

## Metric families

| Mechanism | Metrics |
|---|---|
| Triadic closure | `common_neighbors`, `jaccard`, `adamic_adar` |
| Popularity / degree | `preferential_attachment`, `degree` |
| Structural similarity | `salton`, `sorensen`, `lhn_local` |
| Hub dynamics | `hub_promoted`, `hub_depressed` |
| Diffusion / flow | `resource_allocation` |
| Geodesic proximity | `shortest_path` |
| Extended short paths | `local_path` |
| Global centrality | `katz` |
| Stochastic diffusion | `rwr` |
| Random-walk global metric | `act` |

## Common neighbors

$$
CN(u, v) = |\Gamma(u) \cap \Gamma(v)|
$$

Counts the number of shared neighbors between two nodes.

## Jaccard coefficient

$$
J(u, v) = \frac{|\Gamma(u) \cap \Gamma(v)|}{|\Gamma(u) \cup \Gamma(v)|}
$$

Measures neighborhood overlap normalized by neighborhood union.

## Adamic-Adar index

$$
AA(u, v) = \sum_{w \in \Gamma(u) \cap \Gamma(v)} \frac{1}{\log(k_w)}
$$

Penalizes shared neighbors with high degree.

## Preferential attachment

$$
PA(u, v) = k_u k_v
$$

Scores pairs highly when both nodes have high degree.

## Resource allocation index

$$
RA(u, v) = \sum_{w \in \Gamma(u) \cap \Gamma(v)} \frac{1}{k_w}
$$

Similar to Adamic-Adar, but with a stronger penalty for high-degree shared
neighbors.

## Salton index / cosine similarity

$$
Salton(u, v) = \frac{|\Gamma(u) \cap \Gamma(v)|}{\sqrt{k_u k_v}}
$$

Cosine-like structural similarity between node neighborhoods.

## Sorensen index

$$
Sorensen(u, v) = \frac{2|\Gamma(u) \cap \Gamma(v)|}{k_u + k_v}
$$

Another normalized neighborhood-overlap score.

## Hub promoted index

$$
HPI(u, v) = \frac{|\Gamma(u) \cap \Gamma(v)|}{\min(k_u, k_v)}
$$

Promotes similarity when the smaller-degree node shares many of its neighbors.

## Hub depressed index

$$
HDI(u, v) = \frac{|\Gamma(u) \cap \Gamma(v)|}{\max(k_u, k_v)}
$$

Penalizes similarity when one of the nodes is a high-degree hub.

## Leicht-Holme-Newman local index

$$
LHN(u, v) = \frac{|\Gamma(u) \cap \Gamma(v)|}{k_u k_v}
$$

Reduces degree-driven bias in common-neighbor scores.

## Shortest path

$$
d(u, v) = \text{dist}(u, v)
$$

Lower values indicate closer nodes. Disconnected nodes receive infinite distance
in the current implementation.

## Local path index

$$
LP(u, v) = (A^2)_{uv} + \beta(A^3)_{uv}
$$

The default value is:

$$
\beta = 0.01
$$

This combines length-2 and length-3 walks.

## Katz index

$$
Katz(u, v) = \sum_{\ell=1}^{\infty} \beta^{\ell}(A^{\ell})_{uv}
$$

Matrix form:

$$
Katz = (I - \beta A)^{-1} - I
$$

The default value is:

$$
\beta = 0.005
$$

Katz is a global metric and can be expensive for large graphs.

## Random walk with restart

Random walk with restart estimates the diffusion probability of reaching a node
from a source while repeatedly returning to the source.

The current implementation uses:

$$
RWR = \left(I - (1 - \alpha)P\right)^{-1}
$$

where:

- $P$ is the row-normalized transition matrix.
- $\alpha$ is the restart probability.

The default value is:

$$
\alpha = 0.15
$$

RWR is a global matrix-based metric and can be expensive for large graphs.

## Degree features

$$
degree\_source = k_u
$$

$$
degree\_target = k_v
$$

These features expose the individual degree of each node in the pair.

## Average commute time score

Average commute time is based on the Moore-Penrose pseudoinverse of the graph
Laplacian.

$$
C(u, v) = \text{vol}(G)\left(L^+_{uu} + L^+_{vv} - 2L^+_{uv}\right)
$$

The implemented score is:

$$
ACT\_score(u, v) = \frac{1}{C(u, v)}
$$

Disconnected pairs receive score `0.0`.

This metric requires dense linear algebra and is expensive for large graphs.

## Division by zero policy

When a denominator is zero, the score is set to `0.0`.

This affects metrics such as:

- `jaccard`
- `salton`
- `sorensen`
- `hub_promoted`
- `hub_depressed`
- `lhn_local`
- `act`

## Scalability notes

Sparse matrix operations are used where possible for local metrics.

The following metrics are potentially expensive:

- `katz`
- `rwr`
- `act`

These should be used carefully on large graphs.
