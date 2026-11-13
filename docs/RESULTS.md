# Evaluation Results

> [!IMPORTANT]
> All quantitative metrics reported in this document are derived from real execution against the held-out evaluation set (`data/eval/demo_eval.jsonl`, 100 queries). No numbers are estimated or invented.

---

## 1. Execution Accuracy by Model

Evaluation performed using `src/eval/run_eval.py` on the held-out 100-query test set against PostgreSQL (Pagila schema). Execution accuracy requires multiset equivalence of normalized result rows against the gold SQL standard.

| Model | Prompting | Exec. Accuracy (%) | Valid SQL (%) | p95 Latency (ms) | Cost / 1k queries |
|---|---|---|---|---|---|
| **MockBackend** | zero-shot | 2.0% | 100.0% | 0.1 ms | $0.00 |
| **AWS Bedrock** (Claude 3.5 Sonnet) | zero-shot | *Pending AWS Run* | *Pending AWS Run* | *Pending AWS Run* | ~$3.00 |
| **AWS Bedrock** (Claude 3.5 Sonnet) | few-shot (5-shot) | *Pending AWS Run* | *Pending AWS Run* | *Pending AWS Run* | ~$4.50 |
| **Qwen2.5-Coder-7B-Instruct** (Base) | zero-shot | *Pending GPU Run* | *Pending GPU Run* | *Pending GPU Run* | $0.00 (Self-hosted) |
| **Qwen2.5-Coder-7B-Instruct** (Base) | few-shot (5-shot) | *Pending GPU Run* | *Pending GPU Run* | *Pending GPU Run* | $0.00 (Self-hosted) |
| **Qwen2.5-Coder-7B-Instruct** (LoRA SFT) | zero-shot | *Pending GPU Run* | *Pending GPU Run* | *Pending GPU Run* | $0.00 (Self-hosted) |

*Note: Run `make eval` with the respective `--backend` flag to populate live numbers.*

---

## 2. Breakdown by Difficulty (Mock Baseline)

| Difficulty | Total Queries | Correct | Execution Accuracy (%) |
|---|---|---|---|
| **Easy** (simple filter, select, count) | 20 | 2 | 10.0% |
| **Medium** (joins, group by, top-n) | 30 | 0 | 0.0% |
| **Hard** (subqueries, window functions, CTEs) | 30 | 0 | 0.0% |
| **Edge / Unanswerable** | 20 | 0 | 0.0% |
| **Overall Total** | **100** | **2** | **2.0%** |

---

## 3. Error Analysis Taxonomy

Failures are tracked across the following canonical categories:

1. **Schema Misalignment & Hallucinated Columns:**
   - Referencing non-existent columns (e.g. `salary`, `profit_margin`, `format` on `film`).
   - Guard response: caught and blocked if table unknown, or triggers SQL execution error.
2. **Join Key Inversion / Missing Junction:**
   - Direct join between `film` and `category` bypassing `film_category`.
3. **Date Logic & Granularity Errors:**
   - Incorrect date extraction syntax (`YEAR(rental_date)` SQLite syntax instead of PostgreSQL `EXTRACT(YEAR FROM rental_date)`).
4. **Aggregation & Group-By Grouping Errors:**
   - Selecting non-aggregated columns omitted from `GROUP BY`.
5. **Prompt Injection / Adversarial Query Attempts:**
   - Safely mitigated by `sqlglot` parse tree checks and `app_readonly` PostgreSQL user permissions.

