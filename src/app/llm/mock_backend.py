"""Mock LLM backend for testing and development."""
from __future__ import annotations

from .base import LLMBackend, LLMResponse


class MockBackend(LLMBackend):
    """A mock LLM backend for testing.

    Accepts an optional response_map dict mapping question keywords -> SQL.
    If no keyword matches, falls back to a default SELECT query.
    Tracks the number of calls made via call_count.
    """

    DEFAULT_SQL = "SELECT title FROM film LIMIT 10"

    def __init__(self, response_map: dict[str, str] | None = None) -> None:
        self._response_map: dict[str, str] = response_map or {}
        self.call_count: int = 0
        self.model_id: str = "mock"

    def generate_sql(self, prompt: str) -> LLMResponse:
        """Return a canned SQL response based on keyword matching."""
        self.call_count += 1
        sql = self.DEFAULT_SQL
        prompt_lower = prompt.lower()
        for keyword, mapped_sql in self._response_map.items():
            if keyword.lower() in prompt_lower:
                sql = mapped_sql
                break
        return LLMResponse(
            sql=sql,
            raw_response=sql,
            prompt_tokens=0,
            completion_tokens=0,
            latency_ms=0.1,
            model_id="mock",
        )

    @property
    def name(self) -> str:
        return "mock"
