#!/usr/bin/env python3
"""Collect README files for documentation auditing.

Usage:
    python scripts/collect_readmes.py
    python scripts/collect_readmes.py --output _audit/readmes
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

EXCLUDED_DIRS = {
    ".git", ".hg", ".mypy_cache", ".pytest_cache", ".ruff_cache", ".tox",
    ".venv", "__pycache__", "build", "dist", "htmlcov", "node_modules", "site",
}
README_NAMES = {"readme.md", "readme.rst", "readme.txt"}


def iter_readmes(root: Path) -> list[Path]:
    """Return README files under root."""
    return sorted(
        path for path in root.rglob("*")
        if path.is_file()
        and path.name.lower() in README_NAMES
        and not any(part in EXCLUDED_DIRS for part in path.parts)
    )


def safe_name(path: Path) -> str:
    """Return a path-safe file name."""
    return "__".join(path.parts)


def main() -> int:
    """Collect README files into an audit folder."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, default=Path("_audit/readmes"))
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    readmes = iter_readmes(root)
    index_lines = ["# README audit index", ""]
    for readme in readmes:
        rel = readme.relative_to(root)
        target = output / safe_name(rel)
        shutil.copy2(readme, target)
        index_lines.append(f"- `{rel}` -> `{target.relative_to(root)}`")
        print(rel)
    (output / "README_INDEX.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    print(f"\nFound {len(readmes)} README file(s).")
    print(f"Audit copies written to: {output.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
