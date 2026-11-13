"""LLM backend abstract interface."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    sql: str
    raw_response: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: float
    model_id: str


class LLMBackend(ABC):
    """Abstract base for all LLM backends."""

    @abstractmethod
    def generate_sql(self, prompt: str) -> LLMResponse:
        """Generate SQL from an already-assembled prompt string."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable backend name."""
        ...

