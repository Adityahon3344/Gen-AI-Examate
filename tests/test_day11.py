import pytest
from fastapi.testclient import TestClient

from app import main
from app.records import count_by, get_by_id, load_records, search
from app.tools import check_scheme_eligibility


@pytest.fixture
def client():
    return TestClient(main.app)


# 1. Test loading scheme records
def test_load_records():
    records = load_records()
    assert isinstance(records, list)
    assert len(records) > 0


# 2. Test searching for a scheme
def test_search_scheme():
    records = load_records()
    keyword = records[0]["scheme_name"].split()[0]
    results = search(keyword)
    assert isinstance(results, list)
    assert len(results) > 0


# 3. Test department counting
def test_count_by_department():
    records = load_records()
    department = records[0]["department"]
    assert count_by(department) >= 1


# 4. Test retrieving a scheme by ID
def test_get_by_id():
    records = load_records()
    scheme_id = records[0]["id"]
    result = get_by_id(scheme_id)
    assert result is not None
    assert result["id"] == scheme_id


# 5. Test the health endpoint
def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["application"] == "KrishiYojana"
    assert "vector_database" in response.json()


# 6. Test the records API
def test_records_endpoint(client):
    response = client.get("/records")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# 7. Test the search API
def test_search_endpoint(client):
    records = load_records()
    keyword = records[0]["scheme_name"].split()[0]

    response = client.get("/search", params={"query": keyword})

    assert response.status_code == 200
    assert response.json()["total_results"] > 0


# 8. Test /ask using a fake LLM response
def test_ask_with_fake_llm(client, monkeypatch):
    monkeypatch.setattr(main, "get_scheme_documents", lambda question: None)
    monkeypatch.setattr(main, "vector_collection", object())
    monkeypatch.setattr(main, "embedding_model", object())

    def fake_ask_question(**kwargs):
        return {
            "question": kwargs["question"],
            "answer": "Farm mechanization helps farmers improve productivity.",
            "sources": [{"title": "Test Document"}],
            "confidence": "high",
        }

    monkeypatch.setattr(main, "ask_question", fake_ask_question)

    response = client.post(
        "/ask",
        json={"question": "Explain the benefits of farming technology"},
    )

    assert response.status_code == 200
    assert "productivity" in response.json()["answer"]
    assert response.json()["confidence"] == "high"


# 9. Test the agent eligibility tool
def test_agent_tool_unknown_scheme():
    result = check_scheme_eligibility(
        land_holding="7/12 holder",
        land_size_acres=2.0,
        caste_category="OBC",
        received_same_component_last_10_years=False,
        already_has_tractor=False,
        scheme_id="unknown_test_scheme",
    )

    assert result["eligible"] is False
    assert result["status"] == "ERROR"
