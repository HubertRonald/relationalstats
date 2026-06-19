"""STERGM-inspired separable temporal approximations."""

from .model import STERGM
from .results import STERGMResult, STERGMStageResult
from .temporal_utils import add_temporal_structural_features, build_stergm_datasets

__all__ = [
    "STERGM",
    "STERGMResult",
    "STERGMStageResult",
    "add_temporal_structural_features",
    "build_stergm_datasets",
]
