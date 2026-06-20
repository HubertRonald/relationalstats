"""Term names for the initial ERGM approximation."""

from __future__ import annotations

DEFAULT_TERMS = ["edges", "common_neighbors", "degree1", "gwesp"]
SUPPORTED_TERMS = {"edges", "common_neighbors", "transitiveties", "degree1", "gwesp"}


def is_nodematch_term(term: str) -> bool:
    """Return whether a term is a nodematch term."""
    return term.startswith("nodematch:")


def validate_terms(terms: list[str] | None) -> list[str]:
    """Validate ERGM approximation terms."""
    selected = DEFAULT_TERMS if terms is None else list(terms)
    unknown = [
        term for term in selected
        if term not in SUPPORTED_TERMS and not is_nodematch_term(term)
    ]
    if unknown:
        raise ValueError(
            "Unknown ERGM term(s): "
            + ", ".join(unknown)
            + ". Supported terms include edges, common_neighbors, transitiveties, "
            "degree1, gwesp, and nodematch:<attribute>."
        )
    return selected
