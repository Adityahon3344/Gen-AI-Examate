import logging
import re
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
from unittest.mock import Mock
from uuid import UUID

from fastapi.testclient import TestClient

from app import llm, main
from app.request_context import current_request_id, request_id_context


def test_api_request_logs_latency_without_request_contents(caplog):
    with caplog.at_level(logging.INFO, logger="krishiyojana"):
        response = TestClient(main.app).get("/")

    assert response.status_code == 200
    request_id = response.headers["X-Request-ID"]
    UUID(request_id)
    assert re.search(
        rf"API request request_id={request_id} method=GET path=/ "
        r"status=200 latency_ms=\d+\.\d+",
        caplog.text,
    )
    assert "question" not in caplog.text.casefold()


def test_valid_incoming_request_id_is_returned_and_invalid_id_is_replaced(
    caplog,
):
    client = TestClient(main.app)

    with caplog.at_level(logging.INFO, logger="krishiyojana"):
        missing_response = client.get("/")
        valid_response = client.get(
            "/",
            headers={"X-Request-ID": "client-request-123"},
        )
        invalid_response = client.get(
            "/",
            headers={"X-Request-ID": "not a valid request id"},
        )
        long_id_response = client.get(
            "/",
            headers={"X-Request-ID": "x" * 65},
        )

    assert valid_response.headers["X-Request-ID"] == "client-request-123"
    missing_id = missing_response.headers["X-Request-ID"]
    UUID(missing_id)
    generated_id = invalid_response.headers["X-Request-ID"]
    UUID(generated_id)
    assert generated_id != "not a valid request id"
    assert generated_id != missing_id
    long_id = long_id_response.headers["X-Request-ID"]
    UUID(long_id)
    assert long_id != "x" * 65
    assert "request_id=client-request-123" in caplog.text
    assert "request_id=not a valid request id" not in caplog.text


def test_unhandled_error_response_keeps_request_id_and_logs_latency(
    caplog,
    monkeypatch,
):
    def fail_before_endpoint_error_handling(question):
        raise RuntimeError("internal failure")

    monkeypatch.setattr(
        main,
        "get_scheme_documents",
        fail_before_endpoint_error_handling,
    )
    request_id = "request-error-500"
    client = TestClient(main.app, raise_server_exceptions=False)

    with caplog.at_level(logging.INFO, logger="krishiyojana"):
        response = client.post(
            "/ask",
            json={"question": "error path question"},
            headers={"X-Request-ID": request_id},
        )

    assert response.status_code == 500
    assert response.text == "Internal Server Error"
    assert response.headers["X-Request-ID"] == request_id
    assert (
        f"API request request_id={request_id} method=POST path=/ask "
        "status=500 latency_ms="
        in caplog.text
    )


def test_request_ids_do_not_cross_between_concurrent_requests(monkeypatch):
    monkeypatch.setattr(main, "response_cache", main.TTLResponseCache(300, 10))
    monkeypatch.setattr(main, "vector_collection", object())
    monkeypatch.setattr(main, "get_scheme_documents", lambda question: None)
    monkeypatch.setattr(
        main,
        "ask_question",
        lambda question, vector_collection, top_k: {
            "question": question,
            "answer": current_request_id(),
            "sources": [],
            "confidence": "low",
        },
    )

    def send_request(index):
        request_id = f"concurrent-request-{index}"
        response = TestClient(main.app).post(
            "/ask",
            json={"question": f"unique concurrent question {index}"},
            headers={"X-Request-ID": request_id},
        )
        return request_id, response

    with ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(send_request, range(6)))

    for request_id, response in results:
        assert response.status_code == 200
        assert response.headers["X-Request-ID"] == request_id
        assert response.json()["answer"] == request_id


