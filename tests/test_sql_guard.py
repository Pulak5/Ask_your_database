"""Tests for src/app/sql_guard.py — 35+ test cases."""
from src.app.sql_guard import GuardResult, guard

# ---------------------------------------------------------------------------
# SAFE cases — blocked must be False
# ---------------------------------------------------------------------------

def test_simple_select():
    r = guard("SELECT title FROM film", known_tables={"film"})
    assert isinstance(r, GuardResult)
    assert r.blocked is False


def test_select_with_where():
    r = guard("SELECT * FROM film WHERE rating = 'PG'", known_tables={"film"})
    assert r.blocked is False


def test_select_with_join():
    sql = (
        "SELECT f.title, c.name FROM film f "
        "JOIN film_category fc ON f.film_id = fc.film_id "
        "JOIN category c ON fc.category_id = c.category_id"
    )
    r = guard(sql, known_tables={"film", "film_category", "category"})
    assert r.blocked is False


def test_select_with_group_by():
    r = guard("SELECT rating, COUNT(*) FROM film GROUP BY rating", known_tables={"film"})
    assert r.blocked is False


def test_select_with_having():
    r = guard(
        "SELECT rating, COUNT(*) FROM film GROUP BY rating HAVING COUNT(*) > 5",
        known_tables={"film"},
    )
    assert r.blocked is False


def test_select_with_order_by_limit():
    r = guard(
        "SELECT title FROM film ORDER BY rental_rate DESC LIMIT 10",
        known_tables={"film"},
    )
    assert r.blocked is False


def test_cte():
    sql = (
        "WITH top AS (SELECT film_id, COUNT(*) AS cnt FROM rental GROUP BY film_id) "
        "SELECT film_id, cnt FROM top ORDER BY cnt DESC LIMIT 5"
    )
    r = guard(sql, known_tables={"rental"})
    assert r.blocked is False


def test_subquery():
    sql = (
        "SELECT title FROM film WHERE film_id IN "
        "(SELECT film_id FROM film_category WHERE category_id = 1)"
    )
    r = guard(sql, known_tables={"film", "film_category"})
    assert r.blocked is False


def test_aggregate_functions():
    r = guard(
        "SELECT COUNT(*), SUM(amount), AVG(amount) FROM payment",
        known_tables={"payment"},
    )
    assert r.blocked is False


def test_case_when():
    sql = (
        "SELECT title, CASE WHEN rental_rate > 4 THEN 'expensive' ELSE 'cheap' END AS price_tier "
        "FROM film"
    )
    r = guard(sql, known_tables={"film"})
    assert r.blocked is False


def test_coalesce():
    r = guard(
        "SELECT title, COALESCE(description, 'N/A') FROM film",
        known_tables={"film"},
    )
    assert r.blocked is False


def test_date_trunc():
    r = guard(
        "SELECT DATE_TRUNC('month', payment_date), SUM(amount) FROM payment GROUP BY 1",
        known_tables={"payment"},
    )
    assert r.blocked is False


def test_lower_upper():
    r = guard(
        "SELECT LOWER(first_name), UPPER(last_name) FROM actor",
        known_tables={"actor"},
    )
    assert r.blocked is False


def test_distinct():
    r = guard("SELECT DISTINCT rating FROM film", known_tables={"film"})
    assert r.blocked is False


def test_exists():
    sql = (
        "SELECT title FROM film f WHERE EXISTS "
        "(SELECT 1 FROM inventory i WHERE i.film_id = f.film_id)"
    )
    r = guard(sql, known_tables={"film", "inventory"})
    assert r.blocked is False


def test_no_limit_injects_limit():
    """A SELECT without LIMIT should have LIMIT injected."""
    r = guard("SELECT title FROM film", known_tables={"film"})
    assert r.blocked is False
    assert "LIMIT" in r.sql.upper()


