"""Schema introspection and caching."""
from __future__ import annotations

import time

import psycopg
from psycopg.rows import dict_row

_cache: dict[str, tuple[float, dict[str, list[str]]]] = {}
_CACHE_TTL = 60.0

_SCHEMA_QUERY = """
SELECT table_name, column_name
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position
"""


def get_schema_dict(conn_url: str) -> dict[str, list[str]]:
    """Return {table_name: [column_names]} for all user tables in the public schema.

    Results are cached per connection URL with a TTL of _CACHE_TTL seconds.
    """
    now = time.monotonic()
    if conn_url in _cache:
        cached_at, cached_data = _cache[conn_url]
        if now - cached_at < _CACHE_TTL:
            return cached_data

    schema: dict[str, list[str]] = {}
    with psycopg.connect(conn_url, row_factory=dict_row, connect_timeout=3) as conn:
        with conn.cursor() as cur:
            cur.execute(_SCHEMA_QUERY)
            for row in cur.fetchall():
                table = row["table_name"]
                column = row["column_name"]
                schema.setdefault(table, []).append(column)

    _cache[conn_url] = (now, schema)
    return schema


def get_known_tables(conn_url: str) -> set[str]:
    """Return the set of table names in the public schema."""
    return set(get_schema_dict(conn_url).keys())


def get_schema_text(conn_url: str) -> str:
    """Return formatted schema text for LLM prompt injection."""
    schema = get_schema_dict(conn_url)
    lines: list[str] = []
    for table, cols in sorted(schema.items()):
        lines.append(f"Table: {table}")
        lines.append(f"  Columns: {', '.join(cols)}")
    return "\n".join(lines)