def test_groq_usage_logs_token_counts_without_prompts(caplog, monkeypatch):
    private_prompt = "PRIVATE_USER_PROMPT_SENTINEL"
    private_system_prompt = "PRIVATE_SYSTEM_PROMPT_SENTINEL"
    groq_response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(content="Safe answer"),
            )
        ],
        usage=SimpleNamespace(
            prompt_tokens=42,
            completion_tokens=13,
            total_tokens=55,
        ),
    )
    fake_client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(
                create=Mock(return_value=groq_response),
            )
        )
    )
    monkeypatch.setattr(llm, "get_groq_client", lambda: fake_client)

    context_token = request_id_context.set("groq-request-42")
    try:
        with caplog.at_level(logging.INFO, logger="krishiyojana"):
            answer, usage = llm.generate_response_with_usage(
                private_prompt,
                private_system_prompt,
            )
    finally:
        request_id_context.reset(context_token)

    assert answer == "Safe answer"
    assert usage == {
        "prompt_tokens": 42,
        "completion_tokens": 13,
        "total_tokens": 55,
    }
    assert (
        "Groq token usage request_id=groq-request-42 "
        "prompt_tokens=42 completion_tokens=13 total_tokens=55"
        in caplog.text
    )
    assert private_prompt not in caplog.text
    assert private_system_prompt not in caplog.text


def test_groq_usage_unavailable_is_correlated(caplog, monkeypatch):
    fake_client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(
                create=Mock(
                    return_value=SimpleNamespace(
                        choices=[
                            SimpleNamespace(
                                message=SimpleNamespace(content="Answer"),
                            )
                        ],
                        usage=None,
                    )
                )
            )
        )
    )
    monkeypatch.setattr(llm, "get_groq_client", lambda: fake_client)
    context_token = request_id_context.set("groq-no-usage-7")
    try:
        with caplog.at_level(logging.INFO, logger="krishiyojana"):
            answer, usage = llm.generate_response_with_usage("prompt", "system")
    finally:
        request_id_context.reset(context_token)

    assert answer == "Answer"
    assert usage is None
    assert "Groq token usage unavailable request_id=groq-no-usage-7" in caplog.text


def test_cache_events_and_groq_call_are_correlated_to_each_request(
    caplog,
    monkeypatch,
):
    monkeypatch.setattr(main, "response_cache", main.TTLResponseCache(300, 10))
    monkeypatch.setattr(main, "get_scheme_documents", lambda question: None)
    monkeypatch.setattr(main, "vector_collection", object())
    groq_create = Mock(
        return_value=SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content="Generated answer"),
                )
            ],
            usage=SimpleNamespace(
                prompt_tokens=20,
                completion_tokens=5,
                total_tokens=25,
            ),
        )
    )
    fake_client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(create=groq_create),
        )
    )
    monkeypatch.setattr(llm, "get_groq_client", lambda: fake_client)
    calls = []

    def generate_for_miss(**kwargs):
        calls.append(kwargs["question"])
        answer, _usage = llm.generate_response_with_usage("prompt", "system")
        return {
            "question": kwargs["question"],
            "answer": answer,
            "sources": [],
            "confidence": "medium",
        }

    monkeypatch.setattr(main, "ask_question", generate_for_miss)
    client = TestClient(main.app)

    with caplog.at_level(logging.INFO, logger="krishiyojana"):
        first = client.post(
            "/ask",
            json={"question": "cache correlation question"},
            headers={"X-Request-ID": "cache-miss-1"},
        )
        repeated = client.post(
            "/ask",
            json={"question": "cache correlation question"},
            headers={"X-Request-ID": "cache-hit-2"},
        )

    assert first.status_code == repeated.status_code == 200
    assert calls == ["cache correlation question"]
    assert groq_create.call_count == 1
    assert "response_cache event=miss request_id=cache-miss-1" in caplog.text
    assert "response_cache event=hit request_id=cache-hit-2" in caplog.text
    assert (
        "Groq token usage request_id=cache-miss-1 "
        "prompt_tokens=20 completion_tokens=5 total_tokens=25"
        in caplog.text
    )
    assert "Groq token usage request_id=cache-hit-2" not in caplog.text
