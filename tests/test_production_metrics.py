import logging
import re
from types import SimpleNamespace
from unittest.mock import Mock

from fastapi.testclient import TestClient

from app import llm, main


def test_api_request_logs_latency_without_request_contents(caplog):
    with caplog.at_level(logging.INFO, logger="krishiyojana"):
        response = TestClient(main.app).get("/")

    assert response.status_code == 200
    assert re.search(
        r"API request method=GET path=/ status=200 latency_ms=\d+\.\d+",
        caplog.text,
    )
    assert "question" not in caplog.text.casefold()


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

    with caplog.at_level(logging.INFO, logger="krishiyojana"):
        answer, usage = llm.generate_response_with_usage(
            private_prompt,
            private_system_prompt,
        )

    assert answer == "Safe answer"
    assert usage == {
        "prompt_tokens": 42,
        "completion_tokens": 13,
        "total_tokens": 55,
    }
    assert (
        "Groq token usage prompt_tokens=42 completion_tokens=13 total_tokens=55"
        in caplog.text
    )
    assert private_prompt not in caplog.text
    assert private_system_prompt not in caplog.text
