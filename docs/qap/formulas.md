# QAPLogit formulas

## Dyadic logistic model

For a binary dyadic outcome $Y_{ij}$ and dyadic predictors $X_{ij1}, \dots,
X_{ijp}$, the model is:

$$
\Pr(Y_{ij}=1) = \text{logit}^{-1}
\left(\beta_0 + \sum_{k=1}^{p} \beta_k X_{ijk}\right)
$$

Equivalently:

$$
\log\left(\frac{\Pr(Y_{ij}=1)}{1 - \Pr(Y_{ij}=1)}\right)
=
\beta_0 + \sum_{k=1}^{p} \beta_k X_{ijk}
$$

## Dyad extraction

For directed networks, the default dyad set is:

$$
\{(i,j): i \ne j\}
$$

For undirected networks, the default dyad set is the upper triangle:

$$
\{(i,j): i < j\}
$$

Self-dyads are excluded by default.

## QAP node-label permutations

For each permutation $\pi$ of node labels, the dependent matrix is permuted as:

$$
Y^{(\pi)} = P_{\pi} Y P_{\pi}^{T}
$$

The dyadic predictors remain fixed. The model is then re-fit on the permuted
outcome to obtain a permutation distribution of coefficients.

## Empirical p-values

The initial implementation uses a plus-one empirical p-value:

$$
p =
\frac{1 + \sum_{b=1}^{B}
\mathbb{I}\left(|T_b| \ge |T_{obs}|\right)}
{B + 1}
$$

where:

- $T_{obs}$ is the observed coefficient;
- $T_b$ is the coefficient from permutation $b$;
- $B$ is the number of permutations.

This plus-one correction avoids returning zero p-values from a finite
permutation sample.
