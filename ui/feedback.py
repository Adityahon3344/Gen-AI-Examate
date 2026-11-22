import json
from datetime import datetime
from pathlib import Path


def save_feedback(
    feedback_file: Path,
    question: str,
    answer: str,
    rating: str,
) -> None:
    feedback = []
    if feedback_file.exists():
        with feedback_file.open("r", encoding="utf-8") as file:
            feedback = json.load(file)

    feedback.append({
        "question": question,
        "answer": answer,
        "rating": rating,
        "timestamp": datetime.now().isoformat(),
    })

    with feedback_file.open("w", encoding="utf-8") as file:
        json.dump(feedback, file, indent=4, ensure_ascii=False)
