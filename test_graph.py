
from langgraph.types import Command

from app.graph import build_graph
from app.main import embedding_model, vector_collection

graph = build_graph(
    vector_collection=vector_collection,
    embedding_model=embedding_model
)

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
