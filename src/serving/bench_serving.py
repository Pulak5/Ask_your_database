"""Benchmark vLLM serving endpoint throughput and latency under concurrency."""
from __future__ import annotations

import argparse
import asyncio
import time
from typing import Any

import httpx

TEST_PROMPTS = [
    "### Schema:\nTable: film\n  Columns: film_id, title, rental_rate\n\n### Question:\nList the top 5 most expensive films to rent.\n\n### SQL:\n",
    "### Schema:\nTable: customer\n  Columns: customer_id, first_name, active\n\n### Question:\nHow many customers are active?\n\n### SQL:\n",
    "### Schema:\nTable: category\n  Columns: category_id, name\nTable: film_category\n  Columns: film_id, category_id\n\n### Question:\nShow film count per category.\n\n### SQL:\n",
    "### Schema:\nTable: payment\n  Columns: payment_id, amount\n\n### Question:\nWhat is the total revenue from payments?\n\n### SQL:\n",
]


async def send_single_request(
    client: httpx.AsyncClient,
    url: str,
    model: str,
    prompt: str,
) -> float:
    """Send one request to the /chat/completions endpoint and measure roundtrip latency."""
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "max_tokens": 128,
    }
    t0 = time.perf_counter()
    resp = await client.post(url, json=payload, timeout=60.0)
    resp.raise_for_status()
    latency_ms = (time.perf_counter() - t0) * 1000.0
    return latency_ms


async def run_benchmark_concurrency(
    base_url: str,
    model: str,
    concurrency: int,
    total_requests: int,
) -> dict[str, Any]:
    """Run benchmark for a given concurrency level."""
    endpoint = f"{base_url.rstrip('/')}/v1/chat/completions"
    sem = asyncio.Semaphore(concurrency)
    latencies: list[float] = []

    async with httpx.AsyncClient() as client:
        async def worker(prompt: str) -> None:
            async with sem:
                try:
                    lat = await send_single_request(client, endpoint, model, prompt)
                    latencies.append(lat)
                except Exception as exc:
                    print(f"Request error: {exc}")

        start_time = time.perf_counter()
        tasks = [
            worker(TEST_PROMPTS[i % len(TEST_PROMPTS)])
            for i in range(total_requests)
        ]
        await asyncio.gather(*tasks)
        elapsed_sec = time.perf_counter() - start_time

    if not latencies:
        return {"concurrency": concurrency, "throughput": 0, "p50": 0, "p95": 0, "p99": 0}

    sorted_lats = sorted(latencies)
    p50 = sorted_lats[int(len(sorted_lats) * 0.50)]
    p95 = sorted_lats[int(len(sorted_lats) * 0.95)]
    p99 = sorted_lats[int(len(sorted_lats) * 0.99)]
    throughput = len(latencies) / elapsed_sec

    return {
        "concurrency": concurrency,
        "total_completed": len(latencies),
        "elapsed_sec": round(elapsed_sec, 2),
        "throughput_req_sec": round(throughput, 2),
        "p50_ms": round(p50, 1),
        "p95_ms": round(p95, 1),
        "p99_ms": round(p99, 1),
    }


async def main_async() -> None:
    parser = argparse.ArgumentParser(description="Benchmark vLLM Serving Endpoint")
    parser.add_argument("--base-url", default="http://localhost:8080", help="vLLM base URL")
    parser.add_argument("--model", default="Qwen/Qwen2.5-Coder-7B-Instruct", help="Model name")
    parser.add_argument(
        "--concurrency",
        nargs="+",
        type=int,
        default=[1, 4, 8, 16],
        help="List of concurrency levels to test",
    )
    parser.add_argument(
        "--num-requests",
        type=int,
        default=50,
        help="Number of requests per concurrency test",
    )

    args = parser.parse_args()

    print(f"\nBenchmarking {args.base_url} (model: {args.model})")
    print(f"Requests per concurrency test: {args.num_requests}")
    print("=" * 70)

    results = []
    for c in args.concurrency:
        print(f"Running concurrency = {c}...")
        res = await run_benchmark_concurrency(
            base_url=args.base_url,
            model=args.model,
            concurrency=c,
            total_requests=args.num_requests,
        )
        results.append(res)

    print("\n### Benchmark Results")
    print("| Concurrency | Throughput (req/s) | p50 Latency (ms) | p95 Latency (ms) | p99 Latency (ms) |")
    print("|---|---|---|---|---|")
    for r in results:
        print(
            f"| {r['concurrency']} | {r['throughput_req_sec']} | {r['p50_ms']} | {r['p95_ms']} | {r['p99_ms']} |"
        )


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()

