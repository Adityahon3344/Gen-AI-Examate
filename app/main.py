
from fastapi import FastAPI, HTTPException, Query
from dataclasses import asdict
from pydantic import BaseModel, Field

from app.records import load_json_records
from app.smart_search import smart_search


# Initialize FastAPI application
app = FastAPI(
    title="KrishiYojana API",
    description="Maharashtra Farmer Scheme Eligibility and Benefits Assistant",
    version="1.0.0"
)


# 1. Health Check API
@app.get("/health")
def health_check():
    """
    Check whether the KrishiYojana API is running.
    """
    return {
        "status": "success",
        "message": "KrishiYojana API is running!"
    }


# 2. Get All Records API
@app.get("/records")
def get_all_records(limit: int = Query(default=10, ge=1)):
    """
    Retrieve agricultural scheme records.
    """
    records = load_json_records()

    return {
        "total": len(records[:limit]),
        "records": [asdict(record) for record in records[:limit]]
    }


# 3. Get Record By ID API
@app.get("/records/{record_id}")
def get_record_by_id(record_id: int):
    """
    Retrieve a particular agricultural scheme using its ID.
    """
    records = load_json_records()

    for record in records:
        if record.id == record_id:
            return asdict(record)

    raise HTTPException(
        status_code=404,
        detail="Scheme not found"
    )


# 4. Smart Search API using TF-IDF
@app.get("/search")
def search_records(q: str = Query(..., min_length=1)):
    """
    Search agricultural schemes using TF-IDF and cosine similarity.
    """
    records = load_json_records()

    results = smart_search(records, q, top_k=5)

    return {
        "query": q,
        "total": len(results),
        "results": [asdict(record) for record in results]
    }


# 5. Farmer Question Request Model
class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Enter a farmer's agricultural scheme question"
    )


# 6. Farmer Questions API using Smart Search
@app.post("/questions")
def ask_question(request: QuestionRequest):
    """
    Accept a farmer's question and find relevant schemes.
    """
    records = load_json_records()

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    results = smart_search(records, question, top_k=5)

    return {
        "question": question,
        "total": len(results),
        "matching_schemes": [
            asdict(record) for record in results
        ],
        "message": (
            "Relevant schemes found."
            if results
            else "No matching schemes found."
        )
    }
