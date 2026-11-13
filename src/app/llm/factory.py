"""Factory function for LLM backends."""
from __future__ import annotations

import os

from .base import LLMBackend


def get_backend() -> LLMBackend:
    """Return the appropriate LLM backend based on the LLM_BACKEND env var.

    Supported values (case-insensitive):
        - "mock"           -> MockBackend  (default)
        - "openai_compat"  -> OpenAICompatBackend
        - "bedrock"        -> BedrockBackend
    """
    backend_name = os.getenv("LLM_BACKEND", "mock").lower().strip()

    if backend_name == "mock":
        from .mock_backend import MockBackend
        return MockBackend()

    if backend_name in ("openai_compat", "openai"):
        from .openai_compat_backend import OpenAICompatBackend
        return OpenAICompatBackend()

    if backend_name == "bedrock":
        from .bedrock_backend import BedrockBackend
        return BedrockBackend()

    raise ValueError(
        f"Unknown LLM_BACKEND value: {backend_name!r}. "
        "Choose one of: mock, openai_compat, bedrock."
    )

