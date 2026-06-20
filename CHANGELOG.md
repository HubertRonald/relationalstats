# Changelog

All notable changes to this project will be documented in this file.

The project follows semantic versioning principles, with the understanding that
public APIs may still change before `1.0.0`.

## Unreleased

### Added

- Added initial QAPLogit implementation with `statsmodels` and `sklearn`
  backends.
- Added link prediction core with `ProxFun`, `ProxFunResult`, and
  `proxfun_full`.
- Added manual small-graph tests for link prediction metrics.
- Added internal link prediction helper modules for metrics, random-walk logic,
  and spectral/global helpers.
- Added initial ERGM-inspired dyadic-logistic approximation.
- Added initial STERGM-inspired separable temporal dyadic-logistic
  approximation.
- Added shared modules for graph converters, validation, simulation, plotting,
  and small utilities.
- Added synthetic QAP, Florentine-like, and temporal toy datasets.
- Added public examples for link prediction, QAP, ERGM, and STERGM.
- Added methodology documentation for equivalence, approximation, and
  reproducibility.
- Added skipped placeholders for future R validation fixtures.

### Changed

- Expanded the public README to reflect QAP, link prediction, ERGM, STERGM,
  examples, docs, notebooks, testing, and build validation.
- Clarified that ERGM and STERGM support is approximate and not equivalent to R
  `ergm`, `tergm`, or `stergm`.

### Notes

- ERGM and STERGM support is experimental and approximate.
- R validation fixtures are pending.
