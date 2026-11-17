import json
from pathlib import Path

RULES_FILE = (
    Path(__file__).resolve().parent.parent
    / "data" / "rules" / "scheme_rules.json"
)


def load_scheme_rules():
    with open(RULES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def check_scheme_eligibility(
    land_holding,
    land_size_acres,
    caste_category,
    received_same_component_last_10_years,
    already_has_tractor,
    scheme_id="farm_mechanization_demo"
):
    schemes = load_scheme_rules()

    if scheme_id not in schemes:
        return {
            "eligible": False,
            "status": "ERROR",
            "failed_rules": ["Scheme not found."],
            "message": "The requested scheme does not exist."
        }

    rules = schemes[scheme_id]["rules"]
    failed_rules = []

    if land_holding not in rules["land_holding"]["allowed"]:
        failed_rules.append(rules["land_holding"]["failure_message"])

    if land_size_acres < rules["land_size_acres"]["minimum"]:
        failed_rules.append(rules["land_size_acres"]["failure_message"])

    if caste_category.upper() not in rules["caste_category"]["allowed"]:
        failed_rules.append(rules["caste_category"]["failure_message"])

    if received_same_component_last_10_years != rules[
        "received_same_component_last_10_years"
    ]["must_be"]:
        failed_rules.append(
            rules["received_same_component_last_10_years"]["failure_message"]
        )

    if already_has_tractor != rules["already_has_tractor"]["must_be"]:
        failed_rules.append(
            rules["already_has_tractor"]["failure_message"]
        )

    if failed_rules:
        return {
            "eligible": False,
            "status": "FAIL",
            "failed_rules": failed_rules,
            "message": "Applicant does not pass all demonstration rules."
        }

    return {
        "eligible": True,
        "status": "PASS",
        "failed_rules": [],
        "message": "Applicant passes all demonstration rules."
    }
