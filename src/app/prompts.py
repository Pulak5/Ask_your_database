"""Single source of truth for all prompt templates.
Training data MUST use this exact format.
"""
from __future__ import annotations

SYSTEM_PROMPT = """You are a PostgreSQL SQL expert. Convert the user's natural language question into a valid, read-only PostgreSQL SELECT query.

Rules:
- Output ONLY the SQL query, nothing else. No explanations, no markdown, no code fences.
- Use only SELECT statements. No INSERT, UPDATE, DELETE, DROP, or other DDL/DML.
- Use only the tables and columns listed in the schema.
- Always use table aliases for clarity in joins.
- If the question cannot be answered with the available schema, output: SELECT 'unanswerable' AS answer;
"""

FEW_SHOT_EXAMPLES = [
    {
        "question": "List the top 5 films by rental rate",
        "sql": "SELECT title, rental_rate FROM film ORDER BY rental_rate DESC LIMIT 5",
    },
    {
        "question": "How many customers are active?",
        "sql": "SELECT COUNT(*) AS active_customers FROM customer WHERE active = true",
    },
    {
        "question": "What are the film categories and how many films are in each?",
        "sql": (
            "SELECT c.name AS category, COUNT(fc.film_id) AS film_count "
            "FROM category c JOIN film_category fc ON c.category_id = fc.category_id "
            "GROUP BY c.name ORDER BY film_count DESC"
        ),
    },
    {
        "question": "Which actors have appeared in the most films?",
        "sql": (
            "SELECT a.first_name || ' ' || a.last_name AS actor_name, COUNT(fa.film_id) AS film_count "
            "FROM actor a JOIN film_actor fa ON a.actor_id = fa.actor_id "
            "GROUP BY a.actor_id, a.first_name, a.last_name ORDER BY film_count DESC LIMIT 10"
        ),
    },
    {
        "question": "What is the total revenue from payments?",
        "sql": "SELECT SUM(amount) AS total_revenue FROM payment",
    },
]


def build_prompt(schema_text: str, question: str, examples: list[dict] | None = None) -> str:
    """Assemble the full prompt. Must be IDENTICAL between training and inference."""
    parts = [f"### Schema:\n{schema_text}"]
    if examples:
        ex_text = "\n\n".join(
            f"### Question:\n{e['question']}\n\n### SQL:\n{e['sql']}" for e in examples
        )
        parts.append(f"### Examples:\n{ex_text}")
    parts.append(f"### Question:\n{question}")
    parts.append("### SQL:")
    return "\n\n".join(parts) + "\n"

