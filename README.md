# KrishiYojana – Maharashtra Farmer Scheme Eligibility & Benefits Assistant

## 1. Project Overview

KrishiYojana is a Python-based project designed to help farmers discover agricultural government schemes available in Maharashtra.

The application provides information about agricultural schemes, their benefits, eligibility criteria, and required documents. It also includes a search facility that helps users find relevant schemes using keywords and natural-language questions.

The project is being developed as a learning-based AI application using Python, data processing, FastAPI, and machine learning techniques.

## 2. Project Objectives

- Collect agricultural government scheme information.
- Maintain structured records of Maharashtra farmer schemes.
- Provide information about scheme benefits and eligibility criteria.
- Display documents required for scheme applications.
- Implement keyword-based scheme searching.
- Develop REST APIs using FastAPI.
- Implement intelligent scheme search using TF-IDF and cosine similarity.
- Analyze scheme records using Pandas.
- Build a foundation for an AI-powered farmer assistance system.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | Backend API development |
| Uvicorn | ASGI server |
| Pandas | Data analysis |
| Scikit-learn | TF-IDF and cosine similarity |
| Requests | Downloading web resources |
| BeautifulSoup | HTML data extraction |
| PyPDF | PDF text extraction |
| JSON | Structured data storage |
| Git | Version control |
| GitHub | Source code management |
| VS Code | Development environment |

## 4. Project Structure

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
├── day01_intro.py
├── day01_menu.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 5. Dataset Information

The project currently contains **19 agricultural scheme records** in `data/sample_records.py`.

Each scheme record contains the following fields:

| Field | Description |
|---|---|
| `id` | Unique scheme identification number |
| `scheme_name` | Name of the agricultural scheme |
| `department` | Implementing department |
| `benefit` | Description of scheme benefits |
| `eligibility` | Eligibility conditions |
| `required_documents` | Documents required for application |
| `source_url` | Reference URL for scheme information |

### Complete List of 19 Scheme Records

The following 19 scheme records are included in the current dataset:

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

**Dataset validation:**
- Total records: 19
- Unique IDs: 19
- ID range: 1–19
- Storage file: `data/sample_records.py`

Note: Scheme details, eligibility conditions, benefits, and document requirements should be verified against the latest official government guidelines before being used for actual farmer applications.

## 6. Development Progress

### Day 1 – Python Fundamentals

- Created the KrishiYojana project introduction.
- Practiced Python variables and user input.
- Used formatted strings (f-strings).
- Developed an interactive command-line menu.
- Implemented conditional statements.
- Practiced while loops and basic program flow.

**Files created:**
- `day01_intro.py`
- `day01_menu.py`

### Day 2 – Dataset Creation and CLI Development

- Created structured agricultural scheme records.
- Used Python lists and dictionaries.
- Expanded the dataset from 6 to 19 records.
- Implemented scheme searching.
- Implemented department-wise scheme counting.
- Implemented scheme retrieval using unique IDs.
- Developed an interactive command-line application.

**Files created or updated:**
- `data/sample_records.py`
- `app/records.py`
- `app/cli.py`

### Day 3 – Data Collection and Extraction

- Downloaded agricultural scheme resources.
- Collected HTML and PDF documents.
- Used Requests for downloading resources.
- Used BeautifulSoup for HTML extraction.
- Used PyPDF for PDF text extraction.
- Saved extracted text for further processing.
- Created a Python dataclass model for scheme records.

**Files created or updated:**
- `app/fetch.py`
- `app/ingest.py`
- `app/models.py`
- `data/raw/`

### Day 4 – FastAPI and Intelligent Search

- Created a FastAPI backend application.
- Implemented REST API endpoints.
- Integrated JSON-based scheme records.
- Implemented TF-IDF vectorization.
- Used cosine similarity for ranking search results.
- Created a farmer question endpoint.
- Used Pandas for dataset analysis.
- Tested API endpoints through Swagger UI.

**Files created or updated:**
- `app/main.py`
- `app/smart_search.py`
- `analysis/explore.py`

