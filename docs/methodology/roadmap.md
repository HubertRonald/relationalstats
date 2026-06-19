# Roadmap

This roadmap describes the intended direction of `relationalstats`.

It is intentionally separated from the release changelog. The changelog records
what changed. The roadmap explains where the project is going.

## Current public direction

The package is organized around four areas:

1. Link prediction.
2. QAP logistic models.
3. ERGM-inspired approximations.
4. STERGM-inspired temporal approximations.

## Version direction

```text
0.1.0a1
  First installable alpha.
  Package skeleton, link prediction core, early tests, and distribution setup.

0.1.0
  First public release candidate line.
  Link prediction core, QAPLogit, documentation foundation, and release workflow.

0.2.0
  ERGM approximation promoted from exploratory to usable.
  Expanded ERGM statistics, GOF documentation, and examples.

0.3.0
  STERGM approximation promoted from exploratory to usable.
  Formation/dissolution workflows and temporal examples.

0.4.0
  Expanded R validation fixtures.
  QAP, link prediction, ERGM statistics, and STERGM temporal validation.

1.0.0
  Stable public API.
  Clear compatibility and deprecation policy.
```

## Methodological horizon

The project should remain explicit about the difference between:

- exact or near-exact implementations;
- validated approximations;
- exploratory approximations;
- future research directions.

Current ERGM and STERGM support is intentionally documented as dyadic-logistic
approximation work. Full MCMC-based estimation remains a future research and
engineering direction.

## Packaging horizon

The intended release flow is:

```text
feature/* -> develop -> release/vX.Y.Z -> main -> tag vX.Y.Z -> PyPI
```

Pre-releases should use PEP 440 names:

```text
0.1.0a1
0.1.0b1
0.1.0rc1
0.1.0
```
