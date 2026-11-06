# KrishiYojana

## Project Card

- **Product:** KrishiYojana
- **Target User:** Indian Farmers
- **Problem:** Difficulty finding information about agricultural schemes.
- **Solution:** A simple Python application to introduce agricultural schemes and demonstrate farmer-related queries.
- **Data Sources:**
  - https://www.myscheme.gov.in/
  - https://pmkisan.gov.in/
  - https://mahadbt.maharashtra.gov.in/Farmer

---

## Day 1 – Project Introduction and Basic Python Menu

### Features
- Introduce the KrishiYojana project and its purpose.
- Display the project card with product, target user, problem, and solution.
- Accept farmer-related information using user input.
- Display customized output using Python f-strings.
- Provide an interactive menu for basic farmer-related queries.
- Demonstrate farmer category classification using simple conditions.

### Project Files
- `day01_intro.py` – Displays the project card and accepts user input using variables and f-strings.
- `day01_menu.py` – Provides an interactive menu using a while loop and if/elif/else conditions.

### Concepts Used
- Python variables
- Input and output
- F-strings
- While loop
- If/elif/else conditions
- Basic conditional logic

### How to Run

```bash
python3 day01_intro.py
python3 day01_menu.py
```

**Note:** Farmer category classification is a demonstration rule, not official government eligibility advice.

---

## Day 2 – Scheme Records and Python Application

### Features
- Display all available agricultural schemes.
- Search schemes using keywords.
- Count schemes by department.
- Retrieve scheme details using Scheme ID.
- Display scheme benefits and eligibility criteria.
- Display required documents for each scheme.

### Project Files
- `data/sample_records.py` – Stores agricultural scheme information using Python lists and dictionaries.
- `app/records.py` – Contains functions to load, search, count, and retrieve scheme records.
- `app/cli.py` – Provides an interactive command-line interface for farmers.

### Current Dataset
6 Maharashtra farmer schemes:
1. Sub-mission on Farm Mechanization
2. State Agriculture Mechanization Scheme
3. Birsa Munda Krishi Kranti Yojana
4. Per Drop More Crop
5. PMRKVY – Rainfed Area Development
6. Dr. Babasaheb Ambedkar Krushi Swavalamban Yojana

### Concepts Used
- Python lists and dictionaries
- Functions
- Loops
- Conditional statements
- Python modules and imports
- String methods
- Exception handling

### How to Run

```bash
python -m app.cli
```

### Application Menu

1. Display All Schemes
2. Search Scheme
3. Count by Department
4. Get Scheme by ID
0. Exit

---

## Technologies Used

- **Programming Language:** Python
- **Development Environment:** VS Code
- **Version Control:** Git and GitHub
- **Data Storage:** Python lists and dictionaries
- **Interface:** Command-Line Interface (CLI)

---

## Future Scope

- Add more Maharashtra and Indian government agricultural schemes.
- Implement farmer-based eligibility checking.
- Store scheme records in JSON or a database.
- Develop a user-friendly web application.
- Integrate AI-based scheme recommendations.

---

**Note:** Scheme information is collected for educational and demonstration purposes. Farmers should verify current eligibility, benefits, and documents on official government portals before applying.