# Link prediction metrics

Initial metrics:

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

## Notes

For `directed=False`, the graph is converted to an undirected graph before
scoring. This is the recommended default for the first release.

Global matrix-based metrics are included for completeness, but they should be
used carefully on large networks.
