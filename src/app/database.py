"""Database connection and query execution utilities."""
from __future__ import annotations

import os
import urllib.parse
from typing import Any

import psycopg
from psycopg.rows import dict_row


def get_readonly_conn_url() -> str:
    """Assemble connection URL for the read-only role."""
    base_url = os.getenv("DATABASE_URL")
    user = os.getenv("APP_READONLY_USER", "app_readonly")
    password = os.getenv("APP_READONLY_PASSWORD", "app_readonly_password")

    if base_url:
        try:
            parsed = urllib.parse.urlparse(base_url)
            host = parsed.hostname or "localhost"
            port = parsed.port or 5432
            db = parsed.path.lstrip("/") or "ask_your_db"
            return f"postgresql://{user}:{password}@{host}:{port}/{db}"
        except Exception:
            pass

    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "ask_your_db")
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


def get_admin_conn_url() -> str:
    """Assemble connection URL for the administrative/migration role."""
    return os.getenv(
        "DATABASE_URL",
        "postgresql://app:app_password@localhost:5432/ask_your_db",
    )


def execute_query(
    sql: str,
    conn_url: str,
    timeout_seconds: int = 5,
) -> tuple[list[str], list[dict[str, Any]]]:
    """Execute SQL query safely with statement timeout.

    Returns:
        (column_names, list_of_row_dicts)
    """
    timeout_ms = timeout_seconds * 1000
    with psycopg.connect(conn_url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            # Set per-query statement timeout
            cur.execute(f"SET LOCAL statement_timeout = {int(timeout_ms)}")
            cur.execute(sql)
            if cur.description:
                columns = [desc.name for desc in cur.description]
                rows = [dict(r) for r in cur.fetchall()]
                return columns, rows
            return [], []

