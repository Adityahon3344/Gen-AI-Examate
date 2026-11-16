
# KrishiYojana – AI-Powered Farmer Scheme Assistant

**An AI-powered agricultural government scheme information and assistance system using Generative AI and Retrieval-Augmented Generation (RAG).**

---

# 1. Project Overview

KrishiYojana is an AI-powered application designed to help farmers access information about agricultural government schemes, eligibility criteria, benefits, and required documents.

The project uses Python, FastAPI, Large Language Models (LLMs), semantic search, embeddings, and Retrieval-Augmented Generation (RAG) to provide information based on agricultural documents.

The application retrieves relevant information from its knowledge base and uses an LLM to generate contextual answers. It also provides source references to help users identify the documents used to generate responses.

The system is instructed to avoid generating unsupported information when the available documents do not contain sufficient evidence.

**Project Name:** KrishiYojana

**Project Category:** Generative AI / Retrieval-Augmented Generation

**Development Progress:** Day 1 to Day 8

**Primary Objective:** Develop an AI-powered assistant for agricultural scheme information.

---

# 2. Project Objectives

The main objectives of this project are:

1. Collect agricultural government scheme information and related documents.
2. Create a structured dataset containing scheme information.
3. Extract and preprocess information from PDF and HTML documents.
4. Develop a FastAPI-based backend application.
5. Implement traditional text search using TF-IDF.
6. Generate text embeddings using Sentence Transformers.
7. Store and retrieve document embeddings using ChromaDB.
8. Integrate Groq LLM for AI-powered response generation.
9. Develop a Retrieval-Augmented Generation pipeline.
10. Generate answers using retrieved document context.
11. Provide source-based citations in responses.
12. Evaluate retrieval configurations and generated responses.
13. Improve the reliability of answers by handling unsupported questions.

---

# 3. Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| LLM Provider | Groq |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Database | ChromaDB |
| Traditional Search | TF-IDF |
| Semantic Search | Sentence Transformers |
| Data Processing | Pandas, NumPy |
| Document Processing | PDF and HTML extraction |
| API Testing | Swagger UI |
| Version Control | Git and GitHub |
| Development Environment | VS Code |

## 3.1 AI and RAG Components

**Large Language Model (LLM):** Used to generate natural-language responses based on retrieved context.

**Embeddings:** Convert text documents and user questions into numerical vector representations.

**ChromaDB:** Stores document embeddings and supports similarity-based retrieval.

**Semantic Search:** Retrieves relevant document chunks based on the meaning of a query.

**Retrieval-Augmented Generation:** Combines document retrieval with LLM-based response generation.

---

# 4. Repository Structure

The project is organized into different directories to maintain separation between application code, datasets, documents, prompts, and evaluation resources.

