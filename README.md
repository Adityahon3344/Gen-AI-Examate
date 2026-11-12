# KrishiYojana
### Maharashtra Farmer Scheme Eligibility & Benefits Assistant

**Project Repository:** [Adityahon3344/Gen-AI-Examate](https://github.com/Adityahon3344/Gen-AI-Examate)  
**Project Category:** Artificial Intelligence / Machine Learning / Backend Development  
**Primary Language:** Python  
**Development Status:** Day 1–Day 5 Completed

---

## 1. Project Overview

KrishiYojana is an AI-oriented agricultural assistance application designed to help farmers discover government agricultural schemes available in Maharashtra.

The project aims to organize agricultural scheme information into structured records and provide an accessible interface for retrieving scheme details, understanding benefits, exploring eligibility criteria, and identifying required documents.

The current implementation includes a structured dataset, command-line interface, data extraction utilities, FastAPI backend, and TF-IDF-based intelligent search functionality.

The project is being developed incrementally, with a focus on Python fundamentals, data processing, API development, and foundational AI concepts.

## 2. Project Objectives

- Collect and organize Maharashtra agricultural scheme information.
- Develop a structured dataset containing scheme details.
- Implement scheme retrieval and keyword-based searching.
- Provide RESTful APIs using FastAPI.
- Implement intelligent search using TF-IDF and cosine similarity.
- Analyze structured data using Pandas.
- Understand Large Language Model (LLM) architecture and working principles.
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
│   └── smart_search.py
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
├── day01_intro.py
├── day01_menu.py
├── requirements.txt
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

---

## 7. FastAPI Implementation

The application currently exposes five API endpoints.

| Method | Endpoint | Functionality |
|---|---|---|
| GET | `/health` | Verify API availability |
| GET | `/records` | Retrieve scheme records |
| GET | `/records/{record_id}` | Retrieve a specific scheme |
| GET | `/search` | Perform TF-IDF-based scheme search |
| POST | `/questions` | Retrieve schemes relevant to a farmer's question |

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

### API Documentation

Interactive API documentation is available through FastAPI Swagger UI.

```text
http://127.0.0.1:8000/docs
```

---

## 8. Intelligent Search Approach

The current search implementation uses TF-IDF and cosine similarity.

**Processing Workflow:**

1. Receive a search query or farmer question.
2. Load the available scheme records.
3. Convert scheme information into searchable text.
4. Apply TF-IDF vectorization.
5. Calculate cosine similarity between the query and scheme documents.
6. Rank matching records by similarity.
7. Return the top relevant results.

This is a foundational information retrieval approach. It does not yet implement an LLM-based response generation pipeline.

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

---

## 10. Installation and Execution

### Prerequisites

- Python 3.11 or later
- Git
- Visual Studio Code

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

### Run CLI Application

```bash
python -m app.cli
```

### Run Data Analysis

```bash
python -m analysis.explore
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

### Useful Git Commands

```bash
git status
git log --oneline
git tag
git push origin master
git push origin checkpoint-1
```

**Repository:**  
https://github.com/Adityahon3344/Gen-AI-Examate

---

## 12. Future Development Roadmap

The following improvements are planned for subsequent development stages:

- Expand and validate the agricultural scheme dataset.
- Improve scheme eligibility matching.
- Implement robust handling of questions that cannot be answered from available data.
- Develop an LLM-powered question-answering system.
- Explore Retrieval-Augmented Generation (RAG).
- Introduce multilingual support for Marathi, Hindi, and English.
- Develop a farmer-friendly web interface.
- Integrate a persistent database.
- Improve search relevance and recommendation accuracy.
- Incorporate verified updates from official government sources.

---

## 13. Official References

- [Maharashtra MahaDBT Farmer Portal](https://mahadbt.maharashtra.gov.in/Farmer/)
- [Maharashtra Government Official Portal](https://www.maharashtra.gov.in/)

---

## 14. Disclaimer

KrishiYojana is an educational software development project and is not an official government application.

The information provided by the application should not be considered an official confirmation of eligibility or benefit entitlement.

Users should verify scheme details, eligibility criteria, benefits, application deadlines, and documentation requirements through the relevant government departments and official portals.

---

## 15. Project Information

| Attribute | Details |
|---|---|
| Project | KrishiYojana |
| Domain | Agriculture and Artificial Intelligence |
| Language | Python |
| Backend | FastAPI |
| Search Technique | TF-IDF and Cosine Similarity |
| Dataset | 19 scheme records |
| Development Progress | Day 1–Day 5 |
| Latest Checkpoint | `checkpoint-1` |
| Repository | Adityahon3344/Gen-AI-Examate |

**KrishiYojana – Making Agricultural Scheme Information More Accessible Through Technology.**