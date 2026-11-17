
from langgraph.types import Command

from app.main import vector_collection, embedding_model
from app.graph import build_graph

graph = build_graph(
    vector_collection=vector_collection,
    embedding_model=embedding_model
)

config = {
    "configurable": {
        "thread_id": "farmer-rejection-test-001"
    }
}

initial_state = {
    "question": "What are the benefits of farm mechanization?",
    "farmer_details": {}
}

# Step 1: Start graph
result = graph.invoke(
    initial_state,
    config=config
)

print("\nSTEP 1 - Approval Requested")
print(result)

# Step 2: Reject execution
result = graph.invoke(
    Command(resume=False),
    config=config
)

print("\nSTEP 2 - After Rejection")
print(result)

# Step 3: Verify rejection
assert result.get("status") == "rejected"
assert result.get("approved") is False
assert not result.get("results")

print("\nSUCCESS: Rejection workflow passed!")