```text
Gen-AI-Examate/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── records.py
│   ├── fetch.py
│   ├── ingest.py
│   ├── smart_search.py
│   ├── chunking.py
│   ├── embed.py
│   ├── semantic_search.py
│   ├── vectorstore.py
│   └── rag.py
│
├── data/
│   ├── raw/
│   │   ├── farm_mechanization.html
│   │   ├── Scheme-SubMissionOnFarmMechanization.pdf
│   │   ├── DBT_Farmer_User_Manual.pdf
│   │   └── extracted_text.txt
│   │
│   ├── chroma_db/
│   ├── records.json
│   └── sample_records.py
│
├── docs/
│   ├── how_llms_work.md
│   ├── user_questions.md
│   └── DAILY_PROGRESS.md
│
├── prompts/
│   ├── system_prompt.txt
│   ├── task_prompt_1.txt
│   └── task_prompt_2.txt
│
├── eval/
│   ├── eval_set.json
│   ├── run_eval.py
│   ├── prompt_compare.md
│   ├── search_results.md
│   └── results/
│       ├── rag_eval_results.json
│       └── comparison.md
│
├── day01_intro.py
├── day01_menu.py
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

## 4.1 Directory Description

| Directory / File | Purpose |
|---|---|
| `app/` | Contains backend application code and AI/RAG modules. |
| `data/` | Contains structured scheme records and document data. |
| `data/raw/` | Stores original agricultural PDF and HTML documents. |
| `data/chroma_db/` | Stores the persistent ChromaDB vector database. |
| `docs/` | Contains project documentation and daily progress reports. |
| `prompts/` | Contains system and task-specific LLM prompts. |
| `eval/` | Contains evaluation datasets, scripts, and reports. |
| `requirements.txt` | Contains Python project dependencies. |
| `.gitignore` | Specifies files and directories excluded from Git tracking. |
| `.env` | Stores environment variables and API configuration. |
| `README.md` | Main project documentation. |

**Note:** This is the documented project structure based on the implemented modules. Verify the actual files in the repository before submission. The `.env` file and ChromaDB data should not be committed to GitHub.

---

# 5. Project Development Progress – Day 1 to Day 8

This section documents the development activities, implementation details, files created, testing performed, and deliverables for each development day.

---

## Day 1 – Python Fundamentals

**Objective:** Understand Python fundamentals and develop basic programming skills required for the project.

### Activities Completed

1. Studied Python variables and data types.
2. Practised conditional statements.
3. Implemented loops and functions.
4. Practised user input and output.
5. Created basic Python programs.
6. Understood fundamental programming concepts.

### Files Created

- `day01_intro.py`
- `day01_menu.py`

### Implementation Details

- Practised basic Python syntax.
- Implemented simple programming logic.
- Created programs using variables, conditions, and functions.

### Testing and Verification

- Executed Python programs.
- Checked program outputs.
- Verified basic programming logic.

### Deliverables

- Python practice programs.
- Understanding of Python fundamentals.

**Status:** Completed

---

## Day 2 – Dataset Preparation and Structuring

**Objective:** Prepare a structured dataset containing agricultural government scheme information.

### Activities Completed

1. Identified relevant agricultural government schemes.
2. Collected available scheme information.
3. Created structured scheme records.
4. Organized scheme information using Python data structures.
5. Prepared JSON data for application use.
6. Included available scheme details such as benefits and eligibility information.

### Files Created

- `data/sample_records.py`
- `app/records.py`
- `data/records.json`

### Implementation Details

- Prepared 19 scheme records.
- Organized scheme information into structured records.
- Separated data preparation from application logic.
- Prepared the dataset for search and retrieval operations.

### Testing and Verification

- Loaded scheme records.
- Checked the dataset structure.
- Verified that records could be accessed by the application.

### Deliverables

- Structured agricultural scheme dataset.
- JSON-based scheme records.
- Initial data management module.

**Status:** Completed

---

## Day 3 – Document Collection and Data Ingestion

**Objective:** Collect agricultural scheme documents and extract their content for the application knowledge base.

### Activities Completed

1. Identified relevant agricultural documents.
2. Collected PDF and HTML resources.
3. Implemented document fetching functionality.
4. Extracted text from collected documents.
5. Prepared extracted content for further processing.
6. Organized source documents inside the project.

### Files Created

- `app/fetch.py`
- `app/ingest.py`
- `data/raw/farm_mechanization.html`
- `data/raw/Scheme-SubMissionOnFarmMechanization.pdf`
- `data/raw/DBT_Farmer_User_Manual.pdf`
- `data/raw/extracted_text.txt`

### Implementation Details

- Developed document fetching and ingestion modules.
- Collected agricultural information from available documents.
- Extracted document text for subsequent processing.
- Organized raw documents separately from application code.

### Testing and Verification

- Executed the document ingestion process.
- Checked extracted text output.
- Verified that document content was available for processing.

### Deliverables

- Agricultural document collection.
- Document fetching module.
- Document ingestion module.
- Extracted text dataset.

**Status:** Completed

---

## Day 4 – Backend Development and Traditional Search

**Objective:** Set up the Python development environment and implement the initial backend and search functionality.

### Activities Completed

1. Created a Python virtual environment.
2. Installed required dependencies.
3. Configured the project environment.
4. Developed the FastAPI backend.
5. Implemented TF-IDF-based text search.
6. Connected structured scheme records with search functionality.
7. Used Pandas for dataset exploration.
8. Created initial API endpoints.

### Files Created or Modified

- `app/smart_search.py`
- FastAPI application files.
- `requirements.txt`

### Implementation Details

**FastAPI Backend:**

Developed the initial API application to expose project functionality through HTTP endpoints.

**TF-IDF Search:**

Implemented traditional text search using Term Frequency–Inverse Document Frequency (TF-IDF).

**Dataset Exploration:**

Used Pandas to explore and inspect structured scheme information.

### Testing and Verification

- Started the FastAPI server.
- Tested available API endpoints.
- Verified search responses.
- Checked dataset loading and accessibility.

### Deliverables

- Initial FastAPI backend.
- TF-IDF-based search implementation.
- Python dependency configuration.
- Initial API functionality.

**Status:** Completed

---

## Day 5 – LLM Fundamentals and Question Preparation

**Objective:** Understand Large Language Models and prepare farmer-related questions for the AI assistant.

### Activities Completed

1. Studied Large Language Model fundamentals.
2. Understood the basic LLM input and output workflow.
3. Studied how LLMs generate natural-language responses.
4. Prepared farmer-related questions.
5. Identified questions requiring document-based information.
6. Prepared an intentionally unanswerable question about the current tractor subsidy application deadline.

### Files Created

- `docs/how_llms_work.md`
- `docs/user_questions.md`

### Implementation Details

Prepared 10 farmer-related questions covering agricultural scheme information.

The questions were designed to represent common information requirements from farmers.

One question was intentionally designed to test whether the assistant would avoid inventing a current application deadline when verified information was unavailable in the knowledge base.

### Testing and Verification

- Reviewed the prepared questions.
- Checked whether the questions covered relevant agricultural topics.
- Identified questions requiring additional source information.
- Prepared test scenarios for the AI assistant.

### Deliverables

- LLM fundamentals documentation.
- Farmer-related question dataset.
- Initial question-answering test scenarios.

**Status:** Completed

---

## Day 6 – Groq Integration and Prompt Engineering

**Objective:** Integrate a Large Language Model into the application and implement prompt-based question answering.

### Activities Completed

1. Integrated the Groq API.
2. Configured API access using environment variables.
3. Created system-level instructions.
4. Developed task-specific prompts.
5. Implemented the `/chat` endpoint.
6. Generated responses using retrieved scheme records.
7. Compared two prompt versions.
8. Reviewed generated responses.

### Files Created or Modified

- `prompts/system_prompt.txt`
- `prompts/task_prompt_1.txt`
- `prompts/task_prompt_2.txt`
- `eval/prompt_compare.md`
- `app/main.py`
- LLM integration module.

### Implementation Details

**Groq Integration:**

Connected the backend application to Groq for LLM-based response generation.

**Prompt Engineering:**

Created system and task-specific prompts to guide the model's responses.

**Chat API:**

Implemented the `/chat` endpoint to receive user questions and generate responses using retrieved scheme records.

**Response Structure:**

The chat endpoint returns structured information containing:

- Answer
- Confidence
- Follow-up information

### Testing and Verification

- Tested Groq API connectivity.
- Tested the `/chat` endpoint.
- Compared outputs from two prompt versions.
- Reviewed generated answers.
- Checked the API response structure.

### Deliverables

- Groq LLM integration.
- System and task prompts.
- AI-powered chat endpoint.
- Prompt comparison documentation.

**Status:** Completed

---

## Day 7 – Document Chunking, Embeddings and Vector Database

**Objective:** Implement semantic search by converting agricultural documents into embeddings and storing them in ChromaDB.

### Activities Completed

1. Implemented document chunking.
2. Divided document content into manageable text sections.
3. Added source, page, and title metadata.
4. Generated embeddings using Sentence Transformers.
5. Implemented semantic similarity search.
6. Integrated ChromaDB.
7. Stored document embeddings in a persistent vector database.
8. Implemented the `/search/semantic` endpoint.
9. Reviewed semantic search results.

### Files Created

- `app/chunking.py`
- `app/embed.py`
- `app/semantic_search.py`
- `app/vectorstore.py`
- `eval/search_results.md`

### Implementation Details

**Document Chunking:**

Divided extracted document content into smaller text chunks for efficient retrieval.

**Chunk Configuration:**

- Chunk size: 1000 words.
- Chunk overlap: 150 words.

**Embedding Generation:**

Used the Sentence Transformers model:

`sentence-transformers/all-MiniLM-L6-v2`

Generated numerical vector representations of document chunks.

**Vector Database:**

Integrated ChromaDB to store document embeddings and perform similarity-based retrieval.

**Semantic Search:**

Implemented semantic search to retrieve relevant document sections based on the meaning of user queries.

### Implementation Results

| Parameter | Result |
|---|---|
| Total Document Chunks | 136 |
| Embedding Model | all-MiniLM-L6-v2 |
| Embedding Dimensions | 384 |
| Vector Database | ChromaDB |
| Collection Name | krishiyojana_documents |
| Chunk Size | 1000 words |
| Chunk Overlap | 150 words |

### Testing and Verification

- Tested document chunking.
- Verified embedding generation.
- Checked embedding dimensions.
- Verified vector storage.
- Tested semantic search queries.
- Reviewed retrieved search results.

### Deliverables

- Document chunking module.
- Embedding generation module.
- Semantic search implementation.
- Persistent ChromaDB collection.
- Semantic search evaluation documentation.

**Status:** Completed

---

## Day 8 – RAG Pipeline, Ask API and Evaluation

**Objective:** Implement a complete Retrieval-Augmented Generation workflow and evaluate different retrieval configurations.

### Activities Completed

1. Developed the RAG pipeline.
2. Generated embeddings for user questions.
3. Retrieved relevant document chunks from ChromaDB.
4. Prepared retrieved document context for the LLM.
5. Integrated Groq with the retrieval workflow.
6. Implemented source-based citations.
7. Added instructions for handling unsupported questions.
8. Created the `POST /ask` API endpoint.
9. Prepared a 15-question evaluation dataset.
10. Implemented an evaluation script.
11. Compared two retrieval configurations.
12. Reviewed evaluation results.

### Files Created or Modified

- `app/rag.py`
- `app/main.py`
- `eval/eval_set.json`
- `eval/run_eval.py`
- `eval/results/rag_eval_results.json`
- `eval/results/comparison.md`

### RAG Implementation Details

**Step 1 – User Question**

The user submits a question through the API.

**Step 2 – Question Embedding**

The application converts the question into a numerical embedding using the embedding model.

**Step 3 – Document Retrieval**

ChromaDB retrieves relevant document chunks using similarity search.

**Step 4 – Context Preparation**

The retrieved document chunks are prepared as context for the LLM.

**Step 5 – LLM Response Generation**

The Groq LLM generates an answer based on the retrieved context.

**Step 6 – Source References**

The response includes source references to identify the retrieved documents.

**Step 7 – Unsupported Question Handling**

The model is instructed to respond with `I don't know.` when sufficient supporting information is unavailable.

