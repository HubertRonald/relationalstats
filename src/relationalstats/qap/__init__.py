"""QAP models for relational data."""

from .model import QAPLogit
from .permutation import dyad_frame, empirical_p_values, generate_permutations, permute_square_matrix
from .results import QAPLogitResult

__all__ = [
    "QAPLogit",
    "QAPLogitResult",
    "dyad_frame",
    "empirical_p_values",
    "generate_permutations",
    "permute_square_matrix",
]
