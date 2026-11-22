import logging

import pytest
from fastapi import HTTPException

from app import main
from app.request_context import request_id_context


def test_cache_hit_returns_a_deep_copy_and_logs(caplog):
    cache = main.TTLResponseCache(ttl_seconds=300, max_size=2)
    original = {"answer": {"text": "Cached answer"}}
    cache.set("question", original)
    original["answer"]["text"] = "Changed after caching"

    context_token = request_id_context.set("cache-hit-test")
    try:
        with caplog.at_level(logging.INFO, logger="krishiyojana"):
            first_result = cache.get("question")
            first_result["answer"]["text"] = "Changed after retrieval"
            second_result = cache.get("question")
    finally:
        request_id_context.reset(context_token)

    assert second_result == {"answer": {"text": "Cached answer"}}
    assert "response_cache event=hit request_id=cache-hit-test" in caplog.text


def test_cache_miss_logs(caplog):
    cache = main.TTLResponseCache(ttl_seconds=300, max_size=2)

    context_token = request_id_context.set("cache-miss-test")
    try:
        with caplog.at_level(logging.INFO, logger="krishiyojana"):
            assert cache.get("missing") is None
    finally:
        request_id_context.reset(context_token)

    assert "response_cache event=miss request_id=cache-miss-test" in caplog.text


def test_cache_entry_expires_at_ttl(monkeypatch, caplog):
    now = [100.0]
    monkeypatch.setattr(main.time, "monotonic", lambda: now[0])
    cache = main.TTLResponseCache(ttl_seconds=5, max_size=2)
    cache.set("question", {"answer": "Cached"})

    now[0] = 104.99
    assert cache.get("question") == {"answer": "Cached"}

    now[0] = 105.0
    context_token = request_id_context.set("cache-expiration-test")
    try:
        with caplog.at_level(logging.INFO, logger="krishiyojana"):
            assert cache.get("question") is None
    finally:
        request_id_context.reset(context_token)

    assert (
        "response_cache event=miss request_id=cache-expiration-test"
        in caplog.text
    )
    assert (
        "response_cache event=expired request_id=cache-expiration-test"
        in caplog.text
    )


def test_cache_evicts_least_recently_used_entry():
    cache = main.TTLResponseCache(ttl_seconds=300, max_size=2)
    cache.set("first", 1)
    cache.set("second", 2)
    assert cache.get("first") == 1

    cache.set("third", 3)

    assert cache.get("second") is None
    assert cache.get("first") == 1
    assert cache.get("third") == 3


def test_updating_existing_key_does_not_evict_another_entry():
    cache = main.TTLResponseCache(ttl_seconds=300, max_size=2)
    cache.set("first", 1)
    cache.set("second", 2)

    cache.set("first", 10)

    assert set(cache._items) == {"first", "second"}
    cache.set("third", 3)
    assert cache.get("second") is None
    assert cache.get("first") == 10


def test_cache_is_disabled_when_maximum_size_is_zero():
    cache = main.TTLResponseCache(ttl_seconds=300, max_size=0)

    cache.set("question", {"answer": "Not stored"})

    assert cache.get("question") is None
    assert len(cache._items) == 0


def test_failed_ask_response_is_not_cached(monkeypatch):
    cache = main.TTLResponseCache(ttl_seconds=300, max_size=2)
    calls = []
    monkeypatch.setattr(main, "response_cache", cache)
    monkeypatch.setattr(main, "get_scheme_documents", lambda question: None)
    monkeypatch.setattr(main, "vector_collection", object())

    def fail_rag(**kwargs):
        calls.append(kwargs["question"])
        raise ValueError("RAG failed")

    monkeypatch.setattr(main, "ask_question", fail_rag)

    for _ in range(2):
        with pytest.raises(HTTPException) as error:
            main.ask(main.QuestionRequest(question="cache failure question"))
        assert error.value.status_code == 500

    assert calls == ["cache failure question", "cache failure question"]
    assert len(cache._items) == 0
