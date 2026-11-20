
from langgraph.types import Command

from app.graph import build_graph
from app.main import embedding_model, vector_collection

graph = build_graph(
    vector_collection=vector_collection,
    embedding_model=embedding_model
)

config = {
    "configurable": {
        "thread_id": "eligibility-test-001"
    }
}

# Farmer details for demonstration testing
farmer_details = {
    "land_holding": "7/12 holder",
    "land_size_acres": 2.0,
    "caste_category": "OBC",
    "received_same_component_last_10_years": False,
    "already_has_tractor": False
}

initial_state = {
    "question": "Am I eligible for the farm mechanization scheme?",
    "farmer_details": farmer_details
}

# STEP 1: Start LangGraph
result = graph.invoke(
    initial_state,
    config=config
)

print("\nSTEP 1 - Eligibility Approval Requested")
print(result)

# STEP 2: Approve execution
result = graph.invoke(
    Command(resume=True),
    config=config
)

print("\nSTEP 2 - Eligibility Result")
print(result)

# STEP 3: Verify result
eligibility = result["results"]["eligibility"]

assert result["status"] == "completed"
assert eligibility["status"] == "PASS"
assert eligibility["eligible"] is True

print("\nSUCCESS: Eligibility workflow passed!")
