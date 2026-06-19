# ERGM approximation formulas

This page documents the formulas used by the initial `relationalstats.ergm`
implementation.

The current implementation is a dyadic-logistic approximation. It is not a full
MCMC-MLE ERGM engine and should not be described as equivalent to R `ergm`.

## Dyadic logistic approximation

For a candidate dyad `(i, j)`, the model uses:

$$
\Pr(Y_{ij}=1) =
\text{logit}^{-1}
\left(
\sum_{k=1}^{p} \beta_k x_{ijk}
\right)
$$

Equivalently:

$$
\log
\left(
\frac{\Pr(Y_{ij}=1)}
{1 - \Pr(Y_{ij}=1)}
\right)
=
\sum_{k=1}^{p} \beta_k x_{ijk}
$$

The implementation uses `add_intercept=False` internally because the `edges`
term acts as the baseline edge-propensity term.

## Edges term

$$
x_{ij,\text{edges}} = 1
$$

## Common-neighbor term

$$
x_{ij,\text{common_neighbors}}
=
|N(i) \cap N(j)|
$$

## Transitivity proxy

$$
x_{ij,\text{transitiveties}}
=
|N(i) \cap N(j)|
$$

This is a dyad-level approximation, not a full ERGM change statistic.

## Degree-one term

$$
x_{ij,\text{degree1}}
=
\begin{cases}
1, & \text{if } d_i = 1 \text{ or } d_j = 1 \\
0, & \text{otherwise}
\end{cases}
$$

## GWESP approximation

$$
x_{ij,\text{gwesp}}
=
1 - (1 - e^{-\alpha})^{s_{ij}}
$$

where:

$$
s_{ij} = |N(i) \cap N(j)|
$$

and the default decay parameter is:

$$
\alpha = 0.5
$$

This approximates the intuition of geometrically weighted shared partners, but
it is not the full curved ERGM GWESP term used by R `ergm`.

## Nodematch term

A nodematch term has the form:

```text
nodematch:<attribute>
```

The dyadic feature is:

$$
x_{ij,\text{nodematch:attr}}
=
\begin{cases}
1, & \text{if } a_i = a_j \text{ and both values are non-missing} \\
0, & \text{otherwise}
\end{cases}
$$

## GOF-style statistics

The approximate GOF workflow compares observed and simulated networks using:

- edges;
- density;
- average degree;
- triangle count;
- degree distribution;
- edge-wise shared partners;
- geodesic distance distribution with `NR` for unreachable pairs.
