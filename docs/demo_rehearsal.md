# KrishiYojana Demo Rehearsal Checklist

Complete this checklist twice in two separate practice runs. Leave every box
unchecked until that rehearsal has actually been completed. These checklists
are for the project owner; automated tests do not count as rehearsals.

## Rehearsal 1

- [ ] Start the FastAPI backend and confirm its health/API documentation are
  reachable.
- [ ] Start or open the Streamlit frontend and confirm the page is available
  and connected to the intended backend.
- [ ] Ask a farmer-related scheme question that the checked knowledge base can
  answer.
- [ ] Show the retrieved scheme information and explain the displayed source
  title, filename, and page; do not describe them as an exact GR citation
  unless the source itself verifies that.
- [ ] Choose AI Agent mode, show the pending approval, approve the selected
  tool, and explain the result. Optionally demonstrate rejection without
  executing the tool.
- [ ] Open Document Bag, select multiple schemes, explain deduplication, and
  download the checklist.
- [ ] Submit Helpful or Not Helpful feedback and confirm the UI acknowledgement.
- [ ] Explain the Streamlit → FastAPI → FastEmbed → ChromaDB → Groq RAG flow,
  plus the LangGraph approval step.
- [ ] Ask a question that cannot be supported by the checked knowledge base;
  show the abstention and explain why it is safer than guessing.
- [ ] Do not claim Marathi-English retrieval or financial-year-aware retrieval
  is implemented; explain these as limitations/proposed work.

**Rehearsal 1 completed:** ________  **Date:** ________

## Rehearsal 2

- [ ] Start the FastAPI backend and confirm its health/API documentation are
  reachable.
- [ ] Start or open the Streamlit frontend and confirm the page is available
  and connected to the intended backend.
- [ ] Ask a farmer-related scheme question that the checked knowledge base can
  answer.
- [ ] Show the retrieved scheme information and explain the displayed source
  title, filename, and page; do not describe them as an exact GR citation
  unless the source itself verifies that.
- [ ] Choose AI Agent mode, show the pending approval, approve the selected
  tool, and explain the result. Optionally demonstrate rejection without
  executing the tool.
- [ ] Open Document Bag, select multiple schemes, explain deduplication, and
  download the checklist.
- [ ] Submit Helpful or Not Helpful feedback and confirm the UI acknowledgement.
- [ ] Explain the Streamlit → FastAPI → FastEmbed → ChromaDB → Groq RAG flow,
  plus the LangGraph approval step.
- [ ] Ask a question that cannot be supported by the checked knowledge base;
  show the abstention and explain why it is safer than guessing.
- [ ] Do not claim Marathi-English retrieval or financial-year-aware retrieval
  is implemented; explain these as limitations/proposed work.

**Rehearsal 2 completed:** ________  **Date:** ________

## Before each rehearsal

- Verify `.env` or the deployment environment contains credentials without
  displaying or recording them.
- Use a known, source-supported question and a separate unsupported question.
- Avoid entering real personal farmer details in the demo.
- Feedback is written to the local `ui/feedback.json` runtime file; do not add
  that file to a commit.

Neither rehearsal is marked complete by this document.
