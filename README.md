KrishiYojana – AI-Powered Farmer Scheme Eligibility & Benefits Assistant

[![KrishiYojana CI](https://github.com/Adityahon3344/Gen-AI-Examate/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/Adityahon3344/Gen-AI-Examate/actions/workflows/ci.yml)

An AI-powered assistant that helps farmers in Maharashtra discover government agricultural schemes, understand scheme benefits, search agricultural information, and check eligibility through an intelligent conversational interface.

Project: KrishiYojana
Target Users: Farmers in Maharashtra, India
Primary Data Source: MahaDBT Farmer Portal
Backend: Python, FastAPI
AI Framework: LangGraph
LLM Provider: Groq
Vector Database: ChromaDB
1. Project Overview
KrishiYojana is an AI-powered agricultural scheme assistance application designed to simplify access to government scheme information.

Farmers often face difficulties finding relevant government schemes, understanding eligibility requirements, and identifying the benefits available to them.

The application combines Retrieval-Augmented Generation (RAG), semantic search, Large Language Models (LLMs), and LangGraph-based agent workflows to provide relevant information and assist with eligibility checks.
2. Project Objectives
- Make government agricultural scheme information easier to access.
- Allow farmers to search using natural-language questions.
- Provide information about scheme benefits and eligibility.
- Implement an AI-powered question-answering system.
- Retrieve relevant information from a document knowledge base.
- Check farmer eligibility using configured scheme rules.
- Request missing farmer details when required.
- Introduce human approval before executing agent tools.
- Provide source-based answers for better transparency.
3. Key Features
Scheme Management
- Store and manage agricultural scheme records.
- Retrieve records using unique IDs.
- Search schemes using keywords.
- Organize scheme information by department.
Intelligent Search
- Keyword-based search.
- Semantic search using sentence embeddings.
- Retrieve relevant information based on user questions.
RAG-Based Question Answering
- Accept natural-language questions.
- Retrieve relevant document chunks from ChromaDB.
- Generate contextual answers using Groq.
- Return relevant sources with generated answers.
Farmer Eligibility Checking
- Collect farmer information.
- Validate required farmer details.
- Check eligibility against configured scheme rules.
- Identify missing information.
- Return eligibility results.
LangGraph Agent Workflow
- Select tools based on user questions.
- Route requests to eligibility checking or RAG search.
- Request human approval before tool execution.
- Resume approved workflows.
- Handle rejected requests.
- Maintain workflow state using checkpointing.
4. Technology Stack
Category	Technology
Programming Language	Python
Backend Framework	FastAPI
LLM Provider	Groq
Agent Framework	LangGraph
RAG Architecture	Retrieval-Augmented Generation
Embedding Model	all-MiniLM-L6-v2
Embedding Library	SentenceTransformers
Vector Database	ChromaDB
Data Processing	Pandas
API Server	Uvicorn
API Testing	FastAPI Swagger UI
Version Control	Git and GitHub


5. Project Folder Structure
This tree reflects the files tracked in the repository. The ChromaDB database and the local .env file are generated or configured locally and are not committed.
Gen-AI-Examate/
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
│   ├── semantic_search.py
│   ├── smart_search.py
│   ├── rag.py
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
│   ├── rules/
│   │   └── scheme_rules.json
│   └── raw/
│       ├── DBT_Farmer_User_Manual.pdf
│       ├── Scheme-SubMissionOnFarmMechanization.pdf
│       ├── extracted_text.txt
│       └── farm_mechanization.html
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
│
├── sync_records.py
├── .env.example
├── requirements.txt
├── .gitignore
└── README.md

Folder and File Description
File / Folder	Purpose
app/	FastAPI application, search/RAG modules, LangGraph workflow, and tools
data/records.json	Structured scheme records
data/rules/	Demonstration eligibility rule configuration
data/raw/	Source documents used by ingestion and RAG
data/chroma_db/	Locally generated ChromaDB database; not tracked
analysis/	Data exploration scripts
docs/	Project documentation and daily progress
eval/	Evaluation data, scripts, and results
prompts/	System, task, and evaluation prompts
test_*.py	Root-level API, agent, and eligibility test scripts
.env.example	Environment variable template; copy to a local .env
requirements.txt	Python dependencies
.gitignore	Excludes local secrets, environments, and generated files
README.md	Project documentation


Keep .env, .venv/, and generated vector database files out of commits. Never put API keys in the repository.
6. System Architecture
                 FARMER / USER
                       |
                       v
              User Question / Input
                       |
                       v
                 FastAPI Backend
                       |
                       v
                 LangGraph Agent
                       |
                       v
                  Select Tools
                       |
              +--------+--------+
              |                 |
              v                 v
          RAG Search       Eligibility Check
              |                 |
              v                 v
           ChromaDB          Scheme Rules
              |                 |
              v                 v
        Relevant Chunks    Farmer Validation
              |                 |
              +--------+--------+
                       |
                       v
                Approval Workflow
                       |
                 Human Approval
                       |
              +--------+--------+
              |                 |
              v                 v
           Approved           Rejected
              |                 |
              v                 v
         Execute Tool        Stop Workflow
              |
              v
            Groq LLM
              |
              v
         Final Response
              |
              v
            FARMER

7. Development Progress – Day 1 to Day 10
Day 1 – Project Introduction and Initial Setup
Objective: Establish the project foundation.

Activities:
- Finalized the project title and problem statement.
- Identified Maharashtra farmers as the target users.
- Selected MahaDBT Farmer Portal as the primary information source.
- Created the initial project structure.
- Developed an introductory Python program.
- Implemented a menu-driven interface.
- Tested the initial menu functionality.
Files:
- README.md
- day01_intro.py
- day01_menu.py
Outcome: Initial project setup and menu-driven Python application completed.
Day 2 – Dataset Collection and Scheme Management
Objective: Create a structured dataset of government agricultural schemes.

Activities:
- Prepared sample agricultural scheme records.
- Stored scheme details using structured Python dictionaries.
- Implemented record-loading functionality.
- Developed keyword-based search.
- Implemented department-wise scheme counting.
- Added scheme retrieval using unique IDs.
- Configured the Python virtual environment and dependencies.
Files:
- data/__init__.py
- data/sample_records.py
- app/__init__.py
- app/records.py
- app/cli.py
- requirements.txt
- .gitignore
Outcome: Structured scheme dataset and command-line record management functionality developed.
Day 3 – Data Fetching and Ingestion
Objective: Develop the process for collecting and preparing scheme information.

Development scope:
- Implemented data-fetching functionality.
- Worked with HTML and PDF sources.
- Extracted information from source documents.
- Created structured data models.
- Implemented JSON-based data ingestion.
- Organized collected scheme information.
Files:
- app/fetch.py
- app/ingest.py
- app/models.py
- data/records.json
Outcome: Data collection, extraction, and ingestion components developed.
Day 4 – FastAPI Backend and Intelligent Search
Objective: Develop backend APIs and improve scheme discovery.

Development scope:
- Set up FastAPI and Uvicorn.
- Created the backend API structure.
- Implemented health-check functionality.
- Added scheme-record retrieval.
- Developed search endpoints.
- Added question-related API functionality.
- Explored scheme data using Pandas.
- Worked on TF-IDF and cosine-similarity-based search.
Files:
- app/main.py
- analysis/explore.py
- app/smart_search.py
Outcome: Backend API and intelligent search development milestone completed.
Day 5 – LLM Fundamentals and API Validation
Objective: Understand Large Language Models and validate the backend.

Activities:
- Studied how Large Language Models work.
- Documented the LLM workflow.
- Prepared 10 real-world project-related questions.
- Included questions that could not be answered using available project information.
- Tested backend APIs through Swagger UI.
- Tested the health-check endpoint.
- Created the checkpoint-1 Git tag.
Files:
- docs/how_llms_work.md
- README.md
Outcome: LLM fundamentals documented and backend API validation milestone completed.
Day 6 – LLM Integration and AI-Powered Responses
Objective: Introduce an LLM provider into the application.

Development focus:
- Selected Groq as the LLM provider.
- Worked on API-based LLM integration.
- Explored how user questions can be passed to an LLM.
- Worked toward generating contextual responses.
- Prepared the application for RAG integration.
Outcome: LLM integration development milestone.
Day 7 – RAG and Semantic Retrieval Development
Objective: Develop the retrieval pipeline for knowledge-based question answering.

Development focus:
- Worked on document-based information retrieval.
- Explored text embeddings.
- Used the all-MiniLM-L6-v2 embedding model.
- Integrated semantic retrieval with ChromaDB.
- Worked on retrieving relevant information for user questions.
Outcome: Semantic retrieval and RAG development milestone.
Day 8 – Agent Workflow and Eligibility Integration
Objective: Prepare the application for intelligent tool-based execution.

Development focus:
- Worked on the eligibility-checking functionality.
- Created configurable scheme eligibility rules.
- Identified the farmer details required for eligibility checks.
- Prepared the application for tool selection and execution.
- Integrated the RAG and eligibility workflows into the agent architecture.
Outcome: Eligibility and agent workflow integration milestone.
Day 9 – LangGraph Agent, Human Approval and Workflow Testing
Objective: Implement and validate the LangGraph-based agent workflow.

Activities:

1. LangGraph Workflow
- Implemented the agent state structure.
- Developed the select_tools node.
- Added routing between RAG search and eligibility checking.
- Implemented the approval workflow.
- Added approval_router for approved and rejected requests.
- Implemented the execute_tools node.
- Integrated LangGraph's MemorySaver checkpointer.
2. Human-in-the-Loop Approval
- Implemented interrupt() for approval requests.
- Added support for pausing agent execution.
- Implemented workflow resumption after approval.
- Added rejection handling.
- Ensured rejected requests do not execute tools.
3. Farmer Eligibility Validation
- Implemented required farmer detail validation.
- Added missing-information handling.
- Integrated eligibility checking with the agent.
- Tested eligible and ineligible farmer scenarios.
4. API Integration
- Integrated the agent workflow with FastAPI.
- Tested the /agent endpoint.
- Verified approval, rejection, and workflow resumption.
- Corrected the tools_used response for rejected requests.
5. Testing
- Tested eligibility checking.
- Tested graph execution.
- Tested approval and rejection.
- Tested missing farmer details.
- Tested existing API endpoints.
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
- README.md
Day 9 Test Results:
Test Case	Result
Eligible and ineligible farmer checks	PASS
Existing API endpoints	PASS
Missing farmer details	PASS
Rejection and workflow resumption	PASS
Resume without checkpoint	PASS
Agent missing-details handling	PASS


Total automated tests: 6

Passed: 6/6

Outcome: LangGraph approval workflow, eligibility validation, and API integration successfully tested.
Day 10 – Streamlit Frontend and Document Bag Implementation
Objective: Develop an interactive Streamlit interface and integrate it with the FastAPI backend to provide scheme-related assistance through Direct Chat and an AI Agent.

Activities:

1. Streamlit User Interface
- Developed the application interface using Streamlit.
- Connected the frontend with the FastAPI backend.
- Implemented a conversational interface for submitting questions and displaying responses.
- Added separate interaction modes for Direct Chat and AI Agent.
2. Backend API Integration
- Integrated the /ask endpoint for Direct Chat interactions.
- Integrated the /agent endpoint for AI Agent interactions.
- Added handling for agent approval requests.
- Implemented approval and rejection controls in the interface.
- Maintained the agent thread ID to continue an approval-based workflow.
3. Answers and Source Information
- Displayed generated answers in the chat interface.
- Presented available source citations with responses.
- Displayed confidence information returned by the backend.
4. User Feedback System
- Added positive and negative feedback options for responses.
- Saved submitted feedback in a JSON file.
- Recorded the question, answer, rating, and submission timestamp.
5. Document Bag – Signature Feature
- Developed the Document Bag feature for selecting multiple agricultural schemes.
- Enabled users to select 2–3 schemes.
- Retrieved the required documents for the selected schemes.
- Combined the documents into one consolidated checklist.
- Removed duplicate document entries across selected schemes.
- Displayed the scheme or schemes associated with each required document.
- Added an option to download the consolidated checklist.
6. Testing and Documentation
- Tested Direct Chat through the /ask endpoint.
- Tested AI Agent interactions through the /agent endpoint.
- Verified agent approval and rejection handling.
- Tested feedback submission and JSON storage.
- Tested multi-scheme selection and document deduplication.
- Captured the Document Bag interface screenshot for project documentation.
Files Created/Modified:
- ui/app.py
- screenshots/document-bag.png
- README.md
Outcome: Developed a Streamlit-based interface integrated with the FastAPI backend, providing Direct Chat, AI Agent interactions, source citations, response feedback, and a consolidated downloadable Document Bag checklist.
8. API Endpoints
The FastAPI backend provides the following endpoints.
Method	Endpoint	Purpose
GET	/health	Check API health
GET	/records	Retrieve scheme records
GET	/records/{record_id}	Retrieve a specific scheme
GET	/search	Search scheme records
POST	/questions	Submit project questions
POST	/search/semantic	Perform semantic search
POST	/chat	AI-powered chat
POST	/ask	Ask a question using RAG
POST	/agent	Execute the LangGraph agent workflow


Interactive API documentation:
http://127.0.0.1:8000/docs

9. Farmer Eligibility Information
The eligibility workflow uses the following farmer details:
Field	Description
land_holding	Land ownership or holding information
land_size_acres	Agricultural land size in acres
caste_category	Farmer's caste category
received_same_component_last_10_years	Previous benefit information
already_has_tractor	Tractor ownership information
scheme_id	Optional scheme identifier


The eligibility checker validates the submitted information against the configured rules in:
data/rules/scheme_rules.json

Important: The current rules are demonstration rules. They should be verified against official government scheme guidelines before being used for real eligibility decisions.
10. Installation and Setup
Step 1: Clone the Repository
git clone https://github.com/Adityahon3344/Gen-AI-Examate.git
Step 2: Navigate to the Project
cd Gen-AI-Examate
Step 3: Create a Virtual Environment
python3 -m venv .venv
Step 4: Activate the Environment
For macOS/Linux:
source .venv/bin/activate
Step 5: Install Dependencies
pip install -r requirements.txt
Step 6: Configure Environment Variables
Create a .env file in the project root and configure the required API credentials.

Example:
GROQ_API_KEY=your_groq_api_key
Use the actual environment variable names expected by your application configuration. Never commit API keys to GitHub.
Step 7: Start the FastAPI Server
uvicorn app.main:app --reload
Step 8: Open API Documentation
http://127.0.0.1:8000/docs

### Run with Docker

1. Copy `.env.example` to `.env` and set `GROQ_API_KEY` for LLM-backed answers.
2. Build and start the API and Streamlit UI:

   ```bash
   docker compose up --build
   ```

3. Open the Streamlit UI at http://localhost:8501. The API is available at
   http://localhost:8002, with its health endpoint at
   http://localhost:8002/health and API documentation at
   http://localhost:8002/docs.
4. Stop the services with `Ctrl+C`, then run `docker compose down` to remove the
   containers. ChromaDB data is persisted under `data/chroma_db`.

11. Testing
Run the same checks used by GitHub Actions:

```bash
python -m ruff check .
python -m pytest tests/ -v
docker build -t krishiyojana:ci .
```

12. Human Approval Workflow
The agent uses a human-in-the-loop approach to control tool execution.

Workflow:
1. User submits a question.
2. LangGraph identifies the required tool.
3. The workflow pauses for approval.
4. The user approves or rejects the request.
5. If approved, the selected tool executes.
6. If rejected, the workflow stops without executing the tool.
7. The application returns the appropriate response.
This approach provides greater control and transparency over agent actions.
13. Future Enhancements
- Add a complete web-based farmer interface.
- Support Marathi and other regional languages.
- Expand the verified agricultural scheme knowledge base.
- Add more government scheme eligibility rules.
- Improve RAG retrieval accuracy and evaluation.
- Add persistent conversation and workflow storage.
- Integrate official government data sources where available.
- Add farmer profile management.
- Improve source citations and answer verification.
- Deploy the application to a cloud platform.
14. Project Limitations
- Current eligibility rules are demonstration rules and are not a substitute for official government decisions.
- Answer quality depends on the completeness and accuracy of the knowledge base.
- The current LangGraph MemorySaver checkpointer stores workflow state in memory and is not persistent across application restarts.
- Official scheme information should be periodically verified and updated.
- LLM-generated answers may require verification against official sources.
15. Git and Version Control
The project uses Git and GitHub for source-code management.

Repository:

https://github.com/Adityahon3344/Gen-AI-Examate

Example Git commands:
git add .
git commit -m "Update project implementation"
git push origin master
16. Conclusion
KrishiYojana combines Generative AI, Retrieval-Augmented Generation, semantic search, and agent-based workflow orchestration to make agricultural scheme information more accessible to farmers.

The project progresses from basic Python programming and structured data management to FastAPI backend development, intelligent retrieval, eligibility validation, and LangGraph-based human approval workflows.

The overall goal is to build a reliable, transparent, and user-friendly AI assistant that helps Maharashtra farmers understand government agricultural schemes.
Project: KrishiYojana – AI-Powered Farmer Scheme Eligibility & Benefits Assistant
Repository: Adityahon3344/Gen-AI-Examate
Primary Technologies: Python, FastAPI, Groq, LangGraph, ChromaDB, SentenceTransformers