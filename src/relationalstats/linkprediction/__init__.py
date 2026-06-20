"""Link prediction metrics and estimator-style utilities."""

from .metrics import ALL_METRICS
from .proxfun_full import ProxFun, proxfun_full
from .results import ProxFunResult

__all__ = [
    "ALL_METRICS",
    "ProxFun",
    "ProxFunResult",
    "proxfun_full",
]
