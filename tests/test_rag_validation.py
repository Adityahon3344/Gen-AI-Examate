from uuid import uuid4

import chromadb
import pytest
from fastapi.testclient import TestClient

from app import main, rag


@pytest.fixture
def retrieval_collection():
    client = chromadb.EphemeralClient()
    collection = client.create_collection(
        name=f"rag-validation-{uuid4().hex}",
        metadata={"hnsw:space": "cosine"},
    )
    collection.add(
        ids=["gr-page-12", "benefit-page", "weather-page"],
        embeddings=[[1.0, 0.0], [0.98, 0.02], [0.0, 1.0]],
        documents=[
            "Farm mechanization supports agricultural machinery.",
            "The benefits page describes equipment assistance.",
            "The weather bulletin forecasts seasonal rainfall.",
        ],
        metadatas=[
            {
                "source": "farm-mechanization-gr.pdf",
                "page": 12,
                "title": "Farm Mechanization GR",
            },
            {
                "source": "benefits.html",
                "page": -1,
                "title": "Scheme Benefits",
            },
            {
                "source": "weather.pdf",
                "page": 2,
                "title": "Weather Bulletin",
            },
        ],
    )
    return collection


def test_rag_retrieves_relevant_chunks_and_maps_source_citations(
    retrieval_collection,
    monkeypatch,
):
    captured = {}
    monkeypatch.setattr(
        rag,
        "generate_query_embedding",
        lambda question: [1.0, 0.0],
    )

    def generate_response(user_prompt, system_prompt):
        captured["user_prompt"] = user_prompt
        captured["system_prompt"] = system_prompt
        return "Machinery assistance is described in the sources [Source 1].", None

    monkeypatch.setattr(rag, "generate_response_with_usage", generate_response)

    result = rag.ask_question(
        "What support is available for machinery?",
        retrieval_collection,
        top_k=2,
    )

    assert result["answer"].endswith("[Source 1].")
    assert result["confidence"] == "medium"
    assert result["sources"] == [
        {
            "source": "farm-mechanization-gr.pdf",
            "page": 12,
            "title": "Farm Mechanization GR",
        },
        {
            "source": "benefits.html",
            "page": None,
            "title": "Scheme Benefits",
        },
    ]
    assert "Farm mechanization supports agricultural machinery." in (
        captured["user_prompt"]
    )
    assert "The benefits page describes equipment assistance." in (
        captured["user_prompt"]
    )
    assert "weather bulletin" not in captured["user_prompt"].casefold()
    assert '"reference": "Source 1"' in captured["user_prompt"]
    assert "Answer only using the retrieved document context" in (
        captured["system_prompt"]
    )


def test_empty_collection_abstains_without_calling_the_llm(monkeypatch):
    class EmptyCollection:
        def count(self):
            return 0

    monkeypatch.setattr(
        rag,
        "generate_query_embedding",
        lambda question: [1.0, 0.0],
    )
    monkeypatch.setattr(
        rag,
        "generate_response_with_usage",
        lambda *_args: pytest.fail("LLM must not run for an empty index"),
    )

    result = rag.ask_question("Unsupported question", EmptyCollection())

    assert result == {
        "question": "Unsupported question",
        "answer": "I don't know. No document information is available.",
        "sources": [],
        "confidence": "low",
    }


def test_unsupported_answer_is_low_confidence_and_keeps_retrieved_sources(
    retrieval_collection,
    monkeypatch,
):
    monkeypatch.setattr(
        rag,
        "generate_query_embedding",
        lambda question: [1.0, 0.0],
    )
    monkeypatch.setattr(
        rag,
        "generate_response_with_usage",
        lambda *_args: ("I don't know.", None),
    )

    result = rag.ask_question(
        "What is the current weather forecast?",
        retrieval_collection,
        top_k=1,
    )

    assert result["answer"] == "I don't know."
    assert result["confidence"] == "low"
    assert result["sources"]


def test_retrieval_error_returns_api_error_and_is_not_cached(monkeypatch):
    class BrokenCollection:
        def count(self):
            return 1

        def query(self, **_kwargs):
            raise RuntimeError("simulated vector-store failure")

    cache = main.TTLResponseCache(ttl_seconds=300, max_size=10)
    monkeypatch.setattr(main, "response_cache", cache)
    monkeypatch.setattr(main, "get_scheme_documents", lambda _question: None)
    monkeypatch.setattr(main, "vector_collection", BrokenCollection())
    monkeypatch.setattr(main, "ask_question", rag.ask_question)
    monkeypatch.setattr(
        rag,
        "generate_query_embedding",
        lambda _question: [1.0, 0.0],
    )

    response = TestClient(main.app).post(
        "/ask",
        json={"question": "A question requiring retrieval"},
        headers={"X-Request-ID": "rag-retrieval-error"},
    )

    assert response.status_code == 500
    assert response.headers["X-Request-ID"] == "rag-retrieval-error"
    assert "simulated vector-store failure" in response.json()["detail"]
    assert not cache._items
