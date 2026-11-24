# Project Finalization Progress

The repository did not contain a root `PROGRESS.md` when Day 14 review began.
This tracker records the review evidence and work that remains; it does not
replace the historical entries in [`docs/DAILY_PROGRESS.md`](docs/DAILY_PROGRESS.md).

## Completed with evidence

| Item | Evidence |
|---|---|
| Interview preparation and source-checked hardest-problem story | [`docs/interview.md`](docs/interview.md); claims are labeled implemented, partial, or proposed |
| Two-run demo checklist prepared | [`docs/demo_rehearsal.md`](docs/demo_rehearsal.md); neither run is complete |
| RAG/source metadata and 2025–26 notice checked against local files | The checked HTML snapshot says “from 2025–26 onwards”; PDF guidance is marked 2018–19; no separate Benefit PDF or capture/issue date is present |
| Local feedback file protected from future accidental commits | `ui/feedback.json` was removed from the Git index and preserved locally; `.gitignore` already excludes it |
| RAG retrieval and response validation | New ephemeral ChromaDB tests cover relevant ranking, filename/title/page mapping, HTML page normalization, unsupported answers, empty indexes, and surfaced retrieval failures; no exact GR, financial-year, or multilingual support is asserted |
| Agent/API validation | Tests cover invalid approval schema, rejecting an invalid graph resume without tool execution, initialization failure (503), execution timeout (500 with request ID), plus existing approval and rejection flows |
| Frontend validation | Existing tests cover AI Chat, Document Bag, and feedback; new tests cover direct-chat connection/timeout/server errors and retryable approval timeout handling |
| Groq timeout handling | Explicit `APITimeoutError` mapping added and regression-tested; existing request ID, latency, cache, and token-usage coverage retained |
| Local pytest, Ruff, and compileall checks | `python -m pytest -v`: 77 passed; Ruff and compileall passed; two existing deprecation warnings |
| Deployment availability spot-check | On 23 November 2026, Streamlit URL and a later backend `/health` retry returned HTTP 200; ChromaDB was available, while embedding model and agent were lazy/uninitialized; `/records` returned HTTP 200 |
| Existing `final` tag integrity | Confirmed annotated tag exists locally and on `origin`, with the same tag object and peeled commit (`efd116e`); tag was not modified |

## Open or blocked

| Item | Status | Reason |
|---|---|---|
| Marathi-English mixed-language retrieval | Open — feature gap | No multilingual retrieval configuration or quality evidence is present in the implementation |
| Scheme/year/effective-date-aware retrieval and exact GR citations | Open — feature gap | Indexed metadata and retrieval filters do not identify controlling GR versions or financial years |
| Rehearse the full demo once | Open — owner action | Must be completed and confirmed personally; automated tests are not a rehearsal |
| Rehearse the full demo a second time | Open — owner action | Must be a separate run and personally confirmed |
| Verify live agent approval and live RAG behavior for the final demo | Open — owner action | No live AI/agent request was made during this review; automated tests use mocks or ephemeral local fixtures |
| Measure Render server latency, cache hit/miss totals, and Groq token usage | Open — external access | Requires correlated entries from Render Logs; local tests and client timings do not establish these production values |
| Run CI for the final changes | Open — repository action | The workflow runs on pushes to `main`/`master` or PRs targeting them; no push or PR was created, so no new GitHub Actions run was triggered |
| Record/publish the demo video | Open — owner action | Existing documentation leaves the recording and public link pending; no recording was made here |

Both rehearsal checklists remain unchecked. The existing `final` tag points to
the current committed HEAD, not the uncommitted worktree changes; do not move,
overwrite, or recreate it.
