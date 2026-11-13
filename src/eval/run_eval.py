"""Execution-accuracy evaluator for text-to-SQL.
Usage: python -m src.eval.run_eval --backend mock --run-name baseline_mock
"""
import argparse
import json
import os
from pathlib import Path

import tqdm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", default="mock", choices=["mock", "openai_compat", "bedrock"])
    parser.add_argument("--eval-file", default="data/eval/demo_eval.jsonl")
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--few-shot", action="store_true")
    parser.add_argument("--conn-url", default=None)
    args = parser.parse_args()

    # Set LLM_BACKEND env for factory
    os.environ["LLM_BACKEND"] = args.backend

    from src.app.database import execute_query, get_readonly_conn_url
    from src.app.llm.factory import get_backend
    from src.app.prompts import FEW_SHOT_EXAMPLES, build_prompt
    from src.app.schema import get_known_tables, get_schema_text
    from src.app.sql_guard import guard
    from src.eval.metrics import compute_metrics, result_sets_equal

    conn_url = args.conn_url or get_readonly_conn_url()
    db_available = True
    try:
        schema_text = get_schema_text(conn_url)
        known_tables = get_known_tables(conn_url)
    except Exception as exc:
        db_available = False
        print(f"Notice: Database connection not available ({exc}). Loading static schema description.")
        desc_path = Path("data/demo_db/schema_description.txt")
        schema_text = desc_path.read_text(encoding="utf-8") if desc_path.exists() else "DVD rental schema"
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
    backend = get_backend()

    examples = FEW_SHOT_EXAMPLES if args.few_shot else None

    eval_examples = [
        json.loads(line)
        for line in Path(args.eval_file).read_text().splitlines()
        if line.strip()
    ]

    out_dir = Path("results") / args.run_name
    out_dir.mkdir(parents=True, exist_ok=True)

    results = []
    with open(out_dir / "predictions.jsonl", "w") as f_out:
        for ex in tqdm.tqdm(eval_examples):
            result = {
                "id": ex["id"],
                "question": ex["question"],
                "gold_sql": ex["gold_sql"],
                "difficulty": ex.get("difficulty"),
                "tags": ex.get("tags", []),
            }
            try:
                prompt = build_prompt(schema_text, ex["question"], examples)
                llm_resp = backend.generate_sql(prompt)
                result["predicted_sql"] = llm_resp.sql
                result["latency_ms"] = llm_resp.latency_ms

                guard_result = guard(llm_resp.sql, known_tables)
                result["blocked"] = guard_result.blocked

                if guard_result.blocked:
                    result["valid_sql"] = False
                    result["correct"] = False
                    result["error"] = f"blocked: {guard_result.reason}"
                elif not db_available:
                    result["valid_sql"] = False
                    result["correct"] = False
                    result["error"] = "Database offline (run 'docker compose up -d db' to start PostgreSQL)"
                else:
                    try:
                        _, pred_rows = execute_query(guard_result.sql, conn_url)
                        result["valid_sql"] = True
                        _, gold_rows = execute_query(ex["gold_sql"], conn_url)
                        ordered = "order by" in ex["gold_sql"].lower()
                        result["correct"] = result_sets_equal(pred_rows, gold_rows, ordered)
                    except Exception as e:
                        result["valid_sql"] = False
                        result["correct"] = False
                        result["error"] = str(e)
            except Exception as e:
                result["valid_sql"] = False
                result["correct"] = False
                result["blocked"] = False
                result["error"] = str(e)
                result["latency_ms"] = 0

            results.append(result)
            f_out.write(json.dumps(result) + "\n")

    metrics = compute_metrics(results)
    print("\n=== Evaluation Results ===")
    print(json.dumps(metrics, indent=2))

    # Append row to results summary
    summary_path = out_dir / "metrics.json"
    summary_path.write_text(json.dumps(metrics, indent=2))
    print(f"\nMetrics saved to {summary_path}")

    return metrics


if __name__ == "__main__":
    main()