def test_limit_under_1000_preserved():
    r = guard("SELECT title FROM film LIMIT 50", known_tables={"film"})
    assert r.blocked is False
    assert "50" in r.sql
    assert "1000" not in r.sql


# ---------------------------------------------------------------------------
# UNSAFE cases — blocked must be True
# ---------------------------------------------------------------------------

def test_insert_blocked():
    r = guard("INSERT INTO film (title) VALUES ('hack')", known_tables={"film"})
    assert r.blocked is True


def test_update_blocked():
    r = guard("UPDATE film SET title = 'hack' WHERE film_id = 1", known_tables={"film"})
    assert r.blocked is True


def test_delete_blocked():
    r = guard("DELETE FROM film WHERE film_id = 1", known_tables={"film"})
    assert r.blocked is True


def test_drop_table_blocked():
    r = guard("DROP TABLE film", known_tables={"film"})
    assert r.blocked is True


def test_alter_table_blocked():
    r = guard("ALTER TABLE film ADD COLUMN pwned TEXT", known_tables={"film"})
    assert r.blocked is True


def test_truncate_blocked():
    r = guard("TRUNCATE TABLE film", known_tables={"film"})
    assert r.blocked is True


def test_create_table_blocked():
    r = guard("CREATE TABLE evil (id SERIAL)", known_tables={"film"})
    assert r.blocked is True


def test_grant_blocked():
    r = guard("GRANT ALL ON film TO public", known_tables={"film"})
    assert r.blocked is True


def test_multiple_statements_blocked():
    r = guard("SELECT 1; DROP TABLE film", known_tables={"film"})
    assert r.blocked is True


def test_copy_blocked():
    r = guard("COPY film TO '/tmp/data.csv'", known_tables={"film"})
    assert r.blocked is True


def test_pg_read_file_blocked():
    r = guard("SELECT pg_read_file('/etc/passwd')", known_tables={"film"})
    assert r.blocked is True


def test_pg_sleep_blocked():
    r = guard("SELECT pg_sleep(10)", known_tables={"film"})
    assert r.blocked is True


def test_dblink_blocked():
    r = guard("SELECT dblink('host=evil.com', 'SELECT 1')", known_tables={"film"})
    assert r.blocked is True


def test_lo_import_blocked():
    r = guard("SELECT lo_import('/etc/shadow')", known_tables={"film"})
    assert r.blocked is True


def test_unknown_table_blocked():
    r = guard("SELECT * FROM evil_table", known_tables={"film"})
    assert r.blocked is True


def test_prompt_injection_multi_statement_blocked():
    r = guard(
        "SELECT title FROM film; DROP TABLE customer",
        known_tables={"film", "customer"},
    )
    assert r.blocked is True


def test_limit_cap_to_1000():
    """LIMIT 999999 should be capped to 1000."""
    r = guard("SELECT title FROM film LIMIT 999999", known_tables={"film"})
    assert r.blocked is False
    assert "1000" in r.sql
    assert "999999" not in r.sql


def test_empty_string_blocked():
    r = guard("", known_tables={"film"})
    assert r.blocked is True


# ---------------------------------------------------------------------------
# Extra edge-case tests (beyond the 35 required)
# ---------------------------------------------------------------------------

def test_guard_result_has_sql_attribute():
    r = guard("SELECT 1 FROM film", known_tables={"film"})
    assert hasattr(r, "sql")


def test_guard_result_has_reason_when_blocked():
    r = guard("DROP TABLE film", known_tables={"film"})
    assert r.blocked is True
    assert r.reason  # non-empty reason string


def test_whitespace_only_blocked():
    r = guard("   ", known_tables={"film"})
    assert r.blocked is True


def test_insert_case_insensitive():
    r = guard("insert into film (title) values ('x')", known_tables={"film"})
    assert r.blocked is True


def test_safe_query_returns_guard_result_type():
    r = guard("SELECT film_id FROM film", known_tables={"film"})
    assert isinstance(r, GuardResult)
