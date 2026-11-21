from app.agent_loop import run_agent
from app.main import embedding_model, vector_collection

# Test 1: Eligibility tool
farmer_details = {
    "land_holding": "7/12 holder",
    "land_size_acres": 2.0,
    "caste_category": "OBC",
    "received_same_component_last_10_years": False,
    "already_has_tractor": False
}

result = run_agent(
    question="Am I eligible for the farm mechanization scheme?",
    vector_collection=vector_collection,
    embedding_model=embedding_model,
    farmer_details=farmer_details
)

print("\nTEST 1 - Eligibility Agent")
print(result)


# Test 2: RAG search tool
result = run_agent(
    question="What are the benefits of farm mechanization?",
    vector_collection=vector_collection,
    embedding_model=embedding_model
)

print("\nTEST 2 - RAG Agent")
print(result)