### RAG Evaluation Configuration

Two retrieval configurations were compared.

| Parameter | Configuration A | Configuration B |
|---|---:|---:|
| Chunk Size | 1000 | 500 |
| Chunk Overlap | 150 | 75 |
| Top-K | 3 | 5 |
| Generated Chunks | 136 | 140 |
| Evaluation Questions | 15 | 15 |

### RAG Evaluation Results

| Evaluation Metric | Configuration A | Configuration B |
|---|---:|---:|
| Successful Generations | 15 | 15 |
| Average Keyword Coverage | 0.6667 | 0.6667 |
| Citation Rate | 0.7143 | 0.7143 |
| Correct Abstentions | 1 | 1 |
| Generation Errors | 0 | 0 |

### Evaluation Observations

- Both configurations completed all 15 generations.
- Both configurations produced identical keyword coverage.
- Both configurations produced identical citation rates.
- Both configurations correctly abstained on one designated unanswerable question.
- Configuration A retrieves fewer chunks per query and was selected as the initial operational configuration.
- The evaluation results do not establish that Configuration A is more accurate than Configuration B.

### API Testing

The `POST /ask` endpoint was tested using Swagger UI.

**Test 1 – Agricultural Machinery Question**

- Submitted a question related to agricultural machinery.
- Retrieved relevant document chunks.
- Generated an answer using the retrieved context.
- Checked the source references.

