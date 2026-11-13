"""Chart type selection and Plotly figure generation."""
from __future__ import annotations

import plotly.graph_objects as go


def _is_numeric(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def pick_chart(columns: list[str], rows: list[dict], question: str) -> dict:
    """Heuristically pick a chart type based on result shape and question.

    Rules (in priority order):
    1. Any column name contains 'date', 'month', 'year', or 'day' -> line
    2. Question contains 'percent', 'share', 'distribution', or 'ratio' -> pie
    3. 1 column -> table
    4. 2+ columns, one text + one numeric -> bar
    5. Default -> table
    """
    # Rule 1: time-series column names -> line
    time_keywords = {"date", "month", "year", "day"}
    for col in columns:
        if any(kw in col.lower() for kw in time_keywords):
            return {"type": "line", "x": col, "y": _first_numeric_col(columns, rows, exclude=col)}

    # Rule 2: question keywords -> pie
    question_lower = question.lower()
    if any(kw in question_lower for kw in ("percent", "share", "distribution", "ratio")):
        text_col, numeric_col = _split_text_numeric(columns, rows)
        return {"type": "pie", "labels": text_col, "values": numeric_col}

    # Rule 3: single column -> table
    if len(columns) == 1:
        return {"type": "table", "columns": columns}

    # Rule 4: one text + one numeric -> bar
    text_col, numeric_col = _split_text_numeric(columns, rows)
    if text_col and numeric_col:
        return {"type": "bar", "x": text_col, "y": numeric_col}

    # Default
    return {"type": "table", "columns": columns}


def _split_text_numeric(columns: list[str], rows: list[dict]) -> tuple[str | None, str | None]:
    """Return (first_text_column, first_numeric_column) names, or (None, None)."""
    if not rows:
        # Guess from column names when there are no rows
        return (columns[0] if columns else None, columns[1] if len(columns) > 1 else None)

    text_col: str | None = None
    numeric_col: str | None = None
    sample = rows[0]
    for col in columns:
        val = sample.get(col)
        if _is_numeric(val) and numeric_col is None:
            numeric_col = col
        elif not _is_numeric(val) and text_col is None:
            text_col = col
        if text_col and numeric_col:
            break
    return text_col, numeric_col


def _first_numeric_col(columns: list[str], rows: list[dict], exclude: str = "") -> str | None:
    """Return the first column that holds numeric values (excluding *exclude*)."""
    if not rows:
        return next((c for c in columns if c != exclude), None)
    sample = rows[0]
    for col in columns:
        if col == exclude:
            continue
        if _is_numeric(sample.get(col)):
            return col
    return None


def generate_plotly_fig(chart_spec: dict, rows: list[dict]) -> dict:
    """Generate a Plotly figure dict from chart_spec and data rows.

    Returns fig.to_dict() suitable for JSON serialisation.
    """
    chart_type = chart_spec.get("type", "table")

    if chart_type == "bar":
        x_col = chart_spec.get("x", "")
        y_col = chart_spec.get("y", "")
        x_vals = [r.get(x_col) for r in rows]
        y_vals = [r.get(y_col) for r in rows]
        fig = go.Figure(go.Bar(x=x_vals, y=y_vals, name=y_col))
        fig.update_layout(xaxis_title=x_col, yaxis_title=y_col)

    elif chart_type == "line":
        x_col = chart_spec.get("x", "")
        y_col = chart_spec.get("y") or ""
        x_vals = [r.get(x_col) for r in rows]
        y_vals = [r.get(y_col) for r in rows]
        fig = go.Figure(go.Scatter(x=x_vals, y=y_vals, mode="lines+markers", name=y_col))
        fig.update_layout(xaxis_title=x_col, yaxis_title=y_col)

    elif chart_type == "pie":
        labels_col = chart_spec.get("labels", "")
        values_col = chart_spec.get("values", "")
        labels = [r.get(labels_col) for r in rows]
        values = [r.get(values_col) for r in rows]
        fig = go.Figure(go.Pie(labels=labels, values=values))

    else:
        # table (default)
        if rows:
            all_cols = list(rows[0].keys())
        else:
            all_cols = chart_spec.get("columns", [])
        header_values = all_cols
        cell_values = [[r.get(col) for r in rows] for col in all_cols]
        fig = go.Figure(
            go.Table(
                header=dict(values=header_values),
                cells=dict(values=cell_values),
            )
        )

    return fig.to_dict()

