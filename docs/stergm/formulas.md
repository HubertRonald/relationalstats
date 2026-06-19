# STERGM approximation formulas

This page documents the formulas used by the initial `relationalstats.stergm`
implementation.

The current implementation is a separable dyadic-logistic temporal
approximation. It is not a full MCMC-MLE implementation equivalent to R `tergm`
or `stergm`.

## Two-snapshot setup

Given two graph snapshots:

$$
G_t
$$

and:

$$
G_{t+1}
$$

each dyad has two observed states:

$$
Y_{ij,t}
$$

and:

$$
Y_{ij,t+1}
$$

## Formation risk set

The formation model is fit only on dyads absent at time `t`:

$$
Y_{ij,t} = 0
$$

The formation outcome is:

$$
F_{ij,t+1} = Y_{ij,t+1}
$$

The fitted dyadic-logistic approximation is:

$$
\Pr(F_{ij,t+1}=1 \mid Y_{ij,t}=0)
=
\text{logit}^{-1}
\left(
\sum_{k=1}^{p} \beta^{F}_{k} x^{F}_{ijk,t}
\right)
$$

## Dissolution risk set

The dissolution model is fit only on dyads present at time `t`:

$$
Y_{ij,t} = 1
$$

The dissolution outcome is:

$$
D_{ij,t+1} = 1 - Y_{ij,t+1}
$$

The fitted dyadic-logistic approximation is:

$$
\Pr(D_{ij,t+1}=1 \mid Y_{ij,t}=1)
=
\text{logit}^{-1}
\left(
\sum_{k=1}^{p} \beta^{D}_{k} x^{D}_{ijk,t}
\right)
$$

## Next-period simulation

A simulated next-period graph starts from `G_t`.

For existing ties, dissolution is sampled from:

$$
D_{ij,t+1}
\sim
\text{Bernoulli}(p^{D}_{ij})
$$

For absent ties, formation is sampled from:

$$
F_{ij,t+1}
\sim
\text{Bernoulli}(p^{F}_{ij})
$$

where:

$$
p^{D}_{ij}
=
\text{logit}^{-1}
\left(
\sum_{k=1}^{p} \beta^{D}_{k} x^{D}_{ijk,t}
\right)
$$

and:

$$
p^{F}_{ij}
=
\text{logit}^{-1}
\left(
\sum_{k=1}^{p} \beta^{F}_{k} x^{F}_{ijk,t}
\right)
$$

## Scope note

The current model captures the separable formation/dissolution framing, but it
does not implement full temporal ERGM MCMC-MLE estimation or full equivalence
with R `tergm` / `stergm`.
