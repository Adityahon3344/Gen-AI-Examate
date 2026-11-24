from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from langgraph.types import Command

from app import graph as graph_module
from app import main


def test_invalid_approval_payload_is_rejected_before_graph_access(
    monkeypatch,
):
    monkeypatch.setattr(
        main,
        "get_agent_graph",
        lambda: pytest.fail("Invalid approval must fail request validation"),
    )

    response = TestClient(main.app).post(
        "/agent",
        json={"thread_id": "invalid-approval", "approval": "maybe"},
    )

    assert response.status_code == 422


def test_invalid_graph_resume_is_rejected_without_tool_execution(monkeypatch):
    monkeypatch.setattr(
        graph_module,
        "ask_question",
        lambda *_args, **_kwargs: pytest.fail(
            "An invalid resume decision must not execute a tool"
        ),
    )
    graph = graph_module.build_graph(vector_collection=None)
    config = {"configurable": {"thread_id": f"invalid-{uuid4()}"}}

    pending = graph.invoke(
        {"question": "What is the scheme objective?"},
        config=config,
    )
    assert pending.get("__interrupt__")

    result = graph.invoke(
        Command(resume={"approved": "yes"}),
        config=config,
    )

    assert result["status"] == "rejected"
    assert result["approved"] is False
    assert result.get("results", {}) == {}


def test_agent_initialization_failure_returns_service_unavailable(
    monkeypatch,
):
    def fail_build_graph(_collection):
        raise RuntimeError("simulated agent initialization failure")

    monkeypatch.setattr(main, "agent_graph", None)
    monkeypatch.setattr(main, "vector_collection", object())
    monkeypatch.setattr(main, "build_graph", fail_build_graph)

    response = TestClient(main.app).post(
        "/agent",
        json={"question": "What is the scheme objective?"},
    )

    assert response.status_code == 503
    assert response.json()["detail"] == "AI agent is currently unavailable."


def test_agent_execution_timeout_returns_correlated_server_error(
    monkeypatch,
):
    class TimedOutGraph:
        def invoke(self, *_args, **_kwargs):
            raise TimeoutError("simulated agent execution timeout")

    monkeypatch.setattr(main, "get_agent_graph", lambda: TimedOutGraph())

    response = TestClient(main.app).post(
        "/agent",
        json={"question": "What is the scheme objective?"},
        headers={"X-Request-ID": "agent-timeout"},
    )

    assert response.status_code == 500
    assert response.headers["X-Request-ID"] == "agent-timeout"
    assert "Agent execution failed: simulated agent execution timeout" in (
        response.json()["detail"]
    )
