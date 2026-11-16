
import json
from pathlib import Path
from dataclasses import asdict

import chromadb
from sentence_transformers import SentenceTransformer

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from app.records import load_json_records
from app.smart_search import smart_search
from app.llm import generate_response
from app.rag import ask_question


# --------------------------------------------------
# 1. Initialize FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="KrishiYojana API",
    description="Maharashtra Farmer Scheme Eligibility and Benefits Assistant",
    version="1.3.0"
)


# --------------------------------------------------
# 2. Project directories
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPTS_DIR = BASE_DIR / "prompts"


# --------------------------------------------------
# 3. ChromaDB configuration
# --------------------------------------------------

DB_PATH = BASE_DIR / "data" / "chroma_db"
COLLECTION_NAME = "krishiyojana_documents"

chroma_client = chromadb.PersistentClient(
    path=str(DB_PATH)
)

try:
    vector_collection = chroma_client.get_collection(
        name=COLLECTION_NAME
    )
except Exception:
    vector_collection = None


# --------------------------------------------------
# 4. Load embedding model
# --------------------------------------------------

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


# --------------------------------------------------
# 5. Farmer question request model
# --------------------------------------------------

class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Enter a farmer's agricultural scheme question"
    )


# --------------------------------------------------
# 6. Health Check API
# --------------------------------------------------

@app.get("/health")
def health_check():
    """Check whether the KrishiYojana API is running."""

    return {
        "status": "success",
        "message": "KrishiYojana API is running!"
    }


# --------------------------------------------------
# 7. Get All Records API
# --------------------------------------------------

@app.get("/records")
def get_all_records(limit: int = Query(default=10, ge=1)):
    """Retrieve agricultural scheme records."""

    records = load_json_records()

    return {
        "total": len(records[:limit]),
        "records": [
            asdict(record) for record in records[:limit]
        ]
    }


# --------------------------------------------------
# 8. Get Record By ID API
# --------------------------------------------------

@app.get("/records/{record_id}")
def get_record_by_id(record_id: int):
    """Retrieve an agricultural scheme using its ID."""

    records = load_json_records()

    for record in records:
        if record.id == record_id:
            return asdict(record)

    raise HTTPException(
        status_code=404,
        detail="Scheme not found"
    )


# --------------------------------------------------
# 9. Smart Search API using TF-IDF
# --------------------------------------------------

@app.get("/search")
def search_records(q: str = Query(..., min_length=1)):
    """Search schemes using TF-IDF and cosine similarity."""

    records = load_json_records()
    results = smart_search(records, q, top_k=5)

    return {
        "query": q,
        "total": len(results),
        "results": [
            asdict(record) for record in results
        ]
    }


# --------------------------------------------------
# 10. Farmer Questions API using Smart Search
# --------------------------------------------------

@app.post("/questions")
def ask_farmer_question(request: QuestionRequest):
    """Find relevant agricultural schemes for a farmer's question."""

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    records = load_json_records()
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


# --------------------------------------------------
# 11. Semantic Search API using ChromaDB
# --------------------------------------------------

@app.get("/search/semantic")
def semantic_search(
    q: str = Query(..., min_length=1),
    top_k: int = Query(default=3, ge=1, le=10)
):
    """Search document chunks using semantic similarity."""

    if vector_collection is None:
        raise HTTPException(
            status_code=503,
            detail="ChromaDB collection is not available. Run app.vectorstore first."
        )

    try:
        query_embedding = embedding_model.encode(
            [q.strip()],
            normalize_embeddings=True
        )

        results = vector_collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=min(top_k, vector_collection.count()),
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        matches = []

        for index in range(len(results["ids"][0])):
            metadata = results["metadatas"][0][index]
            distance = results["distances"][0][index]

            matches.append({
                "id": results["ids"][0][index],
                "text": results["documents"][0][index],
                "source": metadata.get("source"),
                "page": (
                    metadata.get("page")
                    if metadata.get("page") != -1
                    else None
                ),
                "title": metadata.get("title"),
                "similarity_score": round(
                    max(0.0, min(1.0, 1.0 - distance)),
                    4
                )
            })

        return {
            "query": q,
            "total_results": len(matches),
            "results": matches
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Semantic search failed: {str(error)}"
        )


# --------------------------------------------------
# 12. Load Prompt Files
# --------------------------------------------------

def load_prompt(filename):
    """Read a prompt file from the prompts directory."""

    prompt_path = PROMPTS_DIR / filename

    try:
        return prompt_path.read_text(encoding="utf-8")

    except OSError:
        raise HTTPException(
            status_code=500,
            detail=f"Prompt file not found: {filename}"
        )


# --------------------------------------------------
# 13. Chat API using Groq LLM and TF-IDF
# --------------------------------------------------

@app.post("/chat")
def chat_with_farmer(request: QuestionRequest):
    """Generate an AI answer using Groq and scheme records."""

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    system_prompt = load_prompt("system_prompt.txt")
    task_prompt = load_prompt("task_prompt_1.txt")

    records = load_json_records()
    results = smart_search(records, question, top_k=5)

    context = "\n\n".join(
        f"Scheme: {record.scheme_name}\n"
        f"Department: {record.department}\n"
        f"Benefits: {record.benefit}\n"
        f"Eligibility: {', '.join(record.eligibility)}\n"
        f"Documents: {', '.join(record.required_documents)}"
        for record in results
    )

    if not context:
        context = "No matching scheme information was found."

    user_prompt = task_prompt.format(
        question=question,
        context=context
    )

    json_instruction = """
Return only valid JSON without Markdown code blocks.

Use exactly this structure:
{
    "answer": "Answer for the farmer",
    "confidence": 0.0,
    "follow_up": "A relevant follow-up question or null"
}

Rules:
- Confidence must be a number between 0 and 1.
- Do not invent scheme information.
- Use only the provided scheme context.
- If no relevant information exists, clearly state that.
- Use null for follow_up if no follow-up is needed.
"""

    try:
        ai_response = generate_response(
            user_prompt + "\n\n" + json_instruction,
            system_prompt
        )

        result = json.loads(ai_response)

        answer = result.get("answer")
        confidence = result.get("confidence")
        follow_up = result.get("follow_up")

        if (
            not isinstance(answer, str)
            or isinstance(confidence, bool)
            or not isinstance(confidence, (int, float))
            or not 0 <= confidence <= 1
            or not (
                follow_up is None
                or isinstance(follow_up, str)
            )
        ):
            raise ValueError("Invalid JSON response structure")

        return {
            "answer": answer,
            "confidence": float(confidence),
            "follow_up": follow_up
        }

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=502,
            detail="Groq returned an invalid JSON response"
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Unable to generate a response from the AI service"
        )


# --------------------------------------------------
# 14. RAG API using ChromaDB and Groq
# --------------------------------------------------

@app.post("/ask")
def ask_with_rag(request: QuestionRequest):
    """
    Answer farmer questions using retrieved document chunks,
    Groq LLM, and source citations.
    """

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    if vector_collection is None:
        raise HTTPException(
            status_code=503,
            detail="ChromaDB collection is not available."
        )

    try:
        result = ask_question(
            question=question,
            vector_collection=vector_collection,
            embedding_model=embedding_model,
            top_k=3
        )

        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Unable to generate a RAG response."
        )
