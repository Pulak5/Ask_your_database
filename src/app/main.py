"""FastAPI backend application for Ask Your Database."""
from __future__ import annotations

import logging
import os
import time
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .charts import generate_plotly_fig, pick_chart
from .database import execute_query, get_admin_conn_url, get_readonly_conn_url
from .llm.factory import get_backend
from .prompts import FEW_SHOT_EXAMPLES, build_prompt
from .schema import get_known_tables, get_schema_text
from .sql_guard import guard

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("ask_your_db")


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Natural language question")
    few_shot: bool = Field(default=False, description="Whether to include few-shot examples")


class AskResponse(BaseModel):
    sql: str
    columns: list[str]
    rows: list[dict[str, Any]]
    chart: dict[str, Any]
    chart_spec: dict[str, Any]
    plotly_fig: dict[str, Any] | None
    latency_ms: float
    backend: str
    blocked: bool = False
    block_reason: str | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Ask Your Database API backend...")
    yield
    logger.info("Shutting down API backend.")


app = FastAPI(
    title="Ask Your Database API",
    version="0.1.0",
    description="Natural language to safe SQL analytics assistant",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint returning system status and active backend."""
    try:
        backend = get_backend()
        backend_name = backend.name
    except Exception as exc:
        backend_name = f"error: {exc}"
    return {"status": "ok", "backend": backend_name}


@app.get("/schema")
def schema() -> dict[str, Any]:
    """Return database schema text and known table list."""
    try:
        admin_url = get_admin_conn_url()
        schema_text = get_schema_text(admin_url)
        tables = sorted(list(get_known_tables(admin_url)))
    except Exception as exc:
        logger.warning("Could not introspect DB schema: %s", exc)
        schema_text = "Schema introspection unavailable (database offline)"
        tables = [
            "country",
            "city",
            "address",
            "customer",
            "language",
            "category",
            "film",
            "film_category",
            "actor",
            "film_actor",
            "store",
            "staff",
            "inventory",
            "rental",
            "payment",
        ]
    return {"schema_text": schema_text, "tables": tables}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    """Process natural language question into safe SQL, execute it, and return visual results."""
    start_time = time.perf_counter()
    backend = get_backend()

    # Introspect or use known schema
    try:
        admin_url = get_admin_conn_url()
        schema_text = get_schema_text(admin_url)
        known_tables = get_known_tables(admin_url)
    except Exception:
        schema_text = "DVD rental database schema"
        known_tables = {
            "country",
            "city",
            "address",
            "customer",
            "language",
            "category",
            "film",
            "film_category",
            "actor",
            "film_actor",
            "store",
            "staff",
            "inventory",
            "rental",
            "payment",
        }

    # 1. Build prompt
    examples = FEW_SHOT_EXAMPLES if req.few_shot else None
    prompt = build_prompt(schema_text, req.question, examples)

    # 2. Generate SQL via pluggable LLMBackend
    try:
        llm_response = backend.generate_sql(prompt)
        generated_sql = llm_response.sql
    except Exception as exc:
        logger.error("LLM backend error: %s", exc)
        raise HTTPException(status_code=500, detail=f"LLM backend generation failed: {exc}")

    # 3. Apply SQL safety guard
    guard_result = guard(generated_sql, known_tables)
    if guard_result.blocked:
        logger.warning(
            "Query blocked by SQL guard. Question: %r, SQL: %r, Reason: %s",
            req.question,
            generated_sql,
            guard_result.reason,
        )
        raise HTTPException(
            status_code=400,
            detail=f"Query blocked by SQL guard: {guard_result.reason}",
        )

    safe_sql = guard_result.sql

    # 4. Execute query using read-only role with timeout
    readonly_url = get_readonly_conn_url()
    timeout_sec = int(os.getenv("QUERY_TIMEOUT_SECONDS", "5"))

    try:
        columns, rows = execute_query(safe_sql, readonly_url, timeout_seconds=timeout_sec)
    except Exception as exc:
        logger.error("Database execution error: %s", exc)
        raise HTTPException(status_code=500, detail=f"Database execution error: {exc}")

    # 5. Chart heuristic and Plotly figure generation
    chart_spec = pick_chart(columns, rows, req.question)
    plotly_fig = None
    try:
        plotly_fig = generate_plotly_fig(chart_spec, rows)
    except Exception as exc:
        logger.warning("Could not generate Plotly figure: %s", exc)

    latency_ms = (time.perf_counter() - start_time) * 1000.0

    logger.info(
        "Successfully answered question: %r | rows: %d | latency: %.1fms",
        req.question,
        len(rows),
        latency_ms,
    )

    return AskResponse(
        sql=safe_sql,
        columns=columns,
        rows=rows,
        chart=chart_spec,
        chart_spec=chart_spec,
        plotly_fig=plotly_fig,
        latency_ms=latency_ms,
        backend=backend.name,
        blocked=False,
        block_reason=None,
    )

