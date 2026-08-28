#!/usr/bin/env python3
"""Fix Markdown math rendering issues for GitHub/VitePress docs.

This script is intentionally scoped to formula documentation pages only.

It fixes common Markdown math issues seen in GitHub rendering:

- Replaces blocked or fragile custom operator macros.
- Escapes underscores in math labels.
- Converts selected text labels to \\mathrm{...}.
- Compacts display math blocks to make GitHub rendering more stable.

Usage:
    python scripts/fix_formula_rendering.py --check
    python scripts/fix_formula_rendering.py --dry-run
    python scripts/fix_formula_rendering.py --write
"""

from __future__ import annotations

import argparse
import difflib
import re
from pathlib import Path


TARGET_FILES = [
    Path("docs/qap/formulas.md"),
    Path("docs/ergm/formulas.md"),
    Path("docs/stergm/formulas.md"),
]


EXACT_REPLACEMENTS = {
    r"\operatorname*{": r"\mathrm{",
    r"\operatorname{": r"\mathrm{",
    r"\text{logit}": r"\mathrm{logit}",
    r"\text{Bernoulli}": r"\mathrm{Bernoulli}",
    r"\text{NR}": r"\mathrm{NR}",
    r"\text{edges}": r"\mathrm{edges}",
    r"\text{degree1}": r"\mathrm{degree1}",
    r"\text{gwesp}": r"\mathrm{gwesp}",
    r"\text{transitiveties}": r"\mathrm{transitiveties}",
    r"\text{common_neighbors}": r"\mathrm{common\_neighbors}",
    r"\text{common\_neighbors}": r"\mathrm{common\_neighbors}",
    r"\text{nodematch:attr}": r"\mathrm{nodematch:attr}",
}


def escape_underscore_labels(text: str) -> str:
    """Convert text labels with underscores into math-safe roman labels.

    Example:
        \\text{common_neighbors} -> \\mathrm{common\\_neighbors}

    This intentionally avoids changing prose-like \\text{if } or
    \\text{otherwise}, which are fine inside cases blocks.
    """

    pattern = re.compile(r"\\text\{([A-Za-z0-9:]+(?:_[A-Za-z0-9:]+)+)\}")

    def replace(match: re.Match[str]) -> str:
        label = match.group(1).replace("_", r"\_")
        return rf"\mathrm{{{label}}}"

    return pattern.sub(replace, text)


def normalize_display_math_blocks(text: str) -> str:
    """Compact Markdown display math blocks delimited by lines containing $$.

    GitHub can be more fragile with highly split multiline display formulas.
    This keeps each display formula as:

        $$
        formula
        $$

    Code fences are skipped.
    """

    lines = text.splitlines(keepends=True)

    output: list[str] = []
    math_buffer: list[str] = []

    in_code_fence = False
    in_math_block = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            if not in_math_block:
                in_code_fence = not in_code_fence
            output.append(line)
            continue

        if not in_code_fence and stripped == "$$":
            if not in_math_block:
                output.append(line)
                in_math_block = True
                math_buffer = []
            else:
                compact_formula = " ".join(
                    item.strip() for item in math_buffer if item.strip()
                )
                compact_formula = re.sub(r"\s+", " ", compact_formula)

                if compact_formula:
                    output.append(compact_formula + "\n")

                output.append(line)
                in_math_block = False
                math_buffer = []
            continue

        if in_math_block:
            math_buffer.append(line)
        else:
            output.append(line)

    if in_math_block:
        output.extend(math_buffer)

    return "".join(output)


def fix_content(text: str) -> str:
    """Apply all formula rendering fixes."""
    updated = text

    for old, new in EXACT_REPLACEMENTS.items():
        updated = updated.replace(old, new)

    updated = escape_underscore_labels(updated)
    updated = normalize_display_math_blocks(updated)

    return updated


def unified_diff(path: Path, before: str, after: str) -> str:
    """Return a unified diff for display."""
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=f"a/{path}",
            tofile=f"b/{path}",
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Fail if changes are needed.")
    mode.add_argument("--dry-run", action="store_true", help="Show planned changes.")
    mode.add_argument("--write", action="store_true", help="Write changes in place.")
    args = parser.parse_args()

    changed_files: list[Path] = []

    for path in TARGET_FILES:
        if not path.exists():
            raise FileNotFoundError(f"Missing target file: {path}")

        before = path.read_text(encoding="utf-8")
        after = fix_content(before)

        if before == after:
            continue

        changed_files.append(path)

        if args.dry_run:
            print(unified_diff(path, before, after))

        if args.write:
            path.write_text(after, encoding="utf-8")
            print(f"updated: {path}")

    if changed_files and args.check:
        print("Formula rendering fixes are needed:")
        for path in changed_files:
            print(f"- {path}")
        return 1

    if not changed_files:
        print("No formula rendering fixes needed.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
