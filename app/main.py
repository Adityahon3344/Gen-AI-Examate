
import json
import logging
import os
import threading
import time
import uuid
from collections import OrderedDict
from copy import deepcopy
from pathlib import Path

import chromadb
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
from langgraph.types import Command
from pydantic import BaseModel, Field

from app.embeddings import is_embedding_model_loaded
from app.graph import build_graph
from app.rag import ask_question
from app.request_context import current_request_id, request_id_context, valid_request_id
from app.vectorstore import COLLECTION_NAME, DB_PATH

# --------------------------------------------------
# 1. FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title="KrishiYojana API",
    description="AI-Powered Farmer Scheme Eligibility and Benefits Assistant",
    version="1.0.0",
)

logger = logging.getLogger("krishiyojana")

MAX_QUESTION_LENGTH = 2000
RESPONSE_CACHE_TTL_SECONDS = int(
    os.getenv("RESPONSE_CACHE_TTL_SECONDS", "300")
)
RESPONSE_CACHE_MAX_SIZE = int(
    os.getenv("RESPONSE_CACHE_MAX_SIZE", "100")
)


class TTLResponseCache:
    def __init__(self, ttl_seconds: int, max_size: int):
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
        self._items = OrderedDict()
        self._lock = threading.RLock()

    def get(self, key: str):
        now = time.monotonic()
        request_id = current_request_id() or "unavailable"
        with self._lock:
            item = self._items.get(key)
            if item is None:
                logger.info(
                    "response_cache event=miss request_id=%s",
                    request_id,
                )
                return None

            expires_at, value = item
            if expires_at <= now:
                del self._items[key]
                logger.info(
                    "response_cache event=expired request_id=%s",
                    request_id,
                )
                logger.info(
                    "response_cache event=miss request_id=%s",
                    request_id,
                )
                return None

            self._items.move_to_end(key)
            logger.info(
                "response_cache event=hit request_id=%s",
                request_id,
            )
            return deepcopy(value)

    def set(self, key: str, value):
        with self._lock:
            if self.max_size <= 0:
                return

            if key not in self._items and len(self._items) >= self.max_size:
                self._items.popitem(last=False)

            self._items[key] = (
                time.monotonic() + self.ttl_seconds,
                deepcopy(value),
            )
            self._items.move_to_end(key)


response_cache = TTLResponseCache(
    ttl_seconds=RESPONSE_CACHE_TTL_SECONDS,
    max_size=RESPONSE_CACHE_MAX_SIZE,
)


@app.middleware("http")
async def log_request_latency(request: Request, call_next):
    supplied_request_id = request.headers.get("X-Request-ID")
    request_id = (
        supplied_request_id
        if valid_request_id(supplied_request_id)
        else str(uuid.uuid4())
    )
    context_token = request_id_context.set(request_id)
    request.state.request_id = request_id
    started_at = time.perf_counter()
    response = None
    try:
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
    finally:
        latency_ms = (time.perf_counter() - started_at) * 1000
        status_code = response.status_code if response is not None else 500
        logger.info(
            "API request request_id=%s method=%s path=%s status=%d latency_ms=%.2f",
            request_id,
            request.method,
            request.url.path,
            status_code,
            latency_ms,
        )
        request_id_context.reset(context_token)


@app.exception_handler(Exception)
async def handle_unexpected_error(request: Request, _error: Exception):
    request_id = getattr(request.state, "request_id", None)
    headers = {"X-Request-ID": request_id} if request_id else None
    return PlainTextResponse(
        "Internal Server Error",
        status_code=500,
        headers=headers,
    )


# --------------------------------------------------
# 2. Paths and Runtime Objects
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
RECORDS_FILE = BASE_DIR / "data" / "records.json"
VECTOR_DB_PATH = BASE_DIR / DB_PATH

vector_collection = None
agent_graph = None

initialization_error = None

ai_lock = threading.RLock()
ai_initialization_attempted = False

# --------------------------------------------------
# 3. Request Models
# --------------------------------------------------


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=MAX_QUESTION_LENGTH)


class AgentRequest(BaseModel):
    question: str | None = Field(
        default=None,
        min_length=1,
        max_length=MAX_QUESTION_LENGTH,
    )
    farmer_details: dict | None = None
    thread_id: str | None = None
    approval: bool | None = None


# --------------------------------------------------
# 4. Initialize ChromaDB
# --------------------------------------------------


def initialize_vector_database():
    global vector_collection
    global initialization_error

    try:
        client = chromadb.PersistentClient(
            path=str(VECTOR_DB_PATH)
        )

        vector_collection = client.get_collection(
            name=COLLECTION_NAME
        )

        print(
            "ChromaDB connected. Documents:",
            vector_collection.count(),
        )

        initialization_error = None

    except Exception as error:
        initialization_error = str(error)
        print("ChromaDB initialization failed:", error)


# --------------------------------------------------
# 6. Initialize AI Agent When Required
# --------------------------------------------------


def get_agent_graph():
    global agent_graph

    if agent_graph is not None:
        return agent_graph

    with ai_lock:
        if agent_graph is not None:
            return agent_graph

        if vector_collection is None:
            raise HTTPException(
                status_code=503,
                detail="Vector database is unavailable.",
            )

        try:
            agent_graph = build_graph(vector_collection)

            print("LangGraph agent initialized.")

            return agent_graph

        except HTTPException:
            raise

        except Exception as error:
            print("Agent initialization failed:", error)

            raise HTTPException(
                status_code=503,
                detail="AI agent is currently unavailable.",
            ) from error


# --------------------------------------------------
# 7. Startup
# --------------------------------------------------


