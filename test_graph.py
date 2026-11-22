from uuid import uuid4

import chromadb
import pytest
from langgraph.types import Command

from app import graph as graph_module
from app import main


@pytest.fixture
def isolated_vector_collection(monkeypatch):
    client = chromadb.EphemeralClient()
    collection = client.create_collection("graph_approval_test")
    collection.add(
        ids=["fixture-document"],
        embeddings=[[0.0] * 384],
        documents=["Fixture content for the graph integration test."],
        metadatas=[{"source": "fixture.txt", "page": 1}],
    )

    def fake_ask_question(question, vector_collection, top_k=3):
        assert vector_collection is collection
        assert top_k == 3
        return {
            "question": question,
            "answer": "Fixture answer [Source 1].",
            "sources": [{"source": "fixture.txt", "page": 1}],
            "confidence": "high",
        }

    monkeypatch.setattr(main, "vector_collection", collection)
    monkeypatch.setattr(main, "agent_graph", None)
    monkeypatch.setattr(graph_module, "ask_question", fake_ask_question)
    return collection


@pytest.mark.integration
def test_graph_approval_flow(isolated_vector_collection):
    assert isolated_vector_collection is not None
    assert isolated_vector_collection.count() == 1

    graph = main.get_agent_graph()
    config = {
        "configurable": {
            "thread_id": f"farmer-test-{uuid4()}",
        }
    }
    initial_state = {
        "question": "What are the benefits of farm mechanization?",
        "farmer_details": {},
    }

    awaiting_result = graph.invoke(initial_state, config=config)

    interruptions = awaiting_result.get("__interrupt__", [])
    assert interruptions
    interrupt_value = interruptions[0].value
    assert interrupt_value["question"] == initial_state["question"]
    assert interrupt_value["tools"] == ["rag_search"]
    assert interrupt_value["message"] == (
        "Please approve the agent's tool execution."
    )

    checkpoint = graph.get_state(config)
    assert checkpoint.values["tools_to_use"] == ["rag_search"]
    assert checkpoint.values.get("status") != "completed"

    completed_result = graph.invoke(
        Command(resume=True),
        config=config,
    )

    assert completed_result["status"] == "completed"
    assert completed_result["approved"] is True
    assert completed_result["tools_to_use"] == ["rag_search"]
    assert completed_result["results"]["rag_search"]["answer"] == (
        "Fixture answer [Source 1]."
    )
