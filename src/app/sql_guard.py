"""SQL safety guard — defence-in-depth for user-generated queries.
All generated SQL passes through guard() before execution.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

import sqlglot
from sqlglot import exp

logger = logging.getLogger(__name__)

DANGEROUS_FUNCTIONS = frozenset(
    {
        "pg_read_file",
        "pg_sleep",
        "pg_ls_dir",
        "pg_read_binary_file",
        "lo_import",
        "lo_export",
        "lo_creat",
        "lo_unlink",
        "dblink",
        "dblink_exec",
        "copy_file",
        "current_setting",
        "set_config",
        "pg_cancel_backend",
        "pg_terminate_backend",
    }
)

MAX_ROWS = 1000


@dataclass
class GuardResult:
    sql: str
    blocked: bool
    reason: str | None


def guard(sql: str, known_tables: set[str] | None = None) -> GuardResult:
    """Validate and sanitise a SQL string.

    Returns GuardResult with possibly-modified sql, blocked flag, and reason.
    """
    # 1. Strip whitespace; reject empty
    sql = sql.strip()
    if not sql:
        logger.warning("guard: empty SQL blocked")
        return GuardResult(sql=sql, blocked=True, reason="Empty SQL string")

    # 2. Parse with sqlglot
    try:
        statements = sqlglot.parse(sql, dialect="postgres")
    except Exception as exc:
        logger.warning("guard: parse error — %s", exc)
        return GuardResult(sql=sql, blocked=True, reason=f"SQL parse error: {exc}")

    if not statements or len(statements) != 1:
        reason = f"Expected exactly 1 statement, got {len(statements) if statements else 0}"
        logger.warning("guard: %s", reason)
        return GuardResult(sql=sql, blocked=True, reason=reason)

    statement = statements[0]

    # 3. Must be a SELECT or UNION
    if not isinstance(statement, (exp.Select, exp.Union)):
        reason = f"Non-SELECT statement blocked: {type(statement).__name__}"
        logger.warning("guard: %s", reason)
        return GuardResult(sql=sql, blocked=True, reason=reason)

    # Check CTEs if present: all CTE expressions must be Select or Union
    cte_names: set[str] = set()
    for cte in statement.ctes:
        cte_name = cte.alias
        if cte_name:
            cte_names.add(cte_name.lower())
        if not isinstance(cte.this, (exp.Select, exp.Union)):
            reason = f"Non-SELECT statement in CTE: {type(cte.this).__name__}"
            logger.warning("guard: %s", reason)
            return GuardResult(sql=sql, blocked=True, reason=reason)

    # 4. Walk for dangerous functions and forbidden expressions
    for node in statement.walk():
        # Check forbidden statement types nested inside
        if isinstance(node, (exp.Insert, exp.Update, exp.Delete, exp.Drop, exp.Alter, exp.Create)):
            reason = f"Forbidden DDL/DML node blocked: {type(node).__name__}"
            logger.warning("guard: %s", reason)
            return GuardResult(sql=sql, blocked=True, reason=reason)

        if isinstance(node, (exp.Anonymous, exp.Func)):
            func_name = ""
            if isinstance(node, exp.Anonymous):
                func_name = node.name.lower()
            else:
                func_name = (node.sql_name() or "").lower()
            if func_name in DANGEROUS_FUNCTIONS:
                reason = f"Dangerous function blocked: {func_name}"
                logger.warning("guard: %s", reason)
                return GuardResult(sql=sql, blocked=True, reason=reason)

    # 5. Table allow-list check
    if known_tables is not None:
        known_lower = {t.lower() for t in known_tables} | cte_names
        for node in statement.walk():
            if isinstance(node, exp.Table):
                table_name = node.name.lower()
                if table_name and table_name not in known_lower:
                    reason = f"Unknown table referenced: {table_name}"
                    logger.warning("guard: %s", reason)
                    return GuardResult(sql=sql, blocked=True, reason=reason)

    # 6. Inject / cap LIMIT
    limit_node = statement.find(exp.Limit)
    if limit_node is None:
        # No LIMIT — inject one
        statement = statement.limit(MAX_ROWS)
        logger.debug("guard: injected LIMIT %d", MAX_ROWS)
    else:
        # Check existing limit value
        limit_expr = limit_node.expression
        try:
            limit_val = int(limit_expr.name)
            if limit_val > MAX_ROWS:
                limit_node.set("expression", exp.Literal.number(MAX_ROWS))
                logger.debug("guard: capped LIMIT %d -> %d", limit_val, MAX_ROWS)
        except (TypeError, ValueError):
            pass

    # 7. Generate final SQL
    final_sql = statement.sql(dialect="postgres")
    logger.info("guard: allowed SQL: %s", final_sql)
    return GuardResult(sql=final_sql, blocked=False, reason=None)
