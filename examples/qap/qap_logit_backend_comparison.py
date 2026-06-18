"""Compare QAPLogit backend outputs on a toy dataset."""

from __future__ import annotations

from relationalstats.datasets import make_qap_toy_data
from relationalstats.qap import QAPLogit


def main() -> None:
    """Run statsmodels and scikit-learn QAPLogit backends."""
    y, x_matrices = make_qap_toy_data()

    for backend in ["statsmodels", "sklearn"]:
        print("=" * 72)
        print(f"Backend: {backend}")
        print("=" * 72)

        result = QAPLogit(
            n_permutations=99,
            random_state=42,
            backend=backend,
            directed=True,
        ).fit(y, x_matrices)

        print(result.summary())
        print(result.to_dataframe().to_string(index=False))
        print()


if __name__ == "__main__":
    main()
