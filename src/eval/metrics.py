"""Evaluation metrics for text-to-SQL execution accuracy."""
from __future__ import annotations

import statistics
from typing import Any


def normalize_value(v: Any) -> Any:
    """Normalize a cell value: round floats, lowercase strings."""
    if isinstance(v, float):
        return round(v, 4)
    if isinstance(v, str):
        return v.strip().lower()
    return v


def normalize_rows(rows: list[dict]) -> list[dict]:
    """Normalize result rows for comparison: sort columns alphabetically, normalize values."""
    if not rows:
        return []
    normalized: list[dict] = []
    for row in rows:
        sorted_items = sorted((k, normalize_value(v)) for k, v in row.items())
        normalized.append(dict(sorted_items))
    return normalized


def _row_to_tuple(row: dict) -> tuple:
    """Convert normalized row dict to tuple of (key, value) pairs."""
    return tuple(sorted((k, normalize_value(v)) for k, v in row.items()))


def result_sets_equal(pred_rows: list[dict], gold_rows: list[dict], ordered: bool = False) -> bool:
    """Compare result sets. ordered=True for ORDER BY queries."""
    norm_pred = [_row_to_tuple(r) for r in normalize_rows(pred_rows)]
    norm_gold = [_row_to_tuple(r) for r in normalize_rows(gold_rows)]

    if ordered:
        return norm_pred == norm_gold
    return sorted(map(str, norm_pred)) == sorted(map(str, norm_gold))


def compute_metrics(results: list[dict]) -> dict:
    """
    Compute aggregate metrics from per-example result dicts.
    Accepts either evaluation output items or items with predicted_rows/gold_rows.
    """
    total = len(results)
    if total == 0:
        return {
            "total": 0,
            "execution_accuracy": 0.0,
            "valid_sql_rate": 0.0,
            "unsafe_rate": 0.0,
            "median_latency_ms": 0.0,
            "p95_latency_ms": 0.0,
            "by_difficulty": {},
            "by_tag": {},
        }

    # Normalize each item to ensure 'correct' and 'valid_sql' are present
    processed = []
    for r in results:
        item = dict(r)
        if "correct" not in item:
            if "predicted_rows" in item and "gold_rows" in item:
                ordered = item.get("ordered", False)
                item["correct"] = result_sets_equal(item["predicted_rows"], item["gold_rows"], ordered=ordered)
                item["valid_sql"] = item.get("valid_sql", True)
            else:
                item["correct"] = False
        if "valid_sql" not in item:
            item["valid_sql"] = item.get("correct", False)
        processed.append(item)

    correct = sum(1 for r in processed if r.get("correct"))
    valid = sum(1 for r in processed if r.get("valid_sql"))
    blocked = sum(1 for r in processed if r.get("blocked"))
    latencies = [r["latency_ms"] for r in processed if r.get("latency_ms") is not None]

    by_difficulty: dict[str, dict] = {}
    for r in processed:
        d = r.get("difficulty", "unknown")
        by_difficulty.setdefault(d, {"total": 0, "correct": 0})
        by_difficulty[d]["total"] += 1
        if r.get("correct"):
            by_difficulty[d]["correct"] += 1

    by_tag: dict[str, dict] = {}
    for r in processed:
        for tag in r.get("tags", []):
            by_tag.setdefault(tag, {"total": 0, "correct": 0})
            by_tag[tag]["total"] += 1
            if r.get("correct"):
                by_tag[tag]["correct"] += 1

    return {
        "total": total,
        "execution_accuracy": correct / total,
        "valid_sql_rate": valid / total,
        "unsafe_rate": blocked / total,
        "median_latency_ms": statistics.median(latencies) if latencies else 0.0,
        "p95_latency_ms": sorted(latencies)[int(0.95 * len(latencies))] if latencies else 0.0,
        "by_difficulty": {d: v["correct"] / v["total"] for d, v in by_difficulty.items()},
        "by_tag": {t: v["correct"] / v["total"] for t, v in by_tag.items()},
    }
