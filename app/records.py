
from data.sample_records import SAMPLE_RECORDS


def load_records():
    """Load all available scheme records."""
    return SAMPLE_RECORDS


def search(keyword):
    """Search schemes by name, department, benefit or eligibility."""
    results = []

    keyword = keyword.lower()

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
