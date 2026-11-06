from dataclasses import dataclass
from typing import List


@dataclass
class Record:
    id: int
    scheme_name: str
    department: str
    benefit: str
    eligibility: List[str]
    required_documents: List[str]
    source_url: str
