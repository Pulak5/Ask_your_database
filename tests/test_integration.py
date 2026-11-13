"""Integration tests — uses MockBackend and mocked DB."""
import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    # Patch execute_query to avoid real DB
    with patch("src.app.main.execute_query") as mock_exec, \
         patch("src.app.main.get_schema_text") as mock_schema, \
         patch("src.app.main.get_known_tables") as mock_tables:
        mock_exec.return_value = (["title"], [{"title": "Test Film"}])
        mock_schema.return_value = "Table: film\n  Columns: film_id, title"
        mock_tables.return_value = {"film", "actor", "category", "rental", "payment", "customer"}

        os.environ["LLM_BACKEND"] = "mock"
        from src.app.main import app
        yield TestClient(app)


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_schema(client):
    resp = client.get("/schema")
    assert resp.status_code == 200
    assert "schema_text" in resp.json()


def test_ask_basic(client):
    resp = client.post("/ask", json={"question": "List all films"})
    assert resp.status_code == 200
    data = resp.json()
    assert "sql" in data
    assert "rows" in data
    assert isinstance(data["rows"], list)


def test_ask_blocked(client):
    # Patch guard to return blocked
    with patch("src.app.main.guard") as mock_guard:
        mock_guard.return_value = MagicMock(
            blocked=True,
            reason="INSERT not allowed",
            sql="INSERT INTO film VALUES (1)",
        )
        resp = client.post("/ask", json={"question": "insert a film"})
        assert resp.status_code == 400


def test_ask_returns_chart_info(client):
    resp = client.post("/ask", json={"question": "List all films"})
    assert resp.status_code == 200
    data = resp.json()
    # chart key may or may not be present, but if it is, it should have a type
    if "chart" in data:
        assert "type" in data["chart"]


def test_ask_missing_question_returns_error(client):
    resp = client.post("/ask", json={})
    assert resp.status_code == 422


def test_health_endpoint_format(client):
    resp = client.get("/health")
    body = resp.json()
    assert "status" in body
