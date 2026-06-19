#!/usr/bin/env python3
"""Replace GitHub-blocked LaTeX macros in Markdown files.

Default replacements:
    \operatorname{...}  -> \text{...}
    \operatorname*{...} -> \text{...}

Usage:
    python scripts/fix_github_math_macros.py --check
    python scripts/fix_github_math_macros.py --dry-run
    python scripts/fix_github_math_macros.py --write
"""

from __future__ import annotations

import argparse
from pathlib import Path

EXCLUDED_DIRS = {
    ".git", ".hg", ".mypy_cache", ".pytest_cache", ".ruff_cache", ".tox",
    ".venv", "__pycache__", "build", "dist", "htmlcov", "node_modules", "site",
}
REPLACEMENTS = {r"\operatorname*{": r"\text{", r"\operatorname{": r"\text{"}


def iter_markdown_files(root: Path) -> list[Path]:
    """Return Markdown files under root, excluding generated/local folders."""
    return sorted(
        path for path in root.rglob("*.md")
        if path.is_file() and not any(part in EXCLUDED_DIRS for part in path.parts)
    )


def apply_replacements(text: str) -> tuple[str, int]:
    """Apply macro replacements and return updated text plus count."""
    updated = text
    count = 0
    for old, new in REPLACEMENTS.items():
        count += updated.count(old)
        updated = updated.replace(old, new)
    return updated, count


def main() -> int:
    """Run the Markdown macro fixer."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    changed: list[tuple[Path, int]] = []
    for path in iter_markdown_files(root):
        text = path.read_text(encoding="utf-8")
        updated, count = apply_replacements(text)
        if count:
            changed.append((path, count))
            if args.write:
                path.write_text(updated, encoding="utf-8")
    if changed:
        for path, count in changed:
            print(f"{path.relative_to(root)}: {count} replacement(s)")
        if args.check:
            print("Blocked GitHub math macros found. Run with --write to fix them.")
            return 1
    else:
        print("No blocked GitHub math macros found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
