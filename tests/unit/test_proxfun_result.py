"""Unit tests for ProxFunResult."""

from __future__ import annotations

import pandas as pd
import pytest

from relationalstats.linkprediction.results import ProxFunResult


def make_result() -> ProxFunResult:
    """Create a small reusable result fixture."""
    scores = pd.DataFrame(
        {
            "source": [0, 0, 1],
            "target": [2, 3, 3],
            "jaccard": [1.0, 0.25, 0.5],
            "adamic_adar": [1.44, 0.20, 0.70],
        }
    )

    return ProxFunResult(
        scores_=scores,
        metrics_=["jaccard", "adamic_adar"],
        directed_=False,
    )


def test_result_validates_dataframe_input() -> None:
    with pytest.raises(TypeError):
        ProxFunResult(scores_=[{"source": 0, "target": 1}], metrics_=[])


def test_result_requires_pair_columns() -> None:
    scores = pd.DataFrame({"source": [0], "jaccard": [1.0]})

    with pytest.raises(ValueError, match="source, target"):
        ProxFunResult(scores_=scores, metrics_=["jaccard"])


def test_len_and_empty_properties() -> None:
    result = make_result()

    assert len(result) == 3
    assert result.is_empty is False


def test_pair_and_score_columns() -> None:
    result = make_result()

    assert result.pair_columns == ["source", "target"]
    assert result.score_columns == ["jaccard", "adamic_adar"]


def test_to_dataframe_returns_copy_by_default() -> None:
    result = make_result()
    df = result.to_dataframe()
    df.loc[0, "jaccard"] = -999

    assert result.scores_.loc[0, "jaccard"] == 1.0


def test_to_dataframe_can_return_internal_reference() -> None:
    result = make_result()
    df = result.to_dataframe(copy=False)

    assert df is result.scores_


def test_pairs_returns_only_source_and_target() -> None:
    result = make_result()

    pairs = result.pairs()

    assert list(pairs.columns) == ["source", "target"]
    assert pairs.shape == (3, 2)


def test_metric_frame_returns_selected_metrics_with_pairs() -> None:
    result = make_result()

    frame = result.metric_frame(["jaccard"])

    assert list(frame.columns) == ["source", "target", "jaccard"]


def test_metric_frame_can_exclude_pairs() -> None:
    result = make_result()

    frame = result.metric_frame(["jaccard"], include_pairs=False)

    assert list(frame.columns) == ["jaccard"]


def test_metric_frame_rejects_unknown_metric_column() -> None:
    result = make_result()

    with pytest.raises(ValueError, match="not available"):
        result.metric_frame(["resource_allocation"])


def test_require_metric_defaults_to_first_score_column() -> None:
    result = make_result()

    assert result.require_metric() == "jaccard"


def test_require_metric_rejects_unknown_metric() -> None:
    result = make_result()

    with pytest.raises(ValueError, match="Available score columns"):
        result.require_metric("resource_allocation")


def test_sort_by_orders_scores() -> None:
    result = make_result()

    sorted_scores = result.sort_by("jaccard")

    assert sorted_scores.iloc[0]["jaccard"] == 1.0
    assert sorted_scores.iloc[-1]["jaccard"] == 0.25


def test_top_k_returns_highest_scores_by_default() -> None:
    result = make_result()

    top = result.top_k(k=2, metric="jaccard")

    assert len(top) == 2
    assert list(top["jaccard"]) == [1.0, 0.5]


def test_top_k_can_rank_ascending_for_distances() -> None:
    result = ProxFunResult(
        scores_=pd.DataFrame(
            {
                "source": [0, 0, 1],
                "target": [1, 2, 2],
                "shortest_path": [1.0, 3.0, 2.0],
            }
        ),
        metrics_=["shortest_path"],
    )

    top = result.top_k(k=2, metric="shortest_path", ascending=True)

    assert list(top["shortest_path"]) == [1.0, 2.0]


def test_top_k_rejects_non_positive_k() -> None:
    result = make_result()

    with pytest.raises(ValueError, match="positive"):
        result.top_k(k=0)


def test_top_k_handles_missing_values() -> None:
    result = ProxFunResult(
        scores_=pd.DataFrame(
            {
                "source": [0, 0, 1],
                "target": [1, 2, 2],
                "jaccard": [1.0, None, 0.5],
            }
        ),
        metrics_=["jaccard"],
    )

    top = result.top_k(k=3, metric="jaccard")

    assert len(top) == 2
    assert top["jaccard"].isna().sum() == 0


def test_result_without_score_columns_raises_for_ranking() -> None:
    result = ProxFunResult(
        scores_=pd.DataFrame({"source": [], "target": []}),
        metrics_=[],
    )

    with pytest.raises(ValueError, match="No score columns"):
        result.top_k(k=1)
