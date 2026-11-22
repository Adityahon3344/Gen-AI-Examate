
from uuid import uuid4

import pytest
from langgraph.types import Command

from app import main
from app.main import get_agent_graph, initialize_vector_database


@pytest.mark.integration
def test_graph_approval_flow():
    initialize_vector_database()
    assert main.vector_collection is not None
    assert main.vector_collection.count() > 0

    graph = get_agent_graph()

    config = {
        "configurable": {
            "thread_id": f"farmer-test-{uuid4()}"
        }
    }

    initial_state = {
        "question": "What are the benefits of farm mechanization?",
        "farmer_details": {}
    }

    # Step 1: Start the graph
    result = graph.invoke(initial_state, config=config)

    interruptions = result.get("__interrupt__", [])
    assert interruptions
    interrupt_value = interruptions[0].value
    assert interrupt_value["question"] == initial_state["question"]
    assert interrupt_value["tools"] == ["rag_search"]

    # Step 2: Approve and resume the graph
    result = graph.invoke(
        Command(resume=True),
        config=config
    )

    assert result["status"] == "completed"
    assert result["approved"] is True
    assert "rag_search" in result["results"]
