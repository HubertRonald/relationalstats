"""Toy QAPLogit example."""

from __future__ import annotations

from relationalstats.datasets import make_qap_toy_data
from relationalstats.qap import QAPLogit


def main() -> None:
    """Run a small synthetic QAP logistic-regression example."""
    y, x_matrices = make_qap_toy_data()

    result = QAPLogit(
        n_permutations=99,
        random_state=42,
        directed=True,
    ).fit(y, x_matrices)

    print(result.summary())
    print()
    print(result.to_dataframe().to_string(index=False))


if __name__ == "__main__":
    main()
