import json
from uuid import UUID

import requests

from scripts import measure_production


class FakeResponse:
    def __init__(self, status_code, headers=None):
        self.status_code = status_code
        self.headers = headers or {}


def test_measurement_script_sends_six_requests_with_unique_ids(monkeypatch):
    calls = []

    def fake_post(url, *, json, headers, timeout):
        calls.append({
            "url": url,
            "question": json["question"],
            "request_id": headers["X-Request-ID"],
            "timeout": timeout,
        })
        return FakeResponse(
            200,
            {"X-Request-ID": headers["X-Request-ID"]},
        )

    monkeypatch.setattr(measure_production.requests, "post", fake_post)
    results = measure_production.collect_measurements(
        "https://api.example.test/",
        "A configurable test question",
        timeout=17,
    )

    assert len(calls) == measure_production.REQUEST_COUNT == 6
    assert {call["url"] for call in calls} == {
        "https://api.example.test/ask"
    }
    assert {call["question"] for call in calls} == {
        "A configurable test question"
    }
    assert {call["timeout"] for call in calls} == {17}
    request_ids = [call["request_id"] for call in calls]
    assert len(set(request_ids)) == 6
    for request_id in request_ids:
        UUID(request_id)

    assert all(result["http_status"] == 200 for result in results)
    assert all(result["success"] for result in results)
    assert all(
        result["returned_request_id"] == result["request_id"]
        for result in results
    )
    assert all(
        "question" not in result and "answer" not in result
        for result in results
    )


def test_measurement_script_records_transport_failures(monkeypatch):
    calls = 0

    def fake_post(*args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise requests.Timeout()
        return FakeResponse(503)

    monkeypatch.setattr(measure_production.requests, "post", fake_post)
    results = measure_production.collect_measurements(
        "https://api.example.test",
        "Question",
    )

    assert len(results) == 6
    assert results[0]["success"] is False
    assert results[0]["http_status"] is None
    assert results[0]["error_type"] == "Timeout"
    assert results[1]["success"] is False
    assert results[1]["http_status"] == 503


def test_measurement_summary_counts_and_averages_successful_requests():
    summary = measure_production.summarize_results(
        [
            {
                "success": True,
                "client_observed_latency_ms": 100.0,
            },
            {
                "success": True,
                "client_observed_latency_ms": 300.0,
            },
            {
                "success": False,
                "client_observed_latency_ms": 700.0,
            },
        ]
    )

    assert summary == {
        "request_count": 3,
        "successful_requests": 2,
        "failed_requests": 1,
        "average_client_observed_latency_ms": 366.67,
        "average_successful_client_observed_latency_ms": 200.0,
    }


def test_measurement_script_saves_and_prints_safe_results(
    tmp_path,
    monkeypatch,
    capsys,
):
    results = [
        {
            "request_id": f"request-{index}",
            "returned_request_id": f"request-{index}",
            "http_status": 200,
            "client_observed_latency_ms": float(index * 10),
            "success": True,
        }
        for index in range(1, 7)
    ]
    monkeypatch.setattr(
        measure_production,
        "collect_measurements",
        lambda api_url, question, timeout: results,
    )
    output_path = tmp_path / "measurements.json"
    private_question = "Do not persist this test question"

    exit_code = measure_production.main(
        [
            "--question",
            private_question,
            "--output",
            str(output_path),
        ]
    )

    saved_report = json.loads(output_path.read_text(encoding="utf-8"))
    printed = capsys.readouterr().out
    assert exit_code == 0
    assert saved_report["latency_kind"] == "client_observed"
    assert saved_report["question_saved"] is False
    assert private_question not in output_path.read_text(encoding="utf-8")
    assert saved_report["summary"]["successful_requests"] == 6
    assert saved_report["summary"]["failed_requests"] == 0
    assert "request=1 http_status=200" in printed
    assert "average_client_observed_latency_ms=35.0" in printed