**Test 2 – Unanswerable Tractor Subsidy Deadline Question**

- Submitted a question about the current tractor subsidy application deadline.
- Tested the model's ability to avoid unsupported claims.
- The tested response returned `I don't know.`
- Checked the returned source references.

### Evaluation Limitations

- Keyword coverage is a proxy metric and does not establish factual correctness.
- Citation rate measures the presence of citations, not whether citations fully support the answers.
- Some questions marked answerable were not answered by either configuration.
- Generated answers and source references require manual verification against official documents.
- The abstention behavior is prompt-driven and requires further validation.
- The evaluation does not establish that all generated responses are factually correct.

### Deliverables

- RAG question-answering pipeline.
- `POST /ask` API endpoint.
- ChromaDB-based document retrieval.
- Groq-based answer generation.
- Source-based response generation.
- 15-question evaluation dataset.
- RAG evaluation script.
- Retrieval configuration comparison report.

**Status:** Completed – Initial RAG evaluation performed.

---

# 6. API Documentation

The FastAPI application provides endpoints for accessing scheme information, searching records, and interacting with the AI assistant.

| HTTP Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Checks application health. |
| GET | `/records` | Retrieves available scheme records. |
| GET | `/records/{id}` | Retrieves a specific scheme record. |
| GET | `/search` | Performs traditional text search. |
| GET | `/questions` | Retrieves prepared farmer questions. |
| POST | `/chat` | Generates AI responses using the existing chat workflow. |
| POST | `/search/semantic` | Performs semantic document search. |
| POST | `/ask` | Generates RAG-based answers with source references. |

