# Daily Development Progress Report

## Day 9 – LangGraph Approval and Eligibility Tool

**Date:** 17 November 2026

### Objective

Complete the approval-gated LangGraph workflow, exercise the eligibility tool and existing API endpoints, handle missing farmer details, and document the implementation and its limitations.

### Tasks Completed

1. Reproduced the reported `KeyError('question')` when an approval was resumed after rebuilding the graph with a fresh in-memory checkpointer.
2. Confirmed the cause: `MemorySaver` loses checkpoint state when the application process restarts. A resume with no pending checkpoint left the graph without the original question, which `select_tools` previously indexed directly.
3. Validated that the approval `thread_id` is reused for the resume and added an API check that returns HTTP 409 with a clear message when no pending approval is available.
4. Added explicit non-empty question validation in the graph and missing/blank farmer-detail handling in the graph and hand-written agent.
5. Verified both eligibility and ineligibility outcomes using the five required farmer fields.
6. Added a focused `unittest` suite for approval/rejection, thread resumption, checkpoint loss, missing details, eligibility outcomes, and existing endpoints.
7. Updated the README with project features, technology, RAG and LangGraph workflows, API usage, setup, testing, and known limitations.

### Files Created or Modified

- `app/main.py` — validate that a pending approval checkpoint exists before resuming.
- `app/graph.py` — validate graph questions, report missing farmer fields, and return a `needs_information` state where appropriate.
- `app/agent_loop.py` — report all missing/blank farmer details without treating `false` as missing.
- `requirements.txt` — declare the LangGraph dependency.
- `test_day9.py` — add automated Day 9 API and workflow tests.
- `README.md` — document the completed Day 9 features and workflows.
- `docs/DAILY_PROGRESS.md` — record this report.

The Day 9 eligibility implementation also uses `app/tools.py` and `data/rules/scheme_rules.json`. These rules are demonstrations only and are not official government criteria.

### Testing Performed

- `.venv/bin/python -m unittest test_day9 -v` — **passed, 6 tests**.
- `.venv/bin/python -m compileall -q app test_day9.py` — **passed**.
- `.venv/bin/python test_eligibility.py` — **passed**; the eligible and ineligible demonstration inputs produced the expected outcomes.
- Pylance diagnostics for `app/main.py`, `app/graph.py`, `app/agent_loop.py`, and `test_day9.py` — **no diagnostics**.
- API tests cover `/health`, `/records`, `/records/{id}`, `/search`, `/questions`, `/search/semantic`, `/chat`, `/ask`, and `/agent`. LLM/RAG calls and semantic retrieval are mocked in this automated suite; the test does not require a Groq API key.

### Results and Observations

- Initial requests return `awaiting_approval`; approval resumes the selected eligibility tool, while rejection returns `rejected` without executing it.
- The same thread ID is returned and supplied across the tested resume flow.
- Approved eligibility checks return both a positive and a negative demonstration result.
- Missing and blank required details are enumerated in the response. Boolean `false` remains a valid supplied value.
- A resume with no in-memory checkpoint returns HTTP 409 instead of an unhandled `KeyError`.

### Known Limitations

- `MemorySaver` checkpoints are process-local and are lost on application restart. The caller must start a new agent request after restart; durable approval resumption requires a persistent checkpointer.
- Eligibility rules are illustrative and do not provide official government eligibility decisions.
- Live Groq-backed generation was not exercised by the automated API tests.

**Status:** Completed

## Day 12 – FastEmbed Runtime and Render Deployment

**Date:** 21 November 2026

### Deployment

- **Backend:** https://gen-ai-examate.onrender.com
- **API documentation:** https://gen-ai-examate.onrender.com/docs
- **Agent API:** `POST https://gen-ai-examate.onrender.com/agent`

### Public Endpoint Verification

- `GET /health` — HTTP 200; status `healthy`; ChromaDB available.
- `GET /docs` — HTTP 200.
- `GET /records` — HTTP 200.
- At the time of the health check, the embedding model and agent were not yet initialized; both load lazily when used.
- A separate public Streamlit UI URL has not been confirmed.

**Status:** Backend deployed and public API endpoints verified; public UI URL still needs confirmation.

## Day 13 – Production Readiness

**Date:** 22 November 2026

### Completed

- Added API request latency logging in milliseconds.
- Added Groq prompt, completion, and total token usage logging.
- Added a thread-safe in-memory `/ask` response cache with TTL and maximum-size eviction.
- Added cache hit/miss logging, fixed existing-key updates, and verified TTL/LRU behavior and failure exclusion.
- Enforced 2,000-character question limits on `/ask` and `/agent`; empty and whitespace-only questions are rejected.
- Strengthened RAG instructions to treat retrieved content as untrusted factual reference material and not reveal internal prompts or secrets.
- Added mocked prompt-contract security coverage, cache tests, input validation tests, and production metric logging tests.
- Added Streamlit tests for direct chat, agent approval/rejection and thread persistence, Document Bag deduplication/download, and both feedback choices.
- Prepared a separate `krishiyojana-ui` Render service in `render.yaml`; it uses `requirements-ui.txt` and the existing backend's `API_URL`.
- Updated the README with the Day 13 section, separate UI deployment instructions, a production measurement checklist, and pending-value markers.
- Added exactly three resume bullets in `docs/resume.md`, using checked scheme and local index counts.

### Locally Verified

- `python -m compileall -q app ui tests` — passed.
- `python -m ruff check .` — passed.
- `python -m pytest -q` — 55 passed; two FastAPI startup-event deprecation warnings. pytest-asyncio also emitted a fixture loop-scope configuration warning.
- `docker build -t krishiyojana:day13 .` — passed; the image build indexed 136 chunks inside the image.
- Frontend automated tests use mocked HTTP requests; no automated production approval or rejection was sent.

### Production and External Status

- Read-only `GET /health` on 22 November 2026 returned HTTP 200 and `status=healthy`; ChromaDB was available. The response reported `embedding_model=false` and `agent=false`, consistent with lazy initialization; no live RAG or agent request was sent during this check. The initial 25-second health request timed out; a subsequent retry returned HTTP 200.
- Read-only `GET /records` returned HTTP 200 with 19 scheme records.
- The backend service remains the existing `Gen-AI-Examate` service; no backend configuration or credentials were changed.
- The separate Streamlit service is prepared but not yet created in Render. A public frontend URL is pending.
- The latest observed GitHub Actions run (before these uncommitted changes) succeeded for its configured Ruff, Pytest, and Docker Build steps. The workflow now selects the full pytest suite; CI for this worktree is pending an approved push/PR.
- Live Render API latency, cache-hit/miss totals, and Groq token totals are pending access to Render Logs. No performance numbers are claimed.
- Day 12 previously documented successful production RAG and LangGraph approval/resume checks. Those production workflows were not re-exercised in this Day 13 run.
- Demo recording and public video link are pending the final project demonstration.

**Status:** Local implementation and validation completed; separate frontend deployment, current-branch CI, live metrics, and demo video remain pending.
