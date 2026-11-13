import json
from pathlib import Path
from data.sample_records import SAMPLE_RECORDS

output_file = Path("data/records.json")

output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(SAMPLE_RECORDS, file, indent=4, ensure_ascii=False)

print(f"Successfully exported {len(SAMPLE_RECORDS)} records to {output_file}")