import argparse
import json
import os
import statistics
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import requests

DEFAULT_API_URL = "https://gen-ai-examate.onrender.com"
DEFAULT_QUESTION = "What are the benefits of farm mechanization?"
REQUEST_COUNT = 6
DEFAULT_TIMEOUT_SECONDS = 120
DEFAULT_OUTPUT = Path("production_measurements.json")


def collect_measurements(
    api_url: str,
    question: str,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> list[dict]:
    endpoint = f"{api_url.rstrip('/')}/ask"
    results = []

    for _ in range(REQUEST_COUNT):
        request_id = str(uuid.uuid4())
        started_at = time.perf_counter()
        try:
            response = requests.post(
                endpoint,
                json={"question": question},
                headers={"X-Request-ID": request_id},
                timeout=timeout,
            )
        except requests.RequestException as error:
            latency_ms = (time.perf_counter() - started_at) * 1000
            results.append({
                "request_id": request_id,
                "returned_request_id": None,
                "http_status": None,
                "client_observed_latency_ms": round(latency_ms, 2),
                "success": False,
                "error_type": type(error).__name__,
            })
            continue

        latency_ms = (time.perf_counter() - started_at) * 1000
        results.append({
            "request_id": request_id,
            "returned_request_id": response.headers.get("X-Request-ID"),
            "http_status": response.status_code,
            "client_observed_latency_ms": round(latency_ms, 2),
            "success": 200 <= response.status_code < 300,
        })

    return results


def summarize_results(results: list[dict]) -> dict:
    successful = [item for item in results if item["success"]]
    all_latencies = [
        item["client_observed_latency_ms"] for item in results
    ]
    successful_latencies = [
        item["client_observed_latency_ms"] for item in successful
    ]

    return {
        "request_count": len(results),
        "successful_requests": len(successful),
        "failed_requests": len(results) - len(successful),
        "average_client_observed_latency_ms": (
            round(statistics.mean(all_latencies), 2)
            if all_latencies
            else None
        ),
        "average_successful_client_observed_latency_ms": (
            round(statistics.mean(successful_latencies), 2)
            if successful_latencies
            else None
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Measure client-observed latency for six requests to the /ask API. "
            "The script does not confirm cache hits or server-side latency."
        )
    )
    parser.add_argument(
        "--api-url",
        default=os.getenv("API_URL", DEFAULT_API_URL),
        help="Backend base URL (default: API_URL or the production backend).",
    )
    parser.add_argument(
        "--question",
        default=DEFAULT_QUESTION,
        help="Same RAG question to send in each request.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="Per-request timeout in seconds.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Local JSON output path.",
    )
    args = parser.parse_args(argv)

    results = collect_measurements(
        args.api_url,
        args.question,
        timeout=args.timeout,
    )
    summary = summarize_results(results)
    report = {
        "measured_at_utc": datetime.now(timezone.utc).isoformat(),
        "endpoint": "/ask",
        "latency_kind": "client_observed",
        "question_saved": False,
        "server_latency_accessed": False,
        "cache_hit_confirmation": "not available from client response",
        "requests": results,
        "summary": summary,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    for index, result in enumerate(results, start=1):
        print(
            f"request={index} "
            f"http_status={result['http_status']} "
            f"client_observed_latency_ms="
            f"{result['client_observed_latency_ms']:.2f} "
            f"request_id={result['request_id']} "
            f"returned_request_id="
            f"{result['returned_request_id'] or 'unavailable'}"
        )
        if result.get("error_type"):
            print(f"request={index} error_type={result['error_type']}")

    print(
        f"successful={summary['successful_requests']} "
        f"failed={summary['failed_requests']} "
        f"average_client_observed_latency_ms="
        f"{summary['average_client_observed_latency_ms']} "
        f"average_successful_client_observed_latency_ms="
        f"{summary['average_successful_client_observed_latency_ms']}"
    )
    print(f"measurements_saved={args.output}")
    return 0 if summary["failed_requests"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
