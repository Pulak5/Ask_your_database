"""Tests for src/eval/metrics.py — 14 test cases."""
from src.eval.metrics import compute_metrics, normalize_rows, result_sets_equal

# ---------------------------------------------------------------------------
# result_sets_equal
# ---------------------------------------------------------------------------

def test_result_sets_equal_same_order():
    rows = [{"title": "Film A", "rating": "PG"}, {"title": "Film B", "rating": "G"}]
    assert result_sets_equal(rows, rows) is True


def test_result_sets_equal_different_order():
    a = [{"title": "Film A"}, {"title": "Film B"}]
    b = [{"title": "Film B"}, {"title": "Film A"}]
    assert result_sets_equal(a, b) is True


def test_result_sets_equal_different_values():
    a = [{"title": "Film A"}]
    b = [{"title": "Film X"}]
    assert result_sets_equal(a, b) is False


def test_result_sets_equal_both_empty():
    assert result_sets_equal([], []) is True


def test_result_sets_equal_empty_vs_nonempty():
    assert result_sets_equal([], [{"title": "Film A"}]) is False


def test_result_sets_equal_float_normalization():
    a = [{"v": 1.5}]
    b = [{"v": 1.5000}]
    assert result_sets_equal(a, b) is True


def test_result_sets_equal_string_case_insensitive():
    a = [{"name": "HELLO"}]
    b = [{"name": "hello"}]
    assert result_sets_equal(a, b) is True


def test_result_sets_equal_ordered_wrong_order():
    a = [{"title": "Film A"}, {"title": "Film B"}]
    b = [{"title": "Film B"}, {"title": "Film A"}]
    assert result_sets_equal(a, b, ordered=True) is False


def test_result_sets_equal_ordered_correct_order():
    a = [{"title": "Film A"}, {"title": "Film B"}]
    b = [{"title": "Film A"}, {"title": "Film B"}]
    assert result_sets_equal(a, b, ordered=True) is True


# ---------------------------------------------------------------------------
# compute_metrics
# ---------------------------------------------------------------------------

def test_compute_metrics_all_correct():
    items = [
        {
            "predicted_rows": [{"title": "Film A"}],
            "gold_rows": [{"title": "Film A"}],
            "difficulty": "easy",
        }
    ]
    metrics = compute_metrics(items)
    assert metrics["execution_accuracy"] == 1.0


def test_compute_metrics_none_correct():
    items = [
        {
            "predicted_rows": [{"title": "Film X"}],
            "gold_rows": [{"title": "Film A"}],
            "difficulty": "easy",
        }
    ]
    metrics = compute_metrics(items)
    assert metrics["execution_accuracy"] == 0.0


def test_compute_metrics_by_difficulty():
    items = [
        {
            "predicted_rows": [{"title": "Film A"}],
            "gold_rows": [{"title": "Film A"}],
            "difficulty": "easy",
        },
        {
            "predicted_rows": [{"title": "Film X"}],
            "gold_rows": [{"title": "Film B"}],
            "difficulty": "hard",
        },
    ]
    metrics = compute_metrics(items)
    assert "by_difficulty" in metrics
    assert metrics["by_difficulty"]["easy"] == 1.0
    assert metrics["by_difficulty"]["hard"] == 0.0


# ---------------------------------------------------------------------------
# normalize_rows
# ---------------------------------------------------------------------------

def test_normalize_rows_empty():
    assert normalize_rows([]) == []


def test_normalize_rows_sorts_columns_alphabetically():
    rows = [{"z_col": 1, "a_col": 2}]
    normalized = normalize_rows(rows)
    assert len(normalized) == 1
    keys = list(normalized[0].keys())
    assert keys == sorted(keys)