## 6.1 API Testing

FastAPI Swagger UI is used for testing and interacting with available API endpoints.

**Swagger UI URL:**

`http://127.0.0.1:8000/docs`

**Note:** Confirm the endpoint paths and HTTP methods against the actual implementation in `app/main.py`.

---

# 7. RAG Architecture

The current RAG workflow consists of the following stages:

```text
             User Question
                   |
                   v
          Question Embedding
                   |
                   v
           ChromaDB Retrieval
                   |
                   v
        Relevant Document Chunks
                   |
                   v
           Context Preparation
                   |
                   v
               Groq LLM
                   |
                   v
          Answer Generation
                   |
                   v
          Source-Based Citations
                   |
                   v
             Final Response
```

## 7.1 Architecture Components

| Component | Responsibility |
|---|---|
| Document Ingestion | Collects and extracts document content. |
| Chunking | Divides documents into smaller sections. |
| Embedding Model | Converts text into numerical vectors. |
| ChromaDB | Stores and retrieves document embeddings. |
| Retriever | Finds relevant document chunks. |
| Groq LLM | Generates answers using retrieved context. |
| RAG Pipeline | Coordinates retrieval and response generation. |
| FastAPI | Exposes project functionality through REST APIs. |

---

# 8. Application Setup and Execution

## 8.1 Prerequisites

- Python installed.
- Git installed.
- VS Code or another Python IDE.
- Groq API key.
- Required Python dependencies.

## 8.2 Clone the Repository

```bash
git clone https://github.com/Adityahon3344/Gen-AI-Examate.git

cd Gen-AI-Examate
```

