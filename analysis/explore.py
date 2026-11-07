
import pandas as pd
from app.records import load_json_records


# Load records
records = load_json_records()

# Convert records into a DataFrame
data = [
    {
        "id": record.id,
        "scheme_name": record.scheme_name,
        "department": record.department,
        "benefit": record.benefit
    }
    for record in records
]

df = pd.DataFrame(data)


# Fact 1: Total schemes
print("\n===== FACT 1 =====")
print("Total Schemes:", len(df))


# Fact 2: Unique departments
print("\n===== FACT 2 =====")
print("Unique Departments:", df["department"].nunique())


# Fact 3: Most common department
print("\n===== FACT 3 =====")
print(df["department"].value_counts().head(1))


# Display records
print("\n===== SCHEME DATA =====")
print(df[["id", "scheme_name", "department"]])
