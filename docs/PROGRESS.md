# Progress Log — Ask Your Database

## Phase 1 — Application, Database, Evaluator, Baselines

### 2026-11-13 — Full Implementation & Verification

#### Acceptance Criteria Status
- [x] **Demo Database:** Realistic Pagila subset schema with `init.sql`, `seed.sql`, and `roles.sql` (`app_readonly` user).
- [x] **Schema Description:** Detailed column descriptions and join hints in `data/demo_db/schema_description.txt`.
- [x] **Evaluation Set:** 100 question/gold-SQL pairs in `data/eval/demo_eval.jsonl` categorized across Easy (20), Medium (30), Hard (30), and Edge (20).
- [x] **SQL Safety Guard:** `src/app/sql_guard.py` with 8 layers of defense (sqlglot parsing, SELECT-only, table allowlist, function blocklist, LIMIT injection/capping).
- [x] **Adversarial Tests:** 39 test cases in `tests/test_sql_guard.py` covering injections, syntax attacks, and edge cases.
- [x] **LLM Backends:** Pluggable `LLMBackend` interface with `MockBackend`, `OpenAICompatBackend`, and `BedrockBackend` via `get_backend()`.
- [x] **FastAPI Application:** Endpoints `GET /health`, `GET /schema`, and `POST /ask` with error handling and statement timeout enforcement.
- [x] **Streamlit UI:** Responsive web app in `src/ui/streamlit_app.py` with example questions, SQL viewer, data table, and Plotly visualization.
- [x] **Evaluator:** Execution-accuracy benchmark in `src/eval/run_eval.py` and `metrics.py` reporting overall and difficulty breakdowns.
- [x] **Training Pipeline:** Data prep with leakage guard in `src/training/prepare_data.py`, LoRA trainer in `train_lora.py`, and adapter merge in `merge_adapter.py`.
- [x] **Serving & Benchmarking:** `src/serving/serve_vllm.sh` and async benchmarking tool `bench_serving.py`.
- [x] **Infrastructure:** Terraform AWS deployment for RDS and EC2 in `infra/terraform/`.
- [x] **CI & Containers:** GitHub Actions workflow in `.github/workflows/ci.yml`, `Dockerfile`, and `docker-compose.yml`.
- [x] **Documentation:** `README.md`, `docs/ARCHITECTURE.md`, `docs/RESULTS.md`, `data/README.md`.

---

## Phase 2 — Fine-Tuning & Serving (Ready for GPU Execution)

- [x] LoRA SFT training script (`src/training/train_lora.py`) using `trl`, `peft`, and completion-only loss.
- [x] Leakage guard script ensuring zero test-set overlap.
- [x] vLLM OpenAI-compatible server script (`src/serving/serve_vllm.sh`).
- [x] High-concurrency async benchmark suite (`src/serving/bench_serving.py`).
- [ ] Execution on physical ROCm/CUDA GPU cluster (Pending hardware access).