## 8.3 Create a Virtual Environment

```bash
python3 -m venv .venv
```

## 8.4 Activate the Virtual Environment

For macOS/Linux:

```bash
source .venv/bin/activate
```

## 8.5 Install Dependencies

```bash
pip install -r requirements.txt
```

## 8.6 Configure Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_configured_groq_model
```

Use the actual model configured in your application.

Do not upload API keys or other secrets to GitHub.

## 8.7 Start the FastAPI Server

```bash
uvicorn app.main:app --reload
```

## 8.8 Open Swagger UI

Open the following URL in your browser:

`http://127.0.0.1:8000/docs`

Use Swagger UI to test the available API endpoints.

**Important:** The ChromaDB collection must be initialized before testing semantic search or the RAG endpoint. Follow the project's document indexing workflow if the vector database is not available.

---

# 9. Testing and Evaluation

Testing is performed throughout development to verify the functionality of individual modules and the overall application.

## 9.1 Testing Categories

| Testing Category | Purpose |
|---|---|
| Python Execution | Verifies basic program execution. |
| Dataset Validation | Checks structured scheme records. |
| Document Ingestion | Checks extracted document content. |
| Traditional Search | Evaluates TF-IDF search results. |
| API Testing | Checks FastAPI endpoint responses. |
| Embedding Testing | Verifies embedding generation and dimensions. |
| Vector Database Testing | Checks document storage and retrieval. |
| Semantic Search | Checks similarity-based retrieval. |
| RAG Testing | Checks generated answers and source references. |
| Evaluation Testing | Compares retrieval configurations. |

## 9.2 Evaluation Files

The following files contain evaluation datasets, scripts, and reports:

- `eval/prompt_compare.md`
- `eval/search_results.md`
- `eval/eval_set.json`
- `eval/run_eval.py`
- `eval/results/rag_eval_results.json`
- `eval/results/comparison.md`

## 9.3 Run the RAG Evaluation

```bash
python eval/run_eval.py
```

The evaluation script compares the configured retrieval experiments and generates result reports.

---

# 10. Current Project Status

| Project Module | Status |
|---|---|
| Python Fundamentals | Completed |
| Scheme Dataset Preparation | Completed |
| Document Collection | Completed |
| Document Ingestion | Completed |
| FastAPI Backend | Implemented |
| TF-IDF Search | Implemented |
| Groq Integration | Implemented |
| Prompt Engineering | Implemented |
| Document Chunking | Implemented |
| Embedding Generation | Implemented |
| ChromaDB Integration | Implemented |
| Semantic Search | Implemented |
| RAG Pipeline | Implemented |
| Source-Based Citations | Implemented |
| RAG Evaluation | Initial Evaluation Completed |

---

# 11. Daily Development Verification

Daily development activities are documented to maintain transparency and make project progress easy for the trainer to review.

Each development day should include:

1. Development objective.
2. Tasks completed.
3. Files created or modified.
4. Implementation details.
5. Testing performed.
6. Results and observations.
7. Evidence screenshots.
8. GitHub commit reference.
9. Completion status.

## 11.1 Daily Progress Report Template

Maintain this format in `docs/DAILY_PROGRESS.md`.

```markdown
# Daily Development Progress Report

## Day [Number] – [Development Topic]

**Date:** [DD Month YYYY]

### Objective
[Describe the development objective.]

### Tasks Completed
1. [Task 1]
2. [Task 2]
3. [Task 3]

### Files Created or Modified
- [File path 1]
- [File path 2]

### Implementation Details
[Explain the implementation.]

### Testing Performed
- [Test 1]
- [Test 2]

### Results and Observations
[Record actual test results.]

### Evidence
- Terminal execution screenshot
- API testing screenshot
- Code implementation screenshot
- Evaluation report, if applicable

### GitHub Commit
[Add GitHub commit URL]

**Status:** Completed / In Progress
```

## 11.2 Trainer Verification

The trainer can review the project's development through:

