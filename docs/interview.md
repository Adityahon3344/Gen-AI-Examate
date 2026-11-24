# KrishiYojana Interview Preparation

## A. 60-second project pitch

“KrishiYojana is a prototype assistant that helps farmers in Maharashtra find
and understand agricultural government scheme information. Scheme rules are
spread across portal pages, structured records, and long PDF documents, so it
can be difficult to find the right information quickly. I built a Streamlit
interface backed by a FastAPI service. For document questions, the service
embeds the query with FastEmbed, retrieves the top matching chunks from
ChromaDB, and asks a Groq-hosted language model to answer from that context.
The response includes the retrieved document title, file, and page where
available. There is also a LangGraph agent that pauses for human approval
before running a selected RAG or demonstration eligibility tool, plus a
Document Bag for combining required-document checklists. The goal is to make
scheme information easier to navigate while keeping its source visible. It is
a prototype, not an official eligibility decision service, and its current
document set does not yet support reliable Marathi-English or financial-year
version-aware retrieval.”

## B. Likely technical interview questions

### 1. What is KrishiYojana and what problem does it solve?

KrishiYojana is a prototype information assistant for agricultural schemes in
Maharashtra. It brings scheme records and a small set of source documents
behind a natural-language interface. A farmer can ask a question, search
records, or prepare a combined document checklist. The goal is to reduce the
effort of finding scheme information; the application does not make an
official eligibility decision.

### 2. Why did you choose RAG instead of a normal LLM chatbot?

A general-purpose chatbot can answer from model training rather than from
current scheme material, which is risky for eligibility, benefits, and
deadlines. RAG retrieves passages from the project's document collection and
passes them to the model as evidence. The current prompt instructs the model to
stay within that context and abstain when it cannot find an answer. This
reduces, but does not eliminate, hallucinations. The corpus and retrieval
quality still limit what can be answered.

### 3. Explain the complete architecture and data flow.

The user interface is written in Streamlit and calls a FastAPI backend. For
`/ask`, the backend first checks whether any structured scheme name appears
in the question; if so, it returns that record's required-document list,
even if the question asks about another detail. Otherwise it embeds the
question with FastEmbed, queries a persistent ChromaDB collection for up to
three chunks, and sends the retrieved text and metadata to a Groq-hosted model.
The response contains the answer, confidence label, and source title, file,
and page when available. `/agent` uses LangGraph to choose between RAG and a
demonstration eligibility check, requests human approval, and only then
executes the selected tool. Its current `MemorySaver` checkpoint is in
process memory, so a restart loses pending approvals. The UI also supports
feedback and a Document Bag checklist.

### 4. How do you extract, clean, chunk, embed, and retrieve PDF content?

The ingestion code uses `pypdf` to extract text page by page, and
BeautifulSoup to remove script, style, and noscript tags from HTML. It splits
text into overlapping chunks of 1,000 words with a 150-word overlap and saves
the source filename, page, and title. Offline document vectors are produced
with SentenceTransformers using `all-MiniLM-L6-v2`; the runtime query vector is
produced by FastEmbed using the same model family. ChromaDB stores the vectors
with cosine distance, and the RAG path retrieves up to three chunks. This is
text extraction, not OCR; scanned pages or poor PDF text extraction need
additional handling.

### 5. How would you support Marathi-English mixed-language retrieval?

I would not claim that the current retrieval is multilingual: the configured
`all-MiniLM-L6-v2` embedding model has not been validated here for Marathi or
mixed-language queries, and the tests do not establish cross-language
retrieval quality. I would compare a multilingual embedding model on a
Marathi-English evaluation set, retain original text and language metadata,
and test both code-switched queries and transliteration. A query expansion or
translation stage could help, but should preserve exact names and amounts and
be evaluated against the official source rather than assumed to work.

### 6. How do you ensure answers cite the exact Government Resolution (GR)?

The current RAG code returns retrieved title, filename, and page metadata; it
does not identify or validate a GR number, preserve a source URL for indexed
chunks, or prove that a citation is the exact controlling GR. The available
corpus also lacks a separate Benefit PDF. I would add verified document
metadata for the official GR title and number, issuing authority, issue and
effective dates, scheme, financial year, official URL, and page. The answer
should cite that metadata and the page that supports each claim. If the
retrieved material cannot support a precise citation, the system should say
so rather than invent one.

### 7. How do you handle multiple versions of a scheme and changing rules?

The current index has no scheme-version or financial-year filters, so it
cannot reliably separate old and current rules. A production design should
record scheme identity, document type, language, financial year, issue date,
effective period, and supersession relationships. Retrieval should first
identify the requested scheme and year, then prefer the newest applicable
official notice for that scheme and year. Upload time is not authority: the
newest file added may be an old notice or a notice for a different scheme.
Conflicting or incomplete evidence should trigger an explicit qualification
or abstention.

### 8. How do you reduce hallucinations and improve retrieval accuracy?