## 7. API Endpoints

The FastAPI application provides the following endpoints:

| HTTP Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API status |
| GET | `/records` | Retrieve scheme records |
| GET | `/records/{record_id}` | Retrieve a scheme using its ID |
| GET | `/search?q=tractor` | Search schemes using TF-IDF |
| POST | `/questions` | Find schemes relevant to a farmer's question |

### Example API Requests

**1. Health Check**

```http
GET /health
```

**2. Get All Records**

```http
GET /records?limit=10
```

**3. Get Scheme by ID**

```http
GET /records/1
```

**4. Search Schemes**

```http
GET /search?q=tractor
```

**5. Ask a Farmer Question**

```http
POST /questions
```

Request body:

```json
{
  "question": "Which schemes provide financial assistance for tractors?"
}
```

## 8. Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/Adityahon3344/Gen-AI-Examate.git
```

### Step 2: Navigate to the Project Directory

```bash
cd Gen-AI-Examate
```

### Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 4: Activate the Virtual Environment

For macOS and Linux:

```bash
source .venv/bin/activate
```

For Windows:

```bash
.venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## 9. How to Run the Project

### Run the Command-Line Application

```bash
python -m app.cli
```

### Run the Data Analysis Script

```bash
python -m analysis.explore
```

### Run the FastAPI Application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### Open Swagger API Documentation

```text
http://127.0.0.1:8000/docs
```

Swagger UI allows users to explore and test the available API endpoints.

## 10. Intelligent Search Methodology

KrishiYojana uses TF-IDF (Term Frequency-Inverse Document Frequency) and cosine similarity to identify relevant agricultural schemes.

### Search Process

1. Accept a search query or farmer question.
2. Convert scheme information into text documents.
3. Apply TF-IDF vectorization.
4. Calculate cosine similarity between the query and scheme records.
5. Rank matching schemes based on similarity scores.
6. Return the most relevant scheme records.

This provides a basic intelligent search mechanism for finding relevant agricultural schemes.

## 11. Data Analysis Using Pandas

Pandas is used to analyze the available scheme records.

The analysis script displays:

- Total number of schemes.
- Number of unique departments.
- Department-wise scheme distribution.
- Scheme names and their departments.

Run the analysis using:

```bash
python -m analysis.explore
```

## 12. Current Project Status

| Component | Status |
|---|---|
| Python Fundamentals | Completed |
| Dataset Creation | Completed |
| 19 Scheme Records | Added |
| Command-Line Interface | Implemented |
| Data Collection | Implemented |
| HTML and PDF Extraction | Implemented |
| FastAPI Backend | Implemented |
| TF-IDF Smart Search | Implemented |
| Pandas Data Analysis | Implemented |

## 13. Future Enhancements

- Add more verified Maharashtra agricultural schemes.
- Improve scheme eligibility matching.
- Develop a farmer-friendly web interface.
- Integrate an AI-powered question-answering system.
- Add multilingual support for Marathi, Hindi, and English.
- Improve recommendation accuracy.
- Integrate a database for managing scheme records.
- Add automated data updates from official government sources.

## 14. Official References

- [Maharashtra MahaDBT Farmer Portal](https://mahadbt.maharashtra.gov.in/Farmer/)
- [Maharashtra Government Official Portal](https://www.maharashtra.gov.in/)

## 15. GitHub Repository

**Repository:** [Gen-AI-Examate](https://github.com/Adityahon3344/Gen-AI-Examate)

**GitHub Username:** Adityahon3344

## 16. Disclaimer

KrishiYojana is an educational project and is not an official government application.

The scheme information provided by this project should not be treated as a final determination of eligibility or benefit entitlement. Farmers should verify scheme details, eligibility conditions, benefits, and required documents through the relevant government departments and official portals.

---

**Project Name:** KrishiYojana – Maharashtra Farmer Scheme Eligibility & Benefits Assistant

**Developed Using:** Python, FastAPI, Pandas, and Scikit-learn.