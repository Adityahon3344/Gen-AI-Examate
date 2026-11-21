
import pytest
from langgraph.types import Command

from app.main import get_agent_graph


@pytest.mark.integration
def test_graph_approval_flow():
    graph = get_agent_graph()

    config = {
        "configurable": {
            "thread_id": "farmer-test-001"
        }
    }

    initial_state = {
        "question": "What are the benefits of farm mechanization?",
        "farmer_details": {}
    }

    # Step 1: Start the graph
    result = graph.invoke(initial_state, config=config)

    print("\nSTEP 1 - Approval Required")
    print(result)

    # Step 2: Approve and resume the graph
    result = graph.invoke(
        Command(resume=True),
        config=config
    )

    print("\nSTEP 2 - After Approval")
    print(result)
