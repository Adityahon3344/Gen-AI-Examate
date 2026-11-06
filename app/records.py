
import json
from pathlib import Path

from data.sample_records import SAMPLE_RECORDS
from app.models import Record

JSON_FILE = Path("data/records.json")


def load_records():
    """Load all available sample scheme records."""
    return SAMPLE_RECORDS


def load_json_records():
    """Load scheme records from JSON and convert them into Record objects."""

    try:
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        records = []

        for row in data:
            try:
                record = Record(**row)
                records.append(record)

            except (TypeError, ValueError) as error:
                print(f"Skipping invalid record: {error}")

        return records

    except (OSError, json.JSONDecodeError) as error:
        print(f"Error loading JSON records: {error}")
        return []


def search(keyword):
    """Search schemes by name, department, benefit or eligibility."""

    results = []
    keyword = keyword.lower().strip()

    for scheme in SAMPLE_RECORDS:
        searchable_text = (
            scheme["scheme_name"] + " " +
            scheme["department"] + " " +
            scheme["benefit"] + " " +
            " ".join(scheme["eligibility"])
        ).lower()

        if keyword in searchable_text:
            results.append(scheme)

    return results


def count_by(department):
    """Count schemes belonging to a department."""

    count = 0

    for scheme in SAMPLE_RECORDS:
        if scheme["department"].lower() == department.lower():
            count += 1

    return count


def get_by_id(scheme_id):
    """Find a scheme using its ID."""

    for scheme in SAMPLE_RECORDS:
        if scheme["id"] == scheme_id:
            return scheme

    return None


if __name__ == "__main__":
    records = load_json_records()

    print("Total JSON records:", len(records))

    if records:
        print("First scheme:", records[0].scheme_name)
