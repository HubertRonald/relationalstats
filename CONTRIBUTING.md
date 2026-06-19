## Methodological contribution rules

When contributing ERGM or STERGM functionality:

- Do not claim equivalence with R `ergm`, `tergm`, or `stergm` unless validation
  fixtures are committed and documented.
- Keep shared code in `src/relationalstats/modules/` only when it is genuinely
  reusable across package modules.
- Keep plotting optional through lazy imports.
