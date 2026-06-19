# Contributing

Thank you for considering a contribution to `relationalstats`.

This project values correctness, reproducibility, clear documentation, and honest
methodological boundaries.

## Development setup

```bash
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev,test]"
```

## Branching model

Use feature branches from `develop`:

```text
feature/<scope>-<short-name>
```

Release branches should use:

```text
release/vX.Y.Z
```

Hotfix branches should use:

```text
hotfix/vX.Y.Z
```

## Validation before opening a PR

```bash
source .venv/bin/activate
pytest -q
```

For packaging changes:

```bash
rm -rf dist build *.egg-info
python -m pip install build twine
python -m build
python -m twine check "dist/*"
```

## Documentation rules

Repository-facing content should be written in English.

Documentation should be clear about whether a feature is equivalent,
near-equivalent, tolerance-based, conceptual, approximate, experimental, or
planned.

## Math in Markdown

GitHub Markdown and future VitePress rendering may reject some LaTeX macros.

Do not use:

```text
\operatorname
```

Prefer:

```text
\text{...}
```

Before committing docs, run:

```bash
python scripts/fix_github_math_macros.py --check
```

To fix files in place:

```bash
python scripts/fix_github_math_macros.py --write
```

## Methodological contribution rules

When contributing ERGM or STERGM functionality:

- Do not claim equivalence with R `ergm`, `tergm`, or `stergm` unless validation
  fixtures are committed and documented.
- Keep shared code in `src/relationalstats/modules/` only when it is genuinely
  reusable across package modules.
- Keep plotting optional through lazy imports.
- Document whether a term is a dyadic feature approximation or a true ERGM
  change statistic.

## Academic and private material

Solved academic notebooks, private experiments, raw course material, and
non-public validation files should not be committed to the public repository.
