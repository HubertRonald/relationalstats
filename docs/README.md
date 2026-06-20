# relationalstats documentation

`relationalstats` is a practical Python toolkit for applied and statistical
social network analysis.

The documentation is organized by module and by methodology.

## Module documentation

- [QAP](qap/README.md)
- [Link prediction](linkprediction/README.md)
- [ERGM approximation](ergm/README.md)
- [STERGM approximation](stergm/README.md)

## Methodology

- [Equivalence vs approximation](methodology/equivalence-vs-approximation.md)
- [Reproducibility](methodology/reproducibility.md)

## Current implementation status

| Area | Status |
|---|---|
| Link prediction | Initial core implemented |
| QAPLogit | Initial core implemented |
| ERGM | Planned experimental approximation |
| STERGM | Planned experimental approximation |

## Validation

Validation is built in layers:

1. deterministic unit tests;
2. manual small-graph tests;
3. synthetic examples;
4. future validation against R fixtures.

R validation placeholders are intentionally kept visible until fixture exports
are added.
