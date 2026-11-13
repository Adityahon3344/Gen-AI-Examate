# KrishiYojana

### Maharashtra Farmer Scheme Eligibility & Benefits Assistant

**Project Repository:** [Adityahon3344/Gen-AI-Examate](https://github.com/Adityahon3344/Gen-AI-Examate)

**Project Category:** Artificial Intelligence / Machine Learning / Backend Development

**Primary Language:** Python

**Development Status:** Day 1–Day 6 Completed

---

## 1. Project Overview

KrishiYojana is an AI-oriented agricultural assistance application designed to help farmers discover government agricultural schemes available in Maharashtra.

The project aims to organize agricultural scheme information into structured records and provide an accessible interface for retrieving scheme details, understanding benefits, exploring eligibility criteria, and identifying required documents.

The current implementation includes:

- Structured agricultural scheme dataset.
- Command-line interface.
- Data collection and extraction utilities.
- FastAPI backend.
- TF-IDF-based intelligent search.
- Groq-powered LLM response generation.
- Prompt engineering and evaluation.

The project is being developed incrementally, focusing on Python fundamentals, data processing, API development, information retrieval, and Large Language Model integration.

## 2. Project Objectives

- Collect and organize Maharashtra agricultural scheme information.
- Develop a structured dataset containing scheme details.
- Implement scheme retrieval and keyword-based searching.
- Provide RESTful APIs using FastAPI.
- Implement intelligent search using TF-IDF and cosine similarity.
- Analyze structured data using Pandas.
- Understand Large Language Model (LLM) architecture and working principles.
- Integrate an LLM using the Groq API.
- Develop prompt templates for farmer assistance.
- Evaluate different prompt versions.
- Prepare the foundation for an AI-powered farmer assistance system.

## 3. Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| API Server | Uvicorn |
| Data Processing | Pandas |
| Machine Learning | Scikit-learn |
| Text Processing | TF-IDF, Cosine Similarity |
| Data Collection | Requests, BeautifulSoup |
| PDF Processing | PyPDF |
| Data Validation | Pydantic |
| Data Storage | Python Dictionaries, JSON |
| LLM Provider | Groq |
| LLM Integration | Groq Python SDK |
| Prompt Engineering | System Prompts, Task Prompts |
| Environment Variables | python-dotenv |
| Evaluation | Prompt Comparison |
| Version Control | Git |
| Repository Hosting | GitHub |
| Development Environment | Visual Studio Code |

## 4. Repository Structure

```text
Gen-AI-Examate/
│
├── analysis/
│   ├── __init__.py
│   └── explore.py
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── records.py
│   ├── cli.py
│   ├── models.py
│   ├── fetch.py
│   ├── ingest.py
│   ├── smart_search.py
│   └── llm.py
│
├── data/
│   ├── raw/
│   │   ├── farm_mechanization.html
│   │   ├── Scheme-SubMissionOnFarmMechanization.pdf
│   │   ├── DBT_Farmer_User_Manual.pdf
│   │   └── extracted_text.txt
│   │
│   ├── records.json
│   ├── sample_records.py
│   └── __init__.py
│
├── docs/
│   ├── how_llms_work.md
│   └── user_questions.md
│
├── prompts/
│   ├── system_prompt.txt
│   ├── task_prompt_1.txt
│   ├── task_prompt_2.txt
│   ├── eval_prompt_v1.txt
│   └── eval_prompt_v2.txt
│
├── eval/
│   ├── run_prompt_eval.py
│   ├── prompt_compare.md
│   └── results.json
│
├── day01_intro.py
├── day01_menu.py
├── sync_records.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 5. Dataset Development

The project currently maintains 19 agricultural scheme records in `data/sample_records.py`.

### Dataset Fields

| Field | Description |
|---|---|
| ID | Unique scheme identifier |
| Scheme Name | Name of the agricultural scheme |
| Department | Implementing department |
| Benefit | Scheme benefit description |
| Eligibility | Eligibility conditions |
| Required Documents | Required application documents |
| Source URL | Reference source for scheme information |

### Scheme Records

| ID | Scheme Name |
|---:|---|
| 1 | Sub-mission on Farm Mechanization |
| 2 | State Agriculture Mechanization Scheme |
| 3 | Birsa Munda Krishi Kranti Yojana |
| 4 | PMRKVY - Rainfed Area Development (RAD) |
| 5 | Dr. Babasaheb Ambedkar Krushi Swavalamban Yojana |
| 6 | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop |
| 7 | National Food Security Mission (NFSM) - Food Grains |
| 8 | Mission for Integrated Development of Horticulture (MIDH) |
| 9 | Bhausaheb Fundkar Phalbaag Lagvad Yojana |
| 10 | Rashtriya Krushi Vikas Yojana (RKVY) - RAFTAAR |
| 11 | Chief Minister Sustainable Agriculture Irrigation Scheme |
| 12 | Chief Minister Sustainable Agriculture Irrigation Scheme - Individual Farm Pond |
| 13 | Dr. Shyamaprasad Mukherjee Jan-Van Vikas Scheme |
| 14 | Gopinath Munde Shetkari Apghat Suraksha Sanugrah Anudan Yojana |
| 15 | Chief Minister Agro and Food Processing Scheme |
| 16 | Kaju Kalma Vatap Scheme |
| 17 | RKVY - Sugarcane Harvester Subsidy |
| 18 | NFSM - Oilseed and Oil Palm |
| 19 | NFSM - Cotton and Sugarcane |

**Dataset Summary**

- Total records: 19
- Unique IDs: 19
- Record ID range: 1–19
- Primary dataset: `data/sample_records.py`
- JSON dataset: `data/records.json`

*Note: Scheme information is maintained for educational development. Eligibility, benefits, and application requirements require verification against current official government guidelines.*

---

## 6. Day-wise Development Progress

### Day 1 – Python Programming Fundamentals

**Objective:** Establish the project foundation and practice core Python programming concepts.

**Implementation:**

- Created the initial KrishiYojana project introduction.
- Implemented user input and output operations.
- Practiced variables and formatted strings.
- Developed an interactive command-line menu.
- Implemented conditional statements and loops.

**Deliverables:**

- `day01_intro.py`
- `day01_menu.py`

**Learning Outcomes:** Python fundamentals, variables, input/output, conditional statements, and loop-based program execution.

### Day 2 – Structured Dataset and CLI Development

**Objective:** Build a structured agricultural scheme dataset and implement retrieval operations.

**Implementation:**

- Created structured scheme records using Python lists and dictionaries.
- Expanded the dataset to 19 records.
- Implemented scheme searching.
- Implemented department-wise scheme counting.
- Implemented scheme retrieval using unique IDs.
- Developed a command-line interface for interacting with the dataset.

**Deliverables:**

- `data/sample_records.py`
- `app/records.py`
- `app/cli.py`

**Learning Outcomes:** Python data structures, modular programming, record retrieval, and basic search operations.

### Day 3 – Data Collection and Extraction

**Objective:** Develop the initial data collection and document extraction pipeline.

**Implementation:**

- Collected agricultural scheme-related HTML and PDF resources.
- Implemented resource downloading using Requests.
- Extracted HTML content using BeautifulSoup.
- Extracted PDF text using PyPDF.
- Stored extracted content for further processing.
- Introduced dataclass-based data modeling.

**Deliverables:**

- `app/fetch.py`
- `app/ingest.py`
- `app/models.py`
- `data/raw/`

**Learning Outcomes:** Web resource retrieval, HTML parsing, PDF processing, and structured data modeling.

### Day 4 – FastAPI Backend and Intelligent Search

**Objective:** Develop REST APIs and introduce machine-learning-based search functionality.

**Implementation:**

- Created the FastAPI application.
- Implemented REST API endpoints.
- Integrated JSON-based record loading.
- Implemented TF-IDF vectorization.
- Applied cosine similarity for search result ranking.
- Developed an API for farmer questions.
- Performed dataset exploration using Pandas.
- Tested API functionality through Swagger UI.

**Deliverables:**

- `app/main.py`
- `app/smart_search.py`
- `analysis/explore.py`

**Learning Outcomes:** REST API development, request handling, JSON processing, TF-IDF, cosine similarity, and exploratory data analysis.

### Day 5 – LLM Fundamentals and API Verification

**Objective:** Understand the fundamentals of Large Language Models and verify the FastAPI application.

**Implementation:**

- Created technical documentation explaining LLM architecture and working principles.
- Documented tokenization, embeddings, transformers, attention mechanisms, and next-token prediction.
- Added a Mermaid flowchart illustrating the LLM processing pipeline.
- Prepared 10 realistic farmer questions.
- Designed Q6 to test a question that cannot be answered using the current dataset.
- Executed the FastAPI application using Uvicorn.
- Accessed and inspected Swagger UI documentation.
- Explained the health-check API function.
- Executed the `/health` endpoint and verified its HTTP 200 response.
- Created and pushed the `checkpoint-1` Git tag.

**Deliverables:**

- `docs/how_llms_work.md`
- `docs/user_questions.md`
- `app/main.py`
- Git tag: `checkpoint-1`

**Learning Outcomes:** LLM fundamentals, technical documentation, API testing, HTTP response validation, and Git checkpoint management.

### Day 6 – Groq LLM Integration and Prompt Engineering

**Objective:** Integrate a Large Language Model into the existing FastAPI application and implement prompt evaluation.

**Implementation:**

- Selected Groq as the LLM provider.
- Installed the Groq Python SDK.
- Installed python-dotenv for environment variable management.
- Configured the Groq API key using a local `.env` file.
- Created `.env.example` with a placeholder API key.
- Added `.env` to `.gitignore` to prevent accidental API key uploads.
- Created `app/llm.py` for Groq client initialization and LLM response generation.
- Integrated the LLM with the existing scheme retrieval workflow.
- Added the `POST /chat` API endpoint.
- Connected retrieved scheme information with the task prompt.
- Created system and task prompt templates.
- Prepared two prompt versions for comparison.
- Created an evaluation script to test both prompt versions.
- Generated 20 evaluation responses using 10 farmer questions for each prompt version.
- Saved evaluation outputs in JSON format.
- Documented preliminary prompt comparison observations.
- Created `sync_records.py` to synchronize scheme records into `data/records.json`.
- Verified that the JSON dataset contains 19 records.
- Committed and pushed the Day 6 implementation to GitHub.

**Deliverables:**

- `app/llm.py`
- `app/main.py`
- `prompts/system_prompt.txt`
- `prompts/task_prompt_1.txt`
- `prompts/task_prompt_2.txt`
- `prompts/eval_prompt_v1.txt`
- `prompts/eval_prompt_v2.txt`
- `eval/run_prompt_eval.py`
- `eval/prompt_compare.md`
- `eval/results.json`
- `sync_records.py`
- `.env.example`

**Learning Outcomes:** Groq API integration, environment variable management, prompt engineering, LLM response generation, prompt evaluation, and secure API key handling.

**Evaluation Summary:**

| Metric | Result |
|---|---:|
| Total Evaluation Questions | 10 |
| Prompt Version 1 Responses | 10 |
| Prompt Version 2 Responses | 10 |
| Total Generated Responses | 20 |
| Evaluation Output | `eval/results.json` |

*Note: Prompt comparison is preliminary. Generated responses require manual review and verification against official scheme information before drawing conclusions about accuracy.*

---

## 7. FastAPI Implementation

The application currently exposes six API endpoints.

| Method | Endpoint | Functionality |
|---|---|---|
| GET | `/health` | Verify API availability |
| GET | `/records` | Retrieve scheme records |
| GET | `/records/{record_id}` | Retrieve a specific scheme |
| GET | `/search` | Perform TF-IDF-based scheme search |
| POST | `/questions` | Retrieve schemes relevant to a farmer's question |
| POST | `/chat` | Generate an LLM-based response using retrieved scheme context |

### Health Check API

**Endpoint:** `GET /health`

```python
@app.get("/health")
def health_check():
    return {
        "status": "success",
        "message": "KrishiYojana API is running!"
    }
```

**Verified Response:**

```json
{
    "status": "success",
    "message": "KrishiYojana API is running!"
}
```

**HTTP Status:** `200 OK`

### Chat API

**Endpoint:** `POST /chat`

The chat endpoint accepts a farmer's question, retrieves relevant scheme information, and uses the Groq LLM to generate a natural-language response based on the available context.

**Processing Workflow:**

1. Receive the farmer's question.
2. Search the available agricultural scheme records.
3. Retrieve relevant scheme information.
4. Prepare the task prompt with the retrieved context.
5. Send the prompt to the Groq LLM.
6. Generate the response.
7. Return the answer, confidence field, and follow-up information through the API.

**Response Fields:**

| Field | Description |
|---|---|
| answer | Generated response to the farmer's question |
| confidence | Application-provided confidence indicator |
| follow_up | Suggested follow-up information or question |

*Note: The confidence field is not a calibrated probability of factual correctness.*

### API Documentation

Interactive API documentation is available through FastAPI Swagger UI.

```text
http://127.0.0.1:8000/docs
```

---

## 8. Intelligent Search and LLM Approach

The current application combines information retrieval with LLM-based response generation.

### Information Retrieval Workflow

The search implementation uses TF-IDF and cosine similarity.

1. Receive a search query or farmer question.
2. Load the available scheme records.
3. Convert scheme information into searchable text.
4. Apply TF-IDF vectorization.
5. Calculate cosine similarity between the query and scheme documents.
6. Rank matching records by similarity.
7. Return the top relevant results.

### LLM Response Generation Workflow

1. Receive a farmer's question through the chat API.
2. Retrieve relevant scheme records using the search functionality.
3. Prepare the retrieved information as context.
4. Combine the context with the task prompt.
5. Send the prompt to the Groq LLM.
6. Generate a natural-language response.
7. Return the response through the FastAPI endpoint.

### Overall Architecture

```text
Farmer Question
       |
       v
   FastAPI API
       |
       v
  TF-IDF Search
       |
       v
Relevant Scheme Records
       |
       v
  Task Prompt
       |
       v
    Groq LLM
       |
       v
Generated Response
       |
       v
   API Response
```

This is an early retrieval-plus-generation workflow. It provides the foundation for further Retrieval-Augmented Generation (RAG) development.

---

## 9. LLM Fundamentals

A Large Language Model is an AI model trained on large text datasets to process and generate natural-language content.

The Day 5 documentation covers:

- Tokenization
- Embeddings
- Transformer architecture
- Attention mechanism
- Next-token prediction
- Response generation
- LLM limitations

**Technical Documentation:** `docs/how_llms_work.md`

### Farmer Question Dataset

Ten sample questions are documented in `docs/user_questions.md`.

These questions cover agricultural machinery, irrigation, horticulture, scheme benefits, required documents, farm ponds, and farmer assistance.

One question intentionally concerns current application deadlines, which are not available in the current dataset. This tests the system's ability to recognize missing information.

### Prompt Engineering

Prompt engineering is used to provide instructions and context to the LLM so that it can generate relevant responses.

The project includes:

- `system_prompt.txt` – General instructions for the assistant.
- `task_prompt_1.txt` – Task instructions used by the current chat endpoint.
- `task_prompt_2.txt` – An additional prompt for future eligibility assessment.
- `eval_prompt_v1.txt` – First evaluation prompt version.
- `eval_prompt_v2.txt` – Second evaluation prompt version.

### Prompt Evaluation

Two prompt versions are evaluated using the same set of 10 farmer questions.

The evaluation script generates 20 responses and stores them in `eval/results.json`.

The preliminary comparison is documented in `eval/prompt_compare.md`.

---

## 10. Installation and Execution

### Prerequisites

- Python 3.11 or later
- Git
- Visual Studio Code
- Groq API key

### Clone Repository

```bash
git clone https://github.com/Adityahon3344/Gen-AI-Examate.git
cd Gen-AI-Examate
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Configure Environment Variables

Create your local `.env` file using the example:

```bash
cp .env.example .env
```

Open `.env` and add your own Groq API key:

```env
GROQ_API_KEY=your_actual_groq_api_key
```

*Important: Keep your actual API key private. Never commit or upload your `.env` file to GitHub.*

### Run CLI Application

```bash
python -m app.cli
```

### Run Data Analysis

```bash
python -m analysis.explore
```

### Run Record Synchronization

```bash
python sync_records.py
```

### Run Prompt Evaluation

```bash
python eval/run_prompt_eval.py
```

### Start FastAPI Server

```bash
uvicorn app.main:app --reload
```

**Application URL:**

`http://127.0.0.1:8000`

**Swagger Documentation:**

`http://127.0.0.1:8000/docs`

---

## 11. Version Control and Checkpoints

Git is used to maintain development history and GitHub is used for repository hosting.

### Completed Tags

| Tag | Description |
|---|---|
| `week-1` | Week 1 development checkpoint |
| `checkpoint-1` | Day 5 documentation and API checkpoint |

### Day 6 Git Commit

`Complete Day 6 Groq LLM integration and prompt evaluation`

### Useful Git Commands

```bash
git status
git log --oneline
git tag
git add .
git commit -m "Your commit message"
git push origin master
```

**Repository:**

https://github.com/Adityahon3344/Gen-AI-Examate

---

## 12. Future Development Roadmap

The following improvements are planned for subsequent development stages:

- Expand and validate the agricultural scheme dataset.
- Improve scheme eligibility matching.
- Implement robust handling of questions that cannot be answered from available data.
- Improve LLM response quality and factual reliability.
- Review and improve prompt evaluation.
- Explore advanced Retrieval-Augmented Generation (RAG).
- Introduce multilingual support for Marathi, Hindi, and English.
- Develop a farmer-friendly web interface.
- Integrate a persistent database.
- Improve search relevance and recommendation accuracy.
- Incorporate verified updates from official government sources.
- Implement more detailed eligibility assessment using verified scheme guidelines.

---

## 13. Official References

- [Maharashtra MahaDBT Farmer Portal](https://mahadbt.maharashtra.gov.in/Farmer/)
- [Maharashtra Government Official Portal](https://www.maharashtra.gov.in/)

---

## 14. Disclaimer

KrishiYojana is an educational software development project and is not an official government application.

The information provided by the application should not be considered an official confirmation of eligibility or benefit entitlement.

Users should verify scheme details, eligibility criteria, benefits, application deadlines, and documentation requirements through the relevant government departments and official portals.

AI-generated responses may contain errors or incomplete information. Users should not rely on generated responses as a substitute for official government guidance.

---

## 15. Project Information

| Attribute | Details |
|---|---|
| Project | KrishiYojana |
| Domain | Agriculture and Artificial Intelligence |
| Language | Python |
| Backend | FastAPI |
| Search Technique | TF-IDF and Cosine Similarity |
| LLM Provider | Groq |
| LLM Integration | Groq Python SDK |
| Prompt Engineering | System and Task Prompts |
| Dataset | 19 scheme records |
| API Endpoints | 6 |
| Development Progress | Day 1–Day 6 |
| Latest Checkpoint | Day 6 Groq LLM Integration |
| Repository | Adityahon3344/Gen-AI-Examate |

---

**KrishiYojana – Making Agricultural Scheme Information More Accessible Through Technology.**