The RAG prompt treats retrieved text as untrusted reference material, tells
the model to answer only from the retrieved context, asks it not to invent
scheme details, and requires “I don't know” when the context lacks the answer.
Retrieved source metadata is returned with the response. These are safeguards,
not guarantees: the code currently retrieves the top three chunks without a
relevance threshold or reranker, and the confidence label is a simple
rule-based value rather than a calibrated score. I would add verified
metadata filters, multilingual retrieval tests, reranking, a relevance
threshold, claim-to-source checks, and hard examples for stale or conflicting
documents.

### 9. How do you evaluate the RAG application?

I use automated tests for API validation, cache behavior, agent approval and
rejection, UI interactions, and source-response contracts. The repository
also has a 15-question evaluation set and a script that compares chunking
configurations using keyword coverage, presence of a `[Source]` marker, and
abstention behavior. Those are useful diagnostics, not proof of factual
correctness or exact citations. I would add manually reviewed expected
passages and GR citations, retrieval recall/ranking measures, factual and
citation correctness, Marathi/code-switch cases, and version-conflict cases.
I would rerun the suite against a pinned corpus before reporting metrics.

### 10. What were the biggest technical challenges and what would you improve next?

The main challenge is discussed in the interview story below: the important
rules are distributed across sources with different languages and years, but
the index currently stores only basic source metadata. I addressed the
retrieval and citation plumbing for a prototype and documented the evidence
gaps; I did not implement version-aware or multilingual retrieval. Next I
would build a verified source registry, add language and effective-date
metadata, implement year-aware retrieval and exact citations, then evaluate
those changes against a human-reviewed test set. I would also replace the
process-local agent checkpointer before relying on approvals across restarts.

## Hardest technical problem: evidence across language and time

### Interview story

“The hardest problem was not simply finding a relevant paragraph. Important
scheme details can be split across an English scheme page, Marathi Government
Resolution text, and a separate benefits document. A useful answer has to
match the scheme and financial year, avoid combining old and new conditions,
and show exactly which official source supports each claim.

“I checked the actual files in this repository before using the
first-come, first-served example. The local HTML snapshot of the MahaDBT
farm-mechanization page says that the approach would apply ‘from the year
2025–26 onwards’ and that earlier-submitted applications are considered
first. The wording says ‘onwards’; it does not say the rule applied only in
2025–26. The snapshot has no capture date or notice issue date. The bundled
`Scheme-SubMissionOnFarmMechanization.pdf` contains Government of India
operational guidelines revised in 2018–19 and a Maharashtra mechanization
procedure marked 2018–19; a text search did not find the 2025–26 notice in
that PDF. The corpus has no separate Benefit PDF. So I cannot claim from
these files when the online notice was issued, that the rule was exclusive
to one year, or which exact current GR controls it.

“That creates a retrieval problem as well as a language problem. The
prototype currently chunks PDF and HTML text and stores only a source name,
title, and page. It uses a single embedding model and retrieves the top
chunks; there are no Marathi-English quality tests, scheme/year filters,
effective-date fields, or supersession links. The RAG response can return the
retrieved file and page, but that is not the same as verifying an exact GR
citation.

“My proposed solution is to register each official source with its scheme,
document type, language, financial year, issue date, effective dates,
official URL, and supersession relationship. I would retrieve across the
verified Marathi and English sources, choose the newest applicable official
notice for the requested scheme and year—not the newest uploaded file—and
cite the exact title or GR identifier and supporting page. I would evaluate
mixed-language queries and old-versus-new rule questions separately. If the
source set does not establish the answer, the assistant should disclose that
and abstain.

“The result so far is a working RAG path with basic file/page references and
a prompt-level abstention rule, plus a clearly identified source/versioning
gap. Multilingual retrieval, exact GR identification, and year-aware
precedence remain proposed work, not implemented features.”

### Implementation status at a glance

| Area | Verified status |
|---|---|
| PDF/HTML text extraction, word-based chunking, and source/title/page metadata | Implemented |
| FastEmbed query vector, ChromaDB top-three retrieval, Groq answer generation | Implemented |
| Basic source filename/title/page response references | Implemented; not a verified exact GR citation |
| Prompt asks for context-only answers and abstention when unsupported | Implemented; not a guarantee |
| Marathi-English mixed-language retrieval | Not validated; proposed improvement |
| Separate Benefit PDF in the checked corpus | Not present |
| Scheme/year/effective-date and supersession-aware retrieval | Not implemented; proposed improvement |

The evidence above was checked in
[`farm_mechanization.html`](../data/raw/farm_mechanization.html),
[`Scheme-SubMissionOnFarmMechanization.pdf`](../data/raw/Scheme-SubMissionOnFarmMechanization.pdf),
[`chunking.py`](../app/chunking.py),
[`rag.py`](../app/rag.py), and
[`vectorstore.py`](../app/vectorstore.py).
