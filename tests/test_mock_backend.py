"""Tests for src/app/llm/mock_backend.py — 6 test cases."""
from src.app.llm.base import LLMResponse
from src.app.llm.mock_backend import MockBackend


def test_generate_sql_returns_llm_response():
    backend = MockBackend()
    result = backend.generate_sql("SELECT films")
    assert isinstance(result, LLMResponse)


def test_sql_attribute_is_non_empty_string():
    backend = MockBackend()
    result = backend.generate_sql("List all actors")
    assert isinstance(result.sql, str)
    assert len(result.sql.strip()) > 0


def test_call_count_increments():
    backend = MockBackend()
    assert backend.call_count == 0
    backend.generate_sql("Query 1")
    assert backend.call_count == 1
    backend.generate_sql("Query 2")
    assert backend.call_count == 2
    backend.generate_sql("Query 3")
    assert backend.call_count == 3


def test_custom_response_map_keyword_match():
    backend = MockBackend(
        response_map={"actor": "SELECT first_name, last_name FROM actor"}
    )
    result = backend.generate_sql("Show all actor names")
    assert "actor" in result.sql.lower()


def test_model_id_is_mock():
    backend = MockBackend()
    assert backend.model_id == "mock"


def test_latency_ms_is_non_negative():
    backend = MockBackend()
    result = backend.generate_sql("SELECT 1 FROM film")
    assert hasattr(result, "latency_ms")
    assert result.latency_ms >= 0
