"""Tests for src/app/prompts.py — 8 test cases."""
from src.app.prompts import FEW_SHOT_EXAMPLES, SYSTEM_PROMPT, build_prompt


def test_build_prompt_returns_string():
    result = build_prompt("Table: film\n  Columns: film_id, title", "List all films")
    assert isinstance(result, str)


def test_build_prompt_contains_question():
    question = "How many films are rated PG?"
    result = build_prompt("Table: film\n  Columns: film_id, title", question)
    assert question in result


def test_build_prompt_contains_schema_text():
    schema = "Table: film\n  Columns: film_id, title, rating"
    result = build_prompt(schema, "List all films")
    assert schema in result


def test_build_prompt_with_examples_includes_sql():
    examples = [{"question": "List films", "sql": "SELECT title FROM film"}]
    result = build_prompt("Table: film", "List all films", examples=examples)
    assert "SELECT title FROM film" in result


def test_build_prompt_ends_with_sql_marker():
    result = build_prompt("Table: film", "List all films")
    assert result.rstrip().endswith("### SQL:") or result.endswith("### SQL:\n")


def test_build_prompt_without_examples_works():
    result = build_prompt("Table: film\n  Columns: film_id", "List films", examples=None)
    assert isinstance(result, str)
    assert len(result) > 0


def test_few_shot_examples_structure():
    assert isinstance(FEW_SHOT_EXAMPLES, list)
    assert len(FEW_SHOT_EXAMPLES) > 0
    for ex in FEW_SHOT_EXAMPLES:
        assert isinstance(ex, dict)
        assert "question" in ex
        assert "sql" in ex


def test_system_prompt_is_non_empty_string():
    assert isinstance(SYSTEM_PROMPT, str)
    assert len(SYSTEM_PROMPT.strip()) > 0
