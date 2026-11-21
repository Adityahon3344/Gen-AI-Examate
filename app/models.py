from dataclasses import dataclass


@dataclass
class Record:
    id: int
    scheme_name: str
    department: str
    benefit: str
    eligibility: list[str]
    required_documents: list[str]
    source_url: str
