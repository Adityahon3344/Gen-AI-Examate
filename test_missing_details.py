
from langgraph.types import Command

from app.graph import build_graph
from app.main import vector_collection

graph = build_graph(
    vector_collection=vector_collection
)

config = {
    "configurable": {
        "thread_id": "missing-details-test-001"
    }
}

# Farmer has not provided complete information
initial_state = {
    "question": "Am I eligible for the farm mechanization scheme?",
    "farmer_details": {
        "land_holding": "7/12 holder",
        "land_size_acres": 2.0
    }
}

# STEP 1: Start graph
result = graph.invoke(
    initial_state,
    config=config
)

print("\nSTEP 1 - Approval Requested")
print(result)

# STEP 2: Approve execution
result = graph.invoke(
    Command(resume=True),
    config=config
)

print("\nSTEP 2 - Missing Farmer Information")
print(result)

# STEP 3: Verify missing fields
eligibility = result["results"]["eligibility"]

assert result["status"] == "needs_information"

assert eligibility["status"] == "needs_information"

assert "caste_category" in eligibility["missing_fields"]

assert "received_same_component_last_10_years" in eligibility["missing_fields"]

assert "already_has_tractor" in eligibility["missing_fields"]

print("\nSUCCESS: Missing farmer details test passed!")
