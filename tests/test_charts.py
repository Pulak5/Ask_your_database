"""Tests for src/app/charts.py — 7 test cases."""
from src.app.charts import pick_chart


def test_single_column_returns_table():
    columns = ["title"]
    rows = [{"title": "Film A"}, {"title": "Film B"}]
    result = pick_chart(columns, rows, "Show me films")
    assert result["type"] == "table"


def test_text_and_numeric_columns_returns_bar():
    columns = ["rating", "count"]
    rows = [{"rating": "PG", "count": 10}, {"rating": "G", "count": 5}]
    result = pick_chart(columns, rows, "How many films per rating?")
    assert result["type"] == "bar"


def test_month_column_returns_line():
    columns = ["month", "revenue"]
    rows = [{"month": "2024-01", "revenue": 1500.0}]
    result = pick_chart(columns, rows, "Revenue over time")
    assert result["type"] == "line"


def test_question_contains_percent_returns_pie():
    columns = ["category", "count"]
    rows = [{"category": "Action", "count": 20}, {"category": "Drama", "count": 30}]
    result = pick_chart(columns, rows, "What percent of films are in each category?")
    assert result["type"] == "pie"


def test_two_text_columns_returns_table():
    columns = ["first_name", "last_name"]
    rows = [{"first_name": "John", "last_name": "Doe"}]
    result = pick_chart(columns, rows, "List all actors")
    assert result["type"] == "table"


def test_pick_chart_returns_dict_with_type_key():
    columns = ["film_id", "title"]
    rows = [{"film_id": 1, "title": "Film A"}]
    result = pick_chart(columns, rows, "Show films")
    assert isinstance(result, dict)
    assert "type" in result


def test_pick_chart_with_year_column_returns_line():
    columns = ["year", "total_rentals"]
    rows = [{"year": 2005, "total_rentals": 400}, {"year": 2006, "total_rentals": 600}]
    result = pick_chart(columns, rows, "Rentals per year")
    assert result["type"] == "line"
