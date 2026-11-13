"""AWS Bedrock LLM backend (Anthropic Claude models)."""
from __future__ import annotations

import json
import os
import re
import time
from typing import Any

import boto3
import botocore.exceptions

from .base import LLMBackend, LLMResponse

_FENCE_RE = re.compile(r"```(?:sql)?\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)


def _strip_fences(text: str) -> str:
    """Remove ```sql ... ``` or ``` ... ``` markdown fences."""
    match = _FENCE_RE.search(text)
    if match:
        return match.group(1).strip()
    return text.strip()


class BedrockBackend(LLMBackend):
    """LLM backend that invokes Anthropic Claude models via AWS Bedrock."""

    def __init__(
        self,
        model_id: str | None = None,
        region: str | None = None,
    ) -> None:
        self._model_id = model_id or os.getenv(
            "BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0"
        )
        self._region = region or os.getenv("AWS_REGION", "us-east-1")
        self._client: Any = boto3.client("bedrock-runtime", region_name=self._region)

    def generate_sql(self, prompt: str) -> LLMResponse:
        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 512,
                "messages": [{"role": "user", "content": prompt}],
            }
        )
        t0 = time.perf_counter()
        try:
            response = self._client.invoke_model(
                modelId=self._model_id,
                contentType="application/json",
                accept="application/json",
                body=body,
            )
        except botocore.exceptions.ClientError as exc:
            raise RuntimeError(f"Bedrock ClientError: {exc}") from exc
        latency_ms = (time.perf_counter() - t0) * 1000.0

        response_body = json.loads(response["body"].read())
        raw_text: str = response_body["content"][0]["text"]
        sql = _strip_fences(raw_text)
        usage = response_body.get("usage", {})

        return LLMResponse(
            sql=sql,
            raw_response=raw_text,
            prompt_tokens=usage.get("input_tokens", 0),
            completion_tokens=usage.get("output_tokens", 0),
            latency_ms=latency_ms,
            model_id=self._model_id,
        )

    @property
    def name(self) -> str:
        return "bedrock"