@app.on_event("startup")
def startup_event():
    initialize_vector_database()
    print("KrishiYojana API startup completed.")


# --------------------------------------------------
# 8. Load Scheme Records
# --------------------------------------------------


def load_records():

    try:
        with open(RECORDS_FILE, "r", encoding="utf-8") as file:
            records = json.load(file)

        if not isinstance(records, list):
            raise ValueError(
                "Expected records.json to contain a list."
            )

        return records

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=500,
            detail="Scheme records file not found.",
        ) from error

    except (json.JSONDecodeError, ValueError) as error:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid scheme records file: {error}",
        ) from error


# --------------------------------------------------
# 9. Find Scheme Document Requirements
# --------------------------------------------------


def get_scheme_documents(question: str):

    records = load_records()
    question_lower = question.casefold()

    for record in records:

        scheme_name = record.get("scheme_name", "")

        if scheme_name and scheme_name.casefold() in question_lower:

            documents = record.get("required_documents", [])

            if not documents:
                return None

            document_list = "\n".join(
                f"{index}. {document}"
                for index, document in enumerate(
                    documents,
                    start=1,
                )
            )

            return {
                "question": question,
                "answer": (
                    f"Required documents for {scheme_name}:\n\n"
                    f"{document_list}"
                ),
                "sources": [
                    {
                        "title": scheme_name,
                        "source": "records.json",
                        "page": "Not applicable",
                        "url": record.get("source_url"),
                    }
                ],
                "confidence": "high",
            }

    return None


# --------------------------------------------------
# 10. Home Endpoint
# --------------------------------------------------


@app.get("/")
def home():

    return {
        "message": "Welcome to KrishiYojana API",
        "status": "running",
    }


# --------------------------------------------------
# 11. Health Check
# --------------------------------------------------


@app.get("/health")
def health():

    database_ready = vector_collection is not None

    return {
        "status": (
            "healthy"
            if database_ready
            else "degraded"
        ),
        "application": "KrishiYojana",
        "vector_database": database_ready,
        "embedding_model": is_embedding_model_loaded(),
        "agent": agent_graph is not None,
        "initialization_error": initialization_error,
    }


# --------------------------------------------------
# 12. Ask Endpoint: Records + RAG
# --------------------------------------------------


@app.post("/ask")
def ask(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    # First check structured scheme records.
    document_answer = get_scheme_documents(question)

    if document_answer:
        return document_answer

    if vector_collection is None:
        raise HTTPException(
            status_code=503,
            detail="Vector database is unavailable.",
        )

    cache_key = f"ask:{question.casefold()}:3"
    cached_answer = response_cache.get(cache_key)
    if cached_answer is not None:
        return cached_answer

    try:
        answer = ask_question(
            question=question,
            vector_collection=vector_collection,
            top_k=3,
        )
        response_cache.set(cache_key, answer)
        return answer

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to generate an answer: {error}",
        ) from error


# --------------------------------------------------
# 13. LangGraph Agent Endpoint
# --------------------------------------------------


@app.post("/agent")
def run_agent(request: AgentRequest):

    if request.approval is None and (
        not request.question or not request.question.strip()
    ):
        raise HTTPException(
            status_code=400,
            detail="A question is required to start the agent.",
        )

    graph = get_agent_graph()

    thread_id = request.thread_id or str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    try:

        if request.approval is not None:
            checkpoint_state = graph.get_state(config)
            if not checkpoint_state.interrupts:
                raise HTTPException(
                    status_code=409,
                    detail=(
                        "In-memory checkpoints have no pending approval "
                        "for this thread."
                    ),
                )

            result = graph.invoke(
                Command(
                    resume={
                        "approved": request.approval,
                    }
                ),
                config=config,
            )

        else:
            result = graph.invoke(
                {
                    "question": request.question.strip(),
                    "farmer_details": request.farmer_details or {},
                },
                config=config,
            )

        interruptions = result.get("__interrupt__", [])

        if interruptions:

            interrupt_data = [
                item.value
                for item in interruptions
            ]

            return {
                "status": "awaiting_approval",
                "thread_id": thread_id,
                "approval_request": interrupt_data,
                "message": (
                    "Please approve or reject the selected tool."
                ),
            }

        return {
            "status": result.get("status", "completed"),
            "thread_id": thread_id,
            "question": result.get("question"),
            "tools_to_use": result.get("tools_to_use", []),
            "approved": result.get("approved"),
            "results": result.get("results", {}),
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Agent execution failed: {error}",
        ) from error


# --------------------------------------------------
# 14. Get All Scheme Records
# --------------------------------------------------


@app.get("/records")
def get_records():

    return load_records()


# --------------------------------------------------
# 15. Get Individual Scheme
# --------------------------------------------------


@app.get("/records/{record_id}")
def get_record(record_id: str):

    records = load_records()

    for record in records:

        if str(record.get("id")) == record_id:
            return record

    raise HTTPException(
        status_code=404,
        detail="Scheme record not found.",
    )


# --------------------------------------------------
# 16. Search Scheme Records
# --------------------------------------------------


@app.get("/search")
def search_schemes(query: str | None = None, q: str | None = None):
    search_query = query if query is not None else q

    if search_query is None:
        raise HTTPException(
            status_code=422,
            detail="A search query is required.",
        )

    query_lower = search_query.strip().casefold()

    if not query_lower:
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty.",
        )

    records = load_records()

    results = [
        record
        for record in records
        if query_lower in record.get(
            "scheme_name", ""
        ).casefold()
    ]

    return {
        "query": search_query,
        "total_results": len(results),
        "results": results,
    }
