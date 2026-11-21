
# KrishiYojana – AI-Powered Farmer Scheme Eligibility & Benefits Assistant

[![KrishiYojana CI](https://github.com/Adityahon3344/Gen-AI-Examate/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/Adityahon3344/Gen-AI-Examate/actions/workflows/ci.yml)

An AI-powered agricultural scheme assistant designed to help farmers in Maharashtra discover government schemes, understand benefits, explore eligibility requirements, and receive information through natural-language conversations.

**Project Name:** KrishiYojana
**Target Users:** Farmers in Maharashtra, India
**Primary Data Source:** MahaDBT Farmer Portal
**GitHub Repository:** https://github.com/Adityahon3344/Gen-AI-Examate

---

# 1. Project Overview

KrishiYojana is an AI-powered agricultural government scheme information assistant developed to make agricultural scheme information easily accessible to farmers in Maharashtra.

Farmers often face difficulties finding relevant government schemes, understanding eligibility conditions, identifying required documents, and accessing accurate information.

KrishiYojana combines Retrieval-Augmented Generation (RAG), Large Language Models (LLMs), semantic search, vector databases, and agent-based workflows to provide relevant scheme information.

The system allows farmers to:

- Search agricultural government schemes.
- Understand scheme benefits.
- View eligibility requirements.
- Find required documents.
- Ask questions in natural language.
- Receive AI-generated answers with source references.
- Check eligibility using configured scheme rules.
- Interact with an AI agent using human approval.

# 2. Project Objectives

1. Make agricultural government scheme information easily accessible.
2. Develop a structured agricultural scheme knowledge base.
3. Implement keyword-based and semantic search.
4. Integrate Large Language Models for intelligent responses.
5. Implement Retrieval-Augmented Generation.
6. Store document embeddings in ChromaDB.
7. Develop a farmer eligibility checking system.
8. Implement an intelligent AI agent using LangGraph.
9. Add human-in-the-loop approval before agent tool execution.
10. Provide source-based answers for better transparency.
11. Deploy the FastAPI application on Render.
12. Optimize application dependencies for limited deployment resources.

# 3. Key Features

## 3.1 Scheme Management
- Store agricultural scheme records.
- Retrieve scheme information using unique IDs.
- Search schemes using keywords.
- Display scheme benefits and eligibility.
- Display required documents.

## 3.2 Intelligent Search
- Keyword-based search.
- Semantic search using sentence embeddings.
- Retrieve relevant information from agricultural documents.
- Search using natural-language queries.

## 3.3 RAG-Based Question Answering
- Accept natural-language questions.
- Generate query embeddings using FastEmbed.
- Retrieve relevant document chunks from ChromaDB.
- Generate contextual responses using Groq.
- Return source references with generated answers.
- Provide answers grounded in retrieved documents.

## 3.4 Farmer Eligibility Checking
- Collect farmer information.
- Validate required farmer details.
- Check configured scheme eligibility rules.
- Identify missing information.
- Return eligibility-related results.

## 3.5 LangGraph AI Agent
- Select tools based on user questions.
- Route requests to RAG search or eligibility checking.
- Request human approval before executing tools.
- Pause workflow using LangGraph interrupt.
- Resume execution after approval.
- Stop execution when rejected.
- Maintain workflow state using MemorySaver.

## 3.6 Streamlit User Interface
- Direct Chat interface.
- AI Agent interaction.
- Display generated answers.
- Display source citations.
- Display confidence information.
- Approval and rejection controls.
- Response feedback.
- Document Bag functionality.

## 3.7 Document Bag
- Select multiple agricultural schemes.
- Select two or three schemes.
- Retrieve required documents.
- Combine document requirements into one checklist.
- Remove duplicate document entries.
- Display the schemes associated with documents.
- Download the consolidated checklist.

# 4. Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| Frontend Framework | Streamlit |
| LLM Provider | Groq |
| Agent Framework | LangGraph |
| RAG Architecture | Retrieval-Augmented Generation |
| Embedding Model | all-MiniLM-L6-v2 |
| Embedding Runtime | FastEmbed |
| Offline Embedding Tools | SentenceTransformers |
| Vector Database | ChromaDB |
| Data Processing | Pandas |
| Numerical Processing | NumPy |
| API Server | Uvicorn |
| API Testing | Swagger UI |
| Code Quality | Ruff |
| Testing Framework | Pytest |
| Containerization | Docker |
| Version Control | Git and GitHub |
| CI/CD | GitHub Actions |
| Deployment Platform | Render |

# 5. Complete Project Folder Structure

Gen-AI-Examate/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── records.py
│   ├── models.py
│   ├── cli.py
│   ├── fetch.py
│   ├── ingest.py
│   ├── chunking.py
│   ├── embed.py
│   ├── embeddings.py
│   ├── semantic_search.py
│   ├── smart_search.py
│   ├── rag.py
│   ├── llm.py
│   ├── graph.py
│   ├── tools.py
│   ├── vectorstore.py
│   └── agent_loop.py
│
├── data/
│   ├── __init__.py
│   ├── sample_records.py
│   ├── records.json
│   ├── chunks.json
│   │
│   ├── rules/
│   │   └── scheme_rules.json
│   │
│   ├── raw/
│   │   ├── DBT_Farmer_User_Manual.pdf
│   │   ├── Scheme-SubMissionOnFarmMechanization.pdf
│   │   ├── extracted_text.txt
│   │   └── farm_mechanization.html
│   │
│   └── chroma_db/
│       └── Generated vector database files
│
├── ui/
│   └── app.py
│
├── analysis/
│   ├── __init__.py
│   └── explore.py
│
├── docs/
│   ├── DAILY_PROGRESS.md
│   ├── how_llms_work.md
│   └── user_questions.md
│
├── eval/
│   ├── results/
│   │   ├── comparison.md
│   │   └── rag_eval_results.json
│   │
│   ├── eval_set.json
│   ├── prompt_compare.md
│   ├── results.json
│   ├── run_eval.py
│   ├── run_prompt_eval.py
│   └── search_results.md
│
├── prompts/
│   ├── eval_prompt_v1.txt
│   ├── eval_prompt_v2.txt
│   ├── system_prompt.txt
│   ├── task_prompt_1.txt
│   └── task_prompt_2.txt
│
├── test_agent.py
├── test_day9.py
├── test_eligibility.py
├── test_eligibility_graph.py
├── test_graph.py
├── test_missing_details.py
├── test_rejection.py
│
├── day01_intro.py
├── day01_menu.py
├── sync_records.py
│
├── Dockerfile
├── .env.example
├── requirements.txt
├── requirements-runtime.txt
├── .gitignore
└── README.md

Note:
- The structure represents the main project modules and files.
- Generated ChromaDB files are not required to be committed.
- Local .env and virtual environment folders should not be pushed to GitHub.
- Keep API credentials outside the source code.

# 6. Folder and File Description

| File / Folder | Purpose |
|---|---|
| app/ | Main application and backend modules |
| app/main.py | FastAPI application and API endpoints |
| app/embeddings.py | FastEmbed query embedding generation |
| app/embed.py | Offline document embedding generation |
| app/rag.py | RAG retrieval and answer generation |
| app/llm.py | Groq LLM integration |
| app/graph.py | LangGraph agent workflow |
| app/tools.py | Eligibility and agent tools |
| app/vectorstore.py | ChromaDB database creation |
| app/fetch.py | Data fetching |
| app/ingest.py | Document ingestion |
| app/chunking.py | Text chunking |
| app/semantic_search.py | Semantic search |
| data/records.json | Structured scheme records |
| data/chunks.json | Document chunks and embeddings |
| data/rules/ | Eligibility configuration |
| data/raw/ | Original source documents |
| data/chroma_db/ | Generated vector database |
| ui/ | Streamlit interface |
| analysis/ | Data exploration scripts |
| docs/ | Project documentation |
| eval/ | RAG evaluation files |
| prompts/ | AI prompts |
| tests | Test scripts |
| Dockerfile | Container build configuration |
| requirements.txt | Project dependencies |
| requirements-runtime.txt | Runtime dependencies |
| README.md | Main project documentation |

---

# 7. Day-by-Day Development Progress (Day 1 to Day 12)

## Day 1 – Project Introduction and Initial Setup

**Objective:** Establish the project foundation.

Activities:
- Finalized the project title as KrishiYojana.
- Identified Maharashtra farmers as the target users.
- Identified the problem of difficulty finding agricultural government scheme information.
- Selected MahaDBT Farmer Portal as the primary data source.
- Created the initial project structure.
- Created README.md.
- Developed an introductory Python program.
- Implemented a menu-driven interface.
- Displayed the project information through the menu.

Files created:
- README.md
- day01_intro.py
- day01_menu.py

Outcome:

Completed the initial project setup and developed a basic menu-driven Python application.

---

## Day 2 – Dataset Collection and Scheme Management

**Objective:** Develop a structured agricultural scheme dataset.

Activities:
- Explored the MahaDBT Farmer Portal.
- Studied agricultural schemes under the Farmer Schemes section.
- Collected scheme overview information.
- Collected eligibility requirements.
- Collected required document information.
- Created sample agricultural scheme records.
- Stored scheme details using Python dictionaries.
- Implemented record-loading functionality.
- Developed keyword-based search.
- Implemented department-wise scheme counting.
- Added scheme retrieval using unique IDs.
- Configured the Python virtual environment.

Files created or modified:
- data/__init__.py
- data/sample_records.py
- app/__init__.py
- app/records.py
- app/cli.py
- requirements.txt
- .gitignore

Outcome:

Developed a structured agricultural scheme dataset and basic command-line scheme management functionality.

---

## Day 3 – Data Fetching and Document Ingestion

**Objective:** Develop the data collection and preparation process.

Activities:
- Implemented data-fetching functionality.
- Worked with agricultural scheme HTML pages.
- Downloaded and explored government PDF documents.
- Extracted relevant text from documents.
- Developed structured data models.
- Implemented JSON-based data ingestion.
- Organized extracted scheme information.
- Prepared documents for further processing.

Files created or modified:
- app/fetch.py
- app/ingest.py
- app/models.py
- data/records.json
- data/raw/
- data/raw/extracted_text.txt

Outcome:

Developed the data collection, extraction, and ingestion components to prepare agricultural scheme information for the AI application.

---

## Day 4 – FastAPI Backend and Intelligent Search

**Objective:** Develop the backend API and improve scheme discovery.

Activities:
- Installed and configured FastAPI.
- Configured Uvicorn.
- Created the backend API structure.
- Implemented the API health-check endpoint.
- Added scheme record retrieval.
- Developed search endpoints.
- Added question-related API functionality.
- Explored scheme data using Pandas.
- Studied TF-IDF-based search.
- Explored cosine similarity.
- Worked on intelligent scheme searching.

Files created or modified:
- app/main.py
- analysis/explore.py
- app/smart_search.py

Outcome:

Developed the initial FastAPI backend and intelligent search functionality.

---

## Day 5 – LLM Fundamentals and API Validation

**Objective:** Understand Large Language Models and validate the backend.

Activities:
- Studied Large Language Models.
- Understood how LLMs process user inputs.
- Explored how LLMs generate responses.
- Documented the working process of LLMs.
- Prepared 10 real-world project-related questions.
- Included questions that could not be answered using available project information.
- Tested backend APIs using Swagger UI.
- Tested the health-check endpoint.
- Created the checkpoint-1 Git tag.

Files created or modified:
- docs/how_llms_work.md
- README.md

Outcome:

Completed LLM fundamentals documentation and backend API validation.

---

## Day 6 – LLM Integration and AI-Powered Responses

**Objective:** Integrate a Large Language Model into the application.

Activities:
- Selected Groq as the LLM provider.
- Explored Groq API integration.
- Configured API-based LLM communication.
- Worked on passing user questions to the LLM.
- Developed the response-generation component.
- Explored system prompts and user prompts.
- Prepared the application for Retrieval-Augmented Generation.

Technology:
- Python
- Groq API
- Large Language Models

Outcome:

Completed the initial LLM integration development milestone and prepared the application for contextual AI responses.

---

## Day 7 – RAG and Semantic Retrieval Development

**Objective:** Develop document-based retrieval for knowledge-grounded question answering.

Activities:
- Studied Retrieval-Augmented Generation.
- Explored document loading and processing.
- Implemented text chunking.
- Explored sentence embeddings.
- Used the all-MiniLM-L6-v2 embedding model.
- Generated document embeddings.
- Integrated ChromaDB as the vector database.
- Developed semantic retrieval functionality.
- Worked on retrieving relevant document chunks.
- Prepared the application for context-based answer generation.

Files created or modified:
- app/chunking.py
- app/embed.py
- app/semantic_search.py
- app/vectorstore.py
- data/chunks.json

Technology:
- SentenceTransformers
- all-MiniLM-L6-v2
- ChromaDB
- NumPy

Outcome:

Developed the semantic retrieval and RAG foundation for agricultural document question answering.

---

## Day 8 – Agent Workflow and Eligibility Integration

**Objective:** Prepare the application for intelligent tool-based execution.

Activities:
- Worked on farmer eligibility checking.
- Created configurable scheme eligibility rules.
- Identified the farmer details required for eligibility checks.
- Prepared eligibility validation functionality.
- Developed tool-based application logic.
- Prepared the application for intelligent tool selection.
- Integrated RAG search and eligibility workflows into the agent architecture.

Important farmer details:
- Land holding
- Land size in acres
- Caste category
- Previous benefit received for the same component
- Existing tractor ownership

Files created or modified:
- data/rules/scheme_rules.json
- app/tools.py
- app/graph.py

Outcome:

Developed the eligibility-checking foundation and prepared the application for LangGraph-based agent orchestration.

---

## Day 9 – LangGraph Agent, Human Approval and Workflow Testing

**Objective:** Implement and validate the LangGraph-based agent workflow.

### 1. LangGraph Workflow

Activities:
- Implemented the agent state structure.
- Developed the select_tools node.
- Added routing between RAG search and eligibility checking.
- Implemented the approval workflow.
- Added approval_router for approved and rejected requests.
- Implemented the execute_tools node.
- Integrated LangGraph MemorySaver checkpointing.

### 2. Human-in-the-Loop Approval

Activities:
- Implemented interrupt() for approval requests.
- Added support for pausing agent execution.
- Implemented workflow resumption after approval.
- Added rejection handling.
- Ensured rejected requests do not execute tools.

### 3. Farmer Eligibility Validation

Activities:
- Implemented required farmer detail validation.
- Added missing-information handling.
- Integrated eligibility checking with the agent.
- Tested eligible and ineligible farmer scenarios.

### 4. API Integration

Activities:
- Integrated the agent workflow with FastAPI.
- Developed the /agent endpoint.
- Tested agent execution.
- Verified approval and rejection workflows.
- Verified workflow resumption.

### 5. Testing

Tests included:
- Eligibility checking.
- Graph execution.
- Approval workflow.
- Rejection workflow.
- Missing farmer details.
- Existing API endpoints.

Files created or modified:
- app/graph.py
- app/tools.py
- app/main.py
- test_agent.py
- test_eligibility.py
- test_eligibility_graph.py
- test_graph.py
- test_missing_details.py
- test_rejection.py
- test_day9.py

Day 9 Test Results:

| Test Case | Result |
|---|---|
| Eligible and ineligible farmer checks | PASS |
| Existing API endpoints | PASS |
| Missing farmer details | PASS |
| Rejection and workflow resumption | PASS |
| Resume without checkpoint | PASS |
| Agent missing-details handling | PASS |

Total automated test cases: 6

Passed: 6/6

Outcome:

Successfully implemented and tested the LangGraph approval workflow, eligibility validation, and agent integration with FastAPI.

---

## Day 10 – Streamlit Frontend and Document Bag Implementation

**Objective:** Develop an interactive Streamlit interface and integrate it with the FastAPI backend.

### 1. Streamlit User Interface

Activities:
- Developed the application interface using Streamlit.
- Connected the frontend with FastAPI.
- Implemented a conversational interface.
- Added Direct Chat interaction mode.
- Added AI Agent interaction mode.
- Displayed generated answers.

### 2. Backend API Integration

Activities:
- Integrated the /ask endpoint for Direct Chat.
- Integrated the /agent endpoint for AI Agent interactions.
- Added handling for agent approval requests.
- Implemented approval and rejection controls.
- Maintained the agent thread ID for workflow continuation.

### 3. Answers and Source Information

Activities:
- Displayed generated AI answers.
- Presented available source citations.
- Displayed confidence information.
- Improved response presentation.

### 4. User Feedback System

Activities:
- Added positive and negative feedback options.
- Saved feedback in a JSON file.
- Recorded user questions.
- Recorded generated answers.
- Stored ratings and submission timestamps.

### 5. Document Bag – Signature Feature

Activities:
- Developed the Document Bag feature.
- Enabled selection of multiple agricultural schemes.
- Allowed selection of two or three schemes.
- Retrieved required documents for selected schemes.
- Combined required documents into one checklist.
- Removed duplicate document entries.
- Displayed associated scheme names.
- Added an option to download the consolidated checklist.

### 6. Testing and Documentation

Activities:
- Tested Direct Chat.
- Tested AI Agent interactions.
- Verified agent approval and rejection handling.
- Tested feedback submission.
- Tested multi-scheme document selection.
- Tested document deduplication.
- Captured the Document Bag interface screenshot.

Files created or modified:
- ui/app.py
- screenshots/document-bag.png
- README.md

Outcome:

Developed a Streamlit-based interface with Direct Chat, AI Agent interaction, source citations, user feedback, and a consolidated Document Bag checklist.

The Streamlit interface was developed locally. A separate public frontend deployment URL has not yet been confirmed.

---

## Day 11 – GitHub Actions, Docker and Deployment Preparation

**Objective:** Prepare the KrishiYojana application for automated checks and cloud deployment.

Activities:

### 1. GitHub Repository Management

- Organized the project repository.
- Worked with feature-based Git branches.
- Used GitHub for version control.
- Prepared project changes for review and merging.
- Maintained the master branch.
- Updated project documentation.

Repository:
https://github.com/Adityahon3344/Gen-AI-Examate

Feature branch:
feature/day11-ci-deployment

### 2. Continuous Integration

- Worked on the GitHub Actions workflow.
- Configured the CI workflow file.
- Added code-quality checks using Ruff.
- Prepared automated testing using Pytest.
- Included Docker build validation in the project workflow.
- Added a GitHub Actions status badge to README.md.

Workflow file:
.github/workflows/ci.yml

### 3. Docker Deployment Preparation

- Worked on the Dockerfile.
- Configured the Python runtime.
- Added dependency installation.
- Organized application files for container deployment.
- Configured the FastAPI startup command.
- Prepared the application for Render deployment.

### 4. Deployment Preparation

- Created the Render service.
- Configured the deployment branch.
- Prepared environment variables.
- Reviewed application startup configuration.
- Investigated the 512 MB memory limitation of the free instance.

### 5. Initial Deployment Issues

During deployment, the application encountered memory limitations.

Render reported:

Ran out of memory (used over 512MB) while running your code.

The issue required reducing the runtime memory footprint before production deployment.

Outcome:

Completed the CI and container deployment preparation and identified the memory optimization required for the Render free instance.

---

## Day 12 – FastEmbed Optimization, Render Deployment and Production Testing

**Objective:** Optimize the application runtime, deploy the backend, and verify its production functionality.

### 1. Runtime Memory Optimization

Activities:
- Investigated the Render 512 MB memory limitation.
- Reviewed the SentenceTransformers runtime dependency.
- Explored FastEmbed as a lightweight ONNX-based embedding runtime.
- Installed and tested FastEmbed locally.
- Updated app/embeddings.py.
- Replaced runtime SentenceTransformer query encoding with FastEmbed.
- Preserved the existing embedding model: all-MiniLM-L6-v2.
- Kept offline document embedding functionality separate from the runtime query embedding component.

### 2. Embedding Compatibility Verification

Compared SentenceTransformer and FastEmbed output.

Test model:
sentence-transformers/all-MiniLM-L6-v2

Test results:

| Test | Result |
|---|---|
| Original embedding dimensions | 384 |
| FastEmbed dimensions | 384 |
| First test cosine similarity | 1.000000 |
| Additional test sentences | 4 |
| Additional similarity results | 1.000000 |

The tested query embeddings were practically identical for the tested sentences.

### 3. RAG Integration Update

Updated:
- app/embeddings.py
- app/rag.py
- app/graph.py
- app/main.py

Activities:
- Integrated FastEmbed into RAG query embedding generation.
- Removed the old SentenceTransformer runtime initialization.
- Updated the RAG retrieval function.
- Updated LangGraph tool execution.
- Updated FastAPI model initialization.
- Preserved ChromaDB retrieval.
- Preserved Groq response generation.
- Preserved source citations.
- Preserved human approval workflow.

### 4. Code Validation

Ran:

python -m compileall -q app/embeddings.py app/main.py app/rag.py app/graph.py

Result:
Python compilation completed without syntax errors.

Also checked that old SentenceTransformer runtime references were removed from the main API, RAG, and agent workflow files.

### 5. GitHub Integration

Activities:
- Committed the FastEmbed runtime changes.
- Verified the feature branch.
- Fetched the latest master branch.
- Confirmed that the FastEmbed commit was included in master.
- Configured Render to deploy from master.

Commit:
Use FastEmbed runtime for deployment

### 6. Render Deployment

Deployment platform:
Render

Service:
Gen-AI-Examate

Deployment URL:
https://gen-ai-examate.onrender.com

API Documentation:
https://gen-ai-examate.onrender.com/docs

Health Endpoint:
https://gen-ai-examate.onrender.com/health

Activities:
- Configured the Render service.
- Configured the master deployment branch.
- Added GROQ_API_KEY through Render environment variables.
- Deployed the latest application version.
- Verified successful application startup.
- Connected ChromaDB.
- Verified the indexed document collection.
- Verified FastEmbed initialization.
- Verified Groq integration.

### 7. Production Health Check

Endpoint:

GET /health

Verified response:

{
  "status": "healthy",
  "application": "KrishiYojana",
  "vector_database": true,
  "embedding_model": true,
  "agent": true,
  "initialization_error": null
}

### 8. Production API Testing

Tested the following endpoints:

| Endpoint | Method | Result |
|---|---|---|
| / | GET | PASS |
| /health | GET | PASS |
| /records | GET | PASS |
| /records/{record_id} | GET | Endpoint available |
| /search | GET | PASS |
| /ask | POST | PASS |
| /agent | POST | PASS |
| /docs | GET | Available |

### 9. RAG Production Test

Test question:

"What is the objective of the farm mechanization scheme?"

Result:
- HTTP 200 response.
- FastEmbed generated the query embedding.
- ChromaDB retrieved relevant document chunks.
- Groq generated the answer.
- Source references were included.
- The answer was grounded in the uploaded farm mechanization PDF.

Source document:
Scheme-SubMissionOnFarmMechanization.pdf

### 10. LangGraph Production Test

Test question:

"What is the objective of the farm mechanization scheme?"

Workflow:
1. Submitted a question to /agent.
2. LangGraph selected rag_search.
3. Agent paused for human approval.
4. Received awaiting_approval response.
5. Sent approval using the returned thread_id.
6. Agent resumed execution.
7. Retrieved relevant document chunks.
8. Generated the final response.
9. Returned status completed.

Result:
- Agent initialization successful.
- Tool selection successful.
- Human approval successful.
- Workflow resumption successful.
- RAG search successful.
- Final answer returned with source references.

### 11. Scheme Records and Search Testing

Records endpoint:

GET /records

Result:
HTTP 200

Returned:
19 agricultural scheme records.

Search endpoint:

GET /search?query=Farm%20Mechanization

Result:
HTTP 200

Matching records:
1

Scheme:
Sub-mission on Farm Mechanization.

### 12. Deployment Monitoring

- Verified the deployed application through Render logs.
- Confirmed Uvicorn startup.
- Confirmed ChromaDB initialization.
- Executed live AI requests.
- Checked Render application metrics.
- Confirmed the free instance has a 512 MB RAM limit.

Note:
Exact CPU and memory consumption could not be verified because the Render dashboard restricted detailed application metrics on the free plan.

Outcome:

Successfully deployed the FastAPI backend and AI agent to Render. Verified RAG question answering, Groq integration, FastEmbed embeddings, ChromaDB retrieval, scheme records, search functionality, and LangGraph human approval execution.

The backend is publicly accessible. A separate public Streamlit frontend URL is not yet confirmed.

---

# 8. System Architecture

FARMER / USER
      |
      v
Streamlit User Interface
      |
      v
FastAPI Backend
      |
      +----------------------+
      |                      |
      v                      v
   /ask                    /agent
      |                      |
      |                 LangGraph Agent
      |                      |
      |                 Select Tools
      |                      |
      |              +-------+-------+
      |              |               |
      |              v               v
      |          RAG Search    Eligibility Check
      |              |               |
      |              v               v
      |           FastEmbed     Scheme Rules
      |              |               |
      |              v               v
      |           ChromaDB      Farmer Validation
      |              |               |
      |              +-------+-------+
      |                      |
      |               Human Approval
      |                      |
      |              +-------+-------+
      |              |               |
      |              v               v
      |           Approved        Rejected
      |              |
      |              v
      |          Execute Tool
      |              |
      +--------------+
             |
             v
          Groq LLM
             |
             v
       Final Response
             |
             v
      Farmer / User

# 9. API Endpoints

Base URL:

https://gen-ai-examate.onrender.com

| Method | Endpoint | Purpose |
|---|---|---|
| GET | / | Application welcome page |
| GET | /health | Application health check |
| GET | /records | Retrieve all scheme records |
| GET | /records/{record_id} | Retrieve an individual scheme |
| GET | /search | Search scheme records |
| POST | /ask | Ask a question using RAG |
| POST | /agent | Execute the LangGraph agent workflow |
| GET | /docs | Interactive Swagger API documentation |

## Live API Links

Backend:
https://gen-ai-examate.onrender.com

Health:
https://gen-ai-examate.onrender.com/health

API Documentation:
https://gen-ai-examate.onrender.com/docs

All Scheme Records:
https://gen-ai-examate.onrender.com/records

Scheme Search:
https://gen-ai-examate.onrender.com/search?query=Farm%20Mechanization

AI Agent API:
https://gen-ai-examate.onrender.com/agent

Note:
The /ask and /agent endpoints use POST requests. They cannot be tested as ordinary browser links. Use Swagger UI or curl.

# 10. API Testing Commands

## 10.1 Health Check

curl -i https://gen-ai-examate.onrender.com/health

## 10.2 Get All Scheme Records

curl -i https://gen-ai-examate.onrender.com/records

## 10.3 Get Individual Scheme

curl -i https://gen-ai-examate.onrender.com/records/1

## 10.4 Search Agricultural Schemes

curl -i "https://gen-ai-examate.onrender.com/search?query=Farm%20Mechanization"

## 10.5 Test RAG Question Answering

curl -i -X POST https://gen-ai-examate.onrender.com/ask \
-H "Content-Type: application/json" \
-d '{"question":"What is the objective of the farm mechanization scheme?"}'

## 10.6 Start AI Agent Workflow

curl -i -X POST https://gen-ai-examate.onrender.com/agent \
-H "Content-Type: application/json" \
-d '{"question":"What is the objective of the farm mechanization scheme?"}'

## 10.7 Approve AI Agent Execution

Use the thread_id returned by the previous request.

curl -i -X POST https://gen-ai-examate.onrender.com/agent \
-H "Content-Type: application/json" \
-d '{
  "thread_id": "YOUR_RETURNED_THREAD_ID",
  "approval": true
}'

To reject an approval request, set:

"approval": false

# 11. Farmer Eligibility Information

The eligibility workflow uses the following details:

| Field | Description |
|---|---|
| land_holding | Farmer's land holding information |
| land_size_acres | Agricultural land size in acres |
| caste_category | Farmer's caste category |
| received_same_component_last_10_years | Previous benefit information |
| already_has_tractor | Tractor ownership information |

The eligibility checker validates submitted information against configured rules in:

data/rules/scheme_rules.json

Important:
The current eligibility rules are demonstration rules. They must be verified against official government guidelines before being used for real eligibility decisions.

The final approval of a government scheme application is decided by the concerned government department.

# 12. Installation and Local Setup

## Step 1 – Clone the Repository

git clone https://github.com/Adityahon3344/Gen-AI-Examate.git

## Step 2 – Navigate to the Project

cd Gen-AI-Examate

## Step 3 – Create a Virtual Environment

python3 -m venv .venv

## Step 4 – Activate the Environment

For macOS/Linux:

source .venv/bin/activate

For Windows:

.venv\Scripts\activate

## Step 5 – Install Dependencies

python -m pip install --upgrade pip

pip install -r requirements.txt

## Step 6 – Configure Environment Variables

Create a .env file in the project root.

Example:

GROQ_API_KEY=your_groq_api_key

Never upload the actual API key to GitHub.

For Render, configure GROQ_API_KEY in the service's Environment settings.

## Step 7 – Build the Vector Database (if required)

python -m app.vectorstore

This command indexes the prepared document chunks into ChromaDB.

If a prebuilt database is already available, verify its contents before rebuilding it.

## Step 8 – Start the FastAPI Backend

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

Backend:

http://127.0.0.1:8000

## Step 9 – Open API Documentation

http://127.0.0.1:8000/docs

## Step 10 – Run the Streamlit Interface

Open another terminal, activate the virtual environment, and run:

streamlit run ui/app.py

Local Streamlit interface:

http://localhost:8501

The frontend must be configured to communicate with the locally running FastAPI backend.

# 13. Docker Setup

The project includes Docker configuration for containerized deployment.

Build Docker image:

docker build -t krishiyojana .

Run the API container:

docker run -p 8000:8000 --env-file .env krishiyojana

For the Docker Compose setup, when the compose configuration is available:

docker compose up --build

Stop the Docker Compose services:

docker compose down

# 14. Testing and Code Quality

Run Ruff:

python -m ruff check .

Run Pytest:

python -m pytest -v

Compile the main application modules:

python -m compileall -q app/

Build the Docker image:

docker build -t krishiyojana:ci .

The Day 9 eligibility and agent test results were 6/6 passed.

Production API and workflow tests completed on Day 12 are documented above.

# 15. Continuous Integration

GitHub Actions workflow:

.github/workflows/ci.yml

The project uses GitHub Actions to support automated development checks.

The CI workflow is linked to the master branch through the README status badge.

GitHub Actions:

https://github.com/Adityahon3344/Gen-AI-Examate/actions

# 16. Deployment Information

Deployment Platform:
Render

Service Name:
Gen-AI-Examate

Deployment Branch:
master

Live Backend:
https://gen-ai-examate.onrender.com

API Documentation:
https://gen-ai-examate.onrender.com/docs

Health Endpoint:
https://gen-ai-examate.onrender.com/health

Deployment Status:
Backend successfully deployed and production endpoints tested.

Important deployment details:
- GROQ_API_KEY is configured as a Render environment variable.
- FastEmbed is used for runtime query embeddings.
- ChromaDB stores document vectors.
- Groq generates contextual answers.
- LangGraph controls the agent workflow.
- The deployment uses a free Render instance with a 512 MB memory limit.

Frontend Deployment:
The Streamlit interface has been developed, but a separate publicly accessible frontend URL has not yet been verified.

# 17. Production Verification Results

| Component | Verification Result |
|---|---|
| Render deployment | PASS |
| FastAPI startup | PASS |
| Health endpoint | PASS |
| ChromaDB connection | PASS |
| FastEmbed loading | PASS |
| Groq integration | PASS |
| RAG question answering | PASS |
| Source citations | PASS |
| Scheme records endpoint | PASS |
| Scheme search endpoint | PASS |
| LangGraph initialization | PASS |
| Agent tool selection | PASS |
| Human approval workflow | PASS |
| Agent execution after approval | PASS |

Final health response:

{
  "status": "healthy",
  "application": "KrishiYojana",
  "vector_database": true,
  "embedding_model": true,
  "agent": true,
  "initialization_error": null
}

# 18. Git and GitHub Commands

Check the current branch:

git branch

Check working-tree changes:

git status

Add documentation changes:

git add README.md docs/DAILY_PROGRESS.md

Commit changes:

git commit -m "docs: update KrishiYojana project documentation"

Push the feature branch:

git push origin feature/day11-ci-deployment

After pushing, create a Pull Request:

Base branch: master

Compare branch: feature/day11-ci-deployment

Merge the pull request after reviewing the changes.

Repository:

https://github.com/Adityahon3344/Gen-AI-Examate

# 19. Project Limitations

1. Scheme information depends on the quality and freshness of the collected documents.
2. Current eligibility rules are demonstration rules and must be verified against official government guidelines.
3. AI-generated information should be checked against official sources for important decisions.
4. LangGraph MemorySaver currently stores workflow state in memory and is not persistent across application restarts.
5. Exact Render CPU and memory consumption could not be confirmed on the free plan because detailed metrics were restricted.
6. The backend is publicly deployed, but a separate public Streamlit frontend URL has not yet been confirmed.
7. Some scheme records contain general or component-specific information that should be validated against current official guidance.

# 20. Future Enhancements

- Deploy the Streamlit frontend publicly.
- Add Marathi and other regional language support.
- Expand the verified agricultural scheme knowledge base.
- Add more scheme-specific eligibility rules.
- Improve RAG retrieval accuracy.
- Implement persistent conversation storage.
- Implement persistent agent checkpoint storage.
- Integrate official government data sources.
- Add farmer profile management.
- Improve source citation and answer verification.
- Introduce multilingual voice-based interaction.
- Improve frontend usability for farmers.
- Add more automated tests and RAG evaluation scenarios.

# 21. Conclusion

KrishiYojana combines Generative AI, Retrieval-Augmented Generation, semantic search, vector databases, and agent-based workflow orchestration to make agricultural scheme information more accessible to farmers in Maharashtra.

The project progresses from basic Python programming and structured data management to document ingestion, FastAPI backend development, intelligent retrieval, eligibility validation, LangGraph agent development, and cloud deployment.

The project also incorporates human-in-the-loop approval to provide greater control over agent tool execution.

The FastAPI backend is successfully deployed on Render, and its health, RAG, records, search, and LangGraph agent workflows have been tested in production.

The overall goal is to develop a reliable, transparent, and user-friendly AI assistant that helps Maharashtra farmers understand agricultural government schemes and their requirements.

---

**Project:** KrishiYojana – AI-Powered Farmer Scheme Eligibility & Benefits Assistant

**Developer:** Aditya Ashok Hon

**Repository:** https://github.com/Adityahon3344/Gen-AI-Examate

**Live Backend:** https://gen-ai-examate.onrender.com

**API Documentation:** https://gen-ai-examate.onrender.com/docs

**Primary Technologies:** Python, FastAPI, Streamlit, Groq, LangGraph, ChromaDB, FastEmbed, Docker, GitHub Actions, Render
