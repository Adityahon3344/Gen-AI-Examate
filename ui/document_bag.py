from typing import TypedDict


class DocumentRequirement(TypedDict):
    name: str
    schemes: list[str]


def build_document_map(
    records: list[dict],
    selected_schemes: list[str],
) -> dict[str, DocumentRequirement]:
    selected = set(selected_schemes)
    document_map: dict[str, DocumentRequirement] = {}

    for record in records:
        scheme_name = record["scheme_name"]
        if scheme_name not in selected:
            continue

        for document in record.get("required_documents", []):
            name = document.strip()
            normalized_name = name.casefold()
            if normalized_name not in document_map:
                document_map[normalized_name] = {
                    "name": name,
                    "schemes": [],
                }

            if scheme_name not in document_map[normalized_name]["schemes"]:
                document_map[normalized_name]["schemes"].append(scheme_name)

    return document_map


def format_document_checklist(
    document_map: dict[str, DocumentRequirement],
) -> str:
    return "\n".join(
        f"- {item['name']} | Required for: {', '.join(item['schemes'])}"
        for item in document_map.values()
    )
