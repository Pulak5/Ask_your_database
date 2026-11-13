"""OpenAI-compatible LLM backend (vLLM, LM Studio, Ollama, etc.)."""
from __future__ import annotations

import os
import re
import time

import httpx

from .base import LLMBackend, LLMResponse

_FENCE_RE = re.compile(r"```(?:sql)?\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)


def _strip_fences(text: str) -> str:
    """Remove ```sql ... ``` or ``` ... ``` markdown fences from text."""
    match = _FENCE_RE.search(text)
    if match:
        return match.group(1).strip()
    return text.strip()


class OpenAICompatBackend(LLMBackend):
    """Backend that talks to any OpenAI-compatible /chat/completions endpoint."""

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        api_key: str | None = None,
    ) -> None:
        self._base_url = (base_url or os.getenv("OPENAI_COMPAT_BASE_URL", "http://localhost:8080/v1")).rstrip("/")
        self._model = model or os.getenv("OPENAI_COMPAT_MODEL", "Qwen/Qwen2.5-Coder-7B-Instruct")
        self._api_key = api_key or os.getenv("OPENAI_COMPAT_API_KEY", "")
        self._client = httpx.Client(
            base_url=self._base_url,
            headers={"Authorization": f"Bearer {self._api_key}"} if self._api_key else {},
            timeout=60.0,
        )

    def generate_sql(self, prompt: str) -> LLMResponse:
        payload = {
            "model": self._model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
            "max_tokens": 512,
        }
        t0 = time.perf_counter()
        response = self._client.post("/chat/completions", json=payload)
        latency_ms = (time.perf_counter() - t0) * 1000.0

        if response.is_error:
            raise RuntimeError(
                f"OpenAI-compat backend returned HTTP {response.status_code}: {response.text}"
            )

        data = response.json()
        raw_text: str = data["choices"][0]["message"]["content"]
        sql = _strip_fences(raw_text)
        usage = data.get("usage", {})

        return LLMResponse(
            sql=sql,
            raw_response=raw_text,
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            latency_ms=latency_ms,
            model_id=self._model,
        )

    @property
    def name(self) -> str:
        return "openai_compat"

