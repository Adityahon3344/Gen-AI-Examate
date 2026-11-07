# 🌾 KrishiYojana – Maharashtra Farmer Scheme Eligibility & Benefits Assistant

KrishiYojana is a Python-based educational project designed to help farmers explore agricultural government schemes in Maharashtra. It provides information about scheme benefits, eligibility criteria, required documents, and departments.

## 🎯 Project Objectives

- Display agricultural government schemes.
- Search schemes using keywords.
- View scheme details using a unique ID.
- Display eligibility criteria and required documents.
- Fetch information from HTML and PDF sources.
- Clean and store scheme records in JSON format.

## 🛠️ Technology Stack

- **Language:** Python
- **Data Storage:** JSON
- **Libraries:** Requests, BeautifulSoup4, PyPDF
- **Concepts:** Functions, Lists, Dictionaries, Dataclasses, Exception Handling
- **Tools:** VS Code, Git, GitHub

## 📁 Project Structure

```text
Gen-AI-Examate/
│
├── app/
│   ├── __init__.py
│   ├── records.py
│   ├── cli.py
│   ├── models.py
│   ├── fetch.py
│   └── ingest.py
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

## 📅 Day 1 – Python Fundamentals

**Topics covered:**
- Variables
- User input and output
- F-strings
- Conditional statements (`if`, `elif`, `else`)
- While loops

**Files created:**
- `day01_intro.py` – Displays project information and accepts user input.
- `day01_menu.py` – Creates an interactive menu using conditional statements and loops.

## 📅 Day 2 – Data Management and CLI

**Topics covered:**
- Python lists and dictionaries
- List of dictionaries
- Functions
- Searching and filtering records
- Working with scheme information

**Files created:**
- `data/sample_records.py` – Contains six sample agricultural scheme records.
- `app/records.py` – Provides functions to load, search, count, and retrieve scheme records.
- `app/cli.py` – Provides an interactive command-line application.

**CLI Features:**

1. Display all schemes
2. Search schemes using keywords
3. Count schemes by department
4. Get scheme details using ID
5. Exit the application

## 📅 Day 3 – Data Fetching and Ingestion

**Topics covered:**
- HTTP requests using Requests
- HTML and PDF data extraction
- Exception handling (`try` and `except`)
- Python dataclasses
- JSON data storage
- Data cleaning and validation

**Files created:**
- `app/models.py` – Defines the `Record` dataclass.
- `app/fetch.py` – Downloads HTML and PDF resources.
- `app/ingest.py` – Extracts text from downloaded HTML and PDF files.
- `data/raw/` – Stores downloaded source documents.
- `data/records.json` – Stores structured scheme records.

**Data Sources:**

1. [MahaDBT Farmer Scheme Data](https://mahadbt.maharashtra.gov.in/Farmer/SchemeData/SchemeData?str=E9DDFA703C38E51A23C0254248DAFF28)
2. [Sub-Mission on Farm Mechanization PDF](https://mahadbt.maharashtra.gov.in/Farmer/PDF/Scheme-SubMissionOnFarmMechanization.pdf)

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Adityahon3344/Gen-AI-Examate.git
cd Gen-AI-Examate
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment (Mac/Linux)

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```
## Day 4 – FastAPI and Smart Search

### Completed Tasks
- Created a FastAPI application for KrishiYojana.
- Implemented GET `/health` to check API status.
- Implemented GET `/records` to retrieve scheme records.
- Implemented GET `/records/{record_id}` to retrieve a scheme by ID.
- Implemented GET `/search` to search agricultural schemes.
- Implemented POST `/questions` to accept farmer questions.
- Integrated TF-IDF and cosine similarity for smart search.
- Used Pandas to analyze agricultural scheme records.

### Data Analysis
- Total scheme records: 6
- Unique departments: 1
- Most common department: Agriculture Department

### How to Run the Project

1. Activate the virtual environment:

```bash
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the FastAPI server:

```bash
uvicorn app.main:app --reload --reload-dir app
```

4. Open Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

5. Run the Pandas analysis:

```bash
python -m analysis.explore
```

### Technologies Used
- Python
- FastAPI
- Pandas
- Scikit-learn
- TF-IDF
- Cosine Similarity
- JSON