- GitHub repository and commit history.
- Daily development progress reports.
- Source code changes.
- API testing results.
- Terminal execution screenshots.
- Evaluation datasets and reports.
- Project documentation.

---

# 12. Daily Project Updates

The KrishiYojana project follows a day-wise development approach. Project activities, implementation changes, and testing results are documented regularly.

## 12.1 Development Tracking

| Day | Development Activity | Status |
|---|---|---|
| Day 1 | Python Fundamentals | Completed |
| Day 2 | Dataset Preparation and Structuring | Completed |
| Day 3 | Document Collection and Ingestion | Completed |
| Day 4 | Backend Development and Traditional Search | Completed |
| Day 5 | LLM Fundamentals and Question Preparation | Completed |
| Day 6 | Groq Integration and Prompt Engineering | Completed |
| Day 7 | Document Chunking, Embeddings and ChromaDB | Completed |
| Day 8 | RAG Pipeline, Ask API and Evaluation | Completed |

## 12.2 Daily GitHub Update Process

After completing and testing daily development activities:

1. Update the relevant source code.
2. Update `README.md` when project documentation changes.
3. Update `docs/DAILY_PROGRESS.md` with actual daily work.
4. Save relevant testing evidence.
5. Stage the required changes using Git.
6. Commit the changes with a descriptive commit message.
7. Push the changes to the GitHub repository.

Example Git commands:

```bash
git status

git add README.md docs/ app/ eval/

git commit -m "docs: update daily project development progress"

git push origin master
```

Only commit files that have been reviewed and do not contain secrets, virtual environments, or generated database files.

---

# 13. Known Limitations and Future Improvements

## 13.1 Current Limitations

1. The current document collection does not cover every agricultural government scheme.
2. Some retrieved information may be incomplete or outdated.
3. Keyword coverage does not establish factual answer accuracy.
4. Citation presence does not guarantee citation correctness.
5. Some answerable evaluation questions currently result in abstentions.
6. The current abstention behavior is prompt-driven and requires further validation.
7. Scheme eligibility, benefits, and application deadlines require verification against current official government sources.

## 13.2 Future Improvements

1. Expand the agricultural scheme knowledge base.
2. Add more verified official government documents.
3. Improve document retrieval and ranking.
4. Improve answer validation and citation verification.
5. Refine the abstention mechanism.
6. Add more evaluation questions.
7. Perform manual factual evaluation against official sources.
8. Improve API response handling and error management.
9. Develop a farmer-friendly frontend.
10. Add multilingual support for Marathi and other regional languages.

---

# 14. Project Disclaimer

KrishiYojana is an educational AI project developed to demonstrate Generative AI and Retrieval-Augmented Generation concepts.

The application provides information based on its available document collection. It is not an official government service and does not make legally binding eligibility decisions.

Farmers should verify scheme eligibility, benefits, required documents, and application deadlines through the relevant official government portals or authorities.

---

# 15. Repository Information

| Field | Details |
|---|---|
| Project Name | KrishiYojana |
| Repository Name | Gen-AI-Examate |
| Development Progress | Day 1 – Day 8 |
| Project Category | Generative AI / RAG |
| Programming Language | Python |
| Backend Framework | FastAPI |
| LLM Provider | Groq |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Database | ChromaDB |
| Version Control | Git and GitHub |

**GitHub Repository:**

https://github.com/Adityahon3344/Gen-AI-Examate

---

# 16. Conclusion

KrishiYojana demonstrates the development of an AI-powered agricultural information assistant using Python, FastAPI, Groq, Sentence Transformers, and ChromaDB.

During the first eight development days, the project progressed from Python fundamentals and dataset preparation to document ingestion, traditional search, LLM integration, semantic search, vector storage, RAG implementation, API development, and initial evaluation.

The current implementation establishes the foundation for document-based agricultural question answering.

Further development will focus on expanding the knowledge base, improving retrieval quality, validating factual accuracy, verifying citations, and supporting multilingual access for farmers.
