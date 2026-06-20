# Equivalence vs approximation

This project distinguishes between equivalent implementations, validated
approximations, and exploratory approximations.

## Current module status

| Module | Status |
|---|---|
| Link prediction | Python implementation with manual tests; R validation pending |
| QAPLogit | Python implementation with unit tests; R `sna::netlogit` validation pending |
| ERGM | Dyadic-logistic approximation; not full MCMC-MLE |
| STERGM | Separable dyadic-logistic approximation; not full MCMC-MLE |

The initial ERGM and STERGM modules should not be presented as full equivalents
to R `ergm`, `tergm`, or `stergm`.